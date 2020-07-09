import tarfile, os, re, shutil, time, sys, linecache, zipfile
import lxml.etree as ET
from datetime import datetime as T
from internetarchive import upload, configure, get_item, modify_metadata
from Util import PrintException
from secret_info import *

image_extension = ["jp2", "jpg", "jpeg", "tif", "tiff", "gif", "bmp", "png", "pdf"]
target_collection = "peel"
target_mediatype = "texts"
# code_mapping = {"LEP": "LPM", "LEQ": "LEM", "LUN": "UNI", ""}

# insert IA "usernme", "password" here
configure(ia_username, ia_password)

class processing_obj():
	def __init__(self, item):
		self.path = item
		# images
		self.pics = {f"{self.path}/{ext}": None for ext in image_extension}
		self.main_pic = None
		# PDF
		self.pdf = f"{self.path}/pdf"

		self.alto = f"{self.path}/alto"
		self.mets = f"{self.path}/mets"
		self.processing_folder = f"{self.path}/processing"
		self.processing_alto = f"{self.path}/processing/extracted_alto"
		self.processing_mets = f"{self.path}/processing/extracted_mets"
		self.processing_extra = f"{self.path}/processing/extra"
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
			if os.path.isfile(f"{path}/1.tar"):
				self.pics[path] = [tarfile.open(f"{path}/1.tar")]
				if self.main_pic is None:
					self.main_pic = path[path.rfind('/') + 1:]
					self.pics[path].append(zipfile.ZipFile(f"{self.processing_extra}/{item_id}_images.zip", 'w', zipfile.ZIP_DEFLATED))
				else:
					self.pics[path].append(tarfile.open(f"{self.processing_extra}/{item_id}_{path[path.rfind('/') + 1:]}.tar", 'w:'))

		# self.tf_jp2 = tarfile.open("%s/1.tar" %(self.jp2)) # Depreciated
		# self.tf_tiff = tarfile.open("%s/1.tar" %(self.tiff)) # Depreciated
		# self.tf_pdf = None
		# if os.path.isfile(f"{self.pdf}/1.tar"):
		# 	self.tf_pdf = tarfile.open(f"{self.pdf}/1.tar")
		# self.out_jp2 = zipfile.ZipFile('%s/%s_images.zip' %(self.processing_folder, item_id), 'w', zipfile.ZIP_DEFLATED) # Depreciated
		# self.out_tiff = tarfile.open('%s/%s_tiff.tar' %(self.processing_folder, item_id), 'w:') # Depreciated
		self.item_id = item_id

	def generate_tar(self, postcards=False):
		for path in self.pics.keys():
			if self.pics[path] is None:
				continue
			ext = path[path.rfind('/') + 1:]
			print (f"Extracting {self.item_id} images {ext}")
			for member in self.pics[path][0].getmembers():
				if "/data/" in member.name:
					member.name = os.path.basename(member.name)
					# print(member.name, member.name.split('.')[1], ext)
					if member.name.split('.')[1] in image_extension:
						if postcards:
							self.pics[path][0].extract(member, path=f"{self.processing_folder}/extra/")
						self.pics[path][0].extract(member, path=f"{self.processing_folder}/extracted_images_{ext}/")
			self.pics[path][0].close()

			print (f"Generating {self.item_id} images {ext} zip/tar")
			names = os.listdir(f"{self.processing_folder}/extracted_images_{ext}")
			names.sort()
			for i, name in enumerate(names):
				obj = f"{self.processing_folder}/extracted_images_{ext}/{name}"
				end_ext = name[name.rfind("."):]
				target = f"{self.processing_folder}/extracted_images_{ext}/{i:03d}{self.item_id}{end_ext}"
				os.rename(obj, target)
			for file1 in os.listdir(f"{self.processing_folder}/extracted_images_{ext}"):
				obj = f"{self.processing_folder}/extracted_images_{ext}/{file1}"
				if ext == self.main_pic:
					self.pics[path][1].write(obj, arcname=file1)
				else:
					self.pics[path][1].add(obj, arcname=file1)
			self.pics[path][1].close()

		# if self.tf_pdf is not None:
		# 	print (f"Extracting {self.item_id} images PDF")
		# 	find_list = dict()
		# 	# min_len = 99999
		# 	for member in self.tf_pdf.getmembers():
		# 		if "/data/" in member.name:
		# 			member.name = os.path.basename(member.name)
		# 			if member.name.split('.')[1] == "pdf":
		# 				find_list[member.name] = member
		# 				# if len(member.name) < min_len:
		# 				# 	min_len = len(member.name)
		# 	# for i in find_list.keys():
		# 	# 	if len(i) == min_len:
		# 	# 		self.tf_pdf.extract(find_list[i], path=f"{self.processing_folder}/extra/")
			
	
		self.copy_to_upload()

	def copy_to_upload(self):
		# uncompressed PDF
		if os.path.isfile("%s/1.pdf" % self.pdf):
			shutil.copyfile("%s/1.pdf" % self.pdf, f"{self.processing_extra}/{self.item_id}.pdf")
		# Copy other stuffs
		for folder in os.listdir(self.path):
			if folder not in image_extension + ["pdf", "alto", "mets"]:
				if os.path.isfile(f"{self.path}/{folder}/1.tar"):
					shutil.copyfile(f"{self.path}/{folder}/1.tar", f"{self.processing_extra}/{folder}.tar")


class metadata(processing_obj):
	def __init__(self, item, code, meta_location):
		try:
			super().__init__(item)
			self.alt = None
			self.met = None
			if os.path.isfile("%s/1.tar" %(self.alto)):
				self.alt = tarfile.open("%s/1.tar" %(self.alto))
			if os.path.isfile("%s/1.tar" %(self.mets)):
				self.met = tarfile.open("%s/1.tar" %(self.mets))
			self.code = code
			self.processing_mods = meta_location
			self.metadata = {}
			self.articles = ''
		except:
			print (self.path)
			shutil.move(self.path, self.issues)
			PrintException()


	def untar_mets_alto(self):
		try:
			if self.alt is None:
				print("No ALTO file detected")
			else:
				print ("Extracting %s ALTO files" %(self.path))
				for member in self.alt.getmembers():
					if '/data/' in member.name:
						member.name = os.path.basename(member.name)
						if member.name.split('.')[1] == 'xml':
							self.alt.extract(member, path='%s/extracted_alto/' %(self.processing_folder))
				shutil.copyfile("%s/1.tar" %(self.alto), f"{self.processing_extra}/ALTO.tar")
				self.alt.close()

			if self.met is None:
				print("No METS file detected")
				if not os.path.isdir(self.processing_mets):
					os.mkdir(self.processing_mets)
				if os.path.isfile("%s/1.xml" %(self.mets)):
					print("1.xml detected")
					shutil.copyfile("%s/1.xml" %(self.mets), f"{self.processing_mets}/1.xml")
				elif self.processing_mods is not None:
					self.get_feilds_xsl = 'xslt/get_fields_item.xsl'
					shutil.copyfile(self.processing_mods, f"{self.processing_mets}/{self.processing_mods[self.processing_mods.rfind('/') + 1:]}")
				self.get_mods_xsl = 'xslt/get_mods_item.xsl'
					
				
			else:
				print ("Extracting %s METS files" %(self.path))
				for member in self.met.getmembers():
					if '/data/' in member.name:
						member.name = os.path.basename(member.name)
						if member.name.split('.')[-1] == 'xml':
							self.met.extract(member, path='%s/extracted_mets/' %(self.processing_folder))
							if member.name.count('.') > 1:
								replace_name = member.name.replace('.', '-')[:-4] + ".xml"
								os.rename(f"{self.processing_folder}/extracted_mets/{member.name}", f"{self.processing_folder}/extracted_mets/{replace_name}")

				self.met.close()
			

		except:
			PrintException()

	def get_mods(self, item=False):
		if self.processing_mods is None:
			return
		try: 
			if not item:
				mods = ET.parse(self.get_mods_xsl)
			else:
				mods = ET.parse('xslt/get_mods_item.xsl')
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
				elif "METS" in mets or self.met is None:
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
					if mets == '1.xml':
						if items[-2]:
							item_id = items[-2]
						else:
							raise ValueError
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
			# print(f"items: {items}")
			# print(item_id)
			return (item_id, items, art_headings)
		except:
			PrintException()

	def set_legacy(self):
		self.get_feilds_xsl = 'xslt/get_fields_leg.xsl'
		self.article_xsl = 'xslt/get_head_leg.xsl'


	def make_IA_metadata(self, items, mods, art_headings, item_id, lang):
		try:
			self.metadata['title'] = items[0]
			if lang is None:
				lang = items[1]
			if lang.lower() in ('eng', 'en'):
				self.metadata['language'] = 'English'
			elif lang.lower() == 'fr':
				self.metadata['language'] = 'French'
			else:
				self.metadata['language'] = lang

			if self.get_feilds_xsl == 'xslt/get_fields_leg.xsl':
				tester = items[0]
				self.metadata['title'] = None
			else:
				tester = items[2]
			
			self.metadata['date'] = None

			if tester:
				year = None
				year = re.search(r'^\d{4}$', tester)
				if '-' in tester and tester.isdigit():
					self.metadata['date'] = tester
				elif tester.count('.') >= 2:
					if not year:
						year = tester.split('.')[2]
					month = tester.split('.')[1]
					day = tester.split('.')[0]
					if year.isdigit() and month.isdigit() and day.isdigit():
						date = '%s-%s-%s' %(year, month, day)
						self.metadata['date'] = date
			else:
				date = items[0][-4:]
				if date.isdigit():
					self.metadata['date'] = date

			self.metadata['collection'] = target_collection
			self.metadata['description'] = ''
			# passing the xsl result as discription will cuase the script to fial
			#metadata['description'] = art_headings
			for line in str(art_headings).split('\n'):
				if line.strip().replace('Page', ''):
					self.articles += "%s \n"  %(line.replace('pageModsBib', ''))
					self.metadata['description'] = self.articles
			
			content = 0
			if self.metadata['description']:
				for char in self.metadata['description'].lower().replace("page", '').replace("\n", '').replace(' ', '').replace("l", ''):
					if char.isalpha():
						content = 1
						break
				if content == 0:
					self.metadata['description'] = ''

			with open('%s/%s_article_headings.txt' %(self.processing_folder, item_id), 'w') as article_file:
				article_file.write(str(art_headings))
			# populatiing MODS metadata
			self.metadata['mediatype'] = target_mediatype
			# print(f"Mods: {mods}")
			if mods != None:
				if len(mods[1]) > 1:
					if not self.metadata['title']:
						self.metadata['title'] = mods[-1].strip("\n") + mods[1]
					self.metadata['subject'] = mods[1]
				if len(mods[2]) > 1:
					self.metadata['mediatype'] = mods[2]
				creator = ''
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
				if self.metadata['date'] is None:
					self.metadata['date'] = mods[11]
				if mods[15]:
					self.metadata['genre'] = mods[15]
				else:
					self.metadata['genre'] = "postcards"
				note_item = mods[14].split('_--_--_')
				# print(note_item)
				if len(note_item) > 0:
					self.metadata['notes'] = ''
				for note in note_item:
					if note == '':
						pass
					else:
						n = note.split('::')
						# print (n)
						if len(n) > 1:
							if n[0].startswith('public') and n[1] != ',':
								self.metadata['notes'] += '[%s]: %s  \n' %(n[0], n[1])
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
		# try: 
		file_upload = []
		print ('uploading %s' %(self.item_id))
		# file_upload.append('%s/%s_images.zip' %(self.processing_folder, self.item_id))
		# file_upload.append('%s/%s_tiff.tar' %(self.processing_folder, self.item_id))

		# select a folder and upload all files in that folder
		# if uploading JP2 files, METS/ALTO files will also be uploaded
		# for folder in [self.processing_alto, self.processing_mets, self.processing_extra]:
		for folder in [self.processing_mets, self.processing_extra]:
			if os.path.isdir(folder):
				for file in os.listdir(folder):
					if file == "ALTO.tar":
						os.rename('%s/%s' %(folder, file), '%s/%s-ALTO.tar' %(folder, self.item_id))
						file_upload.append('%s/%s-ALTO.tar' %(folder, self.item_id))
					else:
						file_upload.append('%s/%s' %(folder, file))

		size_of_upload = 0
		units = ["GB", "MB", "KB", "B"]
		for file in file_upload:
			size_of_upload += os.path.getsize(file)
		
		for i, unit in enumerate(units):
			if size_of_upload >= 1024 ** (3 - i):
				size_of_upload /= 1024 ** (3 - i)
				break
		print(f"Upload size: {size_of_upload:.2f} {unit} ({len(file_upload)} files)")
		print(file_upload)
		input("Pause")
		
		# print(self.metadata)

		ia_uploaded_item = get_item(self.item_id)
		if ia_uploaded_item.identifier_available() or not update_only:
			r = ia_uploaded_item.upload(file_upload, metadata=self.metadata)[0]
		else:
			print("File already uploaded, update metadata")
			r = None
			for k, v in self.metadata.items():
				res = ia_uploaded_item.modify_metadata({k: v})
				if res.status_code == 200 or r is None:
					r = res
		print (r.status_code)
		if r.status_code == 200:
			self.log.write('%s was successfuly uploaded at %s \n' %(self.item_id, T.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
			# print ('moving %s to %s' %(self.path, self.uploaded))
			# shutil.move(self.path, self.uploaded)
		else:
			print ('uploading %s failed -- %s will not be moved to uploaded folder' %(self.item_id, self.path))
			self.log.write('uploading %s failed at %s \n' %(self.item_id, T.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))

		return r.status_code == 200
		# except:
		# 	PrintException()
		# 	return False
