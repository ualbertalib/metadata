import Classes.Transformation.Data as Data
import Classes.Utilities.Triple_Store as Triple_Store
from Classes.Query import Query_Factory
from config import types, sparqlTerms, sparqlData
from tools import PrintException, cleanOutputs
import concurrent.futures
import time
from datetime import datetime
from SPARQLWrapper import JSON, SPARQLWrapper
import random
import json

def main():
    """ main controller: iterates over each object type (generic item metadata, thesis item metadata, and binary-level metadata),
    creates a set of subqueries for each of these types, then cues threads to run each of these subqueries as a job. The migration outout is saved to
    the results folder. The subqueries are cached in the cache folder. Custom settings can be modified in config.py."""
    ts = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') # a timestamp for observing the script walltime
    tripleStoreData = Triple_Store.TripleStore(sparqlData, sparqlTerms) # sets all of the endpoints on one object
    cleanOutputs() # erase the contents of the query cache and the results folder
    
    #URIGenerator(sparqlData)  # generate new proxies
    f = open('Classes/Utilities/proxies/filesetIds.json', 'r+')
    filesetIds = json.load(f)
    f.close()
    f = open('Classes/Utilities/proxies/proxies.json', 'r+')
    proxies = json.load(f)
    f.close()
    # Iterate over every type of object that needs to be migrated.
    for objectType in types:
        validator = Set_Validator(objectType, sparqlTerms).generate_validator()
        print (validator)
        # the queryFactory getMigrationQuery method returns a query object depending on the type it was passed
        # a query object contains all of the queries needed to obtain the data for this type, split into manageably sized groups
        queryObject = Query_Factory.QueryFactory().getMigrationQuery(objectType, tripleStoreData)
        # tell us a little about this query object
        print('{0} queries generated'.format(objectType))
        print('{0} queries of {1} objects to be transformed'.format(len(queryObject.queries), objectType))
        i = 0
        # spawn 8 workers, one for each group in the query object. A data object (see parellelTransform) is created for each group. When the 8 are finished, they return for more queries.
        #with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        #    future_to_result = {executor.submit(parallelTransform, group, queryObject, filesetIds, proxies): group for group in queryObject.queries.keys()}
        #    for future in concurrent.futures.as_completed(future_to_result):
        #       future_to_result[future]
        #        i = i + 1
        #        future.result()
        #        print("{0} of {1} {2} queries transformed".format(i, len(queryObject.queries), objectType))
        #        tf = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        #        print("walltime:", datetime.strptime(tf, '%H:%M:%S') - datetime.strptime(ts, '%H:%M:%S'))

        for group in queryObject.queries.keys():
            parallelTransform(group, queryObject, filesetIds, proxies, validator)
            i = i + 1
            print("{0} of {1} {2} queries transformed".format(i, len(queryObject.queries), objectType))
            tf = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
            print("walltime:", datetime.strptime(tf, '%H:%M:%S') - datetime.strptime(ts, '%H:%M:%S'))
        print("{0} objects transformation completed".format(objectType))
        del queryObject


def parallelTransform(group, queryObject, filesetIds, proxies, validator):
    """the query object, along with a group, along with the uri generator object, are passed into a data object, where transformations occur and the data is saved"""
    Data.Data(group, queryObject, filesetIds, proxies, validator).transformData()  # query, group, object
    # DTO.resultsToTriplestore()


class URIGenerator():
    def __init__(self, sparqlData):
        self.proxyHash = {}
        self. fileSetHash = {}
        sparqlData = SPARQLWrapper(sparqlData)
        query = """prefix info: <info:fedora/fedora-system:def/model#> select distinct ?resource where {?resource info:hasModel ?model . filter(?model='Collection' || ?model='GenericFile')}"""
        sparqlData.setReturnFormat(JSON)
        sparqlData.setQuery(query)  # set the query
        results = sparqlData.query().convert()
        for result in results['results']['bindings']:
            self.generateProxyId(result['resource']['value'].split('/')[10])
            self.generatefileSetId(result['resource']['value'].split('/')[10])
        with open('Classes/Utilities/proxies/proxies.json', 'w+') as f:
            json.dump(self.proxyHash, f, sort_keys=True, indent=4, separators=(',', ': '))
        with open('Classes/Utilities/proxies/filesetIds.json', 'w+') as f:
            json.dump(self.fileSetHash, f, sort_keys=True, indent=4, separators=(',', ': '))

    def generatefileSetId(self, resource):
        fileSetId = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
        if fileSetId not in self.fileSetHash.values():
            if resource not in self.fileSetHash:
                self.fileSetHash[resource] = fileSetId
        else:
            self.generatefileSetId(resource)

    def generateProxyId(self, resource):
        proxyId = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
        if proxyId not in self.proxyHash.values():
            if resource not in self.proxyHash:
                self.proxyHash[resource] = proxyId
        else:
            self.generateProxyId(resource)

class Set_Validator(object):
    def __init__(self, objectType, sparqlTerms):
        self.objectType = objectType
        self.sparqlTerms = SPARQLWrapper(sparqlTerms)
        self.validator = []
        self.query = ""
        #self.generate_validator()

    def generate_validator(self):

        self.sparqlTerms.setReturnFormat(JSON)
        self.query = "PREFIX ual: <http://terms.library.ualberta.ca/> select ?predicate where { graph ual:%s { ?predicate ual:required 'true' } }" %(self.objectType)
        self.sparqlTerms.setQuery(self.query)
        results = self.sparqlTerms.query().convert()['results']['bindings']
        for triple in results:
            self.validator.append(triple['predicate']['value'])
        return self.validator


if __name__ == "__main__":
    main()
