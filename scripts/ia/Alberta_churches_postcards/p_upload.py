import lxml.etree as ET
from datetime import datetime as T
from os import listdir
from internetarchive import upload, configure, get_item

# insert IA "usernme", "password" here
configure('username', 'pasword')

folder = 'Meta'
xslt = ET.parse("get_fields.xsl")
for i, file in enumerate(listdir(folder)):
	item_id = 'prairiechurchespostcards_%s' %(i+2)
	creator = ''
	transform = ET.XSLT(xslt)
	doc = ET.parse(folder + '/' + file)
	transformed = transform(doc)
	values = {}
	items = str(transformed).split('\t')
	values['Call number'] = items[0]
	values['title'] = items[1]
	if items[2] == 'still image':
		values['mediatype'] = 'image'
	else:
		values['mediatype'] = items[2]
	if items[3] != 'N/A' and items[4] != 'N/A':
		creator = items[3] + ':' + items[4]
	elif items[3] != 'N/A' and items[4] == 'N/A':
		creator = items[3]
	print (creator)
	if creator != '':
		values['creator'] = creator
	if items[7] == "Medicine":
		values['coverage'] = items[5].replace(',','') + ';' + items[6].replace(',','') + ';' + "Medicine Hat"
	else:
		values['coverage'] = items[5].replace(',','') + ';' + items[6].replace(',','') + ';' + items[7].replace(',','')
	values['extent'] = items[8]
	if 'description::' in items[13]:
		values['description'] = items[13].split('description::')[1].split('_--_--_')[0]
	values['issuance'] = items[9]
	if items[10] != 'N/A':
		values['date'] = items[10]
	values['language'] = items[11]
	values['subject'] = items[12]
	values['sponsor'] = 'University of Alberta Libraries'
	values['contributor'] = 'University of Alberta Libraries'
	values['collection'] = 'albertapostcards'
	note_item = items[13].replace(values['description'], '').replace('description::', '').replace('public_', '').split('_--_--_')
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

	file_upload = []
	image = file.replace('.xml', '')
	print ('uploading %s %s' %(item_id, file))
	file_upload.append('%s/%s' %(folder, file))
	file_upload.append('All/%s.jpg' %(image))
	file_upload.append('All/%s_verso.jpg' %(image))
	item = get_item(item_id)
	r = item.modify_metadata(values)
	#r = upload(item_id, files=file_upload, metadata=values)
	print (r.status_code)
