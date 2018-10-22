from os import listdir, getcwd, chdir, makedirs
from os.path import isfile, join, exists
import time
from datetime import datetime
import json
import requests
import internetarchive
from internetarchive import get_session

# determine the file type to be downloaded. Add more as needed
file_type = [
	'_djvu.txt',
	'.gif',
	'.pdf'
	]

# Internet Archive API access tokens
IA_access = {'s3': {'access': '<your access token>', 'secret': '<your secret>'}}


def search_IA():
	# set the working directory 
	work_dir = getcwd()
	chdir(work_dir)
	#authenticate to Internet Archives
	s = get_session(config=IA_access)
	s.access_key
	#search IA/heresies_magazine collection
	search = internetarchive.search_items('collection:heresies_magazine')
	print ('As of %s there are %s items in heresies_magazine collection of Internet Archives' % (datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), len(search)))
	# iterate over the results
	for i, result in enumerate(search):
	    # set itemid as identifier (id in Internet Archive)
	    itemid = result['identifier']
	    print ('file: %s' %(itemid))
	    # get all file types for the itemid
	    for filetype in file_type:
	    	# removing extra characters for naming. If you are downloading similar file type (e.g. .pdf and .pdf_meta.txt) this will make sure to store them in different folders 
	    	ft = filetype.replace("djvu", "").replace(".", "").replace("_", "")
	    	print ('getting %s files' %(ft))
	    	folder = 'files/%s' %(ft)
	    	if not exists(folder):
	    		makedirs(folder)
	    	chdir(folder)
	    	filename = itemid + filetype
	    	if isfile(filename):
	    		print ('%s of type %s is in folder -- skipping download' %(itemid, filetype))
	    	else:
	    		item = internetarchive.get_item(itemid)
	    		file = item.get_file(itemid + filetype)
	    		try:
	    			file.download()
	    		except:
	    			PrintException()
	    	chdir(work_dir)

def PrintException():
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	print("EXCEPTION IN (%s, LINE %s '%s'): %s" % (filename, lineno, line.strip(), exc_obj))



if __name__ == "__main__":
	search_IA()
