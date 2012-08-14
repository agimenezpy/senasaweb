from django.contrib.auth.models import User, Group

class Usuario(User):
    def __init__(self, *args, **kwargs):
        super(Usuario, self).__init__(*args, **kwargs)
        self.is_staff = True
        self.is_superuser = False
        self.is_active = True

    class Meta:
        verbose_name = "usuario registrado"
        verbose_name_plural = "usuarios registrados"
        proxy = True

class Rol(Group):

    class Meta:
        verbose_name = "rol"
        verbose_name_plural = "roles"
        proxy = True