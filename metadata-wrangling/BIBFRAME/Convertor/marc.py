from pymarc import MARCReader
from pymarc import XmlHandler
from pymarc import record_to_xml
from pymarc import XMLWriter
with open('PGA-Australiana.mrc', 'rb') as fh:
	#with open ("test.xml", "a") as out:
		#out.write('<root>')
	reader = MARCReader(fh, to_unicode=True, force_utf8=False, utf8_handling='ignore')
	for record in reader:
		i = 0
		if record.title():
			ti = record.title()
			ti = ti.replace("/", "")
			ti = ti.replace(" ", "_")
			ti = ti[0:50]
			writer = XMLWriter(open( ti + '.xml','wb'))
		#wr = record_to_xml(record)
			writer.write(record)
			writer.close()
		else:
			writer = XMLWriter(open('unknownTitle' + i + '.xml','wb'))
			i += 1
		#out.write(wr)
		#out.write('</root>')
	#out.close()
