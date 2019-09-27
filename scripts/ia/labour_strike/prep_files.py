from os import listdir, rename
import shutil

img = 'img'
for folder in listdir('Allison_Practicum'):
	for file in listdir('Allison_Practicum/%s' %(folder)):
		shutil.move('Allison_Practicum/%s/%s' %(folder, file), img)
		if '-002.tif' in file:
			rename('%s/%s' %(img, file), '%s/%s' %(img, file.replace('-002.tif', 'v.tiff')))
		if '-001.tif' in file:
			rename('%s/%s' %(img, file), '%s/%s' %(img, file.replace('-001.tif', '.tiff')))
