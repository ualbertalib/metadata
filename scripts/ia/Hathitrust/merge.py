import os

with open('albertanativenews_marc.xml', 'a+') as out:
	out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
	out.write('<collection xmlns="http://www.loc.gov/MARC21/slim">\n')
	for file in os.listdir('albertanativenews'):
		with open('albertanativenews/{0}'.format(file) , 'r') as f:
			for line in f:
				if '<?xml version="1.0" encoding="UTF-8"?>' not in line:
					out.write(line)

	out.write('</collection>')
		

