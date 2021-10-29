import os
from internetarchive import upload, configure, get_item, modify_metadata
from Passwords import passwords
import lxml.etree as ET
from zipfile import ZipFile


peel = '/home/danydvd/hdd/projects/metadata/Jupiter_2/roleTerm/peel/'

files = {}

def listdirs(base):
    for file in os.listdir(base):
        d = os.path.join(base, file)
        if os.path.isdir(d):
            listdirs(d)
        else:
        	name = d.split('/')[-1].split('.xml')[0]
        	files[name] = d
    return files

 
mods_file = listdirs(peel)



passwd = passwords['IA_digi'][1]
user = passwords['IA_digi'][0]

configure(user, passwd)

tifs = {}
missing_mods = []

with open ("missing-mods.txt", "r") as miss:
	for line in miss:
		l = line.strip()
		missing_mods.append(l)

for image in os.listdir('tif'):
	ia_id = image.split('.')[0].split('(')[0]
	#ia_id = image.split('.tif')[0]
	if ia_id not in tifs.keys():
		tifs[ia_id] = [image]
	else:
		tifs[ia_id].append(image)

for image in tifs.keys():
	#if image in mods_file.keys():
	if image in missing_mods:
		modxml = mods_file[image]
		#modxml = '%s.xml' %(image.split('.')[0])
		mods = ET.parse('get_fields.xsl')
		get_mods = ET.XSLT(mods)
		mod = ET.parse(modxml)
		transformed_mods = get_mods(mod)
		mods_fields = str(transformed_mods).split('\t')
		item_id = "WCW_{0}".format(image.replace('.', '_'))
		metadata = {}
		metadata['title'] = mods_fields[0].strip()
		if mods_fields[1] != '':
			metadata['title'] = mods_fields[0].strip() + ' - ' + mods_fields[1].strip() 
		if mods_fields[2] != '':
			metadata['Alternative_title'] = mods_fields[2].strip()
		metadata['publisher'] = mods_fields[5] + ': ' + mods_fields[8] 
		if mods_fields[4] != '':
			creator = ''
			for i, c in enumerate(mods_fields[4].split('_--_--_')):
				if c != '':
				#creator = creator +  c + '. '
					metadata['Creator[%s]' %(i)] = c
		if mods_fields[9] != '':
			metadata['extent'] = mods_fields[9]
		metadata['issuance'] = mods_fields[10]
		metadata['date'] = mods_fields[11]
		metadata['language'] = mods_fields[12]
		metadata['scale'] = mods_fields[13]
		genre = []
		for g in mods_fields[6].split('_--_--_'):
			genre.append(g)
		metadata['genre'] = genre
		metadata['mediatype'] = 'texts'
		metadata['collection'] = 'wcw_peel'
		n = ''
		note_item =  mods_fields[14].split('_--_--_')
		if len(note_item) > 0:
			for note in note_item:
				if note == '':
					pass
				else:
					n += note + ' '
			metadata['notes'] = n
		subject = []
		for s in mods_fields[7].split('_--_--_'):
			if len(s) > 0 and s[-2] == '-':
				s = s[0:-2]
			subject.append(s)
		metadata['subject'] = subject
		metadata['coordinates'] = mods_fields[15]
		print (item_id)
		#print (metadata)
		file_upload = []
		#file_upload.append(missing_mods[image])
		file_upload.append(modxml)
		for file in tifs[image]:
			with ZipFile('%s_images.zip' %(image), "a") as zip:
				obj = 'tif/%s' %(file)
				print (file)
				zip.write(obj)
				zip.close()
		file_upload.append('%s_images.zip' %(image))
		print (file_upload)
		r = upload(item_id, files=file_upload, metadata=metadata)
		#item = get_item(item_id)
		#print (item_id)
		#r = item.modify_metadata(metadata)
		print (r[0].status_code)
	else:
		if image not in missing_mods:
			missing_mods.append(image)

with open ("missing-mods1.txt", "w") as log:
	for item in missing_mods:
		log.write(item + '\n')
	log.close()
