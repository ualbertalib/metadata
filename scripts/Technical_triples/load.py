from os import listdir
import subprocess
from os import getcwd

for file in listdir('fixity'):
	print (file)
	subprocess.call(["/home/danydvd/git/remote/metadata/scripts/Technical_triples/import.sh", "/home/danydvd/git/remote/metadata/scripts/Technical_triples/fixity/" + file])
