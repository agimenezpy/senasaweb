from django import template
from django.contrib.admin import site
from django.conf import settings

register = template.Library()

@register.inclusion_tag('admin/navigation.html',takes_context=True)
def load_navigation(context):
    req = context['request']
    rst = site.index(req)
    splt = req.path[1:].split("/")
    sel = ''
    splt.remove(settings.CONTEXT.replace("/",""))
    if len(splt) > 1:
        sel =  splt[0]
    context.update({'app_list' : rst.context_data['app_list'], "selected" : sel})
    return context

@register.filter
def disable_attr(wkt):
    wkt.field.widget.attrs['disabled'] = 'disabled'
    return wkt

@register.simple_tag
def context():
    return settings.CONTEXT