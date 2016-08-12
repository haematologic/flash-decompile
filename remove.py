# (C) 2016 Duncan Brian

from os import listdir
from os.path import isfile, isdir, join, exists
from shutil import move
import sys

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


def searchfiles(source_dir, datfile):
	supfiles = []
	dirfiles = [f for f in listdir(source_dir) if isfile(join(source_dir, f))]
	datlines = loadfile(datfile)
 	#print("%s\n\n%s\n" % (datlines, files))
	for f in dirfiles:
		lines = loadfile(join(source_dir,f))
		#print("%s:%s\n\n\n\n\n" % (f,lines))
		for item in datlines:
			result = 0
			for ln, line in enumerate(lines):
				if item in line:
					result = 1
					print("%d: '%s' found in %s:\n(%d) %s\n" % (result, item, f, ln, line))
					supfiles.append(f)
				else:
					result = 0
					#print("%d: %s %s\n" % (result, item, line))
	supuniq = uniqf7(supfiles)
	print("%s\n" % supuniq)


if __name__ == '__main__':
	if len(sys.argv) >= 5:
		command = sys.argv[1]
		datfile = sys.argv[2]
		source_dir = sys.argv[3].strip('/')
		ext = sys.argv[4].strip('.')
		print("command: %s\ndat_file: %s\nsource_dir: %s\nextension: %s\n" % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
		if not isdir(source_dir):
			print("source directory '"+source_dir+"' does not exist.")
		if command == 'move':
			movefiles(datfile, source_dir, ext)
		elif command == 'search':
			searchfiles(source_dir, datfile)
	else:
		print("Input DAT file required: remove.py move|search DATFILE source_dir file_extension e.g. .txt")