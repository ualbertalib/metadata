# this script will find all the theses in the triplestore and find the PDF links and the length of the PDF
from SPARQLWrapper import SPARQLWrapper, JSON, DIGEST
from collections import defaultdict
import requests
import hashlib
from bs4 import BeautifulSoup
import ssl
from io import StringIO, BytesIO
from PyPDF2.pdf import PdfFileReader
import urllib.parse
from urllib.request import urlopen, urlparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

context = ssl._create_unverified_context()

def getPDFUrl(url):
    r = requests.get(url, verify=False)
    html = r.text
    redirect_url = r.url

    soup = BeautifulSoup(html, "html.parser")

    pdf_url = ""
    links = []

    for link in soup.find_all("a"):
        l = link.get("href")
        links.append(l)
        if ".pdf" in str(l).lower():
            if (pdf_url == "" or len(pdf_url) > len(str(l))):
                pdf_url = str(l)

    # convert relative links to absolute links if necessary
    if pdf_url and "http" not in pdf_url and "www" not in pdf_url:
        if pdf_url[0] == "/":
            base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urllib.request.urlparse(redirect_url))
            pdf_url = base_url + pdf_url
        else:
            pdf_url = redirect_url + pdf_url

    # if the ".pdf" url was found - properly format it and return
    if pdf_url:
        pdf_url = urllib.parse.quote(pdf_url, safe="%/:=&?~#+!$,;'@()*[]")
        return(pdf_url)
    else:
        # couldn't find a pdf link  - go through all the links to see which is of pdf type
        # (not ".pdf" extension - those would already be found by now if they existed on the page)
        for link in links:
            if link and link[0:4] == "http":
                r = requests.get(link, verify=False)
                if "pdf" in r.headers["Content-Type"]:
                    pdf_url = urllib.parse.quote(r.url, safe="%/:=&?~#+!$,;'@()*[]")
                    return(pdf_url)

def getNumPages(url):
    try:
        pdf_request = requests.get(pdf_url, verify=False)
        pdf_object = BytesIO(pdf_request.content)
        num_pages = PdfFileReader(pdf_object).getNumPages()
        return(num_pages)
    except:
        pass

def addManifestation(thesis_uri, url, runtime):
    # generate the manifestation uri
    manifestation = "http://canlink.library.ualberta.ca/manifestation/"+hashlib.md5(url.encode("utf-8")).hexdigest()

    sparql = SPARQLWrapper("http://206.167.181.124:7200/repositories/cldi-test/statements")
    #sparql.setHTTPAuth(DIGEST)
    sparql.setCredentials("admin", "4Metadata!")

    sparql.setQuery("""
    PREFIX void:  <http://rdfs.org/ns/void#>
    PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX doap:  <http://usefulinc.com/ns/doap#>
    PREFIX owl:   <http://www.w3.org/2002/07/owl#>
    PREFIX rel:   <http://id.loc.gov/vocabulary/relators/>
    PREFIX bibo:  <http://purl.org/ontology/bibo/>
    PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX cwrc:  <http://sparql.cwrc.ca/ontologies/genre#>
    PREFIX prov:  <http://www.w3.org/ns/prov#>
    PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
    PREFIX dc:    <http://purl.org/dc/terms/>
    PREFIX schema: <http://schema.org/>
    PREFIX frbr: <http://purl.org/vocab/frbr/core#>

    INSERT DATA{
  <%s>    schema:encodesCreativeWork    <%s>  .
  <%s>    schema:contentUrl    <%s>  .
  <%s>    prov:wasGeneratedBy <%s> .
  <%s>    void:inDataset   <http://canlink.library.ualberta.ca/void/canlinkmaindataset>  .
  <%s>    rdf:type   frbr:Manifestation .
  <%s>    rdf:type   schema:MediaObject .

}
    """%(manifestation, thesis_uri, manifestation, url, manifestation, runtime, manifestation, manifestation, manifestation))

    sparql.method = "POST"
    sparql.query()

    print("Adding Manifestation for:", thesis_uri, "with content url =", url)


def addNumPages(thesis_uri, num_pages):
    sparql = SPARQLWrapper("http://206.167.181.124:7200/repositories/cldi-test/statements")
    #sparql.setHTTPAuth(DIGEST)
    sparql.setCredentials("admin", "4Metadata!")

    sparql.setQuery("""
    PREFIX void:  <http://rdfs.org/ns/void#>
    PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX doap:  <http://usefulinc.com/ns/doap#>
    PREFIX owl:   <http://www.w3.org/2002/07/owl#>
    PREFIX rel:   <http://id.loc.gov/vocabulary/relators/>
    PREFIX bibo:  <http://purl.org/ontology/bibo/>
    PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX cwrc:  <http://sparql.cwrc.ca/ontologies/genre#>
    PREFIX prov:  <http://www.w3.org/ns/prov#>
    PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
    PREFIX dc:    <http://purl.org/dc/terms/>
    PREFIX schema: <http://schema.org/>
    PREFIX frbr: <http://purl.org/vocab/frbr/core#>

    INSERT DATA{
	<%s> bibo:numPages "%s"
    }
    """%(thesis_uri, num_pages))

    sparql.method = "POST"
    sparql.query()

    print("Adding Num Pages for:", thesis_uri, "with pages =", num_pages)


sparql = SPARQLWrapper("http://206.167.181.124:7200/repositories/cldi-test")
sparql.setCredentials("admin", "4Metadata!")

sparql.setQuery("""
PREFIX void:  <http://rdfs.org/ns/void#>
PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX doap:  <http://usefulinc.com/ns/doap#>
PREFIX owl:   <http://www.w3.org/2002/07/owl#>
PREFIX rel:   <http://id.loc.gov/vocabulary/relators/>
PREFIX bibo:  <http://purl.org/ontology/bibo/>
PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
PREFIX cwrc:  <http://sparql.cwrc.ca/ontologies/genre#>
PREFIX prov:  <http://www.w3.org/ns/prov#>
PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
PREFIX dc:    <http://purl.org/dc/terms/>
PREFIX schema: <http://schema.org/>
PREFIX frbr: <http://purl.org/vocab/frbr/core#>

SELECT ?thesis ?url ?runtime
WHERE {
	?thesis rdf:type bibo:thesis .
    ?thesis owl:sameAs ?url .
    ?thesis prov:wasGeneratedBy ?runtime .
    MINUS { ?thesis bibo:numPages ?c . }
}
""")

# run the query and put the results in a dictionary with the values being a list of urls associated with the thesis uri
data = defaultdict(list)
runtimes = {}

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for thesis in results["results"]["bindings"]:
    thesis_uri = thesis["thesis"]["value"]
    url = thesis["url"]["value"]
    runtime = thesis["runtime"]["value"]

    data[thesis_uri].append(url)
    runtimes[thesis_uri] = runtime

# process each thesis individually
for thesis_uri in data:
    urls = data[thesis_uri]

    num_pages = 0
    # go through all the urls and find the pdf links for all of them
    # find the num_pages from one of the urls (they should all be the same length so don't need to check all of them)
    print("-"*50)
    for i, url in enumerate(urls):
        if ".pdf" not in url.lower():
            pdf_url = getPDFUrl(url)

            if pdf_url:
                addManifestation(thesis_uri, pdf_url, runtimes[thesis_uri])
        else:
            pdf_url = url

        if pdf_url and num_pages == 0:
            num_pages = getNumPages(url)
            if num_pages != None:
                addNumPages(thesis_uri, num_pages)

        #elif urls.index(url) == len(urls)-1:
        elif i == len(urls)-1 and (num_pages == 0 or num_pages == None):
            # if this is the last url given for this thesis and we still don't have a num_pages
            # then put in numPages = N/A
            # if we don't do this, this record will come up again everytime this function is called
            # and it won't be able to find the number of pages ever due to a broken link

            addNumPages(thesis_uri, num_pages="N/A")
