import requests
import json
import threading

finished = False
all_movies = []
lock = threading.Lock() 
url = 'https://yts.ag/api/v2/list_movies.json'

def get_json(page, params):

	params.update( {'page': page} )
	resp_json={}

	try:
		resp = requests.get(url, params=params)
	except Exception as e:
		print (str(e))

	resp_json = json.loads(resp.text)
	return resp_json


def get_page_number(params):
	resp = get_json(1,params)
	print(resp['data']['movie_count'],resp['data']['limit'] )
	page_number = resp['data']['movie_count'] / resp['data']['limit'] + 1
	return int(page_number)

def collecting(page, params):
	global all_movies, lock
	print( "collecting page%d" % page)
	resp = get_json(page, params)
	lock.acquire()
	all_movies += resp['data']['movies']
	lock.release()
	
def collect_movies(params):
	
	finished = False
	all_movies = []
	threads = []
	page_number = get_page_number(params)
	
	for page in range(1, page_number+1):
	 	thread = threading.Thread(target=collecting, args=(page, params), name='T'+str(page))
	 	threads.append(thread)
	 	thread.start()

	for thread in threads:
		thread.join()
