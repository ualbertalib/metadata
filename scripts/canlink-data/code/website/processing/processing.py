from pymarc import MARCReader
from fuzzywuzzy import fuzz
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
from concurrent.futures import ProcessPoolExecutor
import concurrent.futures
import urllib.request
from langdetect import detect
from io import StringIO, BytesIO
from PyPDF2.pdf import PdfFileReader
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from config import project_folder_path, log_file, query_type, apis
from website.processing.SearchAPI import APIFactory, clean_up, Results

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# necesary to find pdf links from urls with https
context = ssl._create_unverified_context()


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


class Thesis():
    def __init__(self, record, universities, university_uri_cache, subjects, csh, recon_subjects, degrees, silent_output):
        self.record = record
        self.silent_output = silent_output          # used to supress twitter and github output
        self.control = self.getControlNumber()
        self.linking = self.getLinkingControlNumber()       # some theses are split between multiple records joined with a linking number
        self.author = self.getAuthorName()
        self.title = self.getTitle()
        #if self.title in ["Literacy-related professional development preferences of secondary teachers", "Bodies, deviancy, and socio-political Change Judith Butler on intelligibility", "A profile of shared school services in Newfoundland", "Financing education in Newfoundland: 1960-61 to 1970-71", "Au bout du monde : an instructional module for imparting cultural information, with specific reference to Cape St. George, Newfoundland"] :
            #print (self.title)
        self.university = self.getUniversity()
        self.universityUri = self.getUniversityUri(universities, university_uri_cache)
        self.authorUri = self.getAuthorUri()
        self.date = self.getDate()
        self.language = self.getLanguage()
        self.abstracts = self.getAbstract()
        self.subjects = self.getSubjects()
        self.subjectUris = self.getSubjectUris(subjects, csh, recon_subjects)
        self.degree = self.getDegree()
        self.degreeLabel, self.degreeUri = self.getDegreeUri(degrees)
        self.advisors = self.getAdvisors()
        #self.advisorUris = self.getAdvisorUris()
        self.advisorUris = None  #getAdvisorUris is not functioning properly - disabling for now
        self.num_pages = None           # will be generated after the pdf files are downloaded and processed for the length
        self.contentUrl = self.getContentUrl()
        self.manifestations = self.getManifestations()    # will be generated after the pdf links are found on the website
        self.uri = self.getURI()

    def getControlNumber(self):
        try:
            value_001 = getField(self.record, "001")
            if not value_001:
                return None

            return(str(value_001).split()[1])
        except:
            PrintException()

    def getLinkingControlNumber(self):
        try:
            value_004 = getField(self.record, "004")
            if not value_004:
                return None

            return(str(value_004).split()[1])
        except:
            PrintException()


    def getAuthorName(self):
        try:
            value_100a = getField(self.record, "100", "a")
            if not value_100a:
                return None

            return(value_100a[0].strip(" .,"))
        except:
            PrintException()


    def getAuthorUri(self):
        try:
            author_uri = None
            author_uri_obj = None
            author_viaf = None
            author_lc = None
            if not self.author:
                return None

            # some records contain a URI for the author - see if that exists before generating one
            value_100zero = getField(self.record, "100", "0")
            if value_100zero:
                return(value_100zero[0])

            '''else:
                try:
                    author_url = []
                    for api in apis:
                        # getting the API method
                        author_uri_obj = APIFactory().get_API(self.author, query_type, api, log_file)
                        # if the results are not empty, append to "enriched_names" dictionary the result using the api name as key
                        if author_uri_obj:
                            author_url.append(author_uri_obj)
                    author_url = clean_up(author_url)
                    final_author = Results(author_url, 'name', log_file)
                    author_url = final_author.maximizer()
                    if len(author_url) > 0:
                        if 'VIAF' in author_url.keys():
                            author_viaf = 'http://viaf.org/viaf/' + author_url['VIAF'][0]
                        if 'LC' in author_url.keys():
                            author_lc = 'http://id.loc.gov/authorities/names/' + author_url['LC'][0].replace(" ", "").replace("|", "")
                        if author_viaf:
                            return (author_viaf)

                except:
                    print ('errors')'''

            if not self.universityUri:
                return None

            return("http://canlink.library.ualberta.ca/person/"+str(hashlib.md5(self.author.encode("utf-8")+self.universityUri[0].encode("utf-8")).hexdigest()))
        except:
            PrintException()

    def getTitle(self):
        try:
            if not self.record.title():
                return None

            return(self.record.title().strip("/. "))
        except:
            PrintException()


    def getAbstract(self):
        try:
            value_520_a = getField(self.record, "520", "a")
            if not value_520_a:
                return(None)

            return(value_520_a)
        except:
            PrintException()


    def getUniversity(self):
        try:
            university = None

            value_502c = getField(self.record, "502", "c")
            value_710a = getField(self.record, "710", "a")
            value_502a = getField(self.record, "502", "a")
            value_264b = getField(self.record, "264", "b")
            value_260b = getField(self.record, "260", "b")

            if value_502c:
                university = value_502c[0]
            elif value_710a:
                university = value_710a[0]
            elif value_502a:
                university = value_502a[0].split("thesis", 1)[-1].split("Thesis", 1)[-1].split("--", 1)[-1].split("-", 1)[-1]
            elif value_264b:
                university = value_264b[0]
            elif value_260b:
                university = value_260b[0]

            if not university:
                return None

            # remove the extra characters
            university = university.replace(".", "").replace(",", "").strip()
            university = ''.join([i for i in university if not i.isdigit()])

            return university
        except:
            PrintException()

    def getUniversityUri(self, universities, university_uri_cache):
        try:
            if not self.university:
                return None

            universityName = self.university.split("/")[0]

            # remove the special characters like accents
            universityName = unidecode.unidecode(universityName)
            # sometimes one file has all the records from one university
            # add it to the cache and see if it exists there next time instead of searching dbpedia each time
            if universityName in university_uri_cache.keys():
                return(university_uri_cache[universityName])
            else:
                universityNames = universities.keys()
                # find the closest university name in the list of names
                match = difflib.get_close_matches(universityName, universityNames, cutoff=0.8, n=1)
                if match:
                    u = universities[match[0]]

                    # add the university and the uri to the cache
                    university_uri_cache[universityName] = u
                    return u
                else:
                    for name in universityNames:
                        ratio = fuzz.token_set_ratio(universityName,name)
                        if ratio > 90:
                            u = universities[name]
                            university_uri_cache[universityName] = u
                            return u
                        else:
                            # couldn't find a match - submit an issue
                            error_file_name = saveErrorFile(self.record.as_marc(), self.silent_output)
                            title = "Missing University URL"
                            body = "The URI for **"+ self.university.strip() + "** could not be found\n\n**To fix, comment below in the following format:** \n`http://dbpedia.org/resource/WIKIPEDIA_UNIVERSITY_URI`\n\nRecord:\n" + str(self.record) + "\n\nRecord File: " + error_file_name
                            label = "Missing URL"
                            submitGithubIssue(title, body, label, self.silent_output)

                    return None
        except:
            PrintException()

    def getDate(self):
        try:
            value_260c = getField(self.record, "260", "c")
            value_264c = getField(self.record, "264", "c")
            value_008 = getField(self.record, "008")

            date = None

            if value_260c:
                date = value_260c[0]
            elif value_264c:
                date = value_264c[0]
            elif value_008 and len(str(value_008).split()[1]) >= 11 and str(value_008).split()[1][7:11].isdigit():
                date = str(value_008).split()[1][7:11]

            if not date:
                return None
            # remove all non-numeric characters
            indate = str(''.join(c for c in date if str(c).isdigit()))
            try:
                indate = int(indate)
            except:
                indate = indate
            return(indate)
        except:
            PrintException()

    def getSubjects(self):
        try:
            value_630a = getField(self.record, "630", "a")
            value_650a = getField(self.record, "650", "a")
            value_653a = getField(self.record, "653", "a")

            subjects = []

            for subject in value_630a:
                subjects.append(subject)

            for subject in value_650a:
                subjects.append(subject)

            for subject in value_653a:
                subjects.append(subject)

            if not subjects:
                return None

            return([subject.strip(".") for subject in subjects])
        except:
            PrintException()

    def getSubjectUris(self, subjects, csh, recon_subjects):
        try:
            match_subjects = ''
            match_csh = ''
            if not self.subjects:
                return None

            URIs = {} 
            #match_subjects = None
            for subj in self.subjects:
                subject = str(subj).strip(".").lower()
                if subject in recon_subjects.keys():
                    match_subjects = recon_subjects[subject]
                    print ('matched ' + subject)
                else:
                    match_subject = difflib.get_close_matches(subject, subjects.keys(), n=1, cutoff=0.90)
                    if len(match_subject) > 0:
                        match_subjects = subjects[match_subject[0]]
                match_csh = difflib.get_close_matches(subject, csh.keys(), n=1, cutoff=0.90)
                if (len(match_csh) > 0) or (len(match_subjects) > 0):
                    if len(match_subjects) > 0:
                        URIs[subject] = []
                        URIs[subject].append(match_subjects)
                    if len(match_csh) > 0:
                        if subject in URIs.keys():
                            URIs[subject].append(csh[match_csh[0]])
                        else:
                            URIs[subject] = []
                            URIs[subject].append(csh[match_csh[0]])


            '''URIs = {}       # {"subject":"URI"}
                if subject.lower() in subjects.keys():
                    # exact subject found
                    URIs[subject] = subjects[subject.lower()]
                else:
                    URIs[subject] = None'''

            return URIs
        except:
            PrintException()


    def getLanguage(self):
        try:
            value_008 = getField(self.record, "008")
            value_040b = getField(self.record, "040", "b")
            value_041a = getField(self.record, "041", "a")

            language = "eng"        # default to english

            if value_008 and len(str(value_008).split()[1]) >= 38 and str(value_008).split()[1][35:38].isalpha():
                language = str(value_008).split()[1][35:38]
            elif value_041a:
                language = value_041a[0]
            elif value_040b:
                language = value_040b[0]

            return("http://id.loc.gov/vocabulary/languages/"+language)
        except:
            PrintException()

    def getDegree(self):
        try:
            value_502a = getField(self.record, "502", "a")
            value_502b= getField(self.record, "502", "b")

            degree = None

            if value_502b:
                degree = value_502b[0]
            elif value_502a:
                degree = value_502a[0].split("--", 1)[0].split(",", 1)[0]

            if not degree:
                return None

            degree = degree.replace("Thesis", "").replace("thesis", "").replace("(", "").replace(")", "").strip()

            if degree:
                return degree
            return None
        except:
            PrintException()


    def getDegreeUri(self, degrees):
        try:
            if not self.degree:
                return([None, None])

            degree = self.degree
            # remove everything after "in" since that indicates a specialization
            if "in" in degree.split():
                degree = " ".join(degree.split()[:degree.split().index("in")])
            if "," in degree:
                degree = " ".join(degree[:degree.index(",")].split())

            # TODO TODO TODO
            # if "-" in degree:
            #     degree = " ".join(degree[:degree.index("-")])
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


            # if the program has come to this point then a degree uri was not generated
            # save the record to a error file and then submit an issue to github for a human to find the uri
            error_file_name = saveErrorFile(self.record.as_marc(), self.silent_output)
            title = "Missing Degree URL"
            body = "The URI for **"+ self.degree.strip() + "** could not be found\n\n**To fix, comment below in the following format:** \n`MSc http://purl.org/ontology/bibo/degrees/ms`\n\nRecord:\n" + str(self.record) + "\n\nRecord File: " + error_file_name
            label = "Missing URL"
            submitGithubIssue(title, body, label, self.silent_output)

            return([None, None])
        except:
            PrintException()

    def getAdvisors(self):
        try:
            value_500a = getField(self.record, "500", "a")
            value_720a= getField(self.record, "720", "a")

            if value_720a:
                return(value_720a)

            if value_500a:
                for item in value_500a:
                    if "advisor" in item.lower() or "directeur" in item.lower() and ":" in item:
                        return([advisor.strip(" .,") for advisor in item.split(":", 1)[1].split(",")])

            return None
        except:
            PrintException()

    def getAdvisorUris(self):
        try:
            uris = {}
            advisor_uri = None
            advisor_uri_obj = None
            advisor_viaf = None
            advisor_lc = None
            if not self.advisors:
                return None
            else:
                try:
                    for name in self.advisors:
                        uri = ""
                        if self.universityUri:
                            uri = "http://canlink.library.ualberta.ca/person/"+str(hashlib.md5(name.encode("utf-8")+self.universityUri.encode("utf-8")).hexdigest())
                        else:
                            uri = "http://canlink.library.ualberta.ca/person/"+str(hashlib.md5(name.encode("utf-8")).hexdigest())
                        uris[uri] = []
                        advisor_url = []
                        for api in apis:
                            # getting the API method
                            advisor_uri_obj = APIFactory().get_API(name, query_type, api, log_file)
                            # if the results are not empty, append to "enriched_names" dictionary the result using the api name as key
                            if advisor_uri_obj:
                                advisor_url.append(advisor_uri_obj)
                        advisor_url = clean_up(advisor_url)
                        final_advisor = Results(advisor_url, 'name', log_file)
                        advisor_url = final_advisor.maximizer()
                        if len(advisor_url) > 0:
                            if 'VIAF' in advisor_url.keys():
                                advisor_viaf = 'http://viaf.org/viaf/' + advisor_url['VIAF'][0]
                                uris[uri].append(advisor_viaf)
                            if 'LC' in advisor_url.keys():
                                advisor_lc = 'http://id.loc.gov/authorities/names/' + advisor_url['LC'][0].replace(" ", "").replace("|", "")
                                uris[uri].append(advisor_lc)

                except:
                    print ('errors')
            print (uris)
            return uris
        except:
            PrintException()


    def getContentUrl(self):
        try:
            value_856u = getField(self.record, "856", "u")

            if not value_856u:
                return None

            # clean up the urls
            urls = [urllib.parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]") for url in value_856u]

            return urls
        except:
            PrintException()

    def getManifestations(self):
        # returns a list of the content urls hashed and with a ualberta uri
        try:
            if not self.contentUrl:
                return None

            manifestations = []
            for url in self.contentUrl:
                if ".pdf" in url:           # non pdf manifestation will be handled by pdf_processing.py
                    manifestations.append("http://canlink.library.ualberta.ca/manifestation/"+hashlib.md5(url.encode("utf-8")).hexdigest())

            return manifestations
        except:
            PrintException()


    def getURI(self):
        try:
            if self.author and self.title:
                identifier = hashlib.md5((str(self.author).encode("utf-8") + str(self.title).encode("utf-8"))).hexdigest()
                return("http://canlink.library.ualberta.ca/thesis/"+str(identifier))
            return None
        except:
            PrintException()


    def generateRDF(self, g, runtime):
        try:
            # thesis title - don't need to check if it exists because validateRecords did that already
            g.add((URIRef(self.uri), DC.title, Literal(self.title)))
            g.add((URIRef(self.uri), PROV.wasGeneratedBy, URIRef(runtime)))
            g.add((URIRef(self.uri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
            # same as (links that are not pdf files but still contain information about this thesis)
            if self.contentUrl:
                for url in self.contentUrl:
                    if url != "":
                        g.add((URIRef(self.uri), OWL.sameAs, URIRef(url)))
            # date
            if self.date:
                g.add((URIRef(self.uri), DC.issued, Literal(self.date, datatype="http://www.w3.org/2001/XMLSchema#gYear")))
            # language
            if self.language:
                g.add((URIRef(self.uri), DC.language, URIRef(self.language)))
            # degree
            if self.degreeUri:
                g.add((URIRef(self.uri), BIBO.degree, URIRef(self.degreeUri)))
                g.add((URIRef(self.degreeUri), RDF.type, BIBO.thesisDegree))
                g.add((URIRef(self.degreeUri), RDFS.label, Literal(self.degreeLabel)))
                g.add((URIRef(self.degreeUri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
            # author uri
            if self.authorUri:
                # if the uri was provided in the record (LOC or some other), then generate a new ualberta uri
                if "canlink.library.ualberta.ca" not in self.authorUri:
                    provided_uri = self.authorUri
                    if self.author and self.universityUri:
                        self.authorUri = "http://canlink.library.ualberta.ca/person/"+str(hashlib.md5(self.author.encode("utf-8")+self.universityUri[0].encode("utf-8")).hexdigest())
                    elif self.author:
                        self.authorUri = "http://canlink.library.ualberta.ca/person/"+str(hashlib.md5(self.author.encode("utf-8")).hexdigest())
                    elif self.universityUri:
                        self.authorUri = "http://canlink.library.ualberta.ca/person/"+str(hashlib.md5(self.universityUri[0].encode("utf-8")).hexdigest())
                    g.add((URIRef(self.authorUri), OWL.sameAs, URIRef(provided_uri)))

                g.add((URIRef(self.uri), DC.creator, URIRef(self.authorUri)))
                g.add((URIRef(self.uri), REL.aut, URIRef(self.authorUri)))
                # author type
                g.add((URIRef(self.authorUri), RDF.type, FOAF.Person))
                g.add((URIRef(self.authorUri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
                g.add((URIRef(self.authorUri), PROV.wasGeneratedBy, URIRef(runtime)))
                # author name
                if "," in self.author:
                    g.add((URIRef(self.authorUri), FOAF.lastName, Literal(self.author.split(",")[0].strip())))
                    g.add((URIRef(self.authorUri), FOAF.firstName, Literal(self.author.split(",")[1].strip())))
                    # add the full name in there as well for consistency
                    g.add((URIRef(self.authorUri), FOAF.name, Literal(self.author.strip().replace(",",""))))
                else:
                    g.add((URIRef(self.authorUri), FOAF.name, Literal(self.author.strip())))

            # abstract
            if self.abstracts:
                for item in self.abstracts:
                    abstract_language = detect(item)
                    g.add((URIRef(self.uri), BIBO.abstract, Literal(item, lang=abstract_language)))
            # publisher
            if self.universityUri:
                institution = self.universityUri[0].replace('http://dbpedia.org/resource/', '')
                institutionUri = "http://canlink.library.ualberta.ca/institution/"+institution
                #print (self.universityUri, institution, institutionUri)
                g.add((URIRef(self.uri), DC.publisher, URIRef(institutionUri)))
                g.add((URIRef(institutionUri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
                g.add((URIRef(institutionUri), RDF.type, FOAF.Organization))
                g.add((URIRef(institutionUri), OWL.sameAs, URIRef(self.universityUri[0])))
                g.add((URIRef(institutionUri), OWL.sameAs, URIRef(self.universityUri[1])))
                g.add((URIRef(institutionUri), RDFS.label, Literal(institution.replace("_", " "))))
                g.add((URIRef(institutionUri), PROV.wasGeneratedBy, URIRef(runtime)))
                #g.add((URIRef(self.uri), DC.publisher, URIRef(self.universityUri)))

                g.add((URIRef(self.uri), REL.pbl, URIRef(self.universityUri[0])))
            # thesis types
            g.add((URIRef(self.uri), RDF.type, FRBR.Work))
            g.add((URIRef(self.uri), RDF.type, FRBR.Expression))
            g.add((URIRef(self.uri), RDF.type, SCHEMA.creativeWork))
            g.add((URIRef(self.uri), RDF.type, BIBO.thesis))
            g.add((URIRef(self.uri), CWRC.hasGenre, CWRC.genreScholarship))
            # advisors
            if self.advisorUris:
                for index, uri in enumerate(self.advisorUris.keys()):
                    g.add((URIRef(self.uri), REL.ths, URIRef(uri)))
                    g.add((URIRef(uri), FOAF.name, Literal(self.advisors[index])))
                    g.add((URIRef(uri), RDF.type, FOAF.Person))

                    g.add((URIRef(uri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
                    # runtime
                    g.add((URIRef(uri), PROV.wasGeneratedBy, URIRef(runtime)))
                    # add owl:sameAs
                    for recon in self.advisorUris[uri]:
                        g.add((URIRef(uri), OWL.sameAs, URIRef(recon)))
            # subjects
            if self.subjectUris:
                for subject in self.subjectUris.keys():
                    newSubjectUri = "http://canlink.library.ualberta.ca/subject/" + hashlib.md5(subject.lower().encode("utf-8")).hexdigest()
                    # check if we have the uri for it - we made a dictionary and set the value to None if we couldn't find a uri
                    if self.subjectUris[subject]:
                        if isinstance(self.subjectUris[subject], list):
                        #if self.subjectUris[subject].startswith('http://'):
                            g.add((URIRef(newSubjectUri), RDF.type, SKOS.Concept))
                            g.add((URIRef(newSubjectUri), RDFS.label, Literal(subject.lower())))
                            g.add((URIRef(newSubjectUri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
                            g.add((URIRef(self.uri), DC.subject, URIRef(newSubjectUri)))
                            g.add((URIRef(newSubjectUri), PROV.wasGeneratedBy, URIRef(runtime)))
                            for item in self.subjectUris[subject]:
                                g.add((URIRef(newSubjectUri), OWL.sameAs, URIRef(item)))
                            # old model
                            #g.add((URIRef(self.uri), DC.subject, URIRef(self.subjectUris[subject])))
                        else:
                            # the subject uri couldn't be found for this
                            
                            g.add((URIRef(newSubjectUri), RDF.type, SKOS.Concept))
                            g.add((URIRef(newSubjectUri), RDFS.label, Literal(subject.lower())))
                            g.add((URIRef(newSubjectUri), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
                            g.add((URIRef(self.uri), DC.subject, URIRef(newSubjectUri)))
                            g.add((URIRef(newSubjectUri), PROV.wasGeneratedBy, URIRef(runtime)))
            # manifestation
            if self.manifestations:
                for index, manifestation in enumerate(self.manifestations):
                    if ".pdf" not in self.contentUrl[index]: continue       # we already took care of non pdf links by using OWL:sameAs
                    g.add((URIRef(manifestation), SCHEMA.encodesCreativeWork, URIRef(self.uri)))
                    g.add((URIRef(manifestation), SCHEMA.contentUrl, URIRef(self.contentUrl[index])))
                    g.add((URIRef(manifestation), RDF.type, FRBR.Manifestation))
                    g.add((URIRef(manifestation), RDF.type, SCHEMA.MediaObject))
                    g.add((URIRef(manifestation), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))

                    # runtime
                    g.add((URIRef(manifestation), PROV.wasGeneratedBy, URIRef(runtime)))
            if self.num_pages:
                g.add((URIRef(self.uri), BIBO.numPages, Literal(str(self.num_pages))))
        except:
            PrintException()

def getField(record, tag_value, subfield_value=None):
    # tag ex: "710"
    # subfield ex: "b"
    # need this function since just doing record["710"]["b"] doesn't work if
    # there are multiple lines of the same tag
    try:
        results = []
        for field in record.get_fields(tag_value):
            if not subfield_value:
                return(field)
            for subfield in field:
                if subfield[0] == subfield_value:
                    results.append(subfield[1])

        # remove the duplicate results because sometimes they exist
        results = list(set(results))
        return(results)
    except:
            PrintException()

def mergeRecords(thesis1, thesis2):
    # takes in two theses (objects of Thesis class) and merges the information into one
    # example: if thesis1 contains the title and thesis2 contains the abstract, then the abstract will get put into thesis1
    #
    # this works as long as both theses don't contain the same field
    # for example: if thesis1 and thesis2 both contain an author, then the program only keeps the value of thesis1

    # the list of attributes that need to be merged into one object
    attributes = ["title", "author", "abstract", "university", "universityUri", "authorUri", "date", "language", "subjects", "subjectUris", "degree", "degreeUri", "advisors", "advisorUris", "contentUrl", "uri", "manifestations"]

    for attribute in attributes:
        # if thesis1 doesn't have a value for this attribute, then copy it from thesis2
        try:
            thesis1_attribute_value = getattr(thesis1, attribute)
            thesis2_attribute_value = getattr(thesis2, attribute)
        except:
            continue

        if not thesis1_attribute_value and thesis2_attribute_value:
            # copy that value to the same attribute of thesis1
            setattr(thesis1, attribute, thesis2_attribute_value)

    # generate authoruri and uri again since they depend on other values that may not have existed in the individual records before merging
    thesis1.authorUri = thesis1.getAuthorUri()
    thesis1.uri = thesis1.getURI()


def validateRecord(record, errors):
    # validation for showing the errors on the webpage - not for issues
    # example: this won't raise an error if a degree uri is not provided (it will create an issue), but it will if a degree name isn't
    record_errors = []

    # mandatory fields: author, university, title, date, degree
    if not record.title: record_errors.append("Title not found - Record not uploaded")
    if not record.author: record_errors.append("Author Name not found - Record not uploaded")
    if not record.university: record_errors.append("University not found - Record not uploaded")
    if not record.date: record_errors.append("Publication Date not found - Record not uploaded")
    if not record.degree: record_errors.append("Degree not found - Record not uploaded")

    for error in record_errors:
        errors.append("Record #" + record.control + " - " + error)

    if len(record_errors) > 0:
        return False

    return True


def sendTweet(tweet, silent_output):
    if silent_output: return None
    try:
#        api = twitter.Api(consumer_key = os.environ.get("TWITTER_CONSUMER_KEY"),
#                  consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET"),
#                  access_token_key = os.environ.get("TWITTER_ACCESS_KEY"),
#                  access_token_secret=os.environ.get("TWITTER_ACCESS_SECRET"))
        api = twitter.Api(consumer_key = "ZBKSsQBCgo4Zwzsoh7s2dRuHw",
                  consumer_secret = "XsgjTz38Vl1NbxPvSQqarq2NyY2JkGhMb7IFSQZJa7GC1tKDWr",
                  access_token_key = "887064180196388864-cyMpaw8w8gvnHUN6sKbjjzR3XBHwahH",
                  access_token_secret = "J4WRUFYnGMFvfJKRtc5th6LFkmdj26vXn6XNqtpm1ZUoj")

        status = api.PostUpdate(tweet)
        return True
    except:
        print(tweet + " (NOT SUBMITTED)")
        return False


def submitGithubIssue(title, body, label, silent_output):
    if silent_output: return None
    try:
        access_token = "04fb1991a3079558af49be29bd50e9bf29a07690"
        r = requests.post("https://api.github.com/repos/cldi/CanLink/issues?access_token=" + access_token,
                    json = {"title":title.strip(), "body":body.strip(), "labels":[label.strip()]})

    except Exception as e:
        print("Github Issue (NOT SUBMITTED)", title, body, label)


def saveErrorFile(content, silent_output):
    if silent_output: return None
    error_file_name = hashlib.md5(str(time.time() + random.randrange(10000)).encode("utf-8")).hexdigest() + ".mrc"
    with open(project_folder_path + "/website/processing/errors/"+error_file_name, "wb") as error_file:
        error_file.write(content)

    return error_file_name


# def getPDF(url, record_id, num_pages):
#
#     if ".pdf" in url:
#         if not num_pages:
#             pdf_request = requests.get(url, verify=False)
#             pdf_object = BytesIO(pdf_request.content)
#             num_pages = PdfFileReader(pdf_object).getNumPages()
#
#         return {"record_id":record_id, "pdf_url":url, "num_pages":num_pages}
#
#     # finds the pdf link on the website
#     r = requests.get(url, verify=False)
#     html = r.text
#     redirect_url = r.url
#
#     soup = BeautifulSoup(html, "html.parser")
#
#     print("ORIGINAL URL:",redirect_url)
#
#     # see if there is any ".pdf" link on the page
#     pdf_url = ""
#
#     links = []
#     for link in soup.find_all("a"):
#         l = link.get("href")
#         links.append(l)
#         if ".pdf" in str(l).lower():
#             if (pdf_url == "" or len(pdf_url) > len(str(l))):
#                 pdf_url = str(l)
#
#     # convert relative links to absolute links if necessary
#     if pdf_url and "http" not in pdf_url and "www" not in pdf_url:
#         if pdf_url[0] == "/":
#             base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urllib.request.urlparse(redirect_url))
#             pdf_url = base_url + pdf_url
#         else:
#             pdf_url = redirect_url + pdf_url
#
#     # if the ".pdf" url was found - properly format it and return
#     if pdf_url:
#         pdf_url = urllib.parse.quote(pdf_url, safe="%/:=&?~#+!$,;'@()*[]")
#         print("PDF URL:", pdf_url)
#         # return {"pdf_url":pdf_url, "record_id":record_id}
#     else:
#         # couldn't find a pdf link  - go through all the links to see which is of pdf type
#         # (not ".pdf" extension because some pdfs don't have a ".pdf" extension)
#         for link in links:
#             if link and link[0:4] == "http":
#                 r = requests.get(link, verify=False)
#                 if "pdf" in r.headers["Content-Type"]:
#                     pdf_url = urllib.parse.quote(r.url, safe="%/:=&?~#+!$,;'@()*[]")
#                     print("PDF URL:", pdf_url)
#                     # return {"pdf_url":pdf_url, "record_id":record_id}
#
#     if not num_pages and len(pdf_url) >= 10:
#         pdf_request = requests.get(pdf_url, verify=False)
#         pdf_object = BytesIO(pdf_request.content)
#         num_pages = PdfFileReader(pdf_object).getNumPages()
#         print(num_pages)
#
#     return {"record_id":record_id, "pdf_url":pdf_url, "num_pages":num_pages}


def process(records_file, lac_upload, db_update_obj, silent_output):
    # silent_output makes it so that it doesn't generate github issues or tweets
    # ex: first time a record is processed, we put all the issues on github
    # - what if there were multiple issues with one record -> it would generate the
    #   issues again after one issue was fixed since we just call the function again
    # - this would lead to many duplicate issues
    # solution: after the first processing, pass in silent_output = True to stop
    #   creating gitub isues and to stop the tweet since it was already counted in the
    #   original tweet
    try:
        start_time = datetime.datetime.now().isoformat()[:-7] + "Z"
        reader = MARCReader(records_file, force_utf8=True)

        records = {}
        errors = []
        submissions = []

        with open(project_folder_path + "/website/processing/files/universities-1.pickle", "rb") as handle:
            universities_dbpedia = pickle.load(handle)      # key: name, value: uri

        with open(project_folder_path + "/website/processing/files/subject-recon.pickle", "rb") as handle:
            recon_subjects = pickle.load(handle)

        with open(project_folder_path + "/website/processing/files/subjects.pickle", "rb") as handle:
            subjects = pickle.load(handle)      # key: subject name, value: uri

        with open(project_folder_path + "/website/processing/files/csh-1.pickle", "rb") as handle:
            csh = pickle.load(handle)      # key: subject name, value: uri

        with open(project_folder_path + "/website/processing/files/degrees.pickle", "rb") as handle:
            degrees = pickle.load(handle)
        # used to keep non-persistent memory of the universities we have processed before
        # so that we don't need to go to dbpedia every time for the same file
        university_uri_cache = {}

        g = Graph()

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
        print (start_time)
    except:
            PrintException()
    # when the control number isn't given, we use this to generate one
    count = 0
    # keep a list of the unversities seen and take the one that appears the most for the tweet
    universities = []
    # process and merge the records
    try:
        db_update_obj.stage = "Enriching_MARC_records"
        db_update_obj.save()
        for record in reader:
            print (count)
            thesis = Thesis(record, universities_dbpedia, university_uri_cache, subjects, csh, recon_subjects, degrees, silent_output)
            count += 1
            db_update_obj.M_to_B_index = count
            db_update_obj.save()
            # get control number and linking number
            controlNumber = thesis.control
            linkingNumber = thesis.linking
            # if no linking number, check if the control number shows up as a linking number of any other record -> merge
            #  them if linking number, check if the linking number shows up as a control number of any other record ->
            # merge them
            if not controlNumber:
                thesis.control = "R"+str(count)        # permanently replacing the control number with a generated one for validation purposes
                records[thesis.control] = thesis

            elif linkingNumber and linkingNumber in records.keys():
                # linking number for the current record exists and we already processed the other record that this links
                # to -> merge them into one
                rec = records[linkingNumber]        # rec = the record we are merging the current record into
                #mergeRecords(rec, thesis)

            elif not linkingNumber and controlNumber in records.keys():
                # linking number for the current record doesn't exist and we already processed the other record that this
                #  links to -> merge them into one
                rec = records[controlNumber]        # rec = the record we are merging the current record into
                #mergeRecords(rec, thesis)

            elif linkingNumber:
                # pretend the linking number is a control number when adding to dictionary because the top two statements
                # check for the control number and for the supplementary records, the control number is useless but we
                # need to merge using identical linking numbers so store the linking number for searching
                records[linkingNumber] = thesis

            elif not linkingNumber:
                records[controlNumber] = thesis

    except:
        PrintException()
    # # url_map = {"url":"record #"}
    # url_map = {}
    # # pdf_urls = {"record #":[list of pdf urls]}
    # pdf_urls = {}
    #
    # # generate url_map
    # for record_id in records:
    #     record_object = records[record_id]
    #     if not record_object.contentUrl:
    #         continue
    #     for url in record_object.contentUrl:
    #         # if ".pdf" not in url.lower():
    #         url_map[url] = record_id
    #
    #
    # # extract the pdf links from the urls in parallel
    # with ProcessPoolExecutor(max_workers=10) as executor:
    #     tasks = []
    #     for url in url_map:
    #         record_id = url_map[url]
    #         # pass in the num_pages so that if there are multiple urls given per record
    #         # it stops finding the num_pages after the first one since they will all be identical
    #         tasks.append(executor.submit(getPDF, url, record_id, num_pages=records[record_id].num_pages))
    #
    #     for future in concurrent.futures.as_completed(tasks):
    #         # runs after the task has completed
    #         try:
    #             result = future.result()
    #         except Exception as e:
    #             continue
    #
    #         record_id = result["record_id"]
    #         pdf_url = result["pdf_url"]
    #         num_pages = result["num_pages"]
    #
    #         if pdf_url != "":
    #             records[record_id].contentUrl.append(pdf_url)
    #             records[record_id].num_pages = num_pages


    # # add the pdf urls back to the records and generate the manifestations
    # for r in records.values():
    #     r.manifestations = r.getManifestations()
    runtime = "http://canlink.library.ualberta.ca/runtime/"+hashlib.md5(start_time.encode()).hexdigest()
    # this count represents the total number of records (after merging) - will be sent to the website to display at the top
    db_update_obj.stage = "Generating_RDF"
    db_update_obj.save()
    count = 0
    for thesis in records.values():
        try:
            count += 1
            db_update_obj.rdf_index = count
            db_update_obj.save()
            if validateRecord(thesis, errors):
                # if there were no errors then generate RDF
                # if silent output is true, then check if we have the degree and university uris because otherwise it is
                # an incomplete record anyway - there could be another pending issue related to this record in github that needs
                # to be solved for this action to complete
                if not silent_output or silent_output and thesis.degreeUri and thesis.universityUri:
                    thesis.generateRDF(g, runtime)
                    print (count)
                    submissions.append("Record #" + str(thesis.control) + " was uploaded successfully")
                    universities.append(thesis.university) # TODO maybe add the uri with this?
        except:
            PrintException()

    # add to the runtime info
    end_time = datetime.datetime.now().isoformat()[:-7] + "Z"
    g.add((URIRef(runtime), PROV.startedAtTime, Literal(start_time)))
    g.add((URIRef(runtime), PROV.endedAtTime, Literal(end_time)))
    g.add((URIRef(runtime), PROV.activity, CLDI.marclodconverter))
    g.add((URIRef(runtime), VOID.inDataset, URIRef("http://canlink.library.ualberta.ca/void/canlinkmaindataset")))
    g.add((URIRef(runtime), RDF.type, PROV.Activity))
    g.add((URIRef(runtime), RDF.type, PROV.Generation))

    try:
        upload_organization = unidecode.unidecode(max(set(universities), key=universities.count).strip().split("/")[0])
        upload_organization_uri = university_uri_cache[upload_organization][0]
        g.add((URIRef(runtime), PROV.actedOnBehalfOf, URIRef(upload_organization_uri)))
    except:
        pass

    try:
        revision_number = subprocess.check_output(["git","describe", "--all", "--long"]).decode("utf-8").strip()
        g.add((URIRef(runtime), DOAP.revision, Literal(revision_number)))
        g.add((URIRef(runtime), CLDI.pid, Literal(str(os.getpid()))))
    except:
        pass

    # store the successful records in /tmp and call the loadRDF script

    if len(submissions) > 0:
        db_update_obj.stage = "Loading_RDF_statements"
        db_update_obj.save()
        output_file_name = hashlib.md5(str(time.time() + random.randrange(10000)).encode("utf-8")).hexdigest() + ".xml"
        g.serialize(project_folder_path + "/website/processing/tmp/" + output_file_name, format="xml")

        db_update_obj.master_file = project_folder_path + "/website/processing/tmp/" + output_file_name
        db_update_obj.save()

        try:
            print(["."+project_folder_path+"/scripts/loadRDF.sh", project_folder_path + "/website/processing/tmp/" + output_file_name])
            subprocess.call([project_folder_path+"/scripts/loadRDF.sh", project_folder_path + "/website/processing/tmp/" + output_file_name])
        except:
            print("Calling Script Failed:")
            print(project_folder_path+'/scripts/loadRDF.sh '+output_file_name)

    # send the tweet
    if len(universities) > 0:
        if lac_upload:
            upload_organization = "Library and Archives Canada"
        else:
            # find the name of university that appears most in the file
            upload_organization = max(set(universities), key=universities.count).strip()

        tweet = upload_organization + " just added " + str(len(submissions)) + " theses to the dataset!"
        if not sendTweet(tweet, silent_output):
            print("error")

    return([errors, submissions, count])

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print("EXCEPTION IN (%s, LINE %s '%s'): %s" % (filename, lineno, line.strip(), exc_obj))