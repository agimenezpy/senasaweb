# -*- coding: iso-8859-1 -*-
from django.contrib import admin
from django.contrib.gis.geos import Point
from django.conf import settings
from producto.models import *
from producto.forms import ObraForm
from senasaweb.admin import MyGeoModelAdmin as GeoModelAdmin,MyModelAdmin as ModelAdmin
from producto.exporter import export_obras_xls,export_obras_pdf
from functools import update_wrapper
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class EstadoInline(admin.TabularInline):
    model = Estado
    extra = 0
    readonly_fields = ('fecha_insercion','fecha_actualizacion','autor')

class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0
    readonly_fields = ('fecha_insercion','fecha_actualizacion','autor')

class ObraAdmin(GeoModelAdmin):
    list_display = ('codigo','distrito','locacion','proceso','porcentaje','inicio','fin','estado','producto','grupo')
    list_per_page = settings.LIST_PER_PAGE
    list_max_show_all = settings.LIST_PER_PAGE
    list_editable = ('proceso','porcentaje','inicio','fin','estado')
    search_fields = ('producto__etiqueta','codigo')
    list_filter = ('grupo__proyecto__nombre','distrito__departamento__nombre')
    list_select_related = True
    inlines = (EstadoInline,)
    readonly_fields = ('propietario',)
    raw_id_fields = ('distrito','localidad','grupo')
    form = ObraForm

    def __init__(self,model,admin_site):
        super(ObraAdmin, self).__init__(model,admin_site)
        self.listAdmin = ObraListAdmin(model,admin_site)
        self.listAdmin.view = True

    fieldsets = (
        (None, {
            'fields' : ('grupo','producto','cantidad','poblacion','tipo_poblacion','propietario','fecha_inicio')
        }),
        (u"Seguimiento", {
            'fields' : ('inicio','fin','proceso','porcentaje','estado')
        }),
        (u"Junta de Saneamiento", {
            'fields' : ('organizacion','junta')
        }),
        (u"Ubicación", {
            'classes' : ('tab',),
            'fields' : ('distrito','localidad','locacion','coordenada_x','coordenada_y','ubicacion')
        })
    )

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
        if obj.coordenada_x != 0 and obj.coordenada_y != 0:
            pt = Point(obj.coordenada_x, obj.coordenada_y,srid=32721)
            obj.ubicacion = pt
        obj.modifica = request.user
        super(ObraAdmin, self).save_model(request, obj, form, change)

    def get_urls(self):
        urlpatterns = super(ObraAdmin,self).get_urls()
        from django.conf.urls import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
            url(r'^list/$',
                wrap(self.listAdmin.changelist_view),
                name='%s_%s_changelist_ro' % info),
            url(r'^export/$',
                wrap(self.listAdmin.export),
                name='%s_%s_export' % info),
            url(r'^list/(.+)/$',
                wrap(self.list_view),
                name='%s_%s_change_ro' % info),
        ) + urlpatterns
        return urlpatterns

    def list_view(self, request, object_id, form_url='', extra_context=None):
        opts = self.model._meta
        return HttpResponseRedirect(reverse('admin:%s_%s_change' %
                                            (opts.app_label, opts.module_name), args=(object_id,),
            current_app=self.admin_site.name))

    def has_change_permission(self, request, obj=None):
        # Esto se implementa asi porque siempre desde el changelist_view se envia obj=None pero en otra invocacion no
        if obj is None or self.view:
            return self.has_view_permission(request,obj)
        else:
            chPerm = super(ObraAdmin,self).has_change_permission(request,obj)
            if chPerm and obj != False and not request.user.is_superuser:
                objPerm = False
                try:
                    otobj = Obra.objects.get(pk=obj.id,grupo__proyecto__miembro__usuario_id__exact=request.user.id)
                    objPerm = True
                except:
                    pass
                return  objPerm
            else:
                return chPerm

class ObraListAdmin(ModelAdmin):
    list_display = ('codigo','distrito','locacion','fmt_finicio','proceso','progreso','fmt_inicio','fmt_fin','producto','grupo')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('producto__etiqueta','codigo')
    list_filter = ('grupo__proyecto__nombre','distrito__departamento__nombre')
    list_select_related = True
    actions = [export_obras_xls,export_obras_pdf]

    def progreso(self,obj):
        return '<div data-dojo-type="dijit.ProgressBar" style="width:80px" data-dojo-id="myProgressBar%d" id="progress%d" data-dojo-props="value:%d"></div>' \
               % (obj.id,obj.id,obj.porcentaje)
    progreso.allow_tags = True
    progreso.admin_order_field = 'porcentaje'
    progreso.short_description = "Progreso"

    def fmt_finicio(self, obj):
        return obj.inicio.strftime("%d/%m/%Y")
    fmt_finicio.short_description = "Inicio de obra"
    fmt_finicio.admin_order_field = 'fecha_inicio'

    def fmt_inicio(self, obj):
        return obj.inicio.strftime("%d/%m/%Y")
    fmt_inicio.short_description = "Inicio"
    fmt_inicio.admin_order_field = 'inicio'

    def fmt_fin(self, obj):
        return obj.fin.strftime("%d/%m/%Y")
    fmt_fin.short_description = "Fin"
    fmt_fin.admin_order_field = 'fin'

    def export(self, request, extra_context=None):
        return export_obras_xls(self,request,None)

class ContactoAdmin(ModelAdmin):
    list_display = ('cedula', 'nombres', 'apellidos', 'telefono_celular','obra')
    list_display_links = ('cedula',)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('nombres','apellidos')
    raw_id_fields = ('obra',)
    list_select_related = True
    inlines = (ComentarioInline,)

    def save_model(self, request, obj, form, change):
        obj.modifica = request.user
        super(ContactoAdmin, self).save_model(request, obj, form, change)

admin.site.register(Obra, ObraAdmin)
admin.site.register(Contacto, ContactoAdmin)