import lxml.etree as ET
from os import listdir
from internetarchive import upload, configure

# insert IA "usernme", "password" here
configure('username', 'password')

# a text string to hold article headings pulled from issue level METS
articles = ''

# folders that contains files 
upload_folder = ['PDF/data', 'jp2/data']

#METS/ALTO folders
alto_folder = 'Alto/data'
mets_folder = 'METS/data'

#getting the MODS embedded in issue level METS
mods_fields = ET.parse("xslt/get_fields.xsl")
get_mods = ET.XSLT(mods_fields)
doc = ET.parse('VA_19301113_issue.xml')
transformed = get_mods(doc)

# getting article headings from article level METS
mets = ET.parse('METS/data/VA_19301113_article.xml')
get_article_headings = ET.parse("xslt/IA-headlines.xsl")
get_art_headings = ET.XSLT(get_article_headings)
art_headings = get_art_headings(mets)

# populating metada dict
metadata = {}
items = str(transformed).split('\t')
metadata['title'] = items[0]
metadata['language'] = items[1]
if items[2]:
	metadata['date'] = items[2]
# passing the xsl result as discription will cuase the script to fial
#metadata['description'] = art_headings
metadata['mediatype'] = 'texts'
metadata['publisher'] = 'Charles A. Clark, Sr.'
metadata['coverage'] = 'Canada; Alberta; Vulcan'
metadata['extent'] = 'v. : ill. ; 40 cm.'
metadata['issuance'] = 'continuing'
metadata['genre'] = 'Newspaper'
metadata['note'] = 'Weekly'

# a unique value for IA use -- the url will be "https://archive.org/details/IA_id"
# to view the file history : "https://archive.org/history/IA_id"
IA_id = 'vulcan_test_pdf_3'

##################### CURL generator -- use this section if uploading from command line #####################

'''location --header 'x-amz-auto-make-bucket:1' --header 'Authorization: LOW C9khuFEwAKAj5Y5X:8s5NsWQzx1wTKfAd' --header 'x-archive-meta-type:postcards' --upload-file PC015175.xml http://s3.us.archive.org/testing_metadata_upload_8/PC015175.xml --upload-file PC015175.jp2 http://s3.us.archive.org/testing_metadata_upload_8/PC015175.jp2 --upload-file PC015175_verso.jp2 http://s3.us.archive.org/testing_metadata_upload_8/PC015175_verso.jp2
curl_base = 'curl --location --header "x-amz-auto-make-bucket:1" --header "Authorization: LOW JRFefruXR3TBohmx:W4vQLN8UXPNI3EPZ"'
for file in listdir(upload_folder):
	file_upload += "--upload-file %s http://s3.us.archive.org/%s/%s" %(file, IA_id, file)
#metadata = "--upload-file %s.xml http://s3.us.archive.org/%s/%s.xml" %(metadata['Call_number'], IA_id, metadata['Call_number'])
col_info = '--header "x-archive-meta01-collection:albertapostcards" --header "x-archive-meta02-collection:university_of_alberta_libraries" --header "x-archive-meta02-collection:toronto"'
meta_header = ''
for key in metadata.keys():
	meta_header += '--header "x-archive-meta-%s:%s" ' %(key, metadata[key])
for line in str(art_headings).split('\n'):
	articles += '--header "x-archive-meta-description:%s " ' %(line)
curl = '%s %s %s %s' %(curl_base, meta_header, articles, file_upload)
print (curl)'''

file_upload = []
# select a folder and upload all files in that folder
# if uploading JP2 files, METS/ALTO files will also be uploaded
for folder in upload_folder:
	for file in listdir(folder):
		file_upload.append('%s/%s' %(folder, file))
	if 'jp2' in folder:
	for file in listdir(alto_folder):
		file_upload.append('%s/%s' %(alto_folder, file))
	for file in listdir(mets_folder):
		file_upload.append('%s/%s' %(mets_folder, file))
	else:
		continue

	# generate the articles string form xsl output -- passing the xsl output directly will fial
	for line in str(art_headings).split('\n'):
		articles += "%s \n"  %(line)
	metadata['description'] = articles


r = upload(IA_id, files=file_upload, metadata=metadata)
print (r[0].status_code)