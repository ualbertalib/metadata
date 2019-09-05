import lxml.etree as ET
from datetime import datetime as T
from os import listdir
from Passwords import passwords
from internetarchive import upload, configure, get_item
import re, shutil

passwd = passwords['IA_digi'][1]
user = passwords['IA_digi'][0]

# insert IA "usernme", "password" here
configure(user, passwd)

folder = 'Meta'
xslt = ET.parse("get_fields.xsl")
for i, file in enumerate(listdir(folder)):
	if file in ['nothing']:
		pass
	else:
		print (file)
		item_id = 'prairiepromisespostcard_%s' %(i+1)
		creator = ''
		transform = ET.XSLT(xslt)
		doc = ET.parse(folder + '/' + file)
		transformed = transform(doc)
		values = {}
		items = str(transformed).split('\t')
		#values['Call_number'] = items[0]
		values['title'] = items[1]
		if items[2] == 'still image':
			values['mediatype'] = 'image'
		else:
			values['mediatype'] = items[2]
		if items[3] != 'N/A' and items[4] != 'N/A':
			creator = items[3] + ':' + items[4]
		elif items[3] != 'N/A' and items[4] == 'N/A':
			creator = items[3]
		if len(creator) > 1:
			values['creator'] = creator
		if len(items[5]) > 1:
			values['coverage'] = items[5].replace(',','') 
			if len(items[6]) > 1:
				values['coverage'] = items[5].replace(',','') + ';' + items[6].replace(',','')
				if len(items[7]) > 1:
				 values['coverage'] = items[5].replace(',','') + ';' + items[6].replace(',','') + ';' + items[7].replace(',','')
		values['extent'] = items[8]
		if 'public_description::' in items[13]:
			values['description'] = items[13].split('public_description::')[1].split('_--_--_')[0]
		if len(items[9]) > 1:
			values['issuance'] = items[9]
		if items[10] != 'N/A':
			values['date'] = items[10]
		if len(items[11]) > 1:
			values['language'] = items[11]
		subjects = []
		for sub in items[12].split('_--_--_'):
			if len(sub) > 1:
				subjects.append(sub.strip())
		if len(subjects) > 0:
			values['subject'] = subjects
		values['sponsor'] = 'University of Alberta Libraries'
		values['contributor'] = 'University of Alberta Libraries'
		values['collection'] = 'albertapostcards'
		note_item = items[13].replace(values['description'], '').replace('public_description::', '').replace('public_', '').split('_--_--_')
		if len(note_item) > 0:
			values['notes'] = ''
		for note in note_item:
			if note == '':
				pass
			else:
				n = note.split('::')
				if len(n) > 1:
					if n[1] != 'N/A' and n[1] != ',':
						values['notes'] += '[%s]: %s  ' %(n[0], n[1])
					if n[0] == 'postmark_date' and values['date'] == '':
						year = re.search('\d{4}', n[1])
						if (year):
							values['date'] = year.group()

		#print (values)
		#file_upload = []
		#uploaded = 'uploaded'
		image = file.replace('.xml', '')
		print ('uploading %s %s' %(item_id, file))
		#file_upload.append('%s/%s' %(folder, file))
		#file_upload.append('img/%sr.tiff' %(image))
		#file_upload.append('img/%sv.tiff' %(image))
		item = get_item(item_id)
		r = item.modify_metadata(values)
		#r = upload(item_id, files=file_upload, metadata=values)
		print (r.status_code)
		'''if r[0].status_code == 200:
			print ('moving %s to uploaded' %(image))
			shutil.move('img/%sr.tiff' %(image), uploaded)
			shutil.move('img/%sv.tiff' %(image), uploaded)
			shutil.move('Meta/%s.xml' %(image), uploaded)
		else:
			print ('uploading %s failed -- will not be moved to uploaded folder' %(item_id))'''