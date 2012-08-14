from django.db import models

class TipoManager(models.Manager):
    def __init__(self, categoria):
        super(TipoManager, self).__init__()
        self.categoria = categoria

    def get_query_set(self):
        return super(TipoManager, self).get_query_set().filter(categoria__exact=self.categoria)
