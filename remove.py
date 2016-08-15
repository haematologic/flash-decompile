# (C) 2016 Duncan Brian

from os import listdir
from os.path import isfile, isdir, join, exists
from shutil import move
import re
import sys
import timings


def loadfile(filename):
	try:
		with open(filename) as f:
			lines = f.read().splitlines()
	except IOError:
		raise
	return lines


def uniqf7(seq):
	"""
	http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
	"""
	seen = set()
	seen_add = seen.add
	return [x for x in seq if not (x in seen or seen_add(x))]


def movefiles(datfile, source_dir, ext):
	
	files=loadfile(datfile)
	
	print("%s\n" % files)
	
	for f in files:
		destfile = join('morphology',f+'.'+ext)
		sourcefile = join(source_dir,f+'.'+ext)
		try:

			if not exists(sourcefile):
				
				print("%s does not exist" % sourcefile)
			else:

				print(sourcefile, destfile)
				
				move(sourcefile,destfile)
		
		except:
			
			raise
	return


def listfiles(source_dir, source_ext, append_path=0):
	
	dirfiles = [f for f in listdir(source_dir) if (isfile(join(source_dir, f)) and f.endswith(source_ext))]
	
	if (append_path == 1):
		
		dirfiles = [join(source_dir,f) for f in dirfiles]
	
	return dirfiles


def searchlines(query_set, f, query_ext=None):
	
	lines = loadfile(f)
	resv = []
	
	for ln, line in enumerate(lines):
		result = 0			

		for query_string in query_set:
			print(query_string,query_ext)
			if re.search(query_ext,query_string, re.I):
				pattern = re.compile('.+\\'+query_string+'$', re.I)
				match = pattern.search(line)
			else:
				print("md")
				query_string=query_string+query_ext
				pattern = re.compile(query_string, re.I)
				match = pattern.match(line)
				
			if match and result < 1:
				
				result += 1
				match = match.string
				#print(result)

				resv.append((result, ln, match, line))
				#print("%d: '%s' found in line %d of '%s':\t%s" % (result, match, ln, f, line))
			
			else:

				match = None

		if not result:
			
			# Append line if result not found in query set
			resv.append((result, ln, match, line))
			
	#print(resv)
	#print("file %s: resv: %s" % (f, resv))
	return resv


def replacelines(query_set, f, query_ext=None, new_ext=None):

	results = searchlines(query_set, f, query_ext)
	
	for resv in results:
		# resv[0] = result, resv[1]=ln, resv[2] = match.string/None, resv[3]=line
		#print(resv[0],resv[1],resv[2],resv[3],"\n")

		if (resv[0]==1):

			repl = re.sub(query_ext,new_ext,resv[3],re.I)

			print("%d: %s %d query '%s' found replaced with '%s' in line: %s" % (resv[0], f, resv[1], resv[2], repl, resv[3]))
			pass

		elif (resv[0]==0):
				
			#print("%d: %s %d no query item found in line: %s" % (resv[0], f, resv[1], resv[3]))
			pass
		
	return 0


def searchfiles(source_dir, datfile):
	
	supfiles = {}
	dirfiles = listfiles(source_dir,'.txt',1)
	datlines = loadfile(datfile)
	new_ext='.jpg'

 	#print("%s\n\n%s\n" % (datlines, files))
	for f in dirfiles:
		
		#print("%s:%s\n\n\n\n\n" % (f,lines))
		result = replacelines(datlines, f, ext, new_ext)
		
		if result:
	
			supfiles[f]=(f,item,result[1])
	
	#print("%s\n" % supfiles)


if __name__ == '__main__':
	
	ext = None
	
	if len(sys.argv) >= 5:
		ext = '.'+sys.argv[4].strip('.')

	if len(sys.argv) >= 4:
		command = sys.argv[1]
		datfile = sys.argv[2]
		source_dir = sys.argv[3].strip('/')
	
		print("command: %s\ndat_file: %s\nsource_dir: %s\n extension: %s\n" % (sys.argv[1], sys.argv[2], sys.argv[3], ext))
	
		if not isdir(source_dir):
	
			print("source directory '"+source_dir+"' does not exist.")
	
		if command == 'move':
	
			movefiles(datfile, source_dir, ext)
	
		elif command == 'search':
	
			searchfiles(source_dir, datfile)
	else:
		print("Input DAT file required: remove.py move|search DATFILE source_dir (file_extension e.g. .txt)")
	
	