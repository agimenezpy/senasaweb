from django.shortcuts import render_to_response
from django.conf import settings
from senasaweb.admin import MyGeoModelAdmin
from django.http import HttpResponse
from django.template import RequestContext
from models import Obra
from parametros.models import Tipo,Departamento,Distrito,Proyecto,Grupo
from django.contrib.gis.gdal import SpatialReference
from django.views.decorators.cache import cache_page
from django.views.decorators.gzip import gzip_page
from django.core.cache import cache
from django.conf import settings
from re import compile


wgs84 = SpatialReference("EPSG:4326")
FEAT_TMPL = "{type:'Feature',geometry:{type:'Point',coordinates:[%.4f,%.4f]},properties:{%s}}"
#ICONS = {11:"blue",12:"orange",13:"orange",14:"green"}
ext = compile("\(|\)")

def index(request):
    iconos = get_iconos()
    grps = get_grupo()
    prd = get_producto()
    dps = get_deps()
    pry = get_proj()
    return render_to_response("index.html",{"MAP" : settings.TILE_MAP,
                                            "center_x" : -58,
                                            "center_y": -24,
                                            "zoom" : MyGeoModelAdmin.default_zoom,
                                            "theme" : settings.UI_THEME,
                                            "iconos" : "{%s}" % iconos,
                                            "grupos" : grps,
                                            "producto" : prd,
                                            "departamento" : sorted(dps.iteritems()),
                                            "proyecto" : pry}, RequestContext(request))

@gzip_page
@cache_page(settings.CACHE_TIMEOUT)
def obras(request):
    if cache.has_key("obras"):
        return cache.get("obras")
    response = HttpResponse(mimetype="application/json; charset=iso8859-1")
    TIPOS = get_tipos()
    DEPS = get_deps()
    rs = Obra.objects.select_related("distrito").only("locacion",
        "proceso","distrito__nombre","distrito__departamento","producto","cantidad",
        "ubicacion","grupo").filter(ubicacion__isnull=False).exclude(proceso__id__exact=19)
    pre = ""
    response.write('{"type":"FeatureCollection","features":[')
    for rw in rs:
        point = rw.ubicacion.transform(wgs84,clone=True)
        response.write((unicode('%s{"type":"Feature",'+
           '"geometry":{"type":"Point",'+
           '"coordinates":[%.8f,%.8f]},'+
           '"properties":{"locacion":"%s","grupo":"%s","distrito":"%s","departamento":"%s",'+
           '"proceso":"%s","producto":"%s","cantidad":"%d"}}') % (pre,
            point.x,point.y,
            rw.locacion,
            rw.grupo_id,
            rw.distrito.nombre,
            DEPS[rw.distrito.departamento_id][0],
            TIPOS[rw.proceso_id],
            TIPOS[rw.producto_id],
            rw.cantidad
            )).encode("latin-1"))
        pre = ","
    response.write("]}")
    cache.set("obra",response)
    return response

def get_iconos():
    if cache.has_key("iconos"):
        return cache.get("iconos")
    iconos = reduce(lambda i,v: i + u"," + v, map(lambda it: u'"%s" : "%s"' % (it.etiqueta, it.color if it.color is not None else 'default'), Tipo.objects.filter(categoria__exact="PRD")))
    cache.set("iconos",iconos)
    return iconos

def get_tipos(cat=None):
    if cache.has_key("tipos"):
        return cache.get("tipos")
    else:
        TIPOS = {}
        for rw in Tipo.objects.only("id","etiqueta").filter(categoria__in=["PRO","PRD"]):
            TIPOS[rw.id] = rw.etiqueta
        cache.set('tipos',TIPOS)
        return TIPOS

def get_producto():
    if cache.has_key("producto"):
        return cache.get("producto")
    else:
        PROD = {}
        for rw in Tipo.objects.only("id","etiqueta").filter(categoria__exact="PRD"):
            PROD[rw.id] = rw.etiqueta
        cache.set('producto',PROD )
        return PROD

def get_deps():
    if cache.has_key("departamento"):
        return cache.get("departamento")
    else:
        DEPS = {}
        for rw in Departamento.objects.only("codigo","nombre").extra(select={"extension":"box(transform(geom,4326))"}).all():
            DEPS[rw.codigo] = (rw.nombre,ext.sub("",rw.extension))
        cache.set('departamento',DEPS)
        return DEPS

def get_proj():
    if cache.has_key("proyecto"):
        return cache.get("proyecto")
    else:
        PROJ = {}
        for rw in Proyecto.objects.only("id","nombre").all():
            PROJ[rw.codigo] = rw.nombre
        cache.set("proyecto",PROJ)
        return PROJ

def get_grupo():
    if cache.has_key("grupo"):
        return cache.get("grupo")
    else:
        GRP = {}
        for rw in Grupo.objects.select_related("proyecto").only("codigo","descripcion","proyecto__nombre").all():
            GRP[rw.codigo] = (rw.descripcion,rw.proyecto.nombre)
        cache.set("grupo",GRP)
        return GRP