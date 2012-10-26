from django.conf.urls import patterns, include, url
from senasaweb import admin

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

#last_view = admin.site.admin_view
#def my_view(view, cacheable=False):
#    dojo_collector.add_module("dijit.layout.ContentPane")
#    dojo_collector.add_module("dijit.layout.BorderContainer")
#    return last_view(view,cacheable)
#admin.site.admin_view = my_view

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'senasaweb.views.home', name='home'),
    # url(r'^senasaweb/', include('senasaweb.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^lookup/(?P<model>\w+)/(?P<object_id>\w+)$', 'parametros.views.lookup_handler'),
    #(r'^dojango/', include('dojango.urls')),
)
