from django.contrib import admin
from dojango.util import dojo_collector

class MyAdminSite(admin.AdminSite):
    def admin_view(self, view, cacheable=False):
        dojo_collector.add_module("dijit.layout.ContentPane")
        dojo_collector.add_module("dijit.layout.BorderContainer")
        return super(MyAdminSite, self).admin_view(view,cacheable)
site = MyAdminSite()
admin.site = site

admin.autodiscover()
