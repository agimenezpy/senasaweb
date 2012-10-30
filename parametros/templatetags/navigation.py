from django import template
from django.contrib.admin import site
from django.conf import settings

register = template.Library()

REEMP = {'Auth':'Seguridad','Producto':'Obras','Parametros':'Configuraciones'}

@register.inclusion_tag('admin/navigation.html',takes_context=True)
def load_navigation(context):
    req = context['request']
    rst = site.index(req)
    splt = req.path[1:].split("/")
    sel = ''
    splt.remove(settings.CONTEXT.replace("/",""))
    splt.remove("admin")
    if len(splt) > 1:
        sel = REEMP[splt[0].title()].lower() if REEMP.has_key(splt[0].title()) else ""
    app_order(rst.context_data)
    context.update({'app_list' : rst.context_data['app_list'], "selected" : sel})
    return context

@register.filter
def disable_attr(wkt):
    wkt.field.widget.attrs['readonly'] = 'readonly'
    return wkt

@register.simple_tag
def context():
    return settings.CONTEXT

def app_order(context):
    app_list = list(context['app_list'])
    ordered = []
    # look at each app in the user order
    for app in settings.ADMIN_REORDER:
        app_name, app_models = app[0], app[1]
        # look at each app in the orig order
        for app_def in app_list:
            if app_def['name'] == app_name:
                model_list = list(app_def['models'])
                mord = []
                # look at models in user order
                for model_name in app_models:
                    # look at models in orig order
                    for model_def in model_list:
                        if model_def['name'] == model_name:
                            mord.append(model_def)
                            model_list.remove(model_def)
                            break
                mord[len(mord):] = model_list
                ordered.append({'app_url': app_def['app_url'],
                                'models': mord, 'name': REEMP[app_def['name']]})
                app_list.remove(app_def)
                break
    ordered[len(ordered):] = app_list
    context['app_list'] = ordered