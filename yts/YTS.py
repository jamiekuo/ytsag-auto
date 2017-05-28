import json
import requests

# customized module
from . import Job

class Object:
	def __init__(self, var):
		# def keys
		self.limit = var['limit']
		self.page = var['page']
		self.quality = var['quality']
		self.minimum_rating = var['minimum_rating']
		self.query_term = var['query_term']
		self.order_by = var['order_by']
		self.with_rt_ratings = var['with_rt_ratings']

def get_movies(payload):
	try:
		_request = requests.get('https://yts.ag/api/v2/list_movies.json', params=payload)
		_response = json.loads(_request.text)
		return _response
	except Exception as e:
		print('[%10s] %s' % ('api', str(e)))
		return None

def request_api(payload):
	# var
	result = []
	var = get_movies(payload)
	pages_num = int(var['data']['movie_count'] / payload['limit']) + 1

	# information
	print('[%10s] movie_count: %d' % ('info', var['data']['movie_count']))
	print('[%10s] limit: %d' % ('info', var['data']['limit']))
	print('[%10s] pages_num: %d' % ('info', pages_num))

	for i in range(1, pages_num + 1):
		payload['page'] = i
		thread.jobs.put(Object(payload))

	job.run(payload)

	# format
	while Job.movies.qsize() > 0:
		result.append(Job.movies.get())

	return result