import re

class Transformation():
	@staticmethod
	def rdfsyntaxnstype(triple):
		triple['object']['value'] = "I did something to this value"
		triple['object']['type'] = "string"
		return [triple] # a list of triples, in case more triples must be added as a result of this operation

	@staticmethod
	def subject(triple):
		triple['object']['value'] = "this is no longer a subject"
		return[triple]

class TransformationFactory():
	@staticmethod
	def getTransformation(triple):
		function = re.sub(r'[0-9]+', '', triple['predicate']['value'].split('/')[-1].replace('#', '').replace('-', ''))
		if (function == "rdfsyntaxnstype"):
			return Transformation().rdfsyntaxnstype(triple)
		elif (function == "subject"):
			return Transformation().subject(triple)
		else:
			return [triple]
