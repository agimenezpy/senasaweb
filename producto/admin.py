# -*- coding: iso-8859-1 -*-
from django.contrib import admin
from django.contrib.gis import admin as gisadmin
from django.conf import settings
from producto.models import *
from datetime import datetime
from dojango.forms.widgets import DateInput

class MyDateInput(DateInput):
    def __init__(self, attrs=None, format=None):
        super(MyDateInput, self).__init__(attrs,format="%d/%m/%Y")

class CommentariosInline(admin.TabularInline):
    model = Commentario
    extra = 0
    exclude = ('fecha_insercion','fecha_actualizacion','autor')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'autor', None) is None:
            obj.autor = request.user
        if getattr(obj, 'id', None) is None:
            obj.fecha_insercion = datetime.now()
        obj.fecha_actualizacion = datetime.now()
        obj.save()

class ObraAdmin(gisadmin.GeoModelAdmin):
    list_display = ('id','localidad','inicio','fin','programa','porcentaje','producto')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('producto__etiqueta',)
    list_filter = ('grupo__nombre',)
    list_select_related = True
    inlines = (CommentariosInline,)
    readonly_fields = ('propietario',)
    raw_id_fields = ('localidad','grupo')

    fieldsets = (
        ("Datos de la Obra", {
            'fields' : ('descripcion','inicio','fin','producto','cantidad','poblacion','tipo_poblacion')
        }),
        (u"Seguimiento", {
            'fields' : ('proceso','estado','porcentaje','junta','propietario')
        }),
        (u"Proyecto de Inversión", {
            'fields' : ('programa','grupo','organizacion')
        }),
        (u"Ubicación", {
            'classes' : ('collapse',),
            'fields' : ('localidad','coordenada_x','coordenada_y','ubicacion')
        })
    )

#    formfield_overrides = {models.DateField: {
#        'widget' : MyDateInput(attrs = {"required":True})}
#    }
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'propietario', None) is None:
            obj.propietario = request.user
        obj.save()

admin.site.register(Obra, ObraAdmin)