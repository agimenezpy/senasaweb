# -*- coding: iso-8859-1 -*-
from django.contrib import admin
from django.contrib.gis.geos import Point
from django.conf import settings
from producto.models import *
from producto.forms import ObraForm
from senasaweb.admin import MyGeoModelAdmin as GeoModelAdmin,MyModelAdmin as ModelAdmin

class EstadoInline(admin.TabularInline):
    model = Estado
    extra = 0
    readonly_fields = ('fecha_insercion','fecha_actualizacion','autor')

class ObraAdmin(GeoModelAdmin):
    list_display = ('codigo','distrito','localidad','producto','grupo','proceso','progreso','fecha_inicio','fecha_fin')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('producto__etiqueta',)
    list_filter = ('grupo__proyecto__nombre','distrito__departamento__nombre')
    list_select_related = True
    inlines = (EstadoInline,)
    readonly_fields = ('propietario',)
    raw_id_fields = ('distrito','localidad','grupo')
    form = ObraForm

    fieldsets = (
        (None, {
            'fields' : ('grupo','producto','cantidad','poblacion','tipo_poblacion','propietario')
        }),
        (u"Seguimiento", {
            'fields' : ('inicio','fin','proceso','porcentaje')
        }),
        (u"Junta de Saneamiento", {
            'fields' : ('organizacion','junta')
        }),
        (u"Ubicación", {
            'classes' : ('tab',),
            'fields' : ('distrito','localidad','direccion','coordenada_x','coordenada_y','ubicacion')
        })
    )

    def progreso(self,obj):
        return '<div data-dojo-type="dijit.ProgressBar" style="width:80px" data-dojo-id="myProgressBar%d" id="progress%d" data-dojo-props="value:%d"></div>' \
               % (obj.id,obj.id,obj.porcentaje)
    progreso.allow_tags = True
    progreso.admin_order_field = 'porcentaje'
    progreso.short_description = "Progreso"

    def fecha_inicio(self, obj):
        return obj.inicio.strftime("%d/%m/%Y")
    fecha_inicio.short_description = "Inicio"
    fecha_inicio.admin_order_field = 'inicio'

    def fecha_fin(self, obj):
        return obj.fin.strftime("%d/%m/%Y")
    fecha_fin.short_description = "Fin"
    fecha_fin.admin_order_field = 'fin'

    def queryset(self, request):
        qs = super(ObraAdmin, self).queryset(request)

        is_user_admin = False
        rs = request.user.groups.filter(name="ADMINISTRADOR")
        if len(rs) > 0:
            is_user_admin = True
        if request.user.is_superuser or is_user_admin:
            return qs
        rs = request.user.groups.filter(name="LIDER DE PROYECTO")
        if len(rs) > 0:
            return qs.filter(grupo__proyecto__miembro__usuario_id__exact=request.user.id)
        return qs.filter(propietario_id__exact=request.user.id)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'propietario', None) is None:
            obj.propietario = request.user
        if obj.coordenada_x == 0 and obj.coordenada_y == 0:
            ubc = obj.localidad.geom.centroid if obj.localidad is not None else obj.distrito.geom.centroid
            obj.ubicacion = ubc
        elif not obj.ubicacion:
            pt = Point(obj.coordenada_x, obj.coordenada_y,srid=32721)
            obj.ubicacion = pt
        obj.salva = request.user
        obj.save()

class ContactoAdmin(ModelAdmin):
    list_display = ('obra','cedula', 'nombres', 'apellidos', 'telefono_celular')
    list_display_links = ('cedula',)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('nombres','apellidos')
    raw_id_fields = ('obra',)

admin.site.register(Obra, ObraAdmin)
admin.site.register(Contacto, ContactoAdmin)