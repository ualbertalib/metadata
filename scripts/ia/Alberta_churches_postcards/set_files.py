import os
from os import listdir
from shutil import copyfile



for folder in ['A', 'B', 'C', 'D']:
	files = []
	# reading manifest
	with open(folder + '/' + 'manifest.txt', 'r') as man:
		for line in man:
			l = line.replace('\n', '').split(';')
	# renaming files
	'''for i, file in enumerate(listdir(folder)):
		if file.endswith('.jp2'):
			files.append(file)
	files = sorted(files)
	for index, id in enumerate(l):
		front = files[index*2]
		verso = files[(index*2)+1]
		os.rename(folder+'/'+front, folder+'/'+id+'.jp2')
		os.rename(folder+'/'+verso, folder+'/'+id+'_verso.jp2')'''
	#copy metadata files 
	for item in l:
		copyfile('Meta/'+item.strip()+'.xml', folder+'/'+item+'.xml')

