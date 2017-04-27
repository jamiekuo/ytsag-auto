import requests
import json
import subprocess
import time

auth = {}
with open('auth.json', 'r') as fp:
	auth = json.load(fp)

pars = {
	'sort_by' : 'year',
	'limit' : 50,
	'page' : 1
}

for page in range(1, 124):
	
	pars['page']= page
	try:
		r = requests.get('https://yts.ag/api/v2/list_movies.json', params=pars)
	except Exception as e:
		print (str(e))


	result = json.loads(r.text)
	# print(result['data']['movies'])

	for movie in result['data']['movies']:
		for torrent in movie['torrents']:
			subprocess.call(["transmission-remote",
							 "%s:80" % "localhost",
							 "-n",
							 "%s:%s" % ('jamie', auth['password']),
							 "-a",
							  torrent['url']])
