from rdflib import URIRef, Graph, Literal, Namespace
from rdflib.namespace import RDF, FOAF, DC, SKOS, RDFS, OWL
import urllib.parse
import re
from urllib.request import urlopen, urlparse
from bs4 import BeautifulSoup
import ssl
import pickle
import hashlib
import unidecode
import difflib
import sys
import os
import csv
import datetime
import urllib.request
from langdetect import detect
from io import StringIO, BytesIO
from PyPDF2.pdf import PdfFileReader
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
context = ssl._create_unverified_context()
input_graph = Graph()
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

with open("files/subjects.pickle", "rb") as handle:
    subjects = pickle.load(handle)


def getDegreeUri(degree):
    if not degree:
        return None

    if "in" in degree.split():
        degree = " ".join(degree.split()[:degree.split().index("in")])

    if "," in degree:
        degree = " ".join(degree[:degree.index(",")].split())

    if "-" in degree:
        degree = " ".join(degree[:degree.index("-")])

    degree = ''.join([i for i in degree if i.isalpha()]).lower()
    uri = None
    label = None        # label = MSc for degree = msc

    # check for longer sentences if the keywords aren't available
    degrees = {"masterofscience": ["MSc", "http://purl.org/ontology/bibo/degrees/ms"],
               "masterofarts": ["MA", "http://purl.org/ontology/bibo/degrees/ma"],
               "masteroffinearts": ["MFA", "http://canlink.library.ualberta.ca/thesisDegree/mfa"],
               "masterofappliedscience": ["MASc", "http://canlink.library.ualberta.ca/thesisDegree/masc"],
               "masteroflaws": ["LLM", "http://canlink.library.ualberta.ca/thesisDegree/llm"],
               "masterofenvironmentalstudies": ["MEnv", "http://canlink.library.ualberta.ca/thesisDegree/menv"],
               "masterofeducation": ["MEd", "http://canlink.library.ualberta.ca/thesisDegree/med"],
               "masterofnursing": ["MN", "http://canlink.library.ualberta.ca/thesisDegree/mn"],
               "masterofarchitecture": ["MArch", "http://canlink.library.ualberta.ca/thesisDegree/march"],
               "masterofmathematics": ["MMath", "http://canlink.library.ualberta.ca/thesisDegree/mmath"],
               "masterofhealthstudies": ["MHStud", "http://canlink.library.ualberta.ca/thesisDegree/mhstud"],
               "masterofcounselling": ["MCoun", "http://canlink.library.ualberta.ca/thesisDegree/mcoun"],
               "masterofengineering": ["MEng", "http://canlink.library.ualberta.ca/thesisDegree/meng"],
               "masterofadvancedstudies": ["MAS", "http://canlink.library.ualberta.ca/thesisDegree/mas"],
               "masterofphysicaleducation": ["MPhysEd", "http://canlink.library.ualberta.ca/thesisDegree/mphysed"],
               "masterofbusinessadministration": ["MBA", "http://canlink.library.ualberta.ca/thesisDegree/mba"],
               "masterofworshipstudies": ["MWS", "http://canlink.library.ualberta.ca/thesisDegree/mws"],
               "doctorofphilosophy": ["PhD", "http://purl.org/ontology/bibo/degrees/phd"],
               "doctoralthesis": ["PhD", "http://purl.org/ontology/bibo/degrees/phd"],
               "doctorofbusinessadministration": ["DBA", "http://canlink.library.ualberta.ca/thesisDegree/dba"],
               "doctorofscience": ["PhD", "http://purl.org/ontology/bibo/degrees/phd"],
               "doctor": ["PhD", "http://purl.org/ontology/bibo/degrees/phd"]}


    if "master" in degree or "doctor" in degree:
        match = difflib.get_close_matches(
            degree, degrees.keys(), n=1, cutoff=0.90)
        if match:
            return(degrees[match[0]][0], degrees[match[0]][1])

        # # NOTE modification just for this dataset
        # if "-" in degree:
        #     label = degree.split("-")[1]
        #     return([label, "http://canlink.library.ualberta.ca/thesisDegree/"+label.lower()])
        # # TODO IMPLEMENT A USER INPUT FOR THE DEGREES THAT CAN'T BE FOUND (MUSIC)
        #
        # return([input("Enter Label for " + degree + ": "), "http://canlink.library.ualberta.ca/thesisDegree/"+input("Enter Code for " + degree + ": ")])

        if "master" in degree:
            return(["Master", "http://canlink.library.ualberta.ca/thesisDegree/master"])
        return(["PhD", "http://canlink.library.ualberta.ca/thesisDegree/phd"])

    # do the basic ones
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


def getPDFUrl(url):
    try:
        html_object = urlopen(url, context=context)
        html_doc = html_object.read()
        soup = BeautifulSoup(html_doc, "html.parser")

        pdf_url = ""
        # find all the .pdf links in the page
        for link in soup.find_all("a"):
            l = link.get("href")
            if "pdf" in str(l):
                pdf_url = str(l)

        contentUrl = pdf_url
        # convert relative links to absolute links if necessary
        if pdf_url and "http" not in pdf_url and "www" not in pdf_url:
            redirect_url = html_object.geturl()
            if pdf_url[0] == "/":
                # append to the base of the redirect url
                base_url = '{uri.scheme}://{uri.netloc}'.format(
                    uri=urlparse(redirect_url))
                contentUrl = base_url + pdf_url
            else:
                # append to the end of the redirect url
                contentUrl = redirect_url + pdf_url

        return contentUrl
    except:
        return None


start_time = datetime.datetime.now().isoformat()[:-7] + "Z"
runtime = "http://canlink.library.ualberta.ca/runtime/"+hashlib.md5(start_time.encode()).hexdigest()

reader = csv.reader(open("files/ubc.csv", "r", encoding="latin-1"))
next(reader)        # skip the title
for row in reader:
    subject_uris = {}
    author = None
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
    advisor = None
    num_pages = None


    author = max(row[0], row[1])
    try:
        date = int(row[2])
    except:
        date = None

    degree = row[3]

    # if the abstract isn't available then message goes in [ ]
    if row[4] and row[4][0] != "[" and row[4][-1] != "]" and len(row[4]) > 30:
        abstract = row[4].replace("\n", "")
    else:
        abstract = None
    url = row[5]
    contentUrl = getPDFUrl(url)

    try:
        r = requests.get(contentUrl)
        f = BytesIO(r.content)
        num_pages = PdfFileReader(f).getNumPages()
        print(num_pages)
    except:
        pass


    if row[6]:
        language = "http://id.loc.gov/vocabulary/languages/" + row[6]

    subject_names = [i for i in row[7].split("||")+row[8].split("||") if i]
    subject_uris = {}
    for subject in subject_names:
        if subject.lower() in subjects.keys():
            subject_uris[subject] = subjects[subject.lower()]
        else:
            subject_uris[subject] = None

    title = row[9]

    author_uri = row[10]
    if not author_uri and row[11]: author_uri = row[11]
    if not author_uri and row[12]: author_uri = row[12]

    university_uri = "http://dbpedia.org/resource/University_of_British_Columbia"


    if not title or not language or not degree or not author or not date:
        print("ERROR\n\n\n\n\n")


    uri = "http://canlink.library.ualberta.ca/thesis/"+str(hashlib.md5((str(author).encode("utf-8") + str(title).encode("utf-8"))).hexdigest())

    if contentUrl:
        manifestation = "http://canlink.library.ualberta.ca/manifestation/"+hashlib.md5(contentUrl.encode("utf-8")).hexdigest()
    else:
        print(contentUrl, "\n\n")
    degree_label, degree_uri = getDegreeUri(degree)


    print("-"*50)
    print("Author:", author)
    print("Date:", date)
    print("Degree:", degree)
    print("URL:", url)
    print("Content Url:", contentUrl)
    print("Language:", language)
    print("Subjects:", subject_names)
    print("Subjects Uris:", subject_uris)
    print("Title:", title)
    print("Author_uri:", author_uri)
    print("University:", university_uri)
    print("Manifestation:", manifestation)

    # title
    g.add((URIRef(uri), DC.title, Literal(title)))
    g.add((URIRef(uri), PROV.wasGeneratedBy, URIRef(runtime)))
    g.add((URIRef(uri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
    # sameAs for the original handle url
    if url:
        g.add((URIRef(uri), OWL.sameAs, URIRef(url)))
    # date
    g.add((URIRef(uri), DC.issued, Literal(date, datatype="http://www.w3.org/2001/XMLSchema#gYear")))
    # language
    g.add((URIRef(uri), DC.language, URIRef(language)))
    # degree
    g.add((URIRef(uri), BIBO.degree, URIRef(degree_uri)))
    g.add((URIRef(degree_uri), RDF.type, BIBO.thesisDegree))
    g.add((URIRef(degree_uri), RDFS.label, Literal(degree_label)))
    g.add((URIRef(degree_uri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))

    if "canlink.library.ualberta.ca" not in author_uri:
        provided_uri = author_uri
        author_uri = "http://canlink.library.ualberta.ca/person/"+str(hashlib.md5(author.encode("utf-8")+university_uri.encode("utf-8")).hexdigest())
        g.add((URIRef(author_uri), OWL.sameAs, URIRef(provided_uri)))

    g.add((URIRef(uri), DC.creator, URIRef(author_uri)))
    g.add((URIRef(uri), REL.aut, URIRef(author_uri)))
    # author type
    g.add((URIRef(author_uri), RDF.type, FOAF.Person))
    g.add((URIRef(author_uri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
    g.add((URIRef(author_uri), PROV.wasGeneratedBy, URIRef(runtime)))
    # author name
    if "," in author:
        g.add((URIRef(author_uri), FOAF.lastName, Literal(author.split(",")[0].strip())))
        g.add((URIRef(author_uri), FOAF.firstName, Literal(author.split(",")[1].strip())))
        # add the full name in there as well for consistency
        g.add((URIRef(author_uri), FOAF.name, Literal(author.strip().replace(",",""))))
    else:
        g.add((URIRef(author_uri), FOAF.name, Literal(author.strip())))

    # abstract
    if abstract:
        abstract_language = detect(abstract)
        g.add((URIRef(uri), BIBO.abstract, Literal(abstract, lang=abstract_language)))
    # publisher
    g.add((URIRef(uri), DC.publisher, URIRef(university_uri)))
    g.add((URIRef(uri), REL.pub, URIRef(university_uri)))
    # thesis types
    g.add((URIRef(uri), RDF.type, FRBR.Work))
    g.add((URIRef(uri), RDF.type, FRBR.Expression))
    g.add((URIRef(uri), RDF.type, SCHEMA.creativeWork))
    g.add((URIRef(uri), RDF.type, BIBO.thesis))
    g.add((URIRef(uri), CWRC.hasGenre, CWRC.genreScholarship))
    # subjects
    if subject_uris:
        for subject in subject_uris:
            # check if we have the uri for it - we made a dictionary and set the value to None if we couldn't find a uri
            if subject_uris[subject]:
                g.add((URIRef(uri), DC.subject, URIRef(subject_uris[subject])))
            else:
                # the subject uri couldn't be found for this
                newSubjectUri = "http://canlink.library.ualberta.ca/subject/" + hashlib.md5(subject.lower().encode("utf-8")).hexdigest()

                g.add((URIRef(newSubjectUri), RDF.type, SKOS.Concept))
                g.add((URIRef(newSubjectUri), RDFS.label, Literal(subject.lower())))
                g.add((URIRef(newSubjectUri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
                g.add((URIRef(uri), DC.subject, URIRef(newSubjectUri)))
                g.add((URIRef(newSubjectUri), PROV.wasGeneratedBy, URIRef(runtime)))
    # manifestation
    if manifestation:
        g.add((URIRef(manifestation), SCHEMA.encodesCreativeWork, URIRef(uri)))
        if contentUrl:
            g.add((URIRef(manifestation), SCHEMA.contentUrl, URIRef(contentUrl)))
        g.add((URIRef(manifestation), RDF.type, FRBR.Manifestation))
        g.add((URIRef(manifestation), RDF.type, SCHEMA.MediaObject))
        g.add((URIRef(manifestation), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
        g.add((URIRef(manifestation), PROV.wasGeneratedBy, URIRef(runtime)))

    if num_pages:
        g.add((URIRef(uri), BIBO.numPages, Literal(str(num_pages))))

end_time = datetime.datetime.now().isoformat()[:-7] + "Z"
g.add((URIRef(runtime), PROV.startedAtTime, Literal(start_time)))
g.add((URIRef(runtime), PROV.endedAtTime, Literal(end_time)))
g.add((URIRef(runtime), PROV.activity, CLDI.marclodconverter))
g.add((URIRef(runtime), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
g.add((URIRef(runtime), RDF.type, PROV.Activity))
g.add((URIRef(runtime), RDF.type, PROV.Generation))
g.add((URIRef(runtime), PROV.actedOnBehalfOf, URIRef("http://canlink.library.ualberta.ca/ontologies/canlink#MaharshPatel")))


print(g.serialize(format="xml").decode("utf-8"))
g.serialize("ubc.xml", format="xml")
    # print("Abstract: ", abstract)
