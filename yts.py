import requests
import json
import subprocess
import time

pars = {
	'sort_by' : 'year',
	'limit' : 50,
	'page' : 1
}

for page in range(1, 124):

	try:
		r = requests.get('https://yts.ag/api/v2/list_movies.json', params=pars)
	except Exception as e:
		print (str(e))

	# result = json.load(r.text)
	with open("done.%d" % page, "w+") as done:
		done.write(r.text)

	result = json.loads(r.text)
	# print(result['data']['movies'])

	for movie in result['data']['movies']:
		for torrent in movie['torrents']:
			subprocess.call(["transmission-remote",
							 "35.189.175.32:80",
							 "-n",
							 "user:pw",
							 "-a",
							  torrent['url']])
			time.sleep(1)
			#break
		#break
	#break
