from fuzzywuzzy import fuzz
import concurrent.futures
import time
from datetime import datetime
from config import sparqlTerms, mig_ns, sparqlData
from SPARQLWrapper import JSON, SPARQLWrapper
import re, os, json, requests
import nltk
#nltk.download('punkt')
from nltk import word_tokenize

def main():

    def matrix(query):
        sparql.setQuery(query)
        r  = sparql.query().convert()['results']['bindings']
        print ("query done!")
        subjects = []
        ncols = len(r)+1
        subjects = [[0] * ncols for i in range(ncols)]
        subjects[0][0] = 0
        print ("matrix tempelate done!")
        out = (r, subjects)
        normalize(r, ncols, subjects)

    def hasNumbers(inputString):
        return bool(re.search(r'\d', inputString))

    def levDist(subjects, i, ncols):
        for j in range(1, ncols):
            if subjects[i][0] == subjects[0][j]:
                continue
            else:
                subjects[i][j] = fuzz.token_sort_ratio(subjects[i][0], subjects[0][j])
        return subjects

    def normalize(r, ncols, subjects):
        for i, triple in enumerate(r):
            subject = triple['value']['value']
            if hasNumbers(subject):
                pass
            else:
                if subject not in subjects[0]:
                    subjects[0][i+1] = subject
                    subjects[i+1][0] = subject
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            results = {executor.submit(levDist, subjects, i, ncols): i for i in range(1, ncols)}
        print ("distance function is done")
        write(subjects, objectType, ncols)

    subs =[]
    def write(subjects, objectType, ncols):
        for i in range(1, ncols):
            for j in range(1, ncols):
                if j < i:
                    continue
                else:
                    if int(subjects[i][j]) > 90:
                        subs.append(
                            {
                            'useForm': subjects[i][0],
                            'mappings': subjects[0][j],
                            'score': subjects[i][j] 
                            } 
                        )
        #print (subs)
        if objectType == ' ':
            with open('subjects/blank.json', 'a') as out:
                json.dump(subs, out)
            out.close()
        elif objectType == 'Conference/workshop Presentation':
            with open('subjects/Conference-workshop Presentation.json', 'a') as out:
                json.dump(subs, out)
            out.close()
        elif objectType == 'Conference/workshop Poster':
            with open('subjects/Conference-workshop Poster.json', 'a') as out:
                json.dump(subs, out)
            out.close()
        else:
            with open('subjects/' + objectType + '.json', 'a') as out:
                json.dump(subs, out)
            out.close()
        tf = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        print("time for " + objectType + ":", datetime.strptime(tf, '%H:%M:%S') - datetime.strptime(ts, '%H:%M:%S'))
            
    for objectType in [' ','null', 'Conference/workshop Poster', 'Conference/workshop Presentation','Book Chapter', 'Dataset', 'Thesis', 'Report', 'Computing Science Technical Report', 'Research Material', 'Review', 'Learning Object', 'Image', 'Structural Engineering Report', 'Book', 'Journal Article (Published)', 'Journal Article (Draft-Submitted)']:
        ts = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        sparql = SPARQLWrapper(sparqlData)
        sparql.setMethod("POST")
        sparql.setReturnFormat(JSON)
        if objectType == 'Thesis':
            for deg in ["", "Doctoral"]: #, "Master\\'s"
                query = "prefix dcterm: <http://purl.org/dc/terms/> select ?s ?type ?value where {?s dcterm:subject ?value . ?s dcterm:type ?type . ?s <http://terms.library.library.ca/identifiers/thesislevel> ?deg . filter(?deg = '%s' && ?type = '%s')}" % (deg, objectType) 
                print ("running for: " + deg)
                matrix(query)                    
            query = "prefix dcterm: <http://purl.org/dc/terms/> select ?s ?type ?value where {?s dcterm:subject ?value . ?s dcterm:type ?type  . minus {?s <http://terms.library.library.ca/identifiers/thesislevel> ?deg} filter(?type = 'Thesis')}" 
            matrix(query)
        else:
            query = "prefix dcterm: <http://purl.org/dc/terms/> select ?s ?type ?value where {?s dcterm:subject ?value . ?s dcterm:type ?type . filter(?type = '%s')}" % (objectType) 
            matrix(query)     
               
if __name__ == "__main__":
    main()
