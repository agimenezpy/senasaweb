from django.forms import ModelForm,ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.geos import Point
from producto.models import Obra
from parametros.models import Localidad,Distrito

class ObraForm(ModelForm):
    def clean_localidad(self):
        localidad = self.cleaned_data['localidad']
        if self.cleaned_data.has_key('distrito'):
            distrito = self.cleaned_data['distrito']
            if localidad.distrito_id != distrito.codigo:
                raise ValidationError("La localidad no pertenece al distrito")
        return localidad

    def clean(self):
        cleaned_data = super(ObraForm, self).clean()
        coordenadax = self.cleaned_data['coordenada_x']
        coordenaday = self.cleaned_data['coordenada_y']
        if self.cleaned_data.has_key('distrito'):
            distrito = self.cleaned_data['distrito']
            if coordenadax == 0 and coordenaday == 0:
                return cleaned_data
            pt = Point(coordenadax,coordenaday,srid=32721)
            if not distrito.geom.contains(pt):
                raise ValidationError("Las coordenadas X e Y no estan dentro del distrito elegido")
        return cleaned_data

    def clean_ubicacion(self):
        ubicacion = self.cleaned_data['ubicacion']
        if self.cleaned_data.has_key('distrito'):
            distrito = self.cleaned_data['distrito']
            if not distrito.geom.contains(ubicacion):
                raise ValidationError("El punto escogido no esta dentro del distrito elegido")
        return ubicacion

    class Meta:
        model = Obra
