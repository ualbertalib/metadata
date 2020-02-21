import os, re

for file in os.listdir('Q'):
	fi = "Q/%s" %(file)
	with open (fi) as f:
		lines = f.readlines()
		lines[1] = '<mods:mods xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:peel="http://peel.library.ualberta.ca/mods-extensions">'
		for i, text in enumerate(lines):
			if '</mods>' in lines[i]:
				lines[i] = '</mods:mods>'
	with open(fi, "w") as f:
		f.writelines(lines)
	f.close()