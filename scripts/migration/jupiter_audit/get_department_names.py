import requests
import json

solr_q = 'http://solrcloud.library.ualberta.ca:8080/solr/jupiter/select?fl=departments_tesim&indent=on&rows=25000&q=departments_tesim:*&wt=json'
solr_response = requests.get(solr_q).json()

departments = {}
# Print the name of each document.

for i, document in enumerate(solr_response['response']['docs']):
  #if len(document['departments_tesim']) > 1:
  #print (i, document['departments_tesim'])
  for dep in document['departments_tesim']:
  	if dep not in departments.keys():
  		departments[dep] = 1
  	else:
  		departments[dep] += 1

with open("ERA_departments.json", "w") as json_file:
    json.dump(departments, json_file)
    json_file.close()

with open("ERA_departments.tsv", "w") as tsv_file:
    for d in departments.keys():
    	tsv_file.write(str(d) + "\t" + str(departments[d]) + "\n")
    tsv_file.close()

print (len(departments))