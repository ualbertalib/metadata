from config import mig_ns as namespaces
from datetime import datetime
import pickle
import time
import requests
import linecache
import sys
import os


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
			return v.replace(line['uri'], '').replace('/', "_")


def PrintException():
	""" for testing """
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	print("EXCEPTION IN (%s, LINE %s '%s'): %s" % (filename, lineno, line.strip(), exc_obj))


def cleanOutputs():
	types = [
		"collection",
		"community",
		"generic",
		"thesis",
		"technical",
		"relatedObject"
	]
	_deleteQueries()
	_deleteResults(types)
	_deleteAudit()


def _deleteQueries():
	for the_file in os.listdir('cache/'):
		file_path = os.path.join('cache/', the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)


def _deleteResults(types):
	for ptype in types:
		folder = 'results/notInJupiter/%s' % (ptype)
		if not os.path.exists(folder):
			os.makedirs(folder)
		for the_file in os.listdir(folder):
			file_path = os.path.join(folder, the_file)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
			except Exception as e:
				print(e)
	for ptype in types:
		folder = 'results/inJupiter/%s' % (ptype)
		if not os.path.exists(folder):
			os.makedirs(folder)
		for the_file in os.listdir(folder):
			file_path = os.path.join(folder, the_file)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
			except Exception as e:
				print(e)

def _deleteAudit():
	folder = 'Audit'
	if not os.path.exists(folder):
		os.makedirs(folder)
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)

def get_Jupiter_noids():
	response = requests.get("http://solrcloud.library.ualberta.ca:8080/solr/jupiter/select?fl=hydra_noid_ssim&indent=on&q=hydra_noid_ssim:*&rows=50000&wt=json").json()
	jupiter_items = response['response']['numFound']
	print ('As of %s there are %s items in Jupiter' % (datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), jupiter_items))
	noids = []
	for item in response['response']['docs']:
		if item['hydra_noid_ssim'] not in noids:
			noids.append(item['hydra_noid_ssim'][0])
	with open('Jupiter_noids.pickle', 'wb') as Jupiter_noids:
		pickle.dump(noids, Jupiter_noids)

	return (noids)