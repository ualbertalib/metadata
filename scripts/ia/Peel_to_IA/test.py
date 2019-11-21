import tarfile, os, sys, linecache
from Leg_processeing import *
from Util import *

with open('upload-log.txt', 'a') as log:
	code = 'LPM'
	for index, dir in enumerate(os.listdir('Vulcan')):
		try:
			if index < 2500:
				#if os.path.isdir(dir):
				path = 'Vulcan/%s' %(dir)
				print ('%s strat processing %s' %(index+1, path))
				make_process_folder(path)
				metadata_obj = metadata(path, code)
				metadata_obj.untar_mets_alto()
				top_mods = metadata_obj.get_mods()
				mets_data = metadata_obj.get_mets_data()
				item_id = 'test3' + code + '_' + mets_data[0] 
				mets = mets_data[1]
				art = mets_data[2]
				metadata = metadata_obj.make_IA_metadata(mets, top_mods, art, item_id) 
				print (item_id)
				image_obj = images(path, item_id)
				image = image_obj.generate_tar()
				uplaod_obj = file_uplaod(path, item_id, metadata, log)
				uplaod = uplaod_obj.upload_to_IA()
				print ('----------------------------------------------------------')
			else:
				break
		except:
			PrintException()
			pass