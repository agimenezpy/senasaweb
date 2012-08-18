from django.contrib import admin
from dojango.util import dojo_collector

class MyAdminSite(admin.AdminSite):
    def admin_view(self, view, cacheable=False):
        dojo_collector.add_module("dijit.layout.ContentPane")
        dojo_collector.add_module("dijit.layout.BorderContainer")
        dojo_collector.add_module("dijit.layout.AccordionContainer")
        dojo_collector.add_module("dijit.TitlePane")
        dojo_collector.add_module("dijit.Tooltip")
        return super(MyAdminSite, self).admin_view(view,cacheable)
site = MyAdminSite()
admin.site = site

admin.autodiscover()
