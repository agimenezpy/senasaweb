# -*- coding: iso-8859-1 -*-
from django.contrib import admin
from django.contrib.gis import admin as gisadmin
from django.conf import settings
from producto.models import *
from parametros.admin import BaseGeoModelAdmin

class EstadoInline(admin.TabularInline):
    model = Estado
    extra = 0
    readonly_fields = ('fecha_insercion','fecha_actualizacion','autor')

class ObraAdmin(BaseGeoModelAdmin):
    list_display = ('id','localidad','inicio','fin','grupo','porcentaje','producto')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('producto__etiqueta',)
    list_select_related = True
    inlines = (EstadoInline,)
    readonly_fields = ('propietario',)
    raw_id_fields = ('localidad','grupo')

    fieldsets = (
        (None, {
            'fields' : ('inicio','fin','producto','cantidad','poblacion','tipo_poblacion')
        }),
        (u"Seguimiento", {
            'fields' : ('proceso','porcentaje','propietario')
        }),
        (u"Grupo de Trabajo", {
            'fields' : ('grupo','organizacion','junta')
        }),
        (u"Ubicación", {
            'fields' : ('localidad','coordenada_x','coordenada_y','ubicacion')
        })
    )

    def queryset(self, request):
        qs = super(ObraAdmin, self).queryset(request)

        if request.user.is_superuser:
            return qs
        return qs.filter(grupo__miembro__usuario_id__exact=request.user.id)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'propietario', None) is None:
            obj.propietario = request.user
        if obj.coordenada_x == 0 or obj.coordenada_y == 0:
            ubc = obj.localidad.geom.centroid
            obj.coordenada_x, obj.coordenada_y = ubc.x,ubc.y
            obj.ubicacion = ubc
        obj.salva = request.user
        obj.save()

admin.site.register(Obra, ObraAdmin)