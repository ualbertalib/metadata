from internetarchive import upload, configure, get_item, modify_metadata
from Passwords import passwords
import lxml.etree as ET

file = 'WCW.xml'
tree = ET.parse(file)
#output = file.replace('peel/peel_mods_3.7', 'processed_v6')
#out_folder = output.split('.xml')[0]
#if not os.path.exists(out_folder):
#	os.makedirs(out_folder)
root = tree.getroot()
ns = ET.register_namespace('marc', 'http://www.loc.gov/MARC21/slim')
records = {}
for record in root.iter('{http://www.loc.gov/MARC21/slim}record'):
	i = 1
	for control in record.iter('{http://www.loc.gov/MARC21/slim}controlfield'):
		tag = (control.attrib)
		id = (control.text)
		if '008' in str(tag):
			records[id] = {}
	for datafield in record.iter('{http://www.loc.gov/MARC21/slim}datafield'):
		datatag = str(datafield.attrib).split("tag': '")[1].split("',")[0]
		records[id]
		for subfield in datafield.iter('{http://www.loc.gov/MARC21/slim}subfield'):
			subtag = str(subfield.attrib).split("code': '")[1].split("'")[0]
			subf = subfield.text
			if datatag != '':
				tt = datatag+subtag
				if tt in records[id].keys() and subf != None:
					
					records[id][tt] += " " + subf
				else:
					records[id][tt] = subf

#print(records['960820 1870'])

passwd = passwords['IA_digi'][1]
user = passwords['IA_digi'][0]

configure(user, passwd)

metadata = {}
for item in records.keys():
	item_id = 'wcw_test_item_' + item.replace(' ', '_')
	if '245a' in records[item].keys():
		metadata['title'] = records[item]['245a']
	if '255a' in records[item].keys():
		metadata['Scale'] = records[item]['255a']
	if '260c' in records[item].keys():
		metadata['Date'] = records[item]['260c']
	if '300a' in records[item].keys():
		metadata['extent'] = records[item]['300a']
	if '300c' in records[item].keys():
		metadata['Dimensions'] = records[item]['300c']
	if '260b' in records[item].keys():
		metadata['publisher'] = records[item]['260b']
		if '260b' in records[item].keys() and '260a' in records[item].keys(): 
			if records[item]['260b'] != None and records[item]['260a'] != None:
				metadata['publisher'] = records[item]['260b'] + ' - ' + records[item]['260a'] 
	if '650a' in records[item].keys():
		metadata['subject'] = records[item]['650a']
	if '500a' in records[item].keys():
		metadata['notes'] = records[item]['500a']

	print (metadata)
	file = ''
	item = get_item(item_id)
	print (item_id)
	r = item.modify_metadata(metadata)
	'''r = upload(item_id, files='test.txt', metadata=metadata)
	print (r[0].status_code, item_id)'''


		
