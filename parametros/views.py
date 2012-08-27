from models import *
from store import *
from django.http import Http404,HttpResponse
from django.views.decorators.cache import never_cache

@never_cache
def lookup_handler(request, model, object_id):
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
    elif model == "contacto":
        store = ContactoStore()
        model_class = Contacto
    else:
        raise Http404("Modelo %s no existe" % model)
    result = store.to_json(objects=model_class.objects.filter(pk=object_id))
    return HttpResponse(result, mimetype="application/json")