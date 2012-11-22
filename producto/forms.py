from django.forms import ModelForm,ValidationError
from django.contrib.gis.geos import Point
from producto.models import Obra,Junta

class ObraForm(ModelForm):
    def clean_localidad(self):
        localidad = self.cleaned_data['localidad']
        if self.cleaned_data.has_key('distrito') and localidad is not None:
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
        if self.cleaned_data.has_key('distrito') and ubicacion is not None:
            distrito = self.cleaned_data['distrito']
            if not distrito.geom.contains(ubicacion):
                raise ValidationError("El punto escogido no esta dentro del distrito elegido")
        return ubicacion

    def clean_junta(self):
        junta = self.cleaned_data['junta']
        if self.cleaned_data.has_key('tipo_junta') and junta is None:
            tipo_junta = self.cleaned_data['tipo_junta']
            if tipo_junta is not None and tipo_junta.id == 1:
                raise ValidationError("Debe especificar la referencia a la junta conformada")
        return junta

    def clean_grupo(self):
        grupo = self.cleaned_data['grupo']
        if self.cleaned_data.has_key('proceso') and grupo is None:
            proceso = self.cleaned_data['proceso']
            if proceso is not None and proceso.id != 19:
                raise ValidationError("Debe especificar un grupo si esta obra no es una solicitud")
        return grupo

    class Meta:
        model = Obra


class JuntaForm(ModelForm):
    def clean_localidad(self):
        localidad = self.cleaned_data['localidad']
        if self.cleaned_data.has_key('distrito') and localidad is not None:
            distrito = self.cleaned_data['distrito']
            if localidad.distrito_id != distrito.codigo:
                raise ValidationError("La localidad no pertenece al distrito")
        return localidad

    class Meta:
        model = Junta