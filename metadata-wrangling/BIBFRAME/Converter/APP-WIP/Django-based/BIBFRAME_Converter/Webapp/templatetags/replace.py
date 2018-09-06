from django import template

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