from django import template
from django.contrib.admin import site

register = template.Library()

@register.inclusion_tag('admin/navigation.html',takes_context=True)
def load_navigation(context):
    req = context['request']
    rst = site.index(req)
    sel = req.path.split("/")[1]
    return {'app_list' : rst.context_data['app_list'], "selected" : sel}