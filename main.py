import queue
import json
import time
import os.path
import subprocess
import threading
import transmissionrpc
import YTS


# USER INPUT
LIMIT_BYTES = 5*1000*1000*1000
MAX_ETA = 20
# https://yts.ag/api
params = {
	'sort_by' : 'year',
	'limit': 50,
	'minimum_rating': 6
}
ignore_qualities = ['720p']
# load configs
auth = []
with open('auth.json', 'r') as fp:
	auth = json.load(fp)

settings = []
with open('config/settings.json', 'r') as fp:
	settings = json.load(fp)

finished={}
try:
	fp = open('finished.json', 'r')
	finished = json.load(fp)
except:
	pass

with open('finished.json', 'w') as fp:
	json.dump(finished,fp)


def trans_remote_cmd(auth, url):

	argv = [ "transmission-remote",
			 "%s:%s" % (auth['address'],auth['port']),
			 "-n", "%s:%s" % (auth['user'], auth['password']),
			 "-a"
			  	]

	argv.append(url)
	print(argv)
	subprocess.call(argv)
			  	

# login transmissionrpc
print( "authenticate rpc server...")
try:
	tc = transmissionrpc.Client(auth['address'], port=auth['port'],
		user=auth['user'], password=auth['password'])
except Exception as e:
	print(str(e))
	exit(1)

#get movies
print( "start collect yts.ag movies...")
yc = YTS.collector()
yc.start(params)

#get torrents
tq = queue.Queue()
for movie in yc.movies:
	if 'torrents' in movie.keys():
		for torrent in movie['torrents']:
			tq.put(torrent)

thrds = []
while not tq.empty():

	eta = MAX_ETA
	downloading_bytes = 0

	for t in tc.get_torrents():
		if t.isFinished:
			finished.update({t.hashString:t.name})
		else:
			downloading_bytes += t.totalSize
			if t.eta >= 0:
				print(t.name+': eta='+str(t.eta)+' sec')
				if t.eta < eta:
					eta = t.eta

	while not tq.empty():
		t = tq.get()
		if t['hash'].lower() in finished.keys():
			continue
		if downloading_bytes + t['size_bytes'] <= LIMIT_BYTES:
			downloading_bytes += t['size_bytes']
			th = threading.Thread(target=trans_remote_cmd, args=(auth, t['url']))
			thrds.append(th)
			th.start()
		else:
			tq.put(t)
			break

	print("downloading bytes: %d" % downloading_bytes)
	print("wait for %d sec ..." % eta)
	time.sleep(eta)
# 	# upload section
	subprocess.call(['./upload.sh'])


for th in thrds:
	th.join()


with open('finished.json', 'r') as fp:
	json.dump(finished,fp)

print('---finished---')