from models import *
from store import *
from django.http import Http404,HttpResponse,HttpResponseForbidden
from django.views.decorators.cache import never_cache
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from django.utils.encoding import smart_str
import django.utils.simplejson as simplejson
from re import compile
import operator

mcod = compile("localidad|distrito|departamento|grupo|proyecto")

# GRAPPELLI IMPORTS
from grappelli.settings import AUTOCOMPLETE_LIMIT
from grappelli.views.related import get_label

@never_cache
def lookup_handler(request, model, object_id):
    filtro = {"codigo" : object_id}
    if model == "departamento":
        store = DepartamentoStore()
        model_class = Departamento
    elif model == "distrito":
        store = DistritoStore()
        model_class = Distrito
    elif model == "localidad":
        store = LocalidadStore()
        model_class = Localidad
    elif model == "grupo":
        store = GrupoStore()
        model_class = Grupo
    else:
        raise Http404("Modelo %s no existe" % model)
    result = store.to_json(objects=model_class.objects.filter(**filtro))
    return HttpResponse(result, mimetype="application/json")

@never_cache
def related_lookup(request):
    if not (request.user.is_active and request.user.is_staff):
        return HttpResponseForbidden('<h1>Permission denied</h1>')
    data = []
    if request.method == 'GET':
        if request.GET.has_key('object_id') and request.GET.has_key('app_label') and request.GET.has_key('model_name'):
            object_id = request.GET.get('object_id')
            app_label = request.GET.get('app_label')
            model_name = request.GET.get('model_name')
            if object_id:
                try:
                    key = "codigo" if mcod.match(model_name) else "pk"
                    filtro = {key: object_id}
                    model = models.get_model(app_label, model_name)
                    obj = model.objects.get(**filtro)
                    data.append({"value":getattr(obj,key),"label":get_label(obj)})
                    return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')
                except:
                    pass
    data = [{"value":None,"label":""}]
    return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')

@never_cache
def autocomplete_lookup(request):
    if not (request.user.is_active and request.user.is_staff):
        return HttpResponseForbidden('<h1>Permission denied</h1>')
    data = []
    if request.method == 'GET':
        if request.GET.has_key('term') and request.GET.has_key('app_label') and request.GET.has_key('model_name'):
            term = request.GET.get("term")
            app_label = request.GET.get('app_label')
            model_name = request.GET.get('model_name')
            model = models.get_model(app_label, model_name)
            filters = {}
            key = "codigo" if mcod.match(model_name) else "pk"
            # FILTER
            if request.GET.get('query_string', None):
                for item in request.GET.get('query_string').split("&"):
                    if item.split("=")[0] != "t":
                        filters[smart_str(item.split("=")[0])]=smart_str(item.split("=")[1])
                # SEARCH
            qs = model._default_manager.filter(**filters)
            for bit in term.split():
                search = [models.Q(**{smart_str(item):smart_str(bit)}) for item in model.autocomplete_search_fields()]
                search_qs = QuerySet(model)
                search_qs.dup_select_related(qs)
                search_qs = search_qs.filter(reduce(operator.or_, search))
                if model_name == "locacion":
                    qs = qs.filter(reduce(operator.or_, search))
                else:
                    qs = qs & search_qs
            data = [{"value":getattr(f,key),"label":get_label(f)} for f in qs[:AUTOCOMPLETE_LIMIT]]
            label = ungettext(
                '%(counter)s result',
                '%(counter)s results',
                len(data)) % {
                        'counter': len(data),
                        }
            return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')
    data = [{"value":None,"label":_("Server error")}]
    return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')