# -*- coding: iso-8859-1 -*-
from django.contrib import admin
from django.contrib.gis import admin as gisadmin
from models import *
from django.conf import settings
from dojango.forms.widgets import SimpleTextarea,NumberTextInput

class BaseGeoModelAdmin(gisadmin.GeoModelAdmin):
    max_extent =  '-81414.425199, 6950131.660985, 778278.875001, 7864759.500000'
    map_srid = 32721
    wms_url = settings.WMS_SERVICE
    wms_layer = 'default'
    wms_name = 'Senasa WMS'
    units = 'm'
    max_resolution = "'auto'"
    num_zoom = 8
    default_zoom = 0
    default_lon = 454085
    default_lat = 7427009

class DepartamentoAdmin(BaseGeoModelAdmin):
    list_display = ('codigo','nombre')
    list_display_links = ('nombre',)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('nombre',)
    fieldsets = (
        (None, {
            'fields' : ('nombre',)
        }),
        (u"Información Geográfica", {
            'classes' : ('collapse',),
            'fields' : ('geom',)
        })
    )

class DistritoAdmin(BaseGeoModelAdmin):
    list_display = ('codigo','nombre','departamento')
    list_display_links = ('nombre',)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('nombre',)
    list_filter = ('departamento__nombre',)
    list_select_related = True
    fieldsets = (
        (None, {
            'fields' : ('nombre','departamento')
        }),
        (u"Información Geográfica", {
            'classes' : ('collapse',),
            'fields' : ('geom',)
        })
    )

class LocalidadAdmin(BaseGeoModelAdmin):
    list_display = ('codigo','nombre','distrito_nombre')
    list_display_links = ('nombre',)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('nombre','distrito__nombre')
    list_filter = ('distrito__departamento__nombre',)
    list_select_related = True
    fieldsets = (
        (None, {
            'fields' : ('nombre','distrito')
        }),
        (u"Información Geográfica", {
            'classes' : ('collapse',),
            'fields' : ('geom',)
        })
    )
    raw_id_fields = ('distrito',)

    def distrito_nombre(self,obj):
        return obj.distrito.nombre
    distrito_nombre.admin_order_field = 'distrito'
    distrito_nombre.short_description = u"distrito"

class MiembroInline(admin.TabularInline):
    model = Miembro
    raw_id_fields = ("usuario",)
    extra = 0

class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','monto_proyecto')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('nombre',)
    formfield_overrides = {models.TextField: {
                            'widget' : SimpleTextarea(attrs = {"required":True})},
                           models.DecimalField : {
                            'widget' : NumberTextInput(attrs = {"required":True})}
                           }
    inlines = (MiembroInline,)

    def queryset(self, request):
        qs = super(ProyectoAdmin, self).queryset(request)
        is_user_admin = False
        rs = request.user.groups.filter(name="ADMINISTRADOR")
        if len(rs) > 0:
            is_user_admin = True
        if request.user.is_superuser or is_user_admin:
            return qs
        return qs.filter(miembro__usuario_id__exact=request.user.id)

    def monto_proyecto(self, obj):
        return "%s %.2f" % (obj.moneda, obj.presupuesto)
    monto_proyecto.admin_order_field = 'presupuesto'
    monto_proyecto.short_description = u"monto presupuesto"

class GrupoAdmin(admin.ModelAdmin):
    list_display = ('id','descripcion','monto_proyecto','proyecto')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('descripcion',)
    list_filter = ('proyecto__nombre',)
    list_select_related = True

    def queryset(self, request):
        qs = super(GrupoAdmin, self).queryset(request)

        is_user_admin = False
        rs = request.user.groups.filter(name="ADMINISTRADOR")
        if len(rs) > 0:
            is_user_admin = True
        if request.user.is_superuser or is_user_admin:
            return qs
        return qs.filter(proyecto__miembro__usuario_id__exact=request.user.id)

    def monto_proyecto(self, obj):
        return "%s %.2f" % (obj.proyecto.moneda, obj.proyecto.presupuesto)
    monto_proyecto.admin_order_field = 'proyecto__presupuesto'

class TipoAdmin(admin.ModelAdmin):
    list_display = ('id','orden','etiqueta','categoria')
    list_per_page = settings.LIST_PER_PAGE
    list_filter = ('categoria__nombre',)
    list_select_related = True

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('codigo','nombre')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('codigo',)

# Localidad
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Distrito, DistritoAdmin)
admin.site.register(Localidad, LocalidadAdmin)
# Proyecto
admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(Grupo, GrupoAdmin)
# Tipos
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Tipo, TipoAdmin)