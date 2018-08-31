from django import template

register = template.Library()

@register.filter
def replaceMARC(value):
    return value.replace("MARC","")

def replaceBIB(value):
    return value.replace("BIBFRAME","")