from SPARQLWrapper import JSON, SPARQLWrapper
import json

sparql = "http://206.167.181.124:7200/repositories/cldi-test-7"
sparqlData = SPARQLWrapper(sparql)
sparqlData.setCredentials("admin", "4Metadata!")
sparqlData.setReturnFormat(JSON)
j= {}

query = """select distinct ?url ?title ?year ?lang ?author ?subject ?firstName ?lastName ?fullname ?degree ?uni ?abstract where { 
            ?url <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ontology/bibo/thesis> . 
            ?url <http://purl.org/dc/terms/title> ?title .  
                  ?url <http://purl.org/dc/terms/issued> ?year .
                  ?url <http://purl.org/dc/terms/creator> ?author .
                  ?url <http://purl.org/dc/terms/language> ?lang .
    			  optional {?url <http://purl.org/dc/terms/subject> ?sub .
       			  ?sub <http://www.w3.org/2000/01/rdf-schema#label> ?subject}.
                  OPTIONAL {?author <http://xmlns.com/foaf/0.1/name> ?fullname . } 
                  OPTIONAL {?author <http://xmlns.com/foaf/0.1/lastName> ?lastName . } 
                  OPTIONAL {?author <http://xmlns.com/foaf/0.1/firstName> ?firstName . } 
                OPTIONAL {?url <http://purl.org/ontology/bibo/degree> ?deg . ?deg <http://www.w3.org/2000/01/rdf-schema#label> ?degree} 
                OPTIONAL {?url <http://purl.org/ontology/bibo/abstract> ?abstract . }
                ?url <http://purl.org/dc/terms/publisher> ?uni    
            } """
sparqlData.setQuery(query)  # set the query
results = sparqlData.query().convert()
for i, result in enumerate(results["results"]["bindings"]):
	id = result["url"]["value"]
	uni = result["uni"]["value"]
	title = result["title"]["value"]
	author_url = result["author"]["value"]
	year = result["year"]["value"]
	lang = result["lang"]["value"]
	if id not in j.keys():
		j[id] = {}
		j[id]['title'] = title
		j[id]['institution'] = uni
		j[id]['creator_url'] = author_url
		j[id]['year'] = year
		j[id]['lang'] = lang
		if "fullname" in result.keys():
			author_name = result["fullname"]["value"]
			j[id]['creator'] = author_name
		if "lastName" in result.keys():
			author_last = result["lastName"]["value"]
			j[id]['creator_last'] = author_last
		if "firstName" in result.keys():
			author_first = result["firstName"]["value"]
			j[id]['creator_first'] = author_first
		if "degree" in result.keys():
			degree_url = result["degree"]["value"]
			j[id]['degree'] = degree_url
		if "abstract" in result.keys():
			abstract = result["abstract"]["value"]
			j[id]['abstract'] = []
			j[id]['abstract'].append(abstract)
		if "subject" in result.keys():
			subject = result["subject"]["value"]
			j[id]['subject'] = []
			j[id]['subject'].append(subject)
	else:
		if "abstract" in result.keys():
			abstract = result["abstract"]["value"]
			if abstract not in j[id]['abstract']:
				j[id]['abstract'].append(abstract)
		if "subject" in result.keys():
			subject = result["subject"]["value"]
			if subject not in j[id]['subject']:
				j[id]['subject'].append(subject)

solr = []

for i, id in enumerate(j.keys()):
	subject = ''
	solr.append({})
	solr[i]["id"] = id
	solr[i]["year"] = j[id]["year"]
	solr[i]["title"] = j[id]["title"]
	solr[i]["institution"] = j[id]["institution"]
	solr[i]["creator_url"] = j[id]["creator_url"]
	solr[i]["creator"] = j[id]["creator"]
	solr[i]["lang"] = j[id]["lang"]
	if "creator_first" in j[id].keys():
		solr[i]["creator_first"] = j[id]["creator_first"]
	if "creator_last" in j[id].keys():
		solr[i]["creator_last"] = j[id]["creator_last"]
	if "degree" in j[id].keys():
		solr[i]["degree"] = j[id]["degree"]
	if "subject" in j[id].keys():
		solr[i]["subject"] = j[id]["subject"]
	if "abstract" in j[id].keys():
		solr[i]["abstract"] = j[id]["abstract"]
	
with open('test.json', 'w') as f:
	json.dump(solr, f)