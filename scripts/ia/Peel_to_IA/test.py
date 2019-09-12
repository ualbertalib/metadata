import tarfile, os, sys, linecache
from Processing import *
from Process_factory import *
from Util import *

with open('upload-log.txt', 'a') as log:
	code = 'VCA'
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
				metadata_process = metadata_obj.get_mets_data(top_mods)
				item_id = metadata_process[0]
				meta = metadata_process[1]
				image_obj = images(path, item_id)
				image = image_obj.generate_tar()
				#uplaod_obj = file_uplaod(path, item_id, meta, log)
				#uplaod = uplaod_obj.upload_to_IA()
				print ('----------------------------------------------------------')
			else:
				break
		except:
			PrintException()
			pass