import requests 
import xml.etree.ElementTree as ETree

with open('unembargo-issues.txt', 'r') as file:
	for line in file:
		r = requests.get(line)
		print (line, r)