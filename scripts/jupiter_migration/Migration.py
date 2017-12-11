import Classes.Transformation.Data as Data
import Classes.Utilities.URI_Generator as URI_Generator
import Classes.Utilities.Triple_Store as Triple_Store
from Classes.Query import Query_Factory
from config import types, sparqlTerms, sparqlData, sparqlResults
from tools import PrintException, cleanOutputs
import concurrent.futures
import time
from datetime import datetime


def main():
    """ main controller: iterates over each object type (generic item metadata, thesis item metadata, and binary-level metadata),
    creates a set of subqueries for each of these types, then cues threads to run each of these subqueries as a job. The migration outout is saved to
    the results folder and to a triplestore. The subqueries are cached in the cache folder. Custom settings can be modified in config.py."""
    tripleStoreData = Triple_Store.TripleStore(sparqlData, sparqlTerms, sparqlResults)
    uri_generator = URI_Generator.URIGenerator()
    ts = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    print('cleaning the cache')
    cleanOutputs(sparqlResults)
    # Iterate over every type of object that needs to be migrated.
    # This is the first splitting of the data for migration.
    # a queryObject has been split into multiple groups
    # only one group exists for community, and one for collection objects
    # approximately a thousand queries each are minted for thesis and for generic objects
    # these queries are based on the first folder in the fedora pair tree
    # a queryObject knows its type
    # a cache of queries is recorded, results are sent to a "results" triplestore, and results are stored as n-triples
    for objectType in types:
        queryObject = Query_Factory.QueryFactory().getMigrationQuery(objectType, tripleStoreData, uri_generator)
        print('{0} queries generated'.format(objectType))
        print('{0} queries of {1} objects to be transformed'.format(len(queryObject.queries), objectType))
        i = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            future_to_result = {executor.submit(parellelTransform, group, queryObject): group for group in queryObject.queries.keys()}
            for future in concurrent.futures.as_completed(future_to_result):
                future_to_result[future]
                try:
                    i = i + 1
                    future.result()
                    print("{0} of {1} {2} queries transformed".format(i, len(queryObject.queries), objectType))
                except Exception:
                    PrintException()
        print("{0} objects transformation completed".format(objectType))
        del queryObject
    tf = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    print("walltime:", datetime.strptime(tf, '%H:%M:%S') - datetime.strptime(ts, '%H:%M:%S'))


def parellelTransform(group, queryObject):
    DTO = Data.Data(group, queryObject)  # query, group, object
    DTO.transformData()
    # DTO.resultsToTriplestore()


if __name__ == "__main__":
    main()
