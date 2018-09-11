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
def get_item(dictionary, key):
    return dictionary.get(key)

'''@register.filter
def process(id):
	object = Processing.objects.get(id=id)
	return main(object)'''