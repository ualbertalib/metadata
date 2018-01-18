from profiler import Profiler, Backup
from ontology import owlDocument
#from Gsheet import google_generate
from excelg import excelGen
import sys


def main():
	old_stdout = sys.stdout
	with open('data_dictionary/profiles/backup.nquads', "w+") as backup:
		# backup database
		sys.stdout = backup
		Backup()
	with open('data_dictionary/jupiter_ontology.md', "w+") as ontology:
		# serialize a new jupiter ontology file
		sys.stdout = ontology
		owlDocument().generate()
	sys.stdout = old_stdout
	for ptype in ["collection", "community", "generic", "thesis", "oai_pmh", "oai_etdms"]:
		# serialize a profile for each object type
		Profiler(ptype)
	excelGen()
	#google_generate()


if __name__ == "__main__":
	main()
