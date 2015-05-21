from django.contrib import admin
from models import Cuenta
from django.conf import settings
from django.views.generic import DetailView
from functools import update_wrapper
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

class CuentaAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','username')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('username',)
    fields = ('username', 'first_name','last_name','date_joined','last_login')
    readonly_fields = ('username','date_joined','last_login')
    orig_ro_fields = readonly_fields

    def get_urls(self):
        from django.conf.urls import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
            url(r'^$',
                wrap(self.changelist_view),
                name='%s_%s_changelist' % info),
            url(r'^(.+)/history/$',
                wrap(self.history_view),
                name='%s_%s_history' % info),
            url(r'^(.+)/$',
                wrap(self.change_view),
                name='%s_%s_change' % info),
        )
        return urlpatterns

    def changelist_view(self, request, extra_context=None):
        self.readonly_fields = self.fields
        tmp = self.change_view(request, str(request.user.id), '', extra_context)
        self.readonly_fields = self.orig_ro_fields
        if hasattr(tmp, 'context_data'):
            tmp.context_data.update({'change':False,'title':u"Detalle de la Cuenta",
                                     'has_change_permission':False})
        return tmp

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if obj:
            return request.user.id == obj.id
        else:
            False

admin.site.register(Cuenta, CuentaAdmin)