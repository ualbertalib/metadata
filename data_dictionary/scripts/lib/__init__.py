from profiler import Profiler
from ontology import owlDocument
#from Gsheet import google_generate
#from excelg import excelGen
import sys


def main():
	old_stdout = sys.stdout
	with open('data_dictionary/jupiter_ontology.md', "w+") as ontology:
		sys.stdout = ontology
		owlDocument().generate()
	sys.stdout = old_stdout
	for ptype in ["collection", "community", "generic", "thesis"]:
		Profiler(ptype)
	'''excelGen()
	google_generate()'''


if __name__ == "__main__":
	main()