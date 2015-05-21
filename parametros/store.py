from parametros.models import *
from dojango.data.modelstore import *

class BaseStore(Store):
    key = StoreField(get_value=ObjectMethod("__unicode__"))
    codigo = StoreField()
    nombre = StoreField()
    extension = StoreField(get_value=ObjectMethod("get_extent"))

class GrupoStore(Store):
    key = StoreField(get_value=ObjectMethod("__unicode__"))
    codigo = StoreField()
    descripcion = StoreField()
    llamado = StoreField()
    proyecto = ReferenceField()

    class Meta:
        objects = Grupo.objects.all()
        label = 'key'

class DepartamentoStore(BaseStore):

    class Meta:
        objects = Departamento.objects.all()
        label = 'key'

class DistritoStore(BaseStore):
    departamento = ReferenceField()

    class Meta:
        objects = Distrito.objects.all()
        label = 'key'

class LocalidadStore(BaseStore):
    distrito = ReferenceField()

    class Meta:
        objects = Localidad.objects.all()
        label = 'key'