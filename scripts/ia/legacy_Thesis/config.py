import sys
import linecache

degree_level = [{'useForm': "Bachelor of Science",
	'mapping': ['B. Sc.', 'B.Sc.', 'BSc.', 'B.S.', 'BS']},
	{'useForm': "Bachelor of Education",
	'mapping': ['B. Ed.', 'B.Ed.', 'BEd.']},
	{'useForm': "Master of Science",
	'mapping': ['M. Sc.', 'M.Sc.', 'MSc.', 'M.S.']},
	{'useForm': "Master of Arts",
	'mapping': ['M. A.', 'M.A.', 'MA.', 'M.A']},
	{'useForm': "Doctoral of Philosophy",
	'mapping': ["Doctoral", "Ph.D.", "Ph. D.", "PhD"]}]

thesisLevel = [{"uri": "http://purl.org/spar/fabio/BachelorsThesis",
	"mapping": ["B.Ed.", "B. Ed.", "B. Div.", "B.Div.", "B.D."],
	"useForm": "Bachelor"},
	{"uri": "http://purl.org/spar/fabio/MastersThesis",
	"mapping": ["Master's", 'Master', 'M. Sc.', 'M.Ed.', 'M.A.', 'M.Sc.', 'M.A', 'M.Sc. ', 'M. Ed.', 'MSc.', 'M.S. ', 'M.S.'],
	"useForm": "Master"},
	{"uri": "http://purl.org/spar/fabio/DoctoralThesis",
	"mapping": ["Doctoral", "Ph.D.", "Ph. D.", "PhD"],
	"useForm": "Doctoral"}]

Jupiter_predicates = [{"uri": "http://purl.org/dc/terms/title",
	"mapping": ["title"]},
	{"uri": "http://terms.library.ualberta.ca/graduationDate",
	"mapping": ["graduation_date"]},
	{"uri": "http://terms.library.ualberta.ca/dissertant",
	"mapping": ["dissertant"]},
	{"uri": "http://terms.library.ualberta.ca/department",
	"mapping": ["department"]},
	{"uri": "http://ontoware.org/swrc/ontology#institution",
	"mapping": ["institution"]},
	{"uri": "http://terms.library.ualberta.ca/thesisLevel",
	"mapping": ["level"]},
	{"uri": "http://purl.org/ontology/bibo/ThesisDegree",
	"mapping": ["degree"]},
	{"uri": "http://terms.library.ualberta.ca/unicorn",
	"mapping": ["unicorn"]},
	{"uri": "http://purl.org/dc/elements/1.1/subject",
	"mapping": ["subject"]}]

institution = [{"uri": "http://id.loc.gov/authorities/names/n79058482",
	"mapping": ["University of Alberta", "U of A"]},
	{"uri": "http://id.loc.gov/authorities/names/n2009054054",
	"mapping": ["St. Stephen's College"]}]

file_type = [
	'_marc.xml',
	'_meta.mrc',
	'_djvu.txt',
	'.pdf'
	]
sparql = "http://206.167.181.124:9999/blazegraph/namespace/gillingham_20180222/sparql"
IA_access = {'s3': {'access': 'C9khuFEwAKAj5Y5X', 'secret': '8s5NsWQzx1wTKfAd'}}
mypath = "/home/danydvd/git/remote/metadata/scripts/ia/legacy_Thesis/files/xml/"
fedora = "http://mycombe.library.ualberta.ca:8080/fedora/rest/prod"
collection = "http://mycombe.library.ualberta.ca:8080/fedora/rest/prod/44/55/8t/41/44558t416"

def PrintException():
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	print("EXCEPTION IN (%s, LINE %s '%s'): %s" % (filename, lineno, line.strip(), exc_obj))
