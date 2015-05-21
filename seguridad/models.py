from django.contrib.auth.models import User, Group
from django.db import models


class Cuenta(User):
    def has_module_perms(self, app_label):
        return self.is_active

    class Meta:
        verbose_name = "cuenta"
        verbose_name_plural = "cuentas"
        proxy = True