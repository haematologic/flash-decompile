# (C) 2016 Duncan Brian
# encoding: UTF-8

from os import listdir
from os.path import isfile, isdir, join, exists
from shutil import move
import re
import sys
import timings

datfiles = {}
txtfiles = {}
imagefiles = {}
rejectlines = []


def main():
    ext = None
    getdata()

    if len(sys.argv) >= 5:
        ext = '.' + sys.argv[4].strip('.')

    if len(sys.argv) >= 4:
        command = sys.argv[1]
        datfile = sys.argv[2]
        source_dir = sys.argv[3].strip('/')

        print("command: %s\ndat_file: %s\nsource_dir: %s\n extension: %s\n" % (
        sys.argv[1], sys.argv[2], sys.argv[3], ext))

        if not isdir(source_dir):
            print("source directory '" + source_dir + "' does not exist.")

        if command == 'move':

            movefiles(datfile, source_dir, ext)

        elif command == 'search':

            searchfiles(source_dir, datfile, ext)
    else:
        print("Input DAT file required: remove.py move|search DATFILE source_dir (file_extension e.g. .txt)")


def loadfile(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
    except IOError:
        raise
    return lines


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


def dirlist(source_dir, source_ext, append_path=0):

    # generator is the answer - how to combine for and if in python:
    # http://stackoverflow.com/questions/6981717/pythonic-way-to-combine-for-loop-and-if-statement
    dirfiles = (f[:-4] for f in listdir(source_dir) if (isfile(join(source_dir, f)) and f.endswith(source_ext)))
    files = {}

    for f in dirfiles:
        if append_path:
            files[f] = join(source_dir, f+source_ext)
        else:
            files[f] = f+source_ext

    return files


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
                # print(result)

                resv.append((result, ln, match, line))
                # print("%d: '%s' found in line %d of '%s':\t%s" % (result, match, ln, f, line))

            else:

                match = None

        if not result:

            # Append line if result not found in query set
            resv.append((result, ln, match, line))

    # print(resv)
    # print("file %s: resv: %s" % (f, resv))
    return resv


def replacelines(query_set, f, query_ext=None, new_ext=None):

    results = searchlines(query_set, f, query_ext)

    for resv in results:
        # resv[0] = result, resv[1]=ln, resv[2] = match.string/None, resv[3]=line
        # print(resv[0], resv[1], resv[2], resv[3], "\n")

        if (resv[0]==1):

            repl = re.sub(query_ext, new_ext, resv[3],re.I)

            print("%d: %s %d query '%s' found replaced with '%s' in line: %s" % (resv[0], f, resv[1], resv[2], repl, resv[3]))
            pass

        elif (resv[0]==0):

            # print("%d: %s %d no query item found in line: %s" % (resv[0], f, resv[1], resv[3]))
            pass

    return 0


def searchfiles(source_dir, datfile, ext):

    supfiles = {}
    dirfiles = dirlist(source_dir, '.txt', 1)
    new_ext='.jpg'

    # print("%s\n\n%s\n" % (datlines, files))
    # for f in dirfiles:

        # print("%s:%s\n\n\n\n\n" % (f, lines))
        # result = replacelines(datlines, f, ext, new_ext)

        # if result:
          #  pass
    # print("%s\n" % supfiles)

def prepoutput():

    if not isdir('output'):
        print("output dir does not exist")



def getdata():

    datfiles = dirlist('dats', '.dat', 1)
    txtfiles = dirlist('extracts', '.txt', 1)
    imagefiles = dirlist('morphology/images','.jpg', 1)

    if 'reject' in datfiles:
        rejectlines = [re.escape(line) for line in loadfile(datfiles['reject'])]

        print(rejectlines)

        rejectline = re.compile(r"\b%s\b" % r"\b|\b".join(rejectlines), re.I)
        x = 'Arial'
        if not rejectline.search(x):
            print(x)
        else:
            print('no match')

        print(rejectline,'\n',x)

    print (datfiles, txtfiles, imagefiles, sep='\n', end='\n')

    return

if __name__ == '__main__':
    main()