from jsondiff import diff
from SPARQLWrapper import JSON, SPARQLWrapper
import rdflib
import rdflib_jsonld
import json
import urllib2

#Fetching data
#URI of data to be fetched
# uri = 'http://www.worldcat.org/oclc/82671871'

# request_headers = {'Accept': 'application/rdf+xml'}

# request = urllib2.Request(uri, headers = request_headers)

# response = urllib2.urlopen(request).read()

# rdf_triple_data=response

# #Parsing data
# #Create empty graph
# graph = rdflib.Graph()

# #Parse the fetched data into the graph and tell the code the format of the data ('xml')
# graph.parse(data=rdf_triple_data, format='xml')

# new_data = graph.serialize(format='nt')

#======================
uri = 'http://www.worldcat.org/oclc/82671871'

graph = rdflib.Graph()

graph.parse(uri)

new_graph = graph.serialize(format='nt')

print(new_graph)


#======================
# Grab a list of all of the Predicates in the graph

# predicate_query = graph.query("""
#                      select ?predicates
#                      where {?s ?predicates ?o}
#                      """)

predicates = graph.predicates(subject=None, object=None)

# For each result print the value

# for row in predicate_query:
#     print('%s' % row)

for predicate in predicates:
    print(predicate)