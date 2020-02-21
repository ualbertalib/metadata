from os import listdir
import re, shutil

names = []
uploaded = 'uploaded'
for i, file in enumerate(listdir('uploaded')):
	name = file.replace('r.tiff', '').replace('v.tiff', '')
	if name not in names:
		names.append(name)

for file in names:
	shutil.move('Meta/%s.xml' %(file), uploaded)
