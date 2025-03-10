from django import template
from Webapp.models import Processing
#from ..Code.enrich import main

register = template.Library()

@register.filter
def replaceMARC(value):
    return value.replace("MARC/","")

@register.filter
def replaceBIB(value):
    return value.replace("BIBFRAME/","")

@register.filter
def minus(value):
    return value-1

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def replacedot(value):
	return value.replace('.', '')

@register.filter
def get_apis(value):
    apis = []
    AP = ''
    for api in value.split('_-_'):
    	if api == 'search_api_LC':
    		apis.append("LoC (didyoumean)")
    	elif api == 'search_api_LCS':
    		apis.append('Loc (Suggest)')
    	elif api == 'search_api_VF':
    		apis.append('VIAF (General)')
    	elif api == 'search_api_VFP':
    		apis.append('VIAF (Personal)')
    	elif api == 'search_api_VFC':
    		apis.append('VIAF (Corporate)')
    for n, item in enumerate(apis):
    	if n != 0:
    		AP = '%s, %s' %(AP, item)
    	else:
    		AP = item
    return (AP)

@register.filter
def inProcess(obj):
	for docs in Processing.objects.all():
		if '--__--__--' in docs.files:
			file = docs.files.split('--__--__--')
			for n, item in enumerate(file):
				if n == 0:
					pass
				else:
					if obj.name.replace('BIBFRAME/', '') == item:
						return (docs.id)
		else:
			if obj.name == docs.files:
				return (docs.id)
	return False

@register.filter
def get_perc(value, args):
	return ("{0:.2f}".format(round((int(value)/int(args))*100,2)))

'''@register.filter
def process(id):
	object = Processing.objects.get(id=id)
	return main(object)'''