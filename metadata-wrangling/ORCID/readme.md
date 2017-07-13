This folder contains:

- a file listing every ORCID associated with university of alberta (refers to "University of Alberta" somewhere in the profile) obtained using the ORCID API
	i.e. https://pub.orcid.org/v2.0/search?q="University of Alberta"&callback=json

- a folder containing an ORCID profile for each of the Ualberta associated ORCIDs

- a reconcile.py script that 
	1) calls all creator data from the ERA triple store
	2) parses each ORCID profile for a first and last name
	3) iterates over the ERA data to identify match candidates
	4) prints a json object containing all identifiable matches

	- note, there is a choice in the script whether to make the comparison more or less conservative (i.e. recall vs. precision)

- a folder containing two csv files
	- 'liberal.csv' contains 524 ERA-ORCID matches with less precision (approximately 80% reliable)
	- 'conservative.csv' contains 189 matches with very high precision (>99%)
