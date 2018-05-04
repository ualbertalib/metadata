
import requests
import xml.etree.ElementTree as ET

f = open("response", "w")
base = "http://gillingham2.library.ualberta.ca:8080/fedora/rest/oai?verb=ListRecords&metadataPrefix=oai_dc"
req = base + '&from=2014-01-01T00:00:00Z&until=2016-12-31T00:00:00Z'
r = requests.get(req)

#rtree = ET.parse(r)
tree = ET.parse("response.xml")
root = tree.getroot()
token = root.get("resumptionToken")
token2 = root.find("[@resumptionToken]")
#token3 = root.find("./OAI-PMH").attrib['resumptionToken']

#token2 = root.search('<resumptionToken[^>]*>(.*)</resumptionToken>', data) --> if resumption token is element


page = req + "&resumptionToken=" #+ token.text

#while token != '':
#	f.write(r.text)

print str(token) + "\n"
print str(token2) + "\n"
#print str(token3) + "\n"
print str(root) + "\n"
print root.tag
print root.attrib
print r.text
