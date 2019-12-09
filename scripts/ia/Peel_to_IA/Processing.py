import tarfile, os, re, shutil, time, sys, linecache, zipfile
import lxml.etree as ET
from datetime import datetime as T
from internetarchive import upload, configure, get_item, modify_metadata
from Util import PrintException

passwd = '****'
user = '****'
image_extension = ["jp2", "jpg", "jpeg", "tif", "tiff", "gif", "bmp", "png"]
# code_mapping = {"LEP": "LPM", "LEQ": "LEM", "LUN": "UNI", ""}

# insert IA "usernme", "password" here
configure(user, passwd)

class processing_obj():
	def __init__(self, item):
		self.path = item
		# images
		self.pics = {"%s/%s" % (self.path, ext): None for ext in image_extension}
		self.main_pic = None
		# PDF
		self.pdf = "%s/pdf" % self.path

		self.alto = '%s/alto' %(self.path)
		self.mets = '%s/mets' %(self.path)
		self.processing_folder = '%s/processing' %(self.path)
		self.processing_alto = '%s/processing/extracted_alto' %(self.path)
		self.processing_mets = '%s/processing/extracted_mets' %(self.path)
		self.processing_extra = '%s/processing/extra' %(self.path)
		if not os.path.isdir(self.processing_folder):
			os.mkdir(self.processing_folder)
		if not os.path.isdir(self.processing_extra):
			os.mkdir(self.processing_extra)
		self.get_feilds_xsl = 'xslt/get_fields.xsl'
		self.get_mods_xsl = 'xslt/get_mods.xsl'
		self.article_xsl = 'xslt/IA-headlines.xsl'
		self.uploaded = 'uploaded'
		self.issues = 'problematic_issues'

	def generate_tar(self):
		pass

class images(processing_obj):
	def __init__(self, item, item_id):
		super().__init__(item)
		for path in self.pics.keys():
			if os.path.isfile("%s/1.tar" % path):
				self.pics[path] = [tarfile.open("%s/1.tar" % path)]
				if self.main_pic is None:
					self.main_pic = path[path.rfind('/') + 1:]
					self.pics[path].append(zipfile.ZipFile('%s/%s_images.zip' %(self.processing_extra, item_id), 'w', zipfile.ZIP_DEFLATED))
				else:
					self.pics[path].append(tarfile.open('%s/%s_%s.tar' %(self.processing_extra, item_id, path[path.rfind('/') + 1:]), 'w:'))

		# self.tf_jp2 = tarfile.open("%s/1.tar" %(self.jp2))
		# self.tf_tiff = tarfile.open("%s/1.tar" %(self.tiff))
		self.tf_pdf = None
		if os.path.isfile("%s/1.tar" % self.pdf):
			self.tf_pdf = tarfile.open("%s/1.tar" %(self.pdf))

		# self.out_jp2 = zipfile.ZipFile('%s/%s_images.zip' %(self.processing_folder, item_id), 'w', zipfile.ZIP_DEFLATED)
		# self.out_tiff = tarfile.open('%s/%s_tiff.tar' %(self.processing_folder, item_id), 'w:')
		self.item_id = item_id

	def generate_tar(self):
		for path in self.pics.keys():
			if self.pics[path] is None:
				continue
			ext = path[path.rfind('/') + 1:]
			print ("Extracting %s images %s" % (self.item_id, ext))
			for member in self.pics[path][0].getmembers():
				if '/data/' in member.name:
					member.name = os.path.basename(member.name)
					# print(member.name, member.name.split('.')[1], ext)
					if member.name.split('.')[1] in image_extension:
						self.pics[path][0].extract(member, path='%s/extracted_images_%s/' % (self.processing_folder, ext))
			self.pics[path][0].close()

			print ("Generating %s images %s zip/tar" % (self.item_id, ext))
			for file1 in os.listdir("%s/extracted_images_%s" % (self.processing_folder, ext)):
				obj = '%s/extracted_images_%s/%s' %(self.processing_folder, ext, file1)
				if ext == self.main_pic:
					self.pics[path][1].write(obj, arcname="%s" % (file1))
				else:
					self.pics[path][1].add(obj, arcname=file1)
			self.pics[path][1].close()

		if self.tf_pdf is not None:
			print ("Extracting %s images PDF" %(self.item_id))
			find_list = dict()
			min_len = 99999
			for member in self.tf_pdf.getmembers():
				if '/data/' in member.name:
					member.name = os.path.basename(member.name)
					if member.name.split('.')[1] == 'pdf':
						find_list[member.name] = member
						if len(member.name) < min_len:
							min_len = len(member.name)
			for i in find_list.keys():
				if len(i) == min_len:
					self.tf_pdf.extract(find_list[i], path='%s/extra/' %(self.processing_folder))

class metadata(processing_obj):
	def __init__(self, item, code):
		try:
			super().__init__(item)
			self.alt = tarfile.open("%s/1.tar" %(self.alto))
			self.met = tarfile.open("%s/1.tar" %(self.mets))
			self.code = code
			self.processing_mods = 'Modified_Q/%s.xml' %(self.code)
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
				if '/data/' in member.name:
					member.name = os.path.basename(member.name)
					if member.name.split('.')[1] == 'xml':
						self.alt.extract(member, path='%s/extracted_alto/' %(self.processing_folder))

			self.alt.close()

			print ("Extracting %s METS files" %(self.path))
			for member in self.met.getmembers():
				if '/data/' in member.name:
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
			mods_fields = str(transformed_mods).split('\t')
			# print(mods_fields)
			# input("Hi")
			return (mods_fields)
		except:
			PrintException()

	def get_mets_data(self):
		try: 
			mets_fields = ET.parse(self.get_feilds_xsl)
			get_mets = ET.XSLT(mets_fields)
			for mets in os.listdir('%s' %(self.processing_mets)):
				if 'issue' in mets:
					print ("Getting metadata for %s from issue level METS" %(self.path))
					doc = ET.parse('%s/%s' %(self.processing_mets, mets))
					transformed = get_mets(doc)
					items = str(transformed).split('\t')
				elif 'article' in mets:
					print ("Getting article headings for %s from article level METS" %(self.path))
					item_id = mets.split('.')[0].replace('_article', '')
					item_id = mets.split('.')[0].replace('articles_', '')
					mets_art = ET.parse('%s/%s' %(self.processing_mets, mets))
					get_article_headings = ET.parse(self.article_xsl)
					get_art_headings = ET.XSLT(get_article_headings)
					art_headings = get_art_headings(mets_art)
					if self.get_feilds_xsl == 'xslt/get_fields_leg.xsl':
						doc = ET.parse('%s/%s' %(self.processing_mets, mets))
						transformed = get_mets(doc)
						items = str(transformed).split('\t')
				elif "METS" in mets:
					doc = ET.parse('%s/%s' %(self.processing_mets, mets))
					# print(f"doc={doc}")
					transformed = get_mets(doc)
					# print(f"tramsformed={transformed}")
					items = str(transformed).split('\t')
					print("Getting article headings for %s from METS level METS" %(self.path))
					item_id = mets.split('.')[0].replace('-METS', '')
					mets_art = ET.parse('%s/%s' %(self.processing_mets, mets))
					get_article_headings = ET.parse(self.article_xsl)
					get_art_headings = ET.XSLT(get_article_headings)
					art_headings = get_art_headings(mets_art)
					# print(items)
				elif self.get_feilds_xsl != 'xslt/get_fields_leg.xsl':
					print("Legacy METS")
					# with open("skip_log", 'a') as logfile:
					# 	logfile.write(f"{self.path[self.path.rfind('/') + 1:]}, {self.code}, cannot resolve METS\n")
					return False

			if item_id[0] in "0123456789":
				item_id = self.code + '_' + item_id
			if item_id[-1] not in "0123456789":
				for i in range(len(item_id) - 1, -1, -1):
					if item_id[i] in "0123456789":
						item_id = item_id[:i + 1]
						break
			print(f"items: {items}")
			if item_id == "LPM_1924032801":
				item_id = "LPM_1924032802"
			if item_id == "VA_19420514":
				item_id = "VA_1942051401"
			if item_id == "VA_19130128":
				item_id = "VA_1913012801"
			return (item_id, items, art_headings)
		except:
			PrintException()

	def set_legacy(self):
		self.get_feilds_xsl = 'xslt/get_fields_leg.xsl'
		self.article_xsl = 'xslt/get_head_leg.xsl'


	def make_IA_metadata(self, items, mods, art_headings, item_id, lang):
		try:
			self.metadata['title'] = items[0]
			if lang == 'en':
				self.metadata['language'] = 'English'
			elif lang == 'fr':
				self.metadata['language'] = 'French'
			else:
				self.metadata['language'] = lang

			if self.get_feilds_xsl == 'xslt/get_fields_leg.xsl':
				tester = items[0]
				self.metadata['title'] = None
			else:
				tester = items[2]

			if tester:
				year = None
				year = re.search(r'^\d{4}$', tester)
				if '-' in tester:
					self.metadata['date'] = tester
				else:
					if not year:
						year = tester.split('.')[2]
					month = tester.split('.')[1]
					day = tester.split('.')[0]
					date = '%s-%s-%s' %(year, month, day)
					self.metadata['date'] = date
			else:
				temp_date = mods.split('.')[0].replace('_issue', '').replace('VA_', '').replace('articles_', '')
				date = '%s-%s-%s' %(str(temp_date)[0:3], str(temp_date)[4:5], str(temp_date)[6:7])
				self.metadata['date'] = date

			self.metadata['collection'] = 'peel'
			# passing the xsl result as discription will cuase the script to fial
			#metadata['description'] = art_headings
			for line in str(art_headings).split('\n'):
				self.articles += "%s \n"  %(line.replace('pageModsBib', ''))
				self.metadata['description'] = self.articles

			with open('%s/%s_article_headings.txt' %(self.processing_folder, item_id), 'w') as article_file:
				article_file.write(str(art_headings))
			# populatiing MODS metadata
			self.metadata['mediatype'] = 'text'
			print(f"Mods: {mods}")
			if mods != None:
				if len(mods[1]) > 1:
					if not self.metadata['title']:
						self.metadata['title'] = mods[-1].strip("\n") + mods[1]
					self.metadata['subject'] = mods[1]
				if len(mods[2]) > 1:
					self.metadata['mediatype'] = mods[2]
				if mods[3] != 'N/A' and mods[4] != 'N/A':
					creator = mods[3] + ':' + mods[4]
				elif mods[3] != 'N/A' and mods[4] == 'N/A':
					creator = mods[3]
				if len(creator) > 1:
					self.metadata['creator'] = creator
				if len(mods[5]) > 1:
					self.metadata['coverage'] = mods[5].replace(',','') 
					if len(mods[6]) > 1:
						self.metadata['coverage'] = mods[5].replace(',','') + ';' + mods[6].replace(',','')
						if len(mods[7]) > 1:
							self.metadata['coverage'] = mods[5].replace(',','') + ';' + mods[6].replace(',','') + ';' + mods[7].replace(',','')
				if len(mods[8]) > 1:
					self.metadata['extent'] = mods[8]
				if len(mods[9]) > 1:
					self.metadata['publisher'] = mods[9]
				if len(mods[10]) > 1:	
					self.metadata['issuance'] = mods[10]
				self.metadata['genre'] = 'Newspaper'
				note_item = mods[14].split('_--_--_')
				if len(note_item) > 0:
					self.metadata['notes'] = ''
				for note in note_item:
					if note == '':
						pass
					else:
						n = note.split('::')
						# print (n)
						if len(n) > 1:
							if n[0] == 'public' and n[1] != ',':
								self.metadata['notes'] += '[%s]: %s  ' %(n[0], n[1])
			#self.metadata['note'] = 'Weekly'
			return (self.metadata)
		except:
			PrintException()		

class file_upload(processing_obj):
	def __init__(self, item, item_id, metadata, log):
		try:
			super().__init__(item)
			self.item_id = item_id
			self.metadata = metadata
			self.log = log
		except:
			PrintException()

	def upload_to_IA(self, update_only=False):
		try: 
			file_upload = []
			print ('uploading %s' %(self.item_id))
			# file_upload.append('%s/%s_images.zip' %(self.processing_folder, self.item_id))
			# file_upload.append('%s/%s_tiff.tar' %(self.processing_folder, self.item_id))

			# select a folder and upload all files in that folder
			# if uploading JP2 files, METS/ALTO files will also be uploaded
			for folder in [self.processing_alto, self.processing_mets, self.processing_extra]:
				for file in os.listdir(folder):
					file_upload.append('%s/%s' %(folder, file))
			
			# print(self.metadata)

			ia_uploaded_item = get_item(self.item_id)
			if not update_only:
				r = upload(self.item_id, files=file_upload, metadata=self.metadata)
			if ia_uploaded_item:
				print("File already uploaded, update metadata")
				r = [None]
				r[0] = modify_metadata(self.item_id, metadata=self.metadata)
			print (r[0].status_code)
			if r[0].status_code == 200:
				self.log.write('%s was successfuly uploaded at %s \n' %(self.item_id, T.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
				# print ('moving %s to %s' %(self.path, self.uploaded))
				# shutil.move(self.path, self.uploaded)
			else:
				print ('uploading %s failed -- %s will not be moved to uploaded folder' %(self.item_id, self.path))
				self.log.write('uploading %s failed at %s \n' %(self.item_id, T.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))

			return r[0].status_code == 200
		except:
			PrintException()
			return False
