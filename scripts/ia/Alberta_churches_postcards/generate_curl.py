import lxml.etree as ET
from os import listdir

folder = 'Meta'
xslt = ET.parse("get_fields.xsl")
for i, file in enumerate(listdir(folder)):
	creator = ''
	transform = ET.XSLT(xslt)
	doc = ET.parse(folder + '/' + file)
	transformed = transform(doc)
	values = {}
	items = str(transformed).split('\t')
	values['Call_number'] = items[0]
	values['title'] = items[1]
	values['mediatype'] = items[2]
	if items[3] != 'N/A' and items[4] != 'N/A':
		creator = items[3] + ':' + items[4]
	elif items[3] != 'N/A' and items[4] == 'N/A':
		creator = items[3]
	print (creator)
	if creator != '':
		values['creator'] = creator
	values['coverage'] = items[5]+ ';' + items[6]+ ';' + items[7]
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
	#print (values)
	#location --header 'x-amz-auto-make-bucket:1' --header 'Authorization: LOW C9khuFEwAKAj5Y5X:8s5NsWQzx1wTKfAd' --header 'x-archive-meta-type:postcards' --upload-file PC015175.xml http://s3.us.archive.org/testing_metadata_upload_8/PC015175.xml --upload-file PC015175.jp2 http://s3.us.archive.org/testing_metadata_upload_8/PC015175.jp2 --upload-file PC015175_verso.jp2 http://s3.us.archive.org/testing_metadata_upload_8/PC015175_verso.jp2
	IA_id = 'prairiechurchesa01posttester_%s' %(i)
	curl_base = 'curl --location --header "x-amz-auto-make-bucket:1" --header "Authorization: LOW JRFefruXR3TBohmx:W4vQLN8UXPNI3EPZ"'
	image = image_verso = "--upload-file %s.jpg http://s3.us.archive.org/%s/%s.jpg" %(values['Call_number'], IA_id, values['Call_number']) 
	image_verso = "--upload-file %s_verso.jpg http://s3.us.archive.org/%s/%s_verso.jpg" %(values['Call_number'], IA_id, values['Call_number']) 
	metadata = "--upload-file %s.xml http://s3.us.archive.org/%s/%s.xml" %(values['Call_number'], IA_id, values['Call_number'])
	col_info = '--header "x-archive-meta01-collection:albertapostcards" --header "x-archive-meta02-collection:university_of_alberta_libraries" --header "x-archive-meta02-collection:toronto"'
	meta_header = ''
	for key in values.keys():
		meta_header += '--header "x-archive-meta-%s:%s" ' %(key, values[key])
	curl = '%s %s %s %s %s' %(curl_base, meta_header, metadata, image, image_verso)
	print (curl)