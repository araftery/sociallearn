from django import template
from django.core.urlresolvers import resolve

register = template.Library()

# usage: {% navactive request 'comma-separated-list,of-url-pattern-names,to-match'}
@register.simple_tag
def navactive(request, urls):
    if resolve(request.path).url_name in [url.strip() for url in urls.split(',')]:
        return "active"
    return ''

# usage: {% navactive_namespace request 'comma-separated-list,of-name-spaces,to-match'}
@register.simple_tag
def navactive_namespace(request, urls):
    if resolve(request.path).namespace in [url.strip() for url in urls.split(',')]:
        return "active"
    return ''
