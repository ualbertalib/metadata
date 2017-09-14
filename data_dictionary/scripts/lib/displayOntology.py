from config import namespaces, definitions, ddWelcome
import main
from main import owlDocument, addPrefixes


def main():
	owlDoc = owlDocument().output
	print('# Jupiter Data Dictionary')
	print('')
	print("%s" % ddWelcome)
	# declares namespaces (set in config.py)
	print('# Namespaces')
	print('')
	for n in namespaces:
		print('   **%s:** %s  ' % (n['prefix'], n['uri']))
	print('')
	# defines annotations (set in config.py)
	print('# Definitions')
	print('')
	for d in definitions:
		print('   **%s** %s  ' % (d['term'], d['def']))
	print('')
	print('# Table of Contents')
	for t, resources in sorted(owlDoc.items()):
		print("### %s " % (t))
		for s, resource in sorted(resources.items()):
			print("  * [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#%s)  " % (addPrefixes(s), addPrefixes(s).replace(':', '').lower()))
		print('')
	print('')
	# sorts owlDoc alphabetically (so the display is always the same order)
	for t, resources in sorted(owlDoc.items()):
		# prints the key (Property, Term, or Value)
		print("# %s  " % (t))
		# iterates over each dictionary (resources)
		for s, resource in sorted(resources.items()):
			# prints the resource name, replacing the URI with a prefix (defined in config.py)
			print('### %s' % (addPrefixes(s)))
			# iterates over the dictionary for this particular resource
			for annotationName, annotationValues in sorted(resource.items()):
				# checks to see if this is an empty list
				if len(annotationValues) > 0:
					print('')
					# prints the name of the annotation
					print('   **%s**   ' % (addPrefixes(annotationName)))
					# prints annotation values line by line
					for value in annotationValues:
						print('  %s  ' % (value))
			# print("- [ ] Mark for editing")
			print('')
			print('***')


if __name__ == "__main__":
	main()
