# -*- coding: iso-8859-1 -*-
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User
from parametros.models import *

class Obra(gismodels.Model):
    descripcion = models.TextField(u"descripción",max_length=200)
    localidad = models.ForeignKey(Localidad, verbose_name="localidad",on_delete=models.PROTECT)
    programa = models.ForeignKey(Proyecto, verbose_name=u"nombre de programa")
    inicio = models.DateField("inicio de actividades")
    fin = models.DateField("fin de las actividades")
    proceso = models.ForeignKey(Tipo, verbose_name="proceso",related_name="+",
        limit_choices_to={'categoria__exact' : Tipo.TIPO_PROCESO})
    estado = models.ForeignKey(Tipo, verbose_name="estado actual",related_name="+",
        limit_choices_to={'categoria__exact' : Tipo.TIPO_ESTADO})
    porcentaje = models.IntegerField("porcentaje de avance", default=0)
    coordenada_x = models.FloatField("coordenada x",default=0)
    coordenada_y = models.FloatField("coordenada y",default=0)
    ubicacion = gismodels.PointField(u"ubicación geográfica",srid=32721,null=True)
    junta = models.ForeignKey(Tipo, verbose_name=u"situación de junta",related_name="+",
        limit_choices_to={'categoria__exact' : Tipo.TIPO_SITUACION})
    organizacion = models.ForeignKey(Tipo, verbose_name=u"tipo de organización",related_name="+",
        limit_choices_to={'categoria__exact' : Tipo.TIPO_ORGANIZACION})
    grupo = models.ForeignKey(Grupo, verbose_name="grupo de obras")
    producto = models.ForeignKey(Tipo, verbose_name="nombre de producto",related_name="+",
        limit_choices_to={'categoria__exact' : Tipo.TIPO_PRODUCTO})
    cantidad = models.IntegerField("cantidad de producto", default=0)
    poblacion = models.IntegerField(u"población beneficiada", default=0)
    tipo_poblacion = models.ForeignKey(Tipo, verbose_name="nombre de producto",related_name="+",
        limit_choices_to={'categoria__exact' : Tipo.TIPO_POBLACION})
    propietario = models.ForeignKey(User, verbose_name="propietario")

    class Meta:
        db_table = "obra"
        verbose_name = "obra de infraestructura"
        verbose_name_plural = "obras de infraestructura"

class Commentario(models.Model):
    descripcion = models.TextField("commentarios",max_length=200)
    fecha_insercion = models.DateTimeField("insertado")
    fecha_actualizacion = models.DateTimeField("actualizado")
    autor = models.ForeignKey(User,verbose_name="autor")
    obra = models.ForeignKey(Obra, verbose_name="relacionado")

    class Meta:
        db_table = "comentario"
        verbose_name = "comentario"
        verbose_name_plural = "comentarios"