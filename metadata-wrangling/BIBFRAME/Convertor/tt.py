import lxml.etree as ET
import xml.etree.ElementTree as ETree


file = ETree.parse("temp-file.xml")
root = file.getroot()
print (root.tag)
for i in root.iter('{http://www.w3.org/2005/Atom}entry'):
	author = i.find('{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name').text
	title = i.find('{http://www.w3.org/2005/Atom}title').text
	id = i.find('{http://www.w3.org/2005/Atom}id').text
	