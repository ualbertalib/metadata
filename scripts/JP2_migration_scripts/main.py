import os, csv, rdflib, uuid, pickle, difflib, hashlib
import lxml.etree as ET
from config import data_links, namespaces, vocab
from rdflib.namespace import RDFS


with open("{0}/subjects.pickle".format(data_links['recon']), "rb") as handle:
    lcsh = pickle.load(handle)

with open("{0}/csh.pickle".format(data_links['recon']), "rb") as handle:
    csh = pickle.load(handle)

class blitz_database():
	def __init__(self, peelType):
		self.blitz_location = self.get_blitz_location(peelType)
		self.blitz = {}
		#self.blitz = self.get_blitz_data()

	def get_blitz_location(self, peelType):
		return (data_links[peelType])

	def get_blitz_data(self):
		with open(self.blitz_location, 'r') as blitz_newspaper:
			reader = csv.DictReader(blitz_newspaper)
			for row in reader:
				newspaper =  row['Newspaper']
				noid = row['Noid']
				if newspaper not in self.blitz.keys():
					self.blitz[newspaper] = {}
					self.blitz = self.fill_blitz_data(self.blitz, row, newspaper, noid)	
				else:
					self.blitz = self.fill_blitz_data(self.blitz, row, newspaper, noid)
			blitz_newspaper.close()
			return (self.blitz)

	def fill_blitz_data(self, blitz, row, newspaper, noid):
		blitz[newspaper][noid] = {}
		if row['Year'] != '':
			blitz[newspaper][noid]['year'] = row['Year']
		if row['Month'] != '':
			blitz[newspaper][noid]['month'] = row['Month']
		if row['Day'] != '':
			blitz[newspaper][noid]['day'] = row['Day']
		if row['Volume'] != '':
			blitz[newspaper][noid]['volume'] = row['Volume']
		if row['Issue'] != '':
			blitz[newspaper][noid]['issue'] = row['Issue']
		if row['Edition'] != '':
			blitz[newspaper][noid]['edition'] = row['Edition']
		if row['Pages'] != '':
			blitz[newspaper][noid]['pages'] = row['Pages']
		if row['Articles'] != '':
			blitz[newspaper][noid]['articles'] = row['Articles']
		if row['Pictures'] != '':
			blitz[newspaper][noid]['pictures'] = row['Pictures']
		if row['Ads'] != '':
			blitz[newspaper][noid]['ads'] = row['Ads']
		if row['Language'] != '':
			blitz[newspaper][noid]['lang'] = row['Language']

		return (blitz)


class mets_processing():
	def __init__(self, noid):
		self.mets_location = data_links['mets']
		self.noid = noid
		mets_xslt = ET.parse('xslt/mets_metadata.xsl')
		self.get_mets = ET.XSLT(mets_xslt)

	def mets_metadata(self):
		for file in os.listdir('{0}/{1}/METS/data'.format(self.mets_location, self.noid)):
			if 'article' not in file:
				mets_file = os.path.join(self.mets_location, self.noid, 'METS/data/', file)
				doc = ET.parse(mets_file)
				transformed = self.get_mets(doc)
				return(transformed)


class mods_processing():
	def __init__(self, code):
		self.mods_location = data_links['mods']
		self.code = code
		mods_xslt = ET.parse('xslt/mods_metadata.xsl')
		self.get_mods = ET.XSLT(mods_xslt)
		self.metadata = {}

	def mods_metadata(self):
		mods_file = os.path.join(self.mods_location, 'Q/', 'ACN-new.xml')
		doc = ET.parse(mods_file)
		#transformed = self.get_mods(doc)
		#print (transformed)
		root = doc.getroot()
		ns = ET.register_namespace('mods', 'http://www.loc.gov/mods/v3')
		### Title ###
		for titleInfo in root.iter('{http://www.loc.gov/mods/v3}titleInfo'):
			sub_title = ''
			nsort_title = ''
			title_pnumber = ''
			ttype = titleInfo.attrib
			for title in titleInfo.iter('{http://www.loc.gov/mods/v3}title'):
				main_title = title.text
			for s_title in titleInfo.iter('{http://www.loc.gov/mods/v3}subTitle'):
				sub_title = s_title.text
			for nsort in titleInfo.iter('{http://www.loc.gov/mods/v3}nonSort'):
				nsort_title = nsort.text
			for p_title in titleInfo.iter('{http://www.loc.gov/mods/v3}partNumber'):
				title_pnumber = p_title.text
			mapped_title = nsort_title + main_title + sub_title + title_pnumber
			if ttype != '':
				self.metadata['dcterms:alternative'] = mapped_title
			else:
				self.metadata['dcterms:title'] = mapped_title

		### Type of Resource ###
		for resource in root.iter('{http://www.loc.gov/mods/v3}typeOfResource'):
			self.metadata['dcterms:type'] = resource.text

		### genre ###
		for genre in root.iter('{http://www.loc.gov/mods/v3}genre'):
			self.metadata['edm:hasType'] = genre.text

		### language ###
		for l in root.iter('{http://www.loc.gov/mods/v3}language'):
			for lang in l.iter('{http://www.loc.gov/mods/v3}languageTerm'):
				self.metadata['dcterms:language'] = lang.text

		### originInfo ###
		for originfo in root.iter('{http://www.loc.gov/mods/v3}originInfo'):
			### edition ###
			for edition in originfo.iter('{http://www.loc.gov/mods/v3}edition'):
				self.metadata['bf:editionStatement'] = edition.text
			### publisher ##
			for pub in originfo.iter('{http://www.loc.gov/mods/v3}publisher'):
				self.metadata['relators:pbl'] = pub.text
			### placeTerm ###
			for p in originfo.iter('{http://www.loc.gov/mods/v3}place'):
				for place in p.iter('{http://www.loc.gov/mods/v3}placeTerm'):
					self.metadata['relators:pup'] = place.text
			### date ###
			for date in originfo.iter('{http://www.loc.gov/mods/v3}publisher'):
				if date.attrib == '':
					self.metadata['dcterms:issued'] = date.text
				else:
					self.metadata['dcterms:issued'] = []
					self.metadata['dcterms:issued'].append(date.text)
					self.metadata['skos:note'].append('Date: {0}'.format(date.attrib))

		### recordInfo ###
		for info in root.iter('{http://www.loc.gov/mods/v3}recordInfo'):
			### identifier ###
			for id in info.iter('{http://www.loc.gov/mods/v3}recordIdentifier'):
				self.metadata['identifiers:local'] = id.text

		### extent ###
		for phys in root.iter('{http://www.loc.gov/mods/v3}physicalDescription'):
			for extent in phys.iter('{http://www.loc.gov/mods/v3}extent'):
				self.metadata['rdau:extent.en'] = extent.text

		### table of content ###
		for table in root.iter('{http://www.loc.gov/mods/v3}tableOfContents'):
			self.metadata['dcterms:tableOfContents'] = table.text

		### note ###
		for note in root.iter('{http://www.loc.gov/mods/v3}note'):
			print (note.attrib)
			if note.attrib == '':
				self.metadata['skos:note'] = ' '
			elif note.attrib['type'] == 'public':
				self.metadata['skos:note'] += note.text
			elif note.attrib['type'] == 'copyright blocked':
				self.metadata['skos:note'] += 'value is "Permission to reproduce this item has not yet been obtained.'
			elif 'local DOA' in note.attrib['type']:
				self.metadata['schema:temporalCoverage'] = note.attrib.split('DOA:')[1] 
			elif 'local Spatial' in note.attrib['type']:
				self.metadata['dc:Coverage'] = note.attrib.split('Spatial:')[1] 
			elif 'local:oaiset' in note.attrib['type']:
				if note.text == 'newspapers':
					self.metadata['pcdm:memberOf'] = 'http://peel.library.ualberta.ca/newspapers/' 
			elif 'local:oaiset' in note.attrib['type']:
				if note.text == 'hendersons':
					self.metadata['pcdm:memberOf'] = 'http://peel.library.ualberta.ca/hendersons/' 
			elif 'local:oaiset' in note.attrib['type']:
				if note.text == 'lastbestwest':
					self.metadata['pcdm:memberOf'] = 'http://peel.library.ualberta.ca/lastbestwest/' 
			elif 'local:oaiset' in note.attrib['type']:
				if note.text == 'peelmaps':
					self.metadata['pcdm:memberOf'] = 'http://peel.library.ualberta.ca/maps/' 
			
		### subject ###
		for subject in root.iter('{http://www.loc.gov/mods/v3}subject'):
			### geo ###
			for geo in subject.iter('{http://www.loc.gov/mods/v3}geographic'):
				self.metadata['dc:Coverage'] = geo.text
			### Hgeo ###
			for geo in subject.iter('{http://www.loc.gov/mods/v3}hierarchicalGeographic'):
				location = ''
				for item in geo.iter('{http://www.loc.gov/mods/v3}*'):
					location += item.text + ' '
				self.metadata['dc:Coverage'] = location.strip().replace(' ', '--')
			### temporal ###
			for tempo in subject.iter('{http://www.loc.gov/mods/v3}temporal'):
				self.metadata['schema:temporalCoverage'] = tempo.text 
			### topic ###
			for topic in subject.iter('{http://www.loc.gov/mods/v3}topic'):
				self.metadata['dc:subject'] = topic.text 
			### Scale / projection ###
			for cat in subject.iter('{http://www.loc.gov/mods/v3}cartographics'):
				for scale in cat.iter('{http://www.loc.gov/mods/v3}scale'):
					self.metadata['rdau:scale.en'] = scale.text
				for proj in cat.iter('{http://www.loc.gov/mods/v3}projection'):
					self.metadata['rdau:projectionOfCartographicContent.en'] = proj.text

		### relatedItem ###
		for item in root.iter('{http://www.loc.gov/mods/v3}relatedItem'):
			if item.attrib['type'] == 'succeeding':
				self.metadata['dcterms:isReplacedBy'] = 'http://peel.library.ualberta.ca/newspapers/' + item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['type'] == 'constituent':
				self.metadata['dcterms:hasPart'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['type'] == 'host':
				self.metadata['dcterms:isPartOf'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['type'] == 'isReferencedBy':
				self.metadata['dcterms:isReferencedBy'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['type'] == 'original':
				self.metadata['dcterms:source'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['type'] == 'otherFormat':
				self.metadata['dcterms:hasFormat'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['type'] == 'otherVersion':
				self.metadata['dcterms:hasVersion'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['type'] == 'preceding':
				self.metadata['dcterms:replaces'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['type'] == 'series':
				self.metadata['bf:seriesStatement'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['displayLabel'] == 'continues':
				self.metadata['dcterms:replaces'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['displayLabel'] == 'continued by':
				self.metadata['dcterms:isReplacedBy'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['displayLabel'] == 'absorbs':
				self.metadata['rdaw:P10224'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['displayLabel'] == 'absorbed by':
				self.metadata['rdaw:P10145'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['displayLabel'] == 'continues in part':
				self.metadata['rdaw:P10206'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['displayLabel'] == 'continued in part by':
				self.metadata['rdaw:P10021'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['displayLabel'] == 'forms':
				self.metadata['rdaw:P10213'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['displayLabel'] == 'forms from the merger of':
				self.metadata['rdaw:P10212'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['displayLabel'] == 'contains':
				self.metadata['bf:accompaniedBy'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['displayLabel'] == 'contained in':
				self.metadata['bf:accompanies'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['displayLabel'] == 'see also':
				self.metadata['dcterms:references'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['displayLabel'] == 'has supplement':
				self.metadata['rdaw:P10172'] = item.attrib['{http://www.w3.org/1999/xlink}href']
			if item.attrib['displayLabel'] == 'supplement':
				self.metadata['rdaw:P10154'] = item.attrib['{http://www.w3.org/1999/xlink}href']

		return(self.metadata)


class recon():
	def __init__(self, predicate, object):
		self.predicate = predicate
		self.object = object
		func = self.predicate.split('/')[-1]
		
	def coverage(self):
		match_lcsh = difflib.get_close_matches(self.object, lcsh.keys(), n=1, cutoff=0.90)
		match_csh = difflib.get_close_matches(self.object, csh.keys(), n=1, cutoff=0.90)
		if match_lcsh:
			return (match_lcsh)
		elif match_csh:
			return (match_csh)
		else:
			return None

	def subject(self):
		match_subject = difflib.get_close_matches(self.object, lcsh.keys(), n=1, cutoff=0.90)
		match_csh = difflib.get_close_matches(self.object, csh.keys(), n=1, cutoff=0.90)
		if match_lcsh:
			return (match_lcsh)
		elif match_csh:
			return (match_csh)
		else:
			return None


class rdf():
	def __init__(self, mods, mets, code, flag):
		self.mods = mods
		self.mets = mets
		self.code = code
		self.flag = flag
		self.graph = rdflib.Graph()

	def add_mets_triples(self):
		mets_field = str(self.mets).split('\t')
		if mets_field[2] != '':
			sub = rdflib.URIRef('http://peel.library.ualberta.ca/newspapers/{0}/{1}'.format(self.code, mets_field[2].replace('-', '/') ))
			predicate = rdflib.URIRef(namespaces['dcterms'] + 'dateIssued')
			object = rdflib.Literal(mets_field[2])
			self.graph.add((sub, predicate, object))
		if mets_field[5] != '':
			predicate = rdflib.URIRef(namespaces['bf'] + 'editionStatement')
			object = rdflib.Literal(mets_field[5])
			self.graph.add((sub, predicate, object))
		self.add_mods_triples(sub)
		self.graph.serialize('ACN_{0}.nt'.format(mets_field[2]), format="nt")

	def add_mods_triples(self, subject):
		recon_predicates = ['Coverage', 'Subject']
		for data in self.mods.keys():
			prefix = data.split(':')[0]
			metadata_field = data.split(':')[1] 
			if prefix in namespaces.keys():
				#subject = rdflib.URIRef('http://peel.library.ualberta.ca/newspapers/{0}'.format(uuid.uuid4()))
				predicate =	 rdflib.URIRef(namespaces[prefix] + metadata_field)
				if metadata_field in recon_predicates:
					recon_object = getattr(recon(predicate, self.mods[data]), metadata_field.lower())()
					if recon_object:
						object = rdflib.URIRef(recon_object)
					else:
						object = rdflib.URIRef('http://peel.library.ualberta.ca/subjects/{0}'.format(str(hashlib.md5(self.mods[data].encode("utf-8")).hexdigest())))
					self.graph.add((object, rdflib.URIRef(RDFS.label), rdflib.Literal(self.mods[data])))
				elif metadata_field in vocab.keys():
					object = rdflib.URIRef(vocab[metadata_field][self.mods[data]])
					self.graph.add((object, rdflib.URIRef(RDFS.label), rdflib.Literal(self.mods[data].capitalize())))
				elif 'http://' in self.mods[data]:
					object = rdflib.URIRef(self.mods[data])
				else:
					object = rdflib.Literal(self.mods[data])
				#print (subject, predicate, object)
				self.graph.add((subject, predicate, object))
		#self.graph.add((subject, rdflib.URIRef(namespaces['dcterms'] + 'isPartOf'),rdflib.URIRef('http://peel.library.ualberta.ca/newspapers/{0}'.format(self.code))))
		self.graph.add((subject, rdflib.URIRef(namespaces['edm'] + 'rights'),rdflib.URIRef('https://creativecommons.org/share-your-work/public-domain/pdm/')))
		if self.flag:
			self.graph.serialize('{0}.nt'.format(self.code), format="nt")
		

### main controller ###
#newspaper codes
code = ['ACN']
#get data from blitz
b = blitz_database('newspapers').get_blitz_data()
for item in code:
	mets = None
	flag  = True 
	a = mods_processing(item).mods_metadata()
	subject = rdflib.URIRef('http://peel.library.ualberta.ca/newspapers/{0}'.format(item))
	e = rdf(a, mets, item, flag).add_mods_triples(subject)
	flag  = False 
	for i in b[item].keys():
		c = mets_processing(i).mets_metadata()
		d = rdf(a, c, item, flag).add_mets_triples()


'''import time

l = [1, 2, 3, 4, 5, 6, 7]
		
def gen(a, l):
	print (l[a])
	time.sleep(1)
	if a + 1 < len(l):
		gen(a+1, l)
	


i = 0
print(l[i])
gen(i+1, l)'''