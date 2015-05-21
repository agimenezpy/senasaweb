from django.contrib import admin
from django.contrib.gis import admin as gisadmin
from dojango.util import dojo_collector
from django.contrib.gis.admin.options import spherical_mercator_srid
from django.conf import settings


class MyGeoModelAdmin(gisadmin.GeoModelAdmin):
    #max_extent =  '-81414.425199, 6950131.660985, 778278.875001, 7864759.500000'
    #map_srid = 32721
    #wms_url = settings.WMS_SERVICE
    #wms_layer = 'default'
    #wms_name = 'Senasa WMS'
    units = 'm'
    #max_resolution = "'auto'"
    #num_zoom = 8
    #default_zoom = 0
    #default_lon = 454085
    #default_lat = 7427009
    map_template = 'gis/admin/mapbox.html'
    num_zoom = 17
    map_srid = spherical_mercator_srid
    max_extent = '-20037508,-20037508,20037508,20037508'
    max_resolution = '156543.0339'
    point_zoom = 14
    default_zoom = 7
    default_lon = -6395183.6125250775000000
    default_lat = -2664167.8687612307000000
    wms_url = settings.TILE_MAP

    view = False

    def has_view_permission(self, request, obj=None):
        opts = self.opts
        return super(MyGeoModelAdmin,self).has_change_permission(request,obj) or \
               request.user.has_perm(opts.app_label + '.view_%s' % opts.object_name.lower())

    def has_change_permission(self, request, obj=None):
        # Esto se implementa asi porque siempre desde el changelist_view se envia obj=None pero en otra invocacion no
        if obj is None or self.view:
            return self.has_view_permission(request,obj)
        else:
            return super(MyGeoModelAdmin,self).has_change_permission(request,obj)

    def get_model_perms(self, request):
        return {
            'add': self.has_add_permission(request),
            'change': self.has_change_permission(request),
            'delete': self.has_delete_permission(request),
            'view': self.has_view_permission(request)
        }

    def get_readonly_fields(self, request, obj=None):
        if self.view:
            return [f.name for f in self.model._meta.fields if f.name != "geom" and f.name != "ubicacion"]
        else:
            return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if not self.has_change_permission(request,False) and self.has_view_permission(request):
            self.view = True
            tmp = super(MyGeoModelAdmin,self).change_view(request, object_id, form_url, extra_context)
            self.view = False
            if hasattr(tmp, 'context_data'):
                tmp.context_data.update({'change':False,'title':u"Detalle de %s" % self.model._meta.verbose_name,
                                         'has_change_permission':False})
            return tmp
        else:
            return super(MyGeoModelAdmin,self).change_view(request, object_id, form_url, extra_context)

class MyModelAdmin(admin.ModelAdmin):
    view = False

    def has_view_permission(self, request, obj=None):
        opts = self.opts
        return super(MyModelAdmin,self).has_change_permission(request,obj) or \
               request.user.has_perm(opts.app_label + '.view_%s' % opts.object_name.lower())

    def has_change_permission(self, request, obj=None):
        # Esto se implementa asi porque siempre desde el changelist_view se envia obj=None pero en otra invocacion no
        if obj is None or self.view:
            return self.has_view_permission(request,obj)
        else:
            return super(MyModelAdmin,self).has_change_permission(request,obj)

    def get_model_perms(self, request):
        return {
            'add': self.has_add_permission(request),
            'change': self.has_change_permission(request),
            'delete': self.has_delete_permission(request),
            'view': self.has_view_permission(request)
            }

    def get_readonly_fields(self, request, obj=None):
        if self.view:
            return [f.name for f in self.model._meta.fields if f.name != "geom"]
        else:
            return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if not self.has_change_permission(request,False) and self.has_view_permission(request):
            self.view = True
            tmp = super(MyModelAdmin,self).change_view(request, object_id, form_url, extra_context)
            self.view = False
            if hasattr(tmp, 'context_data'):
                tmp.context_data.update({'change':False,'title':u"Detalle de %s" % self.model._meta.verbose_name,
                                         'has_change_permission':False})
            return tmp
        else:
            return super(MyModelAdmin,self).change_view(request, object_id, form_url, extra_context)

class MyAdminSite(admin.AdminSite):
    def admin_view(self, view, cacheable=False):
        dojo_collector.add_module("dojo.NodeList-manipulate")
        dojo_collector.add_module("dijit.layout.ContentPane")
        dojo_collector.add_module("dijit.layout.BorderContainer")
        dojo_collector.add_module("dijit.layout.AccordionContainer")
        dojo_collector.add_module("dijit.layout.TabContainer")
        dojo_collector.add_module("dijit.TitlePane")
        dojo_collector.add_module("dijit.Tooltip")
        dojo_collector.add_module("dijit.ProgressBar")
        return super(MyAdminSite, self).admin_view(view,cacheable)

site = MyAdminSite()
admin.site = site
admin.site.disable_action('delete_selected')
admin.autodiscover()
