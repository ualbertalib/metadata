import tarfile, os, re, shutil, time, sys, linecache
import lxml.etree as ET
from datetime import datetime as T
from internetarchive import upload, configure
from Util import PrintException

# insert IA "usernme", "password" here
configure('username', 'password')

class processing_obj():
	def __init__(self, item):
		try:
			self.path = item
			self.alto = '%s/alto' %(self.path)
			self.mets = '%s/mets' %(self.path)
			self.jp2 = '%s/jp2' %(self.path)
			self.processing_folder = '%s/processing' %(self.path)
			self.processing_alto = '%s/processing/extracted_alto' %(self.path)
			self.processing_mets = '%s/processing/extracted_mets' %(self.path)
			self.get_feilds_xsl = 'xslt/get_fields.xsl'
			self.get_mods_xsl = 'xslt/get_mods.xsl'
			self.article_xsl = 'xslt/IA-headlines.xsl'
			self.uploaded = 'uploaded'
			self.issues = 'problematic_issues'
		except:
			PrintException()

	def generate_tar(self):
		pass

class images(processing_obj):
	def __init__(self, item, item_id):
		try:
			super().__init__(item)
			self.tf = tarfile.open("%s/1.tar" %(self.jp2))
			self.out = tarfile.open('%s/%s_images.tar' %(self.processing_folder, item_id), 'w:gz')
			self.item_id = item_id
		except:
			PrintException()

	def generate_tar(self):
		try: 
			print ("Extracting %s images" %(self.item_id))
			for member in self.tf.getmembers():
			    if 'VA' in member.name:
			    	member.name = os.path.basename(member.name)
			    	if member.name.split('.')[1] == 'jp2':
			    		self.tf.extract(member, path='%s/extracted_images/' %(self.processing_folder))

			self.tf.close()
			print ("Generating %s images tar" %(self.item_id))
			for file in os.listdir('%s/extracted_images' %(self.processing_folder)):
				obj = '%s/extracted_images/%s' %(self.processing_folder, file)
				self.out.add(obj, arcname=file)
			self.out.close()
		except:
			PrintException()

class metadata(processing_obj):
	def __init__(self, item, code):
		try:
			super().__init__(item)
			self.alt = tarfile.open("%s/1.tar" %(self.alto))
			self.met = tarfile.open("%s/1.tar" %(self.mets))
			self.code = code
			self.processing_mods = '/home/danydvd/git/remote/peel/metadata/Q/%s.xml' %(self.code)
			self.metadata = {}
			self.articles = ''
		except:
			print (self.path)
			shutil.move(self.path, self.issues)
			PrintException()


	def untar_mets_alto(self):
		try:
			print ("Extracting %s ALTO files" %(self.path))
			for member in self.alt.getmembers():
			    if 'VA' in member.name:
			    	member.name = os.path.basename(member.name)
			    	if member.name.split('.')[1] == 'xml':
			    		self.alt.extract(member, path='%s/extracted_alto/' %(self.processing_folder))

			self.alt.close()

			print ("Extracting %s METS files" %(self.path))
			for member in self.met.getmembers():
			    if 'VA' in member.name:
			    	member.name = os.path.basename(member.name)
			    	if member.name.split('.')[1] == 'xml':
			    		self.met.extract(member, path='%s/extracted_mets/' %(self.processing_folder))

			self.met.close()
		except:
			PrintException()

	def get_mods(self):
		try: 
			mods = ET.parse(self.get_mods_xsl)
			get_mods = ET.XSLT(mods)
			mod = ET.parse('%s' %(self.processing_mods))
			transformed_mods = get_mods(mod)
			print (transformed_mods)
			mods_fields = str(transformed_mods).split('\t')
			return (mods_fields)
		except:
			PrintException()

	def get_mets_data(self, mods):
		try: 
			mets_fields = ET.parse(self.get_feilds_xsl)
			get_mets = ET.XSLT(mets_fields)
			print ("Getting metadata for %s from issue level METS" %(self.path))
			for mets in os.listdir('%s' %(self.processing_mets)):
				if 'issue' in mets:
					doc = ET.parse('%s/%s' %(self.processing_mets, mets))
					transformed = get_mets(doc)

					# populating metada dict
					items = str(transformed).split('\t')
					self.metadata['title'] = items[0]
					if items[1] == 'en':
						self.metadata['language'] = 'English'
					elif items[1] == 'fr':
						self.metadata['language'] = 'French'
					else:
						self.metadata['language'] = items[1]
					if items[2]:
						year = None
						year = re.search('^\d{4}$', items[2])
						if not year:
							year = items[2].split('.')[2]
						month = items[2].split('.')[1]
						day = items[2].split('.')[0]
						date = '%s-%s-%s' %(year, month, day)
						self.metadata['date'] = date
					else:
						temp_date = mods.split('.')[0].replace('_issue', '').replace('VA_', '')
						date = '%s-%s-%s' %(str(temp_date)[0:3], str(temp_date)[4:5], str(temp_date)[6:7])
						self.metadata['date'] = date
					# passing the xsl result as discription will cuase the script to fial
					#metadata['description'] = art_headings
					self.metadata['mediatype'] = 'texts'
					self.metadata['publisher'] = 'Charles A. Clark, Sr.'
					self.metadata['coverage'] = 'Canada; Alberta; Vulcan'
					self.metadata['extent'] = 'v. : ill. ; 40 cm.'
					self.metadata['issuance'] = 'continuing'
					self.metadata['genre'] = 'Newspaper'
					self.metadata['note'] = 'Weekly'
					self.metadata['collection'] = 'ualberta_testing'


				elif 'article' in mets:
					print ("Getting article headings for %s from article level METS" %(self.path))
					item_id = mets.split('.')[0].replace('_article', '')
					mets_art = ET.parse('%s/%s' %(self.processing_mets, mets))
					get_article_headings = ET.parse(self.article_xsl)
					get_art_headings = ET.XSLT(get_article_headings)
					art_headings = get_art_headings(mets_art)

					for line in str(art_headings).split('\n'):
						self.articles += "%s \n"  %(line)
						self.metadata['description'] = self.articles

					with open('%s/%s_article_headings.txt' %(self.processing_folder, item_id), 'w') as article_file:
						article_file.write(str(art_headings))

			return (item_id, self.metadata)
		except:
			PrintException()

class file_uplaod(processing_obj):
	def __init__(self, item, item_id, metadata, log):
		try:
			super().__init__(item)
			self.item_id = item_id
			self.metadata = metadata
			self.log = log
		except:
			PrintException()

	def upload_to_IA(self):
		try: 
			file_upload = []
			print ('uploading %s' %(self.item_id))
			file_upload.append('%s/%s_images.tar' %(self.processing_folder, self.item_id))
			# select a folder and upload all files in that folder
			# if uploading JP2 files, METS/ALTO files will also be uploaded
			for folder in [self.processing_alto, self.processing_alto]:
				for file in os.listdir(folder):
					file_upload.append('%s/%s' %(folder, file))

			r = upload(self.item_id, files=file_upload, metadata=self.metadata)
			print (r[0].status_code)
			if r[0].status_code == 200:
				self.log.write('%s was successfuly uploaded at %s \n' %(self.item_id, T.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
				print ('moving %s to %s' %(self.path, self.uploaded))
				shutil.move(self.path, self.uploaded)
			else:
				print ('uploading %s failed -- %s will not be moved to uploaded folder' %(self.item_id, self.path))
				self. log.write('uploading %s fialed at %s \n' %(self.item_id, T.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
		except:
			PrintException()