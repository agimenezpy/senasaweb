# -*- coding: iso-8859-1 -*-
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User
from parametros.models import *
from datetime import datetime

class Obra(gismodels.Model):
    localidad = models.ForeignKey(Localidad, verbose_name="localidad",on_delete=models.PROTECT)
    inicio = models.DateField("inicio de actividades")
    fin = models.DateField("fin de las actividades")
    proceso = models.ForeignKey(Tipo, verbose_name="proceso",related_name="+",
        limit_choices_to={'categoria__exact' : Tipo.TIPO_PROCESO})
    porcentaje = models.IntegerField("porcentaje de avance", default=0)
    coordenada_x = models.FloatField("coordenada x",default=0)
    coordenada_y = models.FloatField("coordenada y",default=0)
    ubicacion = gismodels.PointField(u"ubicación geográfica",srid=32721,null=True,blank=True)
    junta = models.ForeignKey(Tipo, verbose_name=u"situación de junta",related_name="+",
        limit_choices_to={'categoria__exact' : Tipo.TIPO_SITUACION})
    organizacion = models.ForeignKey(Tipo, verbose_name=u"tipo de organización",related_name="+",
        limit_choices_to={'categoria__exact' : Tipo.TIPO_ORGANIZACION})
    grupo = models.ForeignKey(Grupo, verbose_name="grupo de obras")
    producto = models.ForeignKey(Tipo, verbose_name="nombre de producto",related_name="+",
        limit_choices_to={'categoria__exact' : Tipo.TIPO_PRODUCTO})
    cantidad = models.IntegerField("cantidad de producto", default=0)
    poblacion = models.IntegerField(u"población beneficiada", default=0)
    tipo_poblacion = models.ForeignKey(Tipo, verbose_name=u"tipo de población",related_name="+",
        limit_choices_to={'categoria__exact' : Tipo.TIPO_POBLACION})
    propietario = models.ForeignKey(User, verbose_name="propietario",null=True)
    objects = gismodels.GeoManager()

    def __unicode__(self):
        return u"[%s] %s" % (self.id, self.producto.etiqueta)

    class Meta:
        db_table = "obra"
        verbose_name = "obra de infraestructura"
        verbose_name_plural = "obras de infraestructura"
        ordering = ('id',)

class Estado(models.Model):
    descripcion = models.TextField(u"descripción",max_length=200)
    fecha_insercion = models.DateTimeField("insertado")
    fecha_actualizacion = models.DateTimeField("actualizado")
    autor = models.ForeignKey(User, verbose_name="autor")
    obra = models.ForeignKey(Obra, verbose_name="obra")

    def __unicode__(self):
        return u"[%s] %s" % (self.id, self.descripcion)

    def save(self, force_insert=False, force_update=False, using=None):
        self.autor = self.obra.salva
        if getattr(self, 'id', None) is None:
            self.fecha_insercion = datetime.now()
        self.fecha_actualizacion = datetime.now()
        super(Estado, self).save(force_insert, force_update, using)

    class Meta:
        db_table = "estado"
        verbose_name = "estado"
        verbose_name_plural = "estados"