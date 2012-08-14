from django.contrib import admin
from django.contrib.auth.models import User, Group
from models import Usuario, Rol
from django.conf import settings

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','username')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('username',)

class RolAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_per_page = settings.LIST_PER_PAGE

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Rol, RolAdmin)