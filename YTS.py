import requests
import json
import threading
import queue

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
	page_number = resp['data']['movie_count'] / resp['data']['limit'] + 1
	return int(page_number)
	
class collector:
	def __init__(self):
		self.movies = []
		self.page_number = 0
		self.lock = threading.Lock() 
	    
	def start(self, params):
		self.movies = []
		self.page_number = get_page_number(params)
		threads = []

		for page in range(1, self.page_number+1):
		 	thread = threading.Thread(target=self.collect, args=(page, params), name='T'+str(page))
		 	threads.append(thread)
		 	thread.start()

		for thread in threads:
			thread.join()
	
	def collect(self, page, params):
		print( "collecting page%d ..." % page)
		resp = get_json(page, params)
		self.lock.acquire()
		self.movies += resp['data']['movies']
		self.lock.release()
