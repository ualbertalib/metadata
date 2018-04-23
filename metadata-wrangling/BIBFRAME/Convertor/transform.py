import subprocess
import lxml.etree as ET

#subprocess.call(["java net.sf.saxon.Transform", "-o:output.xml", "-s:Abel_Janszoon_Tasman_his_Life_and_Voyages..xml", "../marc2bibframe2-master/xsl/marc2bibframe2.xsl"])

dom = ET.parse("Abel_Janszoon_Tasman_his_Life_and_Voyages.xml")
xslt = ET.parse("../marc2bibframe2-master/xsl/marc2bibframe2.xsl")
transform = ET.XSLT(xslt)
newdom = transform(dom)
with open ("T.xml", "w+") as f:
	f.write(str(newdom).replace('<?xml version="1.0"?>', ''))