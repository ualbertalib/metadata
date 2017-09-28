from config import mig_ns as namespaces
import linecache
import sys


def addPrefixes(v):
	""" replaces a namespace with a prefix """
	for line in namespaces:
		if line['uri'] in v:
			v = v.replace(line['uri'], line['prefix'] + ':')
	return v


def removeNS(v):
	""" removes the namespace from a predicate, leaving only the predicate term """
	for line in namespaces:
		if line['uri'] in v:         
			return v.replace(line['uri'], '')


def PrintException():
	""" for testing """
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	print("EXCEPTION IN (%s, LINE %s '%s'): %s" % (filename, lineno, line.strip(), exc_obj))
