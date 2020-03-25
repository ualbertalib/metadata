from pymarc import MARCReader
import hashlib
import re
import difflib
import pickle
import unidecode
from rdflib import URIRef, Graph, Literal, Namespace
from rdflib.namespace import RDF, FOAF, DC, SKOS, RDFS, OWL
import urllib.parse
from urllib.request import urlopen, urlparse
from bs4 import BeautifulSoup
import os
import ssl
import random
import twitter
import time
import datetime
import requests
import traceback
import subprocess
# from concurrent.futures import ProcessPoolExecutor
# import concurrent.futures
import urllib.request
from langdetect import detect
from io import StringIO, BytesIO
from PyPDF2.pdf import PdfFileReader
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from website.models import P_progress
from config import project_folder_path, log_file, query_type, apis
from website.processing.SearchAPI import APIFactory, clean_up, Results

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

context = ssl._create_unverified_context()

g = Graph()     # output graph

DC = Namespace("http://purl.org/dc/terms/")
REL = Namespace("http://id.loc.gov/vocabulary/relators/")
BIBO = Namespace("http://purl.org/ontology/bibo/")
SCHEMA = Namespace("http://schema.org/")
FRBR = Namespace("http://purl.org/vocab/frbr/core#")
CWRC = Namespace("http://sparql.cwrc.ca/ontologies/genre#")
PROV = Namespace("http://www.w3.org/ns/prov#")
CLDI = Namespace("http://canlink.library.ualberta.ca/ontologies/canlink#")
DOAP = Namespace("http://usefulinc.com/ns/doap#")
VOID = Namespace("http://rdfs.org/ns/void#")
VIVO = Namespace("http://vivoweb.org/ontology/core#")

g.bind("dc", DC)
g.bind("foaf", FOAF)
g.bind("rdf", RDF)
g.bind("rel", REL)
g.bind("frbr", FRBR)
g.bind("bibo", BIBO)
g.bind("schema", SCHEMA)
g.bind("skos", SKOS)
g.bind("rdfs", RDFS)
g.bind("owl", OWL)
g.bind("cwrc", CWRC)
g.bind("prov", PROV)
g.bind("cldi", CLDI)
g.bind("doap", DOAP)
g.bind("void", VOID)
g.bind("vivo", VIVO)

with open(project_folder_path + "/website/processing/files/subjects.pickle", "rb") as handle:
    subjects = pickle.load(handle)      # key: subject name, value: uri

with open(project_folder_path + "/website/processing/files/subject-recon.pickle", "rb") as handle:
    recon_subjects = pickle.load(handle)

with open(project_folder_path + "/website/processing/files/csh-1.pickle", "rb") as handle:
    csh = pickle.load(handle)      # key: subject name, value: uri

with open(project_folder_path + "/website/processing/files/degrees.pickle", "rb") as handle:
    degrees = pickle.load(handle)

start_time = datetime.datetime.now().isoformat()[:-7] + "Z"

university_uri = "http://dbpedia.org/resource/University_of_Alberta"
institutionUri = "http://canlink.library.ualberta.ca/institution/University_of_Alberta"
institutionLabel = "University of Alberta"

def getDegreeUri(degree, degrees):
    if not degree:
        return([None, None])

    # remove everything after "in" since that indicates a specialization
    if "in" in degree.split():
        degree = " ".join(degree.split()[:degree.split().index("in")])

    if "," in degree:
        degree = " ".join(degree[:degree.index(",")].split())

    degree = ''.join([i for i in degree if i.isalpha()]).lower()
    uri = None
    label = None        # label = "MSc" for degree = "msc"

    # see if the degree exists in the degrees.pickle file - find the value that matches >90%
    match = difflib.get_close_matches(degree, degrees.keys(), n=1, cutoff=0.90)
    if match:
        return(degrees[match[0]][0], degrees[match[0]][1])

    if "master" in degree:
        return(["Master", "http://canlink.library.ualberta.ca/thesisDegree/master"])
    elif "doctor" in degree:
        return(["PhD", "http://purl.org/ontology/bibo/degrees/phd"])

    # see if it contains one of the common degree codes
    degree_codes = {
                    "maîtrise":["Master", "http://canlink.library.ualberta.ca/thesisDegree/master"],
                    "mphysed":["MPhysEd", "http://canlink.library.ualberta.ca/thesisDegree/mphysed"],
                    "menvsc":["MEnv", "http://canlink.library.ualberta.ca/thesisDegree/menv"],
                    "mdent":["MDent", "http://canlink.library.ualberta.ca/thesisDegree/mdent"],
                    "maît":["Master", "http://canlink.library.ualberta.ca/thesisDegree/master"],
                    "maed":["MAEd", "http://canlink.library.ualberta.ca/thesisDegree/maed"],
                    "meng":["MEng", "http://canlink.library.ualberta.ca/thesisDegree/meng"],
                    "mdes":["MDes", "http://canlink.library.ualberta.ca/thesisDegree/mdes"],
                    "dent":["MDent", "http://canlink.library.ualberta.ca/thesisDegree/mdent"],
                    "masc":["MASc", "http://canlink.library.ualberta.ca/thesisDegree/masc"],
                    "msc":["MSc", "http://purl.org/ontology/bibo/degrees/ms"],
                    "llm":["LLM", "http://canlink.library.ualberta.ca/thesisDegree/llm"],
                    "lld":["LLD", "http://canlink.library.ualberta.ca/thesisDegree/lld"],
                    "mws":["MWS", "http://canlink.library.ualberta.ca/thesisDegree/mws"],
                    "mhk":["MHK", "http://canlink.library.ualberta.ca/thesisDegree/mhk"],
                    "mpp":["MPP", "http://canlink.library.ualberta.ca/thesisDegree/mpp"],
                    "mba":["MBA", "http://canlink.library.ualberta.ca/thesisDegree/mba"],
                    "mfa":["MFA", "http://canlink.library.ualberta.ca/thesisDegree/mfa"],
                    "sjd":["SJD", "http://canlink.library.ualberta.ca/thesisDegree/sjd"],
                    "edd":["EDD", "http://canlink.library.ualberta.ca/thesisDegree/edd"],
                    "med":["MEd", "http://canlink.library.ualberta.ca/thesisDegree/med"],
                    "phd":["PhD", "http://purl.org/ontology/bibo/degrees/phd"],
                    "dba":["DBA", "http://canlink.library.ualberta.ca/thesisDegree/dba"],
                    "dsc":["DSc", "http://canlink.library.ualberta.ca/thesisDegree/dsc"],
                    "des":["Des", "http://canlink.library.ualberta.ca/thesisDegree/des"],
                    "msw":["MSW", "http://canlink.library.ualberta.ca/thesisDegree/msw"],
                    "ma":["MA", "http://purl.org/ontology/bibo/degrees/ma"],
                    "mn":["MN", "http://canlink.library.ualberta.ca/thesisDegree/mn"],
                    "docteur":["PhD", "http://purl.org/ontology/bibo/degrees/phd"]
    }

    for code in degree_codes:
        if code in degree:
            return(degree_codes[code][0], degree_codes[code][1])

    return([None, None])

# old version reads from folder
'''files = [i for i in os.listdir() if ".xml" in i]
count = 0
for f in files:'''
def processRDF(f, add_process, rdf_tps):
    from website.views import add_to_archive
    count = 0

    db_update_obj = P_progress(pid=add_process)
    db_update_obj.num_of_rec = 1
    db_update_obj.stage = "parsing_RDF"
    db_update_obj.save()

    input_graph = Graph()
    try:
        input_graph.parse(f, format="n3")
    except:
        input_graph.parse(f, format="xml")

    #print (input_graph)
    
    runtime = "http://canlink.library.ualberta.ca/runtime/"+hashlib.md5(start_time.encode()).hexdigest()
    g.add((URIRef(runtime), CLDI.pid, Literal(str(os.getpid()))))
    print("Start: ", f, str(count))
    count += 1


    db_update_obj.stage = "Generating_URIs_for_items_in_GRAPH"
    db_update_obj.save()
    thesis = []

    FEDORA = Namespace("info:fedora/fedora-system:def/model#")
    ns = dict(fedora=FEDORA)
    q = "SELECT DISTINCT ?item WHERE {?item ?p 'IRThesis'} limit 26000"
    for row in input_graph.query(
        q):
        thesis.append(row)
    db_update_obj.num_of_rec = len(thesis)
    db_update_obj.save()
    print (len(thesis))
    for i, row in enumerate(input_graph.query(
        q,
        initNs=ns)):

        for item in row:
            subject_uris = {}
            author = None
            author_uri = None
            author_uri_obj = None
            degree = None
            title = None
            url = None
            degree_uri = None
            degree_label = None
            contentUrl = None
            manifestation = None
            date = None
            language = None
            abstract = None
            advisor = {}
            committee = {}
            advisor_uri = None
            advisor_uri_obj = None
            committee_uri = None
            committee_uri_obj = None
            num_pages = None
            author_viaf = None
            author_lc = None
            advisor_viaf = None
            advisor_lc = None
            committee_viaf = None
            committee_lc = None
            for predicates, object in input_graph.predicate_objects(item):

                db_update_obj.rdf_index = i + 1
                db_update_obj.save()
                if str(predicates) == "http://purl.org/dc/terms/creator":
                    author = str(object.strip(",. ")) 

                elif str(predicates) == "http://id.loc.gov/vocabulary/relators/dis":
                    author = str(object.strip(",. "))

                # creator (thesis) in new ERA (Jupiter)
                elif str(predicates) == "http://terms.library.ualberta.ca/dissertant":
                    author = str(object.strip(",. "))
                    author_url = []
                    for api in apis:
                        # getting the API method
                        author_uri_obj = APIFactory().get_API(author, query_type, api, log_file)
                        # if the results are not empty, append to "enriched_names" dictionary the result using the api name as key
                        if author_uri_obj:
                            author_url.append(author_uri_obj)
                    author_url = clean_up(author_url)
                    final_author = Results(author_url, 'name', log_file)
                    author_url = final_author.maximizer()
                    if 'VIAF' in author_url.keys():
                        author_viaf = 'http://viaf.org/viaf/' + author_url['VIAF'][0]
                    if 'LC' in author_url.keys():
                        author_lc = 'http://id.loc.gov/authorities/names/' + author_url['LC'][0].replace(" ", "").replace("|", "")

                elif str(predicates) == "http://purl.org/ontology/bibo/ThesisDegree":
                    degree = str(object)

                # thesis degrees in new ERA (Jupiter)
                elif str(predicates) == "http://purl.org/ontology/bibo/degree":
                    degree = str(object)

                elif str(predicates) == "http://purl.org/dc/terms/title":
                    title = str(object.strip(",. "))

                elif str(predicates) == "http://terms.library.library.ca/identifiers/fedora3handle":
                    url = str(object)

                # Handle in new ERA (Jupiter)
                elif str(predicates) == "http://terms.library.ualberta.ca/fedora3Handle":
                    url = str(object)

                    print("Finding PDF", url, i)
                    try:
                        html_object = urlopen(url, context=context)
                        html_doc = html_object.read()
                        soup = BeautifulSoup(html_doc, "html.parser")

                        pdf_url = ""
                        # find all the .pdf links in the page
                        for link in soup.find_all("a"):
                            l = link.get("href")
                            if ".pdf" in str(l):
                                pdf_url = str(l)

                        # convert relative links to absolute links if necessary
                        if pdf_url and "http" not in pdf_url and "www" not in pdf_url:
                            redirect_url = html_object.geturl()
                            if pdf_url[0] == "/":
                                # append to the base of the redirect url
                                base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(redirect_url))
                                contentUrl = base_url + pdf_url
                            else:
                                # append to the end of the redirect url
                                contentUrl = redirect_url + pdf_url
                        if not contentUrl:
                            contentUrl = pdf_url


                        r = requests.get(contentUrl)
                        pdf_file = BytesIO(r.content)
                        num_pages = PdfFileReader(pdf_file).getNumPages()
                        # testing pdf parse
                        '''with open('test.txt', 'a') as file:
                            for i in range(1, num_pages):
                                print (i)
                                page = PdfFileReader(pdf_file).getPage(i)
                                print (page.extractText())
                                file.write(page.extractText())
                            file.close()'''

                    except Exception as e:
                        print(traceback.format_exc())
                        pass

                elif str(predicates) == "http://terms.library.ualberta.ca/graduationDate" or str(predicates) == "http://purl.org/dc/terms/dateAccepted":
                    try:
                        date = int(str(object)[:4])
                    except:
                        date = None
                        pass

                elif str(predicates) == "http://terms.library.ualberta.ca/sortYear":
                    try:
                        sdate = int(str(object)[:4])
                    except:
                        sdate = None
                        pass

                elif str(predicates) == "http://purl.org/dc/terms/language":
                    language = str(object)

                    languages = {"english":"eng", "french":"fre", "spanish":"spa"}
                    if language.lower() in languages:
                        language = "http://id.loc.gov/vocabulary/languages/" + languages[language.lower()]
                    else:
                        continue

                elif str(predicates) == "http://purl.org/dc/terms/abstract":
                    abstract = str(object)

                elif str(predicates) == "http://id.loc.gov/vocabulary/relators/ths":
                    advisor = re.sub(r'\([^)]*\)', '', str(object.strip(",. ")))

                # advisor in new ERA (Jupiter)
                elif str(predicates) == "http://terms.library.ualberta.ca/supervisor":
                    advisor_tmp = re.sub(r'\([^)]*\)', '', str(object.strip(",. "))).rstrip()
                    advisor[advisor_tmp] = {}
                    advisor_url = []
                    for api in apis:
                        # getting the API method
                        advisor_uri_obj = APIFactory().get_API(advisor_tmp, query_type, api, log_file)
                        # if the results are not empty, append to "enriched_names" dictionary the result using the api name as key
                        if advisor_uri_obj:
                            advisor_url.append(advisor_uri_obj)
                    advisor_url = clean_up(advisor_url)
                    final_advisor = Results(advisor_url, 'name', log_file)
                    advisor_url = final_advisor.maximizer()
                    if 'VIAF' in advisor_url.keys():
                        advisor_viaf = 'http://viaf.org/viaf/' + advisor_url['VIAF'][0]
                        advisor[advisor_tmp]['viaf'] = advisor_viaf
                    if 'LC' in advisor_url.keys():
                        advisor_lc = 'http://id.loc.gov/authorities/names/' + advisor_url['LC'][0].replace(" ", "").replace("|", "")
                        advisor[advisor_tmp]['lc'] = advisor_lc

                # committee member in new ERA (Jupiter)
                elif str(predicates) == "http://terms.library.ualberta.ca/commiteeMember":
                    committee_tmp = re.sub(r'\([^)]*\)', '', str(object.strip(",. "))).rstrip()
                    committee[committee_tmp] = {}
                    committee_url = []
                    for api in apis:
                        # getting the API method
                        committee_uri_obj = APIFactory().get_API(committee_tmp, query_type, api, log_file)
                        # if the results are not empty, append to "enriched_names" dictionary the result using the api name as key
                        if committee_uri_obj:
                            committee_url.append(committee_uri_obj)
                    committee_url = clean_up(committee_url)
                    final_committee = Results(committee_url, 'name', log_file)
                    committee_url = final_committee.maximizer()
                    if 'VIAF' in committee_url.keys():
                        committee_viaf = 'http://viaf.org/viaf/' + committee_url['VIAF'][0]
                        committee[committee_tmp]['viaf'] = committee_viaf
                    if 'LC' in committee_url.keys():
                        committee_lc = 'http://id.loc.gov/authorities/names/' + committee_url['LC'][0].replace(" ", "").replace("|", "")
                        committee[committee_tmp]['lc'] = committee_lc

                elif str(predicates) == "http://purl.org/dc/elements/1.1/subject":
                    match_subjects = None
                    subject = str(object).strip(".").lower()
                    if subject in recon_subjects.keys():
                        match_subjects = recon_subjects[subject]
                    else:
                        match_subject = difflib.get_close_matches(subject, subjects.keys(), n=1, cutoff=0.90)
                        if len(match_subject) > 0:
                            match_subjects = subjects[match_subject[0]]
                    match_csh = difflib.get_close_matches(subject, csh.keys(), n=1, cutoff=0.90)
                    if (len(match_csh) > 0) or (len(match_subjects) > 0):
                        if len(match_subjects) > 0:
                            subject_uris[subject] = []
                            subject_uris[subject].append(match_subjects)
                        if len(match_csh) > 0:
                            if subject in subject_uris.keys():
                                subject_uris[subject].append(csh[match_csh[0]])
                            else:
                                subject_uris[subject] = []
                                subject_uris[subject].append(csh[match_csh[0]])
                    else:
                        subject_uris[subject] = subject
                    '''if (subject.lower() in subjects.keys()) or subject.lower() in csh.keys():
                        if subject.lower() in subjects.keys():
                            print ('lc')
                            # exact subject found LCSH
                            subject_uris[subject] = []
                            subject_uris[subject].append(subjects[subject.lower()])
                            # URIs.append(subjects[subject.lower()])
                        if subject.lower() in csh.keys():
                            print ('csh')
                            # exact subject found in CSH
                            if isinstance(subject_uris[subject], list):
                                subject_uris[subject].append(csh[subject.lower()])
                            else:
                                subject_uris[subject] = []
                                subject_uris[subject].append(csh[subject.lower()])'''

            try:
                degree_label, degree_uri = getDegreeUri(degree, degrees)
            except:
                pass

            # error checking
            if not title or not language or not degree_uri or not author or not date:
                if not title:
                    print("not title")
                if not language:
                    print("not language")
                if not degree_uri:
                    print("not degree")
                if not author:
                    print("not author")
                if not date:
                    print("not date")
                print("-"*50)
                #continue

            if author:
                author_uri = "http://canlink.library.ualberta.ca/person/"+str(hashlib.md5(author.encode("utf-8")+university_uri.encode("utf-8")).hexdigest())
                if title:
                    uri = "http://canlink.library.ualberta.ca/thesis/"+str(hashlib.md5((str(author).encode("utf-8") + str(title).encode("utf-8"))).hexdigest())

            '''if len(advisor) > 0:
                for adv in advisor.keys():
                    advisor_uri = "http://canlink.library.ualberta.ca/person/"+str(hashlib.md5(adv.encode("utf-8")+university_uri.encode("utf-8")).hexdigest())
                    advisor[adv]['u'] = advisor_uri'''
            if contentUrl:
                manifestation = "http://canlink.library.ualberta.ca/manifestation/"+hashlib.md5(contentUrl.encode("utf-8")).hexdigest()

            # revision_number = subprocess.check_output(["git","describe", "--all", "--long"]).decode("utf-8").strip()
            # g.add((URIRef(runtime), DOAP.revision, Literal(revision_number)))     
            try:
                # title
                if title:
                    g.add((URIRef(uri), DC.title, Literal(title)))
                    g.add((URIRef(uri), PROV.wasGeneratedBy, URIRef(runtime)))
                    g.add((URIRef(uri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
                # sameAs for the original handle url
                if url:
                    g.add((URIRef(uri), OWL.sameAs, URIRef(url)))
                # date
                if date:
                    g.add((URIRef(uri), DC.issued, Literal(date, datatype="http://www.w3.org/2001/XMLSchema#gYear")))
                # language
                if language:
                    g.add((URIRef(uri), DC.language, URIRef(language)))
                # degree
                if degree:
                    g.add((URIRef(uri), BIBO.degree, URIRef(degree_uri)))
                    g.add((URIRef(degree_uri), RDF.type, BIBO.thesisDegree))
                    g.add((URIRef(degree_uri), RDFS.label, Literal(degree_label)))
                    g.add((URIRef(degree_uri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
                # author
                if author:
                    g.add((URIRef(uri), DC.creator, URIRef(author_uri)))
                    g.add((URIRef(uri), REL.aut, URIRef(author_uri)))
                    g.add((URIRef(author_uri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
                    g.add((URIRef(author_uri), PROV.wasGeneratedBy, URIRef(runtime)))
                    # author type
                    g.add((URIRef(author_uri), RDF.type, FOAF.Person))
                    # author name
                    g.add((URIRef(author_uri), FOAF.name, Literal(author.replace(",","").strip("., "))))
                    if author_viaf:
                        g.add((URIRef(author_uri), OWL.sameAs, URIRef(author_viaf)))
                    if author_lc:
                        g.add((URIRef(author_uri), OWL.sameAs, URIRef(author_lc)))
                    if "," in author and len(author.split(" ")) <= 3:
                        g.add((URIRef(author_uri), FOAF.lastName, Literal(author.split(",")[0].strip("., "))))
                        g.add((URIRef(author_uri), FOAF.firstName, Literal(author.split(",")[1].strip("., "))))


                # abstract
                if abstract:
                    abstract_language = detect(abstract)
                    g.add((URIRef(uri), BIBO.abstract, Literal(abstract, lang=abstract_language)))
                # publisher
                g.add((URIRef(uri), DC.publisher, URIRef(institutionUri)))
                g.add((URIRef(institutionUri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
                g.add((URIRef(institutionUri), OWL.sameAs, URIRef(university_uri)))
                g.add((URIRef(institutionUri), RDF.type, FOAF.Organization))
                g.add((URIRef(institutionUri), RDFS.label, Literal(institutionLabel)))
                g.add((URIRef(institutionUri), PROV.wasGeneratedBy, URIRef(runtime)))
                # old model (dbpedia link)
                #g.add((URIRef(uri), DC.publisher, URIRef(university_uri)))
                g.add((URIRef(uri), REL.pbl, URIRef(university_uri)))
                # thesis types
                g.add((URIRef(uri), RDF.type, FRBR.Work))
                g.add((URIRef(uri), RDF.type, FRBR.Expression))
                g.add((URIRef(uri), RDF.type, SCHEMA.creativeWork))
                g.add((URIRef(uri), RDF.type, BIBO.thesis))
                g.add((URIRef(uri), CWRC.hasGenre, CWRC.genreScholarship))
                # advisor uri
                if len(advisor) > 0:
                    for adv in advisor.keys():
                        advisor_uri = "http://canlink.library.ualberta.ca/person/"+str(hashlib.md5(adv.encode("utf-8")+university_uri.encode("utf-8")).hexdigest())
                        g.add((URIRef(uri), REL.ths, URIRef(advisor_uri)))
                        g.add((URIRef(advisor_uri), FOAF.name, Literal(adv.strip())))
                        g.add((URIRef(advisor_uri), RDF.type, FOAF.Person))
                        g.add((URIRef(advisor_uri), PROV.wasGeneratedBy, URIRef(runtime)))
                        g.add((URIRef(advisor_uri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
                        if "," in adv and len(adv.split(" ")) <= 3:
                            g.add((URIRef(advisor_uri), FOAF.lastName, Literal(adv.split(",")[0].strip("., "))))
                            g.add((URIRef(advisor_uri), FOAF.firstName, Literal(adv.split(",")[1].strip("., "))))
                        if 'viaf' in advisor[adv].keys():
                            g.add((URIRef(advisor_uri), OWL.sameAs, URIRef(advisor[adv]['viaf'])))
                        if 'lc' in advisor[adv].keys():
                            g.add((URIRef(advisor_uri), OWL.sameAs, URIRef(advisor[adv]['lc'])))
                # committee uri
                if len(committee) > 0:
                    committe_obj_uri = "http://canlink.library.ualberta.ca/committee/"+str(hashlib.md5(title.encode("utf-8")+university_uri.encode("utf-8")).hexdigest())
                    g.add((URIRef(uri), VIVO.committee, URIRef(committe_obj_uri)))
                    g.add((URIRef(committe_obj_uri), RDF.type, FOAF.Group))
                    g.add((URIRef(committe_obj_uri), PROV.wasGeneratedBy, URIRef(runtime)))
                    g.add((URIRef(committe_obj_uri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
                    for comm in committee.keys():
                        committee_uri = "http://canlink.library.ualberta.ca/person/"+str(hashlib.md5(comm.encode("utf-8")+university_uri.encode("utf-8")).hexdigest())
                        g.add((URIRef(committe_obj_uri), FOAF.member, URIRef(committee_uri)))
                        g.add((URIRef(committee_uri), FOAF.name, Literal(comm.strip())))
                        g.add((URIRef(committee_uri), RDF.type, FOAF.Person))
                        g.add((URIRef(committee_uri), PROV.wasGeneratedBy, URIRef(runtime)))
                        g.add((URIRef(committee_uri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
                        if "," in comm and len(comm.split(" ")) <= 3:
                            g.add((URIRef(committee_uri), FOAF.lastName, Literal(comm.split(",")[0].strip("., "))))
                            g.add((URIRef(committee_uri), FOAF.firstName, Literal(comm.split(",")[1].strip("., "))))
                        if 'viaf' in committee[comm].keys():
                            g.add((URIRef(committee_uri), OWL.sameAs, URIRef(committee[comm]['viaf'])))
                        if 'lc' in committee[comm].keys():
                            g.add((URIRef(committee_uri), OWL.sameAs, URIRef(committee[comm]['lc'])))
                # subjects
                if subject_uris:
                    for subject in subject_uris.keys():
                        # check if we have the uri for it - we made a dictionary and set the value to None if we couldn't find a uri
                        # the subject uri couldn't be found for this
                        newSubjectUri = "http://canlink.library.ualberta.ca/subject/" + hashlib.md5(subject.lower().encode("utf-8")).hexdigest()
                        if subject_uris[subject]:
                            #if subject_uris[subject].startswith('http://'):
                            if isinstance(subject_uris[subject], list):
                                #g.add((URIRef(uri), DC.subject, URIRef(subject_uris[subject])))
                                g.add((URIRef(uri), DC.subject, URIRef(newSubjectUri)))
                                g.add((URIRef(newSubjectUri), RDF.type, SKOS.Concept))
                                g.add((URIRef(newSubjectUri), RDFS.label, Literal(subject.lower())))
                                g.add((URIRef(newSubjectUri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
                                g.add((URIRef(newSubjectUri), PROV.wasGeneratedBy, URIRef(runtime)))
                                for item in subject_uris[subject]:
                                    g.add((URIRef(newSubjectUri), OWL.sameAs, URIRef(item)))
                                #this is when CSH subject are also added and the item is a list
                                #this part does not work -- TODO
                                '''if len(subjectUris[subject]) > 1:
                                    g.add((URIRef(newSubjectUri), OWL.sameAs, URIRef(subjectUris[subject][1])))'''
                                #g.add((URIRef(newSubjectUri), OWL.sameAs, URIRef(subject_uris[subject])))
                            else:
                                g.add((URIRef(newSubjectUri), RDF.type, SKOS.Concept))
                                g.add((URIRef(newSubjectUri), RDFS.label, Literal(subject.lower())))
                                g.add((URIRef(uri), DC.subject, URIRef(newSubjectUri)))

                                g.add((URIRef(newSubjectUri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
                                g.add((URIRef(newSubjectUri), PROV.wasGeneratedBy, URIRef(runtime)))
                # manifestation
                if manifestation:
                    g.add((URIRef(manifestation), SCHEMA.encodesCreativeWork, URIRef(uri)))
                    if contentUrl:
                        g.add((URIRef(manifestation), SCHEMA.contentUrl, URIRef(contentUrl)))
                    g.add((URIRef(manifestation), RDF.type, FRBR.Manifestation))
                    g.add((URIRef(manifestation), RDF.type, SCHEMA.MediaObject))
                    g.add((URIRef(manifestation), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))

                if num_pages:
                    g.add((URIRef(uri), BIBO.numPages, Literal(str(num_pages))))
            except:
                pass

    db_update_obj.stage = "adding_URIs_to_GRAPH"
    db_update_obj.save()

    end_time = datetime.datetime.now().isoformat()[:-7] + "Z"
    g.add((URIRef(runtime), PROV.startedAtTime, Literal(start_time)))
    g.add((URIRef(runtime), PROV.endedAtTime, Literal(end_time)))
    g.add((URIRef(runtime), PROV.activity, CLDI.marclodconverter))
    g.add((URIRef(runtime), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
    g.add((URIRef(runtime), RDF.type, PROV.Activity))
    g.add((URIRef(runtime), RDF.type, PROV.Generation))
    g.add((URIRef(runtime), PROV.actedOnBehalfOf, URIRef(university_uri)))


    if len(g) > 0:
        db_update_obj.stage = "Writing_to_File"
        db_update_obj.save()
        output_file_name = hashlib.md5(str(time.time() + random.randrange(10000)).encode("utf-8")).hexdigest() + ".xml"
        g.serialize(project_folder_path + "/website/processing/tmp/" + output_file_name, format="xml")

        db_update_obj.stage = "Loading_RDF_statements"
        db_update_obj.save()

        try:
            print(["."+project_folder_path+"/scripts/loadRDF.sh", project_folder_path + "/website/processing/tmp/" + output_file_name])
            subprocess.call([project_folder_path+"/scripts/loadRDF.sh", project_folder_path + "/website/processing/tmp/" + output_file_name])
        except:
            print("Calling Script Failed:")
            print(project_folder_path+'/scripts/loadRDF.sh '+output_file_name)

        # send the tweet
        #tweet = "University of Alberta just added " + str(len(submissions)) + " theses to the dataset!"
        #if not sendTweet(tweet, silent_output):
         #   print("error")

    # process end time
    rdf_tpf = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    # total process time
    process_time = datetime.datetime.strptime(rdf_tpf, '%H:%M:%S') - datetime.datetime.strptime(rdf_tps, '%H:%M:%S')

    db_update_obj.stage = "The process was completed in %s" %(process_time)
    db_update_obj.save()

    # adding the process to processing archive
    add_to_archive(add_process, db_update_obj, process_time)

    print("Done: ", f)
    print("-"*50)