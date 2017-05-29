#!/usr/bin/python
import os
import time
import internetarchive

#without s3
#from internetarchive import configure
#configure('IA username', 'password')

#s3 for Danoosh
from internetarchive import get_session
c = {'s3': {'access': 'C9khuFEwAKAj5Y5X', 'secret': '8s5NsWQzx1wTKfAd'}}
s = get_session(config=c)
s.access_key
'C9khuFEwAKAj5Y5X'

#preparing the input file 
with open('albertagovpub_duplicates_file_names.json', 'r') as file:
	#this is the list of new files added to the collection from the last download
	with open('albertagovpub_duplicates_file_names_temp.json', "w") as f_new:
		for eachLine in file:
			line = eachLine.replace(" ", "")
			line = line.replace("{", "")
			line = line.replace("}", "")
			line = line.replace(":", "")
			line = line.replace("identifier", "")
			line = line.replace("\"", "")
			f_new.write("%s" % line)

with open('albertagovpub_duplicates_file_names_temp.json', 'r') as file_new:
	#segmenting large file to avoid running down the IA servers 
	segment = file_new.readlines()[11003:11010]
	for lines in segment:
		itemid = lines
		itemid = itemid.strip()
		item = internetarchive.get_item(itemid)
		marc = item.get_file(itemid + '_meta.xml')
		marc.download()
		print "Downloading " + itemid + " ..."
		time.sleep(0)

os.remove('albertagovpub_duplicates_file_names_temp.json')



