#!/usr/bin/python

import os

#trimming the new list of identifiers 
with open('identifiers/ualbertawiedrick.json', 'r') as file_new:
	with open('ualbertawiedrick_new.json', "w") as f_new:
		for eachLine in file_new:
			line = eachLine.replace(" ", "")
			f_new.write("%s" % line)


#trimming the old list of identifiers 
with open('../metadata-wrangling/internet_archive_coll/identifiers/ualbertawiedrick.json', 'r') as file_old:
	with open('ualbertawiedrick_old.json', "w") as f_old:
		for eachLine in file_old:
			line = eachLine.replace(",", "")
			f_old.write("%s" % line)

with open('ualbertawiedrick_old.json', 'r') as file1:
    with open('ualbertawiedrick_new.json', 'r') as file2:
        same = set(file2).difference(file1)

same.discard('\n')

with open('Diff.json', 'w') as file_out:
    for line in same:
        file_out.write(line)

os.remove('ualbertawiedrick_new.json')
os.remove('ualbertawiedrick_old.json')