import json, pickle
from Canlink_Reconciled import data

subject_mapping = {}
for item in data['rows']:
	if item['SH URIs'] != '':
		key = item['Original Label']
		if key not in subject_mapping.keys():
			subject_mapping[key] = item['SH URIs']

pickle_out = open("subject-recon.pickle","wb")
pickle.dump(subject_mapping, pickle_out)
pickle_out.close()
