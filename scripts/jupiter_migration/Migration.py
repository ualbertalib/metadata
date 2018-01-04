import Classes.Transformation.Data as Data
import Classes.Utilities.URI_Generator as URI_Generator
import Classes.Utilities.Triple_Store as Triple_Store
from Classes.Query import Query_Factory
from config import types, sparqlTerms, sparqlData
from tools import PrintException, cleanOutputs
import concurrent.futures
import time
from datetime import datetime


def main():
    """ main controller: iterates over each object type (generic item metadata, thesis item metadata, and binary-level metadata),
    creates a set of subqueries for each of these types, then cues threads to run each of these subqueries as a job. The migration outout is saved to
    the results folder. The subqueries are cached in the cache folder. Custom settings can be modified in config.py."""
    ts = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') # a timestamp for observing the script walltime
    tripleStoreData = Triple_Store.TripleStore(sparqlData, sparqlTerms) # sets all of the endpoints on one object
    uri_generator = URI_Generator.URIGenerator() # an object for handling the creation and management of proxies
    cleanOutputs() # erase the contents of the query cache and the results folder
    # Iterate over every type of object that needs to be migrated.
    for objectType in types:
        # the queryFactory getMigrationQuery method returns a query object depending on the type it was passed
        # a query object contains all of the queries needed to obtain the data for this type, split into manageably sized groups
        queryObject = Query_Factory.QueryFactory().getMigrationQuery(objectType, tripleStoreData)
        # tell us a little about this query object
        print('{0} queries generated'.format(objectType))
        print('{0} queries of {1} objects to be transformed'.format(len(queryObject.queries), objectType))
        i = 0
        # spawn 8 workers, one for each group in the query object. A data object (see parellelTransform) is created for each group. When the 8 are finished, they return for more queries.
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            future_to_result = {executor.submit(parellelTransform, group, queryObject, uri_generator): group for group in queryObject.queries.keys()}
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


def parellelTransform(group, queryObject, UG):
    """the query object, along with a group, along with the uri generator object, are passed into a data object, where transformations occur and the data is saved"""
    DTO = Data.Data(group, queryObject)  # query, group, object
    DTO.transformData(UG)
    # DTO.resultsToTriplestore()


if __name__ == "__main__":
    main()
