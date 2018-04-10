with open ("checksums.txt", "r") as f:
	checksums = {}
	for line in f:
		c = line.split("------")[0]
		noid = line.split("------")[1].replace(".xml\n", "")
		if c not in checksums.keys():
			checksums[c] = [noid] 
		else:
			checksums[c].append(noid)

with open("duplicates.tsv", "w+") as o:
	for i in checksums.keys():
		if len(checksums[i]) > 1:
			o.write(i + "\t" + str(checksums[i]) + "\n")

