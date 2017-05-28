import time
import queue
import threading
import subprocess

# customized module
from . import YTS

# global
jobs = queue.Queue()
movies = queue.Queue()

class next:
	def movie():
		while jobs.qsize() > 0:
			# init
			job = jobs.get()

			response = YTS.get_movies(job.__dict__)

			if response:
				list(map(movies.put, response['data']['movies']))

def run(args, func):
	# init
	threads = []
	for i in range(0, args['threads_num']):
		t = threading.Thread(
			name='T' + str(i), 
			target=getattr(globals()['next'](), func),
			args=(var['mode'], var['auto'], var['password'])
		)
		threads.append(t)

	# run
	for i in range(0, len(threads)):
		threads[i].start()

	# wait until finish
	while any(thread.is_alive() for thread in threads):
		time.sleep(1)