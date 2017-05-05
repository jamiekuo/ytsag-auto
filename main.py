import transmissionrpc
import requests
import json
import subprocess
import time
import threading
import YTS

auth = {}
with open('auth.json', 'r') as fp:
	auth = json.load(fp)

# finished = []
# with open('finished.json', 'r') as fp:
# 	finished = json.load(fp)

print("connect transmission...")
try:
	tc = transmissionrpc.Client(
		auth['address'],
		port=auth['port'],
		user=auth['user'],
		password=auth['password'] )
except Exception as e:
	print (str(e))

print("get torrents...")
ts = tc.get_torrents()

remote_finish = []
for i in ts:
	if i.isFinished:
		remote_finish.append(i.hashString)

finished = remote_finish
# finished = list(set(finished)|set(remote_finish))


# get movie
print("get all movies")
params = {
	'sort_by' : 'year',
	'limit': 50
}
YTS.collect_movies(params)
time.sleep(1)


def add_torrent(url):
	global auth
	print("add: "+url)
	subprocess.call([ "transmission-remote",
			 "%s:%s" % (auth['address'],auth['port']),
			 "-n",
			 "%s:%s" % (auth['user'], auth['password']),
			 "-a",
			  url
			  ])

threads = []
ignore_qualities = ['720p']
for movie in YTS.all_movies:
	if 'torrents' in movie.keys():
		for torrent in movie['torrents']:
			if not torrent['quality'] in ignore_qualities:
				if not torrent['hash'].lower() in finished:
					thread = threading.Thread(target=add_torrent, args=(torrent['url'],), name="T"+torrent['url'])
					threads.append(thread)
					thread.start()
					time.sleep(0.4)
for t in threads:
	t.join()

print("finish")

