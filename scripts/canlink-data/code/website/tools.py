import os
import sys
import linecache
import ast
import more_itertools as mit
import urllib
from config import solr_deg_map

def get_facets(new_facets, old_facets, facet_type, facet):
# get the old facets from the GET and produce the new list of facets (add or remove facet)
    solr_fq = ''
    if old_facets != '':
        new_facets = ast.literal_eval(old_facets)
    if facet_type == 'page':
    	pass
    elif facet_type not in new_facets and facet_type != 'rm':
        new_facets[facet_type] = []
        new_facets[facet_type].append(facet)
    elif facet_type == 'rm':
        for f in new_facets.keys():
            for i, fa in enumerate(new_facets[f]):
                if facet == new_facets[f][i]:
                    del new_facets[f][i]
    else:
        if facet not in new_facets[facet_type]:
            new_facets[facet_type].append(facet)
    for i in new_facets.keys():
        for j in new_facets[i]:
            if i == "degree" and j != "":
                solr_fq = solr_fq + '&fq=%s:"%s"' %(i, urllib.parse.quote_plus(j))
            else:
                solr_fq = solr_fq + '&fq=%s_str:"%s"' %(i, urllib.parse.quote_plus(j))  
    print (solr_fq)
    return (new_facets, solr_fq)

def get_facets_dict(raw_response):
    facets = {}
    for k,v in raw_response['facet_counts']['facet_fields'].items():
        spec_list = [list(spec) for spec in mit.chunked(v, 2)]
        facet = []
        for n, spec in enumerate(spec_list):
            facet.append([])
            facet[n].append(spec[0])
            facet[n].append(spec[1])
        facets[k] = facet
    return facets

def get_sparql_filter(new_facets):
	# generate a drill-down sparql query based on the selected facets (new_facets)
	sparql_filter = ''
	if "subject" in new_facets.keys():
		for i, sub in enumerate(new_facets['subject']):
			sparql_filter += '?url <http://purl.org/dc/terms/subject> ?sub_%s . ?sub_%s <http://www.w3.org/2000/01/rdf-schema#label> "%s" . ' %(i, i, sub)
	if "creator" in new_facets.keys():
		for i, aut in enumerate(new_facets['creator']):
			sparql_filter += '?author <http://xmlns.com/foaf/0.1/name> "%s" . ' %(aut)
	if "degree" in new_facets.keys():
		for i, deg in enumerate(new_facets['degree']):
			if deg in solr_deg_map.keys():
				deg = solr_deg_map[deg]
				sparql_filter += '?url <http://purl.org/ontology/bibo/degree> ?deg_%s . ?deg_%s <http://www.w3.org/2000/01/rdf-schema#label> "%s" . ' %(i, i, deg)
	return sparql_filter

def PrintException(log_file, error):
    with open (log_file, "a+") as logs:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print("EXCEPTION IN (%s, LINE %s '%s'): %s name: %s" % (filename, lineno, line.strip(), exc_obj, error))
        logs.write("EXCEPTION IN (%s, LINE %s '%s'): %s name: %s" % (filename, lineno, line.strip(), exc_obj, error))
        logs.write("\n")
