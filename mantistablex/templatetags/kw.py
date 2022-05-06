from django import template
register = template.Library()

@register.filter
def kw(dict, key):    
    try:
        return dict[key]
    except KeyError:
        return ''