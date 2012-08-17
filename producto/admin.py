from django.contrib import admin
from django.contrib.gis import admin as gisadmin
from django.conf import settings
from producto.models import *

class CommentariosInline(admin.TabularInline):
    model = Commentario
    extra = 0

class ObraAdmin(gisadmin.GeoModelAdmin):
    list_display = ('id','localidad','inicio','fin','programa','porcentaje','producto')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('producto__etiqueta',)
    list_filter = ('grupo__nombre',)
    list_select_related = True
    inlines = (CommentariosInline,)
    exclude = ('propietario',)

admin.site.register(Obra, ObraAdmin)