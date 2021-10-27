from Passwords import passwords
from internetarchive import upload, configure, get_item, search_items, download
from os import listdir, getcwd, chdir, makedirs
from os.path import exists



class Hathi():
	def __init__(self, collection):
		self.collection = collection
		self.search = search_items('collection:{0}'.format(self.collection))
		self.ua_files = '{0}_ua'.format(self.collection)
		passwd = passwords['IA_digi'][1]
		user = passwords['IA_digi'][0]
		configure(user, passwd)


	def get_archive_file(self):
		if not exists(self.collection):
			makedirs(self.collection)
		chdir(self.collection)

		for i, result in enumerate(self.search):
			    itemid = result['identifier']
			    print (i, itemid)
			    item = get_item(itemid)
			    file = item.get_file(itemid+'_archive_marc.xml')
			    file.download()

	def get_ua_files(self):
		if not exists(self.ua_files):
			makedirs(self.ua_files)
		chdir(self.ua_files)

		for i, result in enumerate(self.search):
			    itemid = result['identifier']
			    print (i, itemid)
			    item = get_item(itemid)
			    file = item.get_file(itemid+'_marc.xml')
			    file.download()


	def add_035(self):
		for file in listdir(self.ua_files):
			with open("{0}/{1}".format(self.ua_files, file), 'r') as f:
				lines = f.readlines()
				for i, line in enumerate(lines):
					if '<datafield tag="035"' in lines[i]:
						l = (lines[i+1])
				f.close()
			with open("{0}/{1}".format(self.collection, file.replace('_marc.xml', '_archive_marc.xml')), 'r') as ff:
				lines = ff.readlines()
				new_lines = []
				flag = 0
				for i, line in enumerate(lines):
					if '<datafield tag=' in lines[i]:
						digit = int(lines[i].split('="')[1].split('"')[0])
						if digit > 34 and flag == 0:
							flag = 1
							new_lines.append('<datafield tag="035" ind1="0" ind2=" ">\n {0}\n </datafield>'.format(l)) 
						else:
							pass
					new_lines.append(line)
				ff.close()

			if not exists('{0}/new_files'.format(self.collection)):
				makedirs('{0}/new_files'.format(self.collection))		

			with open("{0}/new_files/new_{1}".format(self.collection, file), 'w') as out:
				for i in new_lines:
					out.write(i)
					

	def merge(self):
		with open('{0}_marc.xml'.format(self.collection), 'a+') as out:
			out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
			out.write('<collection xmlns="http://www.loc.gov/MARC21/slim">\n')
			for file in listdir('{0}/new_files'.format(self.collection)):
				with open('{0}/new_files/{1}'.format(self.collection, file) , 'r') as f:
					for line in f:
						if '<?xml version="1.0" encoding="UTF-8"?>' not in line:
							out.write(line)

			out.write('</collection>')    


if __name__ == "__main__":
	 collection = input('collection:')
	 action = input('action (1 = get_archive_file, 2 = get_ua_files, 3 = add_035, 4 = merge):')
	 hathi = Hathi(collection)
	 if action == '1':
	 	hathi.get_archive_file()
	 if action == '2':
	 	hathi.get_ua_files()
	 if action == '3':
	 	hathi.add_035()
	 if action == '4':
	 	hathi.merge()


	 