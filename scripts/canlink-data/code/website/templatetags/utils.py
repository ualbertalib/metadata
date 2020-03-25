from django import template
from website.models import Processing
from config import sparql, sparqlData, namespaces, init_results_limit
import os

register = template.Library()

@register.filter
def minus(value):
    return value-1

@register.filter
def replaceFolder(value):
    return str(value).replace("MARC/","").replace("CSV/","").replace("RDF/","") 

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def replacedot(value):
	return value.replace('.', '')

@register.filter
def multi(index, arg):
    page = int(arg[1])
    results_limit = int(arg[0])
    if page == 1:
        return index
    else:
        number = index+((page-1)*results_limit)
        return number

@register.filter
def concat(results_limit, results_number):
    return [results_limit, results_number]

@register.filter
def result_range_start(page, results_limit):
    if page == 1:
        return 1
    else:
        number = ((page-1)*int(results_limit))+1
        return number

@register.filter
def result_range_end(page, results_limit):
    if page == 1:
        return results_limit
    else:
        number = ((page-1)*int(results_limit))+int(results_limit)
        return number

@register.filter
def get_name(value):
    if 'http://dbpedia.org' in value:
        name = value.replace('http://dbpedia.org/resource/', '').replace('_', ' ')
        return (name)
    else:
        return value

@register.filter
def get_image(value):
    logos = []
    if isinstance(value, list):
        #name = value[0].replace('http://dbpedia.org/resource/', '')
        name = value[0].replace('http://canlink.library.ualberta.ca/institution/', '')
    else:
        #name = value.replace('http://dbpedia.org/resource/', '')
        name = value.replace('http://canlink.library.ualberta.ca/institution/', '')
    for files in os.listdir('website/static/website/img/'):
        logos.append(files.split('.')[0])
    if name in logos:
        return ('website/img/%s.jpg' %(name))
    else:
        return ('website/img/no_logo.jpeg')

@register.filter
def get_uni(value):        
    return (value[0])

@register.filter
def get_pub_name(value): 
    return (value[5].replace('http://canlink.library.ualberta.ca/institution/', '').replace('_', ' '))

@register.filter
def get_abstract_blob(value):
    return (value[:500])

@register.filter
def test_abstract_len(value):
    if len(value) < 500:
        return (True)
    else: 
        return (False)

@register.filter
def get_subject_degree(value):
    query = """select ?label where {<%s> <http://www.w3.org/2000/01/rdf-schema#label> ?label}""" %(value)
    sparqlData.setQuery(query)  # set the query
    results = sparqlData.query().convert()
    for result in results['results']['bindings']:
        return result['label']['value']

@register.filter
def get_full_name(value):
    query = """select ?name where {<%s> <http://xmlns.com/foaf/0.1/name> ?name}""" %(value)
    sparqlData.setQuery(query)  # set the query
    results = sparqlData.query().convert()
    for result in results['results']['bindings']:
        return result['name']['value']

@register.filter
def inProcess(obj):
    for docs in Processing.objects.all():
        if obj.name == docs.name.replace("MARC/","").replace("CSV/","").replace("RDF/","") :
            return (docs.id)
    return False

@register.filter
def get_ns(obj):
    for ns in namespaces.keys():
        if ns in obj:
            return (obj.replace(ns, namespaces[ns]))
    return (obj)

@register.filter
def remove_url(value):
    return (value.split('/')[-1].replace('_', ' '))

@register.filter
def translate(sort):
    if sort == 'Relevance':
      solr_sort = 'Relevance'
    elif sort == 'tia':
      solr_sort = 'Title (A-Z)'
    elif sort == 'tid':
      solr_sort = 'Title (Z-A)'
    elif sort == 'da':
      solr_sort = 'Date (Asc)'
    elif sort == 'dd':
      solr_sort = 'Date (Desc)'
    return solr_sort