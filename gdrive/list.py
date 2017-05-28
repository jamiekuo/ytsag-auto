import os
import re
import argparse
import subprocess

# constant
__version__ = '1.0'
__description__ = 'upload - my google drive upload script'
__epilog__ = 'Report bugs to <cjyeh@cs.nctu.edu.tw>'

# pattern
query_pattern = '"{id}" in parents'

class Object:
	def __init__(self, var):
		self.id = var[:28]
		self.type = 'bin' if 'bin' in var else 'dir'
		self.name = var[29:var.find(self.type)].replace(' ', '')

def parse_argv():
	# init
	parser = argparse.ArgumentParser(
		description=__description__,
		epilog=__epilog__
	)

	# add argument
	parser.add_argument(
		'-v', '-V', '--version', 
		action='version', 
		help='Print program version', 
		version='v{}'.format(__version__)
	)
	parser.add_argument(
		'-p', '--parent',
		action='store',
		help='Remote folder id',
		default='root'
	)

	results = parser.parse_args()
	
	return {
		'parent': results.parent
	}

def list(id):
	# var
	temp = None
	results = []

	proc = subprocess.Popen(
		['gdrive', 'list','--query',query_pattern.format(id=id), '--no-header'],
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE
	)

	out, err = proc.communicate()

	out = out.decode('utf-8')[:-1]
	err = err.decode('utf-8')[:-1]

	results = [Object(i).__dict__ for i in out.split('\n')]

	# recursive
	for i in results:
		if i['type'] == 'bin':
			continue
		i['children'] = list(i['id']) 

	return results

def main():
	# var
	args = parse_argv()

	a = list(args['parent'])


if __name__ == '__main__':
	main()