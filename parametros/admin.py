from django.contrib import admin
from django.contrib.gis import admin as gisadmin
from models import *
from django.conf import settings
from dojango.forms.widgets import SimpleTextarea
class DepartamentoAdmin(gisadmin.GeoModelAdmin):
    list_display = ('codigo','nombre')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('nombre',)

class DistritoAdmin(gisadmin.GeoModelAdmin):
    list_display = ('codigo','nombre','departamento')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('nombre',)
    list_filter = ('departamento',)
    list_select_related = True

class LocalidadAdmin(gisadmin.GeoModelAdmin):
    list_display = ('codigo','nombre','distrito_nombre')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('nombre','distrito')
    list_select_related = True

    def distrito_nombre(self,obj):
        return obj.distrito.nombre
    distrito_nombre.admin_order_field = 'distrito'
    distrito_nombre.short_description = u"distrito"

class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','monto_proyecto')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('nombre',)
    formfield_overrides = {models.TextField: {'widget' : SimpleTextarea(attrs={"required":True})}}

    def monto_proyecto(self, obj):
        return "%s %.2f" % (obj.moneda, obj.presupuesto)
    monto_proyecto.admin_order_field = 'presupuesto'
    monto_proyecto.short_description = u"monto presupuesto"

class GrupoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','monto_grupo', 'proyecto')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('nombre',)
    list_filter = ('proyecto',)
    list_select_related = True

    def monto_grupo(self, obj):
        return "%s %.2f" % (obj.proyecto.moneda, obj.presupuesto)
    monto_grupo.admin_order_field = 'presupuesto'
    monto_grupo.short_description = u"monto presupuesto"

class TipoAdmin(admin.ModelAdmin):
    list_display = ('id','orden','etiqueta','categoria')
    list_per_page = settings.LIST_PER_PAGE
    list_filter = ('categoria',)
    list_select_related = True

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('codigo','nombre')
    list_per_page = settings.LIST_PER_PAGE

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