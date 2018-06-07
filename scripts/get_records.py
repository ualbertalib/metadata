#!/usr/bin/env python

import requests
import xml.etree.ElementTree as ET

base = "http://avalon.library.ualberta.ca:8080/fedora/objects?terms=*&pid=true&resultFormat=xml&maxResults=100"
query = ""
ns = {'foxml':'http://www.fedora.info/definitions/1/0/types/'}
name = 0
while True:
    # setup
    request_url = base + query
    response = requests.get(request_url)
    treeElement = ET.fromstring(response.content)
    elements = treeElement.findall(".//foxml:token", ns)
    # actions
    # exit gracefully if no elements are returned
    if len(elements) == 0:
        break
    token = elements[0].text
    print(token)
    tree = ET.ElementTree(treeElement)
    tree.write(str(name) + ".xml", 'utf-8')
    name += 1 
    if token == "":
        break
    # proxima ronda
    query = "&sessionToken=" + token