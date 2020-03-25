from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from website.forms import searchForm, DocumentForm, CSV_DocumentForm, UploadFileForm
from django.contrib.auth.forms import PasswordChangeForm
from website.models import Institution_code, Documents, CSV_Documents, RDF_Documents, Processing, P_progress, Progress_archive
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
import os
import ast
import requests
import threading
from ipware.ip import get_ip
import time
from datetime import datetime as T
import codecs
import urllib
from urllib.request import urlopen
import simplejson
import json
import io
from pymarc import MARCReader
from config import project_folder_path, sparql, csh_sparql, dbp_data, sparqlData, csh_sparqlData, JSON, N3, solr_base, solr_facet_fields, solr_facet_limit, solr_rows, solr_sort_init, init_results_limit
from website.tools import get_facets, get_sparql_filter, get_facets_dict

#try:
 #   from .processing import *
#except:
 #   from processing import *

try:
    from .processing.processing import *
    from .processing.ualberta import processRDF
except:
    from website.processing.processing import *
    from website.processing.ualberta import processRDF

from django.views.decorators.csrf import csrf_exempt
import traceback


def index(request):
    return render(request, "website/header.html")

def main(request):
    collections = []
    form = searchForm(request.POST)  
    query = """select ?institution ?instLink ?instLabel ?num_of_docs (count (distinct ?resource) as ?num_of_docs) where {?resource <http://purl.org/dc/terms/publisher> ?institution. ?institution <http://www.w3.org/2000/01/rdf-schema#label> ?instLabel. ?institution <http://www.w3.org/2002/07/owl#sameAs> ?instLink} group by ?institution ?instLabel ?instLink order by DESC(?num_of_docs)"""
    sparqlData.setQuery(query)  # set the query
    results = sparqlData.query().convert()
    for i, result in enumerate(results['results']['bindings']):
        collections.append([])
        collections[i].append(result['institution']['value'])
        collections[i].append(result['instLink']['value'])
        collections[i].append(result['instLabel']['value'])
        collections[i].append(result['num_of_docs']['value'])
    query = """select ?num_of_docs (count (distinct ?resource) as ?num_of_docs) where {?resource <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ontology/bibo/thesis> }"""
    sparqlData.setQuery(query)  # set the query
    results = sparqlData.query().convert()
    for result in results['results']['bindings']:
        num_of_thesis = result['num_of_docs']['value']
    TM = T.now()
    return render(request, "website/index.html", {'docs': collections, 'num_of_thesis': num_of_thesis, 'form': form, 'time': TM})

def csh(request):
  query_result = []
  q = request.POST['search']
  query = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> select distinct ?uri ?label where {?uri <http://www.w3.org/2004/02/skos/core#prefLabel> ?label . filter(contains(?label, '%s'))} order by ?label""" %(q)
  csh_sparqlData.setQuery(query)  # set the query
  results = csh_sparqlData.query().convert()
  for i, result in enumerate(results['results']['bindings']):
          query_result.append([])
          query_result[i].append(result['uri']['value'])
          query_result[i].append(result['label']['value'])
  return render(request, "website/csh_results.html", {'results': query_result, 'query': q})

def search(request):
    query_result = []
    solr_fq =''
    solr_sort = solr_sort_init
    new_facets = {}
    new_facets['subject'] = []
    new_facets['degree'] = []
    new_facets['creator'] = []
    new_facets['lang'] = []
    new_facets['institution'] = []
    if 'results_limit' in request.POST.keys():
      results_limit = request.POST['results_limit']
    else:
      results_limit = init_results_limit
    if request.method == 'POST':
        search_type = request.POST['search_type']
        q = request.POST['search']
        if search_type == "institution":
          solr_q = urllib.parse.quote_plus(q)
          solr_facets = urlopen('%s?%s&facet.mincount=1&facet.limit=%s&facet=on&q=institution:"%s"&%s&%s' %(solr_base, solr_facet_fields, solr_facet_limit, solr_q, solr_rows, solr_sort))
        # search with Lucene index
        elif search_type == "All":
          solr_q = urllib.parse.quote_plus(q)
          try:
            test_q = int(solr_q)
            if isinstance(test_q, int):
              solr_query = 'q=title:' + solr_q + '%20or%20year:' + solr_q + '%20or%20creator:' + solr_q + '%20or%20creator_first:' + solr_q + '%20or%20creator_last:' + solr_q + '%20or%20abstract:' + solr_q + '%20or%20subject:' + solr_q + '%20or%20degree:' + solr_q
          except:
            solr_query = 'q=title:' + solr_q + '%20or%20creator:' + solr_q + '%20or%20creator_first:' + solr_q + '%20or%20creator_last:' + solr_q + '%20or%20abstract:' + solr_q + '%20or%20subject:' + solr_q + '%20or%20degree:' + solr_q
          solr_facet = ('%s?%s&facet.mincount=1&facet.limit=%s&facet=on&%s&%s&%s' %(solr_base, solr_facet_fields, solr_facet_limit, solr_query, solr_rows, solr_sort))
          print (solr_facet)
          solr_facets = urlopen(solr_facet)
        elif search_type == "Title":
          solr_q = urllib.parse.quote_plus(q)
          solr_facets = urlopen('%s?%s&facet.mincount=1&facet.limit=%s&facet=on&q=title:%s&%s&%s' %(solr_base, solr_facet_fields, solr_facet_limit, solr_q, solr_rows, solr_sort))
        elif search_type == "Author":
          solr_q = urllib.parse.quote_plus(q)
          solr_query = 'q=creator:' + solr_q + '%20or%20creator_first:' + solr_q + '%20or%20creator_last:' + solr_q 
          solr_facets = urlopen('%s?%s&facet.mincount=1&facet.limit=%s&facet=on&%s&%s&%s' %(solr_base, solr_facet_fields, solr_facet_limit, solr_query, solr_rows, solr_sort))
        elif search_type == "Date":   
          solr_q = urllib.parse.quote_plus(q)
          solr_facets = urlopen('%s?%s&facet.mincount=1&facet.limit=%s&facet=on&q=year:%s&%s&%s' %(solr_base, solr_facet_fields, solr_facet_limit, solr_q, solr_rows, solr_sort))
        elif search_type == "Subject": 
          solr_q = urllib.parse.quote_plus(q)
          solr_facets = urlopen('%s?%s&facet.mincount=1&facet.limit=%s&facet=on&q=subject:%s&%s&%s' %(solr_base, solr_facet_fields, solr_facet_limit, solr_q, solr_rows, solr_sort))
        elif search_type == "Abstract":  
          solr_q = urllib.parse.quote_plus(q)
          solr_facets = urlopen('%s?%s&facet.mincount=1&facet.limit=%s&facet=on&q=abstract:%s&%s&%s' %(solr_base, solr_facet_fields, solr_facet_limit, solr_q, solr_rows, solr_sort))
        
        raw_response = simplejson.load(solr_facets)
        facets = get_facets_dict(raw_response)

        for i, doc in enumerate(raw_response["response"]["docs"]):
          id = doc['id']
          title = doc['title'][0]
          if 'abstract' in doc.keys():
            abstract = doc['abstract'][0]
          year = doc['year'][0]
          creator = doc['creator'][0]
          creator_url = doc['creator_url'][0]
          institution = doc['institution'][0]

          query_result.append([])
          query_result[i].append(id)
          query_result[i].append(title)
          query_result[i].append(year)
          query_result[i].append(creator)
          query_result[i].append(creator_url)
          query_result[i].append(institution)
          if 'abstract' in doc.keys():
            query_result[i].append(abstract)
          else:
            query_result[i].append('No abstract')
        docs_len = len(query_result)
        paginator = Paginator(query_result, results_limit)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        index = contacts.number
        # This value is maximum index of your pages, so the last page - 1
        max_index = len(paginator.page_range)
        # You want a range of 7, so lets calculate where to slice the list
        start_i = index - 3 if index >= 3 else 0
        end_i = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range)[start_i:end_i]
        return render(request, "website/search.html", {'results': contacts, 'page_range': page_range, 'results_limit': results_limit, 'solr_sort': 'Relevance','query': q, 'search_type': search_type, 'docs_len': docs_len, 'f_creators': facets['creator_str'], 'f_subjects': facets['subject_str'], 'f_degree': facets['degree'], 'f_lang': facets['lang_str'], 'f_inst': facets['institution_str']})
    elif request.method == "GET":
        sparql_filter = ''
        p = request.GET.get('page')
        page = p.split('?q=')[0]
        tmp = p.split('?q=')[1]
        q = tmp.split('?search_type=')[0]
        if '?facet=' in tmp:
          search_type = tmp.split('?search_type=')[1].split('?l=')[0]
          results_limit = tmp.split('?search_type=')[1].split('?l=')[1].split('?so=')[0]
          sort = tmp.split('?search_type=')[1].split('?l=')[1].split('?so=')[1].split('?facet=')[0]
          facet = tmp.split('?search_type=')[1].split('?l=')[1].split('?so=')[1].split('?facet=')[1].split('?facet_type=')[0]
          facet_type = tmp.split('?search_type=')[1].split('?l=')[1].split('?so=')[1].split('?facet=')[1].split('?facet_type=')[1].split('?f=')[0]
          old_facets = tmp.split('?search_type=')[1].split('?l=')[1].split('?so=')[1].split('?facet=')[1].split('?facet_type=')[1].split('?f=')[1]
          get_facet = get_facets(new_facets, old_facets, facet_type, facet)
          new_facets = get_facet[0]
          solr_fq = get_facet[1]
        else:
          search_type = tmp.split('?search_type=')[1].split('?l=')[0]
          results_limit = tmp.split('?search_type=')[1].split('?l=')[1].split('?so=')[0]
          sort = tmp.split('?search_type=')[1].split('?l=')[1].split('?so=')[1]
        
        if sort == 'Relevance':
          solr_sort = 'sort=score%20Desc'
        elif sort == 'tia':
          solr_sort = 'sort=title_str%20asc'
        elif sort == 'tid':
          solr_sort = 'sort=title_str%20desc'
        elif sort == 'da':
          solr_sort = 'sort=year%20asc'
        elif sort == 'dd':
          solr_sort = 'sort=year%20desc'

        if search_type == "institution":
          solr_q = urllib.parse.quote_plus(q)
          solr_facets = urlopen('%s?%s&facet.mincount=1&facet.limit=%s&facet=on&%s&q=institution:"%s"&%s&%s' %(solr_base, solr_facet_fields, solr_facet_limit, solr_fq, solr_q, solr_rows, solr_sort))
        elif search_type == "All":
          solr_q = urllib.parse.quote_plus(q)
          try:
            test_q = int(solr_q)
            if isinstance(test_q, int):
              solr_query = 'q=title:' + solr_q + '%20or%20year:' + solr_q + '%20or%20creator:' + solr_q + '%20or%20creator_first:' + solr_q + '%20or%20creator_last:' + solr_q + '%20or%20abstract:' + solr_q + '%20or%20subject:' + solr_q + '%20or%20degree:' + solr_q
          except:
            solr_query = 'q=title:' + solr_q + '%20or%20creator:' + solr_q + '%20or%20creator_first:' + solr_q + '%20or%20creator_last:' + solr_q + '%20or%20abstract:' + solr_q + '%20or%20subject:' + solr_q + '%20or%20degree:' + solr_q
          solr_facet = ('%s?%s&facet.mincount=1&facet.limit=%s&facet=on%s&%s&%s&%s' %(solr_base, solr_facet_fields, solr_facet_limit, solr_fq, solr_query, solr_rows, solr_sort))
          solr_facets = urlopen(solr_facet)
        elif search_type == "Title":
          solr_q = urllib.parse.quote_plus(q)
          solr_facets = urlopen('%s?%s&facet.mincount=1&facet.limit=%s&facet=on&%s&q=title:%s&%s&%s' %(solr_base, solr_facet_fields, solr_facet_limit, solr_fq, solr_q, solr_rows, solr_sort))
        elif search_type == "Author":
          solr_q = urllib.parse.quote_plus(q)
          solr_query = 'q=creator:' + solr_q + '%20or%20creator_first:' + solr_q + '%20or%20creator_last:' + solr_q 
          solr_facets = urlopen('%s?%s&facet.mincount=1&facet.limit=%s&facet=on&%s&sq=year:%s&%s&%s' %(solr_base, solr_facet_fields, solr_facet_limit, solr_fq, solr_q, solr_rows, solr_sort))
        elif search_type == "Date":   
          solr_q = urllib.parse.quote_plus(q)
          solr_facets = urlopen('%s?%s&facet.mincount=1&facet.limit=%s&facet=on&%s&sq=year:%s&%s&%s' %(solr_base, solr_facet_fields, solr_facet_limit, solr_fq, solr_q, solr_rows, solr_sort))
        elif search_type == "Subject":   
          solr_q = urllib.parse.quote_plus(q)
          solr_facets = urlopen('%s?%s&facet.mincount=1&facet.limit=%s&facet=on&%s&q=subject:%s&%s&%s' %(solr_base, solr_facet_fields, solr_facet_limit, solr_fq, solr_q, solr_rows, solr_sort))
        elif search_type == "Abstract":   
          solr_q = urllib.parse.quote_plus(q)
          solr_facets = urlopen('%s?%s&facet.mincount=1&facet.limit=%s&facet=on&%s&q=abstract:%s&%s&%s' %(solr_base, solr_facet_fields, solr_facet_limit, solr_fq, solr_q, solr_rows, solr_sort))
        raw_response = simplejson.load(solr_facets)
        facets = get_facets_dict(raw_response)
        for i, doc in enumerate(raw_response["response"]["docs"]):
          id = doc['id']
          title = doc['title'][0]
          if 'abstract' in doc.keys():
            abstract = doc['abstract'][0]
          year = doc['year'][0]
          creator = doc['creator'][0]
          creator_url = doc['creator_url'][0]
          institution = doc['institution'][0]

          query_result.append([])
          query_result[i].append(id)
          query_result[i].append(title)
          query_result[i].append(year)
          query_result[i].append(creator)
          query_result[i].append(creator_url)
          query_result[i].append(institution)
          if 'abstract' in doc.keys():
            query_result[i].append(abstract)
          else:
            query_result[i].append('No abstract')
        
        docs_len = len(query_result)
        paginator = Paginator(query_result, results_limit)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        index = contacts.number
        # This value is maximum index of your pages, so the last page - 1
        max_index = len(paginator.page_range)
        # You want a range of 7, so lets calculate where to slice the list
        start_i = index - 3 if index >= 3 else 0
        end_i = index + 3 if index <= max_index - 3 else max_index
        # Get our new page range. In the latest versions of Django page_range returns 
        # an iterator. Thus pass it to list, to make our slice possible again.
        page_range = list(paginator.page_range)[start_i:end_i]
        return render(request, "website/search.html", {'results': contacts, 'page_range': page_range, 'results_limit': results_limit, 'solr_sort': sort, 'query': q, 'search_type': search_type, 'docs_len': docs_len, 'f_creators': facets['creator_str'], 'f_subjects': facets['subject_str'], 'f_degree': facets['degree'], 'f_lang': facets['lang_str'], 'f_inst': facets['institution_str'], 'f': new_facets, 'subject_filters': new_facets['subject'], 'degree_filters': new_facets['degree'], 'creator_filters': new_facets['creator'], 'lang_filters': new_facets['lang'], 'inst_filters': new_facets['institution']})

def getitem(request, id):
    if request.method == 'GET':
        tmp = request.get_full_path()
        item = tmp.replace('/getitem/', '').split('?')[0]
        query_result = []
        tmp_results = {}
        works = []
        subjects = []
        title = ''
        institution = ''
        query = """select * where {<%s> ?predicate ?object}""" %(item)
        sparqlData.setReturnFormat(JSON)
        sparqlData.setQuery(query)  # set the query
        results = sparqlData.query().convert()
        for result in results['results']['bindings']:
            if result['predicate']['value'] not in tmp_results.keys():
                tmp_results[result['predicate']['value']] = []
                tmp_results[result['predicate']['value']].append(result['object']['value'])
            else:
                tmp_results[result['predicate']['value']].append(result['object']['value'])
            if result['predicate']['value'] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and result['object']['value'] == "http://xmlns.com/foaf/0.1/Person":
                q = """select ?title ?s ?p where { ?s <http://purl.org/dc/terms/title> ?title {{select ?s ?p where {?s ?p <%s>}}}}""" %(item)
                sparqlData.setQuery(q)  # set the query
                r = sparqlData.query().convert()
                for j, re in enumerate(r['results']['bindings']):
                    works.append([])
                    works[j].append(re['p']['value'])
                    works[j].append(re['s']['value'])
                    works[j].append(re['title']['value'])
            if result['predicate']['value'] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and result['object']['value'] == "http://www.w3.org/2004/02/skos/core#Concept":
                q = """select ?title ?year ?author ?fullname ?uni ?s where { ?s <http://purl.org/dc/terms/title> ?title . ?s <http://purl.org/dc/terms/publisher> ?uni . ?s <http://purl.org/dc/terms/issued> ?year . ?s <http://purl.org/dc/terms/creator> ?author . ?author <http://xmlns.com/foaf/0.1/name> ?fullname . {{select ?s where {?s <http://purl.org/dc/terms/subject> <%s>}}}}""" %(item)
                sparqlData.setQuery(q)  # set the query
                r = sparqlData.query().convert()
                for j, re in enumerate(r['results']['bindings']):
                    subjects.append([])
                    subjects[j].append(re['s']['value'])
                    subjects[j].append(re['title']['value'])
                    subjects[j].append(re['year']['value'])
                    subjects[j].append(re['author']['value'])
                    subjects[j].append(re['fullname']['value'])
                    subjects[j].append(re['uni']['value'])
        for i, predicate in enumerate(tmp_results.keys()):
            if predicate == 'http://purl.org/dc/terms/title':
                title = tmp_results[predicate][0]
            if predicate == 'http://purl.org/dc/terms/publisher':
                institution = tmp_results[predicate][0]
            query_result.append([])
            query_result[i].append(predicate)
            query_result[i].append(tmp_results[predicate])
        return render(request, "website/item_view.html", {'results': query_result, 'works': works, 'subjects': subjects, 'item': item, 'title': title, 'institution': institution})

def csh_search(request):
  return render(request, "website/csh.html")

def get_csh(request, id):
  query_result = []
  pref_label = ''
  related = []
  j = 0
  tmp = request.get_full_path()
  item = tmp.replace('/get_csh/', '').split('?')[0]
  query = """select * where {<%s> ?predicate ?object}""" %(item)
  csh_sparqlData.setQuery(query)  # set the query
  results = csh_sparqlData.query().convert()
  for i, result in enumerate(results['results']['bindings']):
    if 'http://www.w3.org/2004/02/skos/core#prefLabel' in result['predicate']['value']:
      pref_label = result['object']['value']
    elif 'http://www.w3.org/2004/02/skos/core#related' in result['predicate']['value']:
      query = """select ?related where {<%s> <http://www.w3.org/2004/02/skos/core#prefLabel> ?related}""" %(result['object']['value'])
      csh_sparqlData.setQuery(query)  # set the query
      rel_results = csh_sparqlData.query().convert()
      for i, re in enumerate(rel_results['results']['bindings']):
        related.append([result['object']['value'], re['related']['value']])
      print (related)
    else:
      query_result.append([])
      query_result[j].append(result['predicate']['value'])
      query_result[j].append(result['object']['value'])
      j += 1
  return render(request, "website/csh_view.html", {'results': query_result, 'label': pref_label, 'related': related})

def download(request):
  if request.method == 'POST':
    file_format = request.POST['format']
    if file_format == 'json-ld':
      ext = 'json'
    elif file_format == 'pretty-xml':
      ext = 'xml'
    else:
      ext =file_format
    item = request.POST['item']
    from rdflib.serializer import Serializer
    with open('ual.nt', 'a') as file:
      prefix = 'prefix dcterms: <http://purl.org/dc/terms/> prefix bibo: <http://purl.org/ontology/bibo/>'
      query = "%s construct {<%s> ?p ?o} where {<%s> ?p ?o}" %(prefix, item, item)
      sparqlData.setQuery(query)
      sparqlData.setReturnFormat(N3)
      result = sparqlData.query().convert()
      g = Graph()
      g.parse(data=result, format="n3")
      g.serialize("download/"+item.split('/')[-1]+"."+ext, format=file_format)
      file.close()
    file_path = os.path.join("download/"+item.split('/')[-1]+"."+ext)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/%s" %(ext))
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    return HttpResponse('Http404') 

@login_required(login_url='/accounts/login/')
def upload(request, file=None, status=None):
    docs = Documents.objects.all()
    processing_docs = Processing.objects.all()
    processing_archive = Progress_archive.objects.all()
    csv_docs = CSV_Documents.objects.all()
    rdf_docs = RDF_Documents.objects.all()
    if len(request.FILES) > 0:
        print (request.FILES)
        UploadFile = UploadFileForm(request.POST, request.FILES)
        checksum="thisisadummyobjectonlynumber123456"
        if docs.filter(description=checksum).exists():
            pass
        else:
            adddummy = Documents(description=checksum, 
                        name="dumy_object", 
                        file_type="dummy data",
                        uploaded_at="2014-09-04 23:34:40.834676",
                        file_format=".dum")
            adddummy.save()
        files = request.FILES.getlist('file')
        for file in files:
            uploaded_file = file
            filename = uploaded_file.name
            file_ext = os.path.splitext(filename)[1]
            if file_ext == ".mrc"or file_ext == '.marc':
                f_type = 'MARC_Data'
                marc_folder = 'website/source/MARC'
                if UploadFile.is_valid():
                    doc = Documents(description=request.POST['Description'], 
                            name=file, 
                            document=file,
                            uploader=request.user,
                            file_type=f_type,
                            file_format=file_ext)
                    doc.save()
            if file_ext == ".csv":
                f_type = 'Tabular_Data'
                marc_folder = 'website/source/CSV'
                if UploadFile.is_valid():
                    doc = CSV_Documents(description=request.POST['Description'], 
                            name=file, 
                            document=file,
                            uploader=request.user,
                            file_type=f_type,
                            file_format=file_ext)
                    doc.save()
            if file_ext == ".xml" or file_ext == ".nt":
                f_type = 'RDF_Data'
                marc_folder = 'website/source/RDF'
                if UploadFile.is_valid():
                    doc = RDF_Documents(description=request.POST['Description'], 
                            name=file, 
                            document=file,
                            uploader=request.user,
                            file_type=f_type,
                            file_format=file_ext)
                    doc.save()
        return redirect('upload', 'files', 'success')
    else:
        UploadFile = UploadFileForm()
        return render(request, 'website/upload.html', {"UploadFileForm": UploadFile, "rdf_docs": rdf_docs, "csv_docs": csv_docs, "docs": docs, "processing_docs": processing_docs, "processing_archive": processing_archive, "del_file": file, 'status': status})

def deleteRecord(request, id =None, format=None):
    folder = 'website/source'
    if format == '.mrc':
        object = Documents.objects.get(id=id)
    elif format == '.csv':
        object = CSV_Documents.objects.get(id=id)
    elif format == '.xml' or format == '.nt':
        object = RDF_Documents.objects.get(id=id)
    file = str(object.document)
    object.delete()
    file_path = os.path.join(folder, file)
    print (file_path)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)
    return redirect('upload', file.split('/')[-1], 'deleted')

def deleted(request, file):
    docs = Documents.objects.all()
    csv_docs = CSV_Documents.objects.all()
    rdf_docs = RDF_Documents.objects.all()
    UploadFile = UploadFileForm()
    return render(request, 'website/upload.html', {"UploadFileForm": UploadFile, "rdf_docs": rdf_docs, "csv_docs": csv_docs, "docs": docs, "del_file": file})

@login_required(login_url='/accounts/login/')
def profile(request, username=None, error=None):
    print (username, error)
    documents = []
    usr = User.objects.get(username=username)
    institutions = Group.objects.all()
    a = len(Documents.objects.filter(uploader=usr))
    b = len(CSV_Documents.objects.filter(uploader=usr))
    for i, docs in enumerate(Documents.objects.filter(uploader=usr)):
        documents.append([])
        name = str(docs.document).replace("MARC/","")
        documents[i].append(name)
        documents[i].append(docs.description)
        documents[i].append(docs.uploaded_at)
        documents[i].append(docs.file_type)
    for j, docs in enumerate(CSV_Documents.objects.filter(uploader=usr)):
        documents.append([])
        name = str(docs.document).replace("CSV/","")
        documents[j+a].append(name)
        documents[j+a].append(docs.description)
        documents[j+a].append(docs.uploaded_at)
        documents[j+a].append(docs.file_type)
    for z, docs in enumerate(RDF_Documents.objects.filter(uploader=usr)):
        documents.append([])
        name = str(docs.document).replace("RDF/","")
        documents[z+a+b].append(name)
        documents[z+a+b].append(docs.description)
        documents[z+a+b].append(docs.uploaded_at)
        documents[z+a+b].append(docs.file_type)
    return render(request, 'website/usr_profile.html', {'user': usr, 'institutions': institutions, 'documents': documents, 'error': error})

def register(request):
    institutions = Group.objects.all()
    return render(request, 'website/register.html', {'institutions': institutions})

def reg_user(request):
    if request.method == "POST":
        institutions = Group.objects.all()
        inst = Institution_code.objects.get(name=request.POST['inst_selector'])
        if inst.skey != request.POST['inst_code']:
            return render(request, 'website/register.html', {'institutions': institutions, 'error': 'institution_key'})
        else:
            if (request.POST['Password'] != request.POST['Password_conf']):
                return render(request, 'website/register.html', {'institutions': institutions, 'error': 'password'})
            else:
                password = request.POST['Password']
                fname = request.POST['first_name']
                lname = request.POST['last_name']
                email = request.POST['email']
                institution = request.POST['inst_selector']
                username = email
                if User.objects.filter(username=username).exists():
                    return render(request, 'website/register.html', {'institutions': institutions, 'error': 'user'})
                else:
                    user = User.objects.create_user(username, email, password)
                    user.last_name = lname
                    user.first_name = fname
                    user.save()
                    group = Group.objects.get(name=institution)
                    group.user_set.add(user)
                    return render(request, 'website/register.html', {'institutions': institutions, 'error': 'none'})
    else:
        return render(request, 'website/register.html', {'institutions': institutions})

def  update_user(request):
    if request.method == "POST":
        user = User.objects.get(username=request.POST['user_name'])
        institutions = Group.objects.all()
        inst = Institution_code.objects.get(name=request.POST['inst_selector'])
        if inst.skey != request.POST['inst_code']:
            return redirect('profile', user.username, 'institution_key')
        else:
            user.last_name = request.POST['last_name_edit']
            user.first_name = request.POST['first_name_edit']
            user.save()
            user.groups.clear()
            institution = request.POST['inst_selector']
            group = Group.objects.get(name=institution)
            group.user_set.add(user)
        return redirect('profile', user.username, "updated")
        #return render(request, 'website/usr_profile.html', {'user': user, 'error': 'updated'})

def change_password(request):
    if request.method == 'POST':
        cp = request.POST['Current_Password']
        user = User.objects.get(username=request.POST['user_name'])
        if user.check_password('{}'.format(cp)) == True:
            if request.POST['Password'] == request.POST['Password_conf']:
                user.set_password(request.POST['Password'])
                user.save()
                return redirect('profile', user.username, "none")    
            else:
                return redirect('profile', user.username, "pass_match")
        else:
            return redirect('profile', user.username, "old_pass")


@csrf_exempt
def checkUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        response_data = ''

        if User.objects.filter(username=username).exists():
            response_data = 'This email address is taken'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return HttpResponse('&#10004;')

@csrf_exempt
# checks if the institution key matches the database records (activated on keyup in the registration form [institution code field])  
def checkskey(request):
    if request.method == 'POST':
        # get the institution name selected by the user 
        institution = request.POST.get('institution')
        skey = request.POST.get('skey')
        response_data = ''
        # if the code matches, send a response with a check mark
        # if response is empty, a red croess will be displayed 
        if Institution_code.objects.filter(name=institution).exists():
            inst = Institution_code.objects.get(name=institution)
            key = inst.skey
            if key == skey:
                response_data = '&#10004;'
                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )
            else:
                return HttpResponse(response_data)
        else:
            return HttpResponse(response_data)

@csrf_exempt
def csh_autosuggest(request):
  if request.method == 'POST':
    htmlresponse = ''
    query_result = []
    q = request.POST.get('query')
    query = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> select distinct ?label where {?s <http://www.w3.org/2004/02/skos/core#prefLabel> ?label . filter(contains(?label, '%s'))} limit 5""" %(q)
    csh_sparqlData.setQuery(query)  # set the query
    results = csh_sparqlData.query().convert()
    for i, result in enumerate(results['results']['bindings']):
            query_result.append(result['label']['value'])
    if len(query_result) > 0:
      htmlresponse = '<ul>'
      for item in query_result:
        htmlresponse += '<li class="autosuggested" val="testing" onclick="select_autoseggest()">%s</li>' %(item)
    htmlresponse += '</ul>'
    print (query_result)
    return HttpResponse(htmlresponse)

# delete a process from processing (and P_progress) tables
def stop(request, id=None):
    try:
        object = Processing.objects.get(id=id)
        pid = object.id
        name = object.name
        files = P_progress.objects.get(pid_id=pid)
        object.delete()
        return(render(request, "website/stop.html", {"stoped": name}))
    # when the process is done it will be added to processing_archives and will be deleted from processing
    # however, it will be displayed in the page (if the page is not refreshed). This will re-render the page to avoid error
    except:
        return redirect('thesisSubmission')

def progress(request):
    update_marc = [item.as_marc() for item in P_progress.objects.all()]
    update_rdf = [item.as_rdf() for item in P_progress.objects.all()]
    return JsonResponse({'latest_progress_marc':update_marc, 'latest_progress_rdf':update_rdf})

def archive(request):
    archives = Progress_archive.objects.all()
    return render(request, 'website/archive.html', {'archives': archives})

def delete_archive(request, id =None):
    object = Progress_archive.objects.get(id=id)
    master_file = object.master_file
    object.delete()
    return render(request, 'website/archive.html')

def delete_archive_all(request):
    for object in Progress_archive.objects.all():
        master_file = object.master_file
        object.delete()
        if os.path.isfile(master_file):
            os.unlink(master_file)
    return render(request, 'website/archive.html')

def thesisSubmission(request):
    # called when the presses the submit button after pasting the records
    overload = Processing.objects.all()
    if request.method == 'POST':
        lac_upload = False
        #form = CheckForm(request.POST or None)
        file_dict = dict(request.POST.lists())
        if 'file_selected' in file_dict.keys():
            olcheck = len(overload) + len(file_dict["file_selected"])
            if olcheck > 4:
                return redirect('upload', 'files', 'overload')
            else:
                # get all files that were selected in the upload.html for processing
                for item in file_dict['file_selected']:
                    # send files to the proper processing script based on file type (extension)
                    if item.endswith('.mrc'):
                        # get the object info from the database and add it to processing table
                        object = Documents.objects.get(document=item)
                        add_process = Processing(description=object.description, 
                                    name=str(object.document), 
                                    uploaded_at=object.uploaded_at,
                                    file_format=object.file_format,
                                    file_type=object.file_type,
                                    status="started")
                        # if there was an error adding to processing table (duplicated), return to upload.html with an proper error 
                        try:
                            add_process.save()
                        except:
                            return redirect('upload', 'files', 'duplicated_process')
                        # process start time
                        tps = T.fromtimestamp(time.time()).strftime('%H:%M:%S')  
                        # decode the file and get number of records in the marc file
                        with open('website/source/' + item, 'rb') as f:
                            file = f.read()
                            num_of_rec = len(list(MARCReader(file, force_utf8=True)))
                            print (num_of_rec)
                            for enc in ["cp1252", "utf-8"]:
                                try:
                                    raw_records = file.decode(enc)
                                    break
                                except:
                                    continue
                            f.close()

                        # start a single thread and call the marc processing script
                        t = threading.Thread(target=processRecords, args=[raw_records, lac_upload, add_process, num_of_rec, tps] )
                        t.setDaemon(True)
                        t.start()
                    # send files to the proper processing script based on file type (extension)
                    elif item.endswith('.xml') or item.endswith('.nt'):
                        object = RDF_Documents.objects.get(document=item)
                        add_process = Processing(description=object.description, 
                                    name=str(object.document), 
                                    uploaded_at=object.uploaded_at,
                                    file_format=object.file_format,
                                    file_type=object.file_type,
                                    status="started")
                        # if there was an error adding to processing table (duplicated), return to upload.html with an proper error 
                        try:
                            add_process.save()
                        except:
                            return redirect('upload', 'files', 'duplicated_process')
                        # rdf process start time
                        rdf_tps = T.fromtimestamp(time.time()).strftime('%H:%M:%S')
                        # start a single thread and call the rdf processing script
                        t = threading.Thread(target=processRDF, args=['website/source/' + item, add_process, rdf_tps] )
                        t.setDaemon(True)
                        t.start()
                # once the threads are created get everything for the processing table (items being processed) and render the page
                processing_docs = Processing.objects.all()
                return(render(request, "website/processing.html", {"processing_docs": processing_docs}))
        # if no process in being started (no files was selected in upload.html) get everything for the processing table (items being processed) and render the page
        processing_docs = Processing.objects.all()
        return(render(request, "website/processing.html", {"processing_docs": processing_docs}))

        '''if request.is_ajax():
            if len(request.FILES) != 0:
                # a file was uploaded
                file = request.FILES["records_file"].read()
                
                for enc in ["cp1252", "utf-8"]:
                    try:
                        raw_records = file.decode(enc)
                        break
                    except:
                        continue

                    return(HttpResponse(json.dumps({"status":1, "errors":["Error processing file --- Please make sure it is in proper MARC format"], "submissions":[], "total_records": 0})))

            else:
                # copy and paste
                raw_records = request.POST.get("records")

            # recaptcha_response = request.POST.get("recaptcha")
            user_ip = get_ip(request)

            # convert js true/false to python True/False
            if request.POST.get("lac") == "false":
                lac_upload = False
            else:
                lac_upload = True


            # print(recaptcha_response, raw_records, user_ip)

            # if validateRecaptcha(recaptcha_response, user_ip):
            #     # process the records
            #     processRecords(raw_records)
            #     return HttpResponse("1")
            # else:
            #     return HttpResponse("0")

            return_values = processRecords(raw_records, lac_upload)

            return(HttpResponse(json.dumps(return_values)))     # success'''
    # process a get response (currently not in use)
    if request.method == "GET":
        processing_docs = Processing.objects.all()
        return(render(request, "website/processing.html", {"processing_docs": processing_docs}))
    return HttpResponse("Server Error")


def validateRecaptcha(recaptcha_response, user_ip):
    data = {
        'secret': settings.RECAPTCHA_SECRET,
        'response': recaptcha_response,
        'remoteip': user_ip
    }

    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()

    if result['success']:
        print("Validation Successful")
        return(True)
    else:
        print(result)
        return(False)


def processRecords(raw_records, lac_upload, processing_files, num_of_rec, tps, silent_output=False):
    # try out the common encoding types
    encoding = ""
    db_update_obj = P_progress(pid=processing_files)
    db_update_obj.num_of_rec = num_of_rec
    db_update_obj.stage = "Decoding/Encoding_MARC"
    db_update_obj.save()

    for enc in ["cp1252", "utf-8"]:
        try:
            records_file = io.BytesIO(raw_records.encode(enc))
            encoding = enc
            break
        except:
            continue
        # if the program comes to this point, then the encoding was not utf-8 or cp1252
        return({"status":1, "errors":["Error processing file - Please make sure it is in proper MARC format in UTF-8 Encoding"], "submissions":[], "total_records": 0})

    try:
        # set all environment variables
        #subprocess.call(["/home/danydvd/passWords.sh"],shell=True)
        # shell=True
        # process the records
        response = process(records_file, lac_upload, db_update_obj, silent_output)
        # process end time
        tpf = T.fromtimestamp(time.time()).strftime('%H:%M:%S')
        # total process time
        process_time = Tstrptime(tpf, '%H:%M:%S') - T.strptime(tps, '%H:%M:%S')

        db_update_obj.stage = "The process was completed in %s" %(process_time)
        db_update_obj.save()
        # the the process details to archives and delete it form processing and P_progress tables
        add_to_archive(processing_files, db_update_obj, process_time)
    except Exception as e:
        # save file locally
        error_file_name = saveErrorFile(raw_records.encode(encoding), silent_output)
        # submit github issue
        python_stacktrace = traceback.format_exc()
        title = "Error Processing File"
        body = "File: " + error_file_name + "\nPython Stacktrace:\n\n" + python_stacktrace
        label = "BUG"
        submitGithubIssue(title, body, label, silent_output=False)

        # there was some type of error processing the file
        return({"status":1, "errors":["Error processing file -- Please make sure it is in proper MARC format"], "submissions":[], "total_records": 0})

    status = 1      # 1 = recaptcha successful
    errors = response[0]
    submissions = response[1]
    total_records = response[2]

    return_response = {"status":status, "errors":errors, "submissions":submissions, "total_records": total_records}

    return(return_response)

# add the recently finished process to archive and delete it from processing 
def add_to_archive(processing_files, db_update_obj, process_time):
    archive=Progress_archive(process_ID = processing_files.id,
        description=processing_files.description,
        name = processing_files.name,
        uploaded_at = processing_files.uploaded_at,
        file_format = processing_files.file_format,
        file_type = processing_files.file_type,
        start_time = processing_files.start_time,
        status = 'Completed in %s' %(process_time),
        stage = db_update_obj.stage,
        M_to_B_index = db_update_obj.M_to_B_index,
        rdf_index = db_update_obj.rdf_index,
        num_of_rec = db_update_obj.num_of_rec,
        master_file = db_update_obj.master_file)

    archive.save()
    time.sleep(10)
    processing_files.delete()

@csrf_exempt
def updateUri(request):
    if request.method == "POST":
        response = json.loads(request.body.decode('utf-8'))
        # only check for comments created/edited in an open issue
        if response["action"] == "deleted" or response["issue"]["state"] == "closed":
            return HttpResponse(1)

        issue_title = response["issue"]["title"]
        issue = response["issue"]["body"]
        issue_number = response["issue"]["number"]
        comment = response["comment"]["body"]

        if comment[0] == ">":
            # this means that the issue was generated by our program and not the person - skip it
            return HttpResponse(1)

        elif issue_title == "Missing University URL":
            # take the university name from the issue and not the comment
            # so we don't need to worry about spelling mistakes
            university_name = issue.split("The URI for **")[1].split("** could not be found")[0].strip()
            university_uri = comment.strip()
            record_file = issue.split("Record File: ")[1].strip()
            print(response)

            # check if the university uri is in the proper format
            if "http" not in university_uri or len(university_uri.split()) != 1:
                #createComment(issue_number, "> Invalid URI\n> Example: http://dbpedia.org/resource/University_of_Alberta")
                return HttpResponse(1)

            print(university_name)
            print(university_uri)
            print(record_file)

            # add the new uri to the universities.pickle file
            with open(project_folder_path + "/website/processing/files/universities.pickle", "rb") as handle:
                testing_universities = pickle.load(handle)

            testing_universities[university_name] = university_uri

            with open(project_folder_path + "/website/processing/files/universities.pickle", "wb") as handle:
                pickle.dump(testing_universities, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("Saved:", university_name, university_uri)

            # reprocess the file
            with open(project_folder_path + "/website/processing/errors/"+record_file, "rb") as error_file:
                data = error_file.read()

                for enc in ["cp1252", "utf-8"]:
                    try:
                        raw_records = data.decode(enc)
                        processRecords(raw_records, False, silent_output=True)
                        break
                    except:
                        continue
            print("fixed university")
            #createComment(issue_number, "> University has been updated in the records\n> Closing Issue")
            #closeIssue(issue_number)
            removeFile(project_folder_path + "/website/processing/errors/"+record_file)

        elif issue_title == "Missing Degree URL":

            # check if the comment is in the proper format
            if len(comment.split()) != 2 or "http" not in comment.split()[1]:
                #createComment(issue_number, "> Invalid Format\n> Example: MSc http://purl.org/ontology/bibo/degrees/ms")
                return HttpResponse(1)


            degree_name = issue.split("The URI for **")[1].split("** could not be found")[0].strip()
            degree_label, degree_uri = comment.split()
            record_file = issue.split("Record File: ")[1].strip()

            degree_name = ''.join([i for i in degree_name if i.isalpha()]).lower()
            print(degree_name)
            print(degree_uri)
            print(record_file)

            # save the new degree
            with open(project_folder_path + "/website/processing/files/degrees.pickle", "rb") as handle:
                testing_degrees = pickle.load(handle)

            if degree_name not in testing_degrees:
                testing_degrees[degree_name] = [degree_label, degree_uri]

                with open(project_folder_path + "/website/processing/files/degrees.pickle", "wb") as handle:
                    pickle.dump(testing_degrees, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    print("Saved:", degree_name, degree_uri)

            # reprocess the file
            try:
                with open(project_folder_path + "/website/processing/errors/"+record_file, "rb") as error_file:
                    data = error_file.read()

                    for enc in ["cp1252", "utf-8"]:
                        try:
                            raw_records = data.decode(enc)
                            processRecords(raw_records, False, silent_output=True)
                            break
                        except:
                            continue
            except:
                # if there is an error finding the file, that means the issue has been solved already so we can just close the issue
                pass

            print("fixed degree")
            #createComment(issue_number, "> Degree has been updated in the records\n> Closing Issue")
            #closeIssue(issue_number)
            removeFile(project_folder_path + "/website/processing/errors/"+record_file)
        return HttpResponse(1)

def createComment(issue_number, body):
    try:
        access_token = "04fb1991a3079558af49be29bd50e9bf29a07690"
        r = requests.post("https://api.github.com/repos/cldi/CanLink/issues/"+str(issue_number)+"/comments?access_token=" + access_token, json = {"body":body.strip()})

    except Exception as e:
        print("Created Comment", body)
        # print(traceback.format_exc())

def closeIssue(issue_number):
    try:
        access_token = "04fb1991a3079558af49be29bd50e9bf29a07690"
        r = requests.patch("https://api.github.com/repos/cldi/CanLink/issues/"+str(issue_number)+"?access_token=" + access_token, json = {"state":"closed"})

    except Exception as e:
        print("Closed Issue", issue_number)
        # print(traceback.format_exc())

def removeFile(file_location):
    try:
        os.remove(file_location)
        print("Removed File: ", file_location)
    except Exception as e:
        print(traceback.format_exc())
        return False
    return True