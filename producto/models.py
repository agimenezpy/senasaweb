# -*- coding: iso-8859-1 -*-
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User
from parametros.models import *
from datetime import datetime
from django.core.validators import RegexValidator

class Obra(gismodels.Model):
    codigo = models.CharField("codigo",max_length=20,unique=True,editable=False)
    distrito = models.ForeignKey(Distrito, verbose_name="distrito",to_field="codigo",on_delete=models.PROTECT)
    localidad = models.ForeignKey(Localidad, verbose_name=u"barrio/compañia",to_field="codigo",on_delete=models.PROTECT,null=True,blank=True)
    locacion = models.CharField(u"localidad",max_length=150)
    fecha_inicio = models.DateField("inicio de obra")
    inicio = models.DateField("inicio de actividades")
    fin = models.DateField("fin de las actividades")
    proceso = models.ForeignKey(Tipo, verbose_name="proceso",related_name="+",
        limit_choices_to={'categoria__exact' : Tipo.TIPO_PROCESO})
    estado = models.CharField("estado actual",max_length=200)
    porcentaje = models.IntegerField("porcentaje de avance", default=0)
    coordenada_x = models.FloatField("coordenada x",default=0)
    coordenada_y = models.FloatField("coordenada y",default=0)
    ubicacion = gismodels.PointField(u"ubicación geográfica",srid=32721,null=True,blank=True)
    junta = models.ForeignKey(Tipo, verbose_name=u"situación de junta",related_name="+",
        limit_choices_to={'categoria__exact' : Tipo.TIPO_SITUACION},on_delete=models.PROTECT)
    organizacion = models.ForeignKey(Tipo, verbose_name=u"tipo de organización",related_name="+",
        limit_choices_to={'categoria__exact' : Tipo.TIPO_ORGANIZACION},on_delete=models.PROTECT)
    grupo = models.ForeignKey(Grupo, verbose_name="grupo de obras",to_field='codigo',on_delete=models.PROTECT,null=True,blank=True)
    producto = models.ForeignKey(Tipo, verbose_name="nombre de producto",related_name="+",
        limit_choices_to={'categoria__exact' : Tipo.TIPO_PRODUCTO},on_delete=models.PROTECT)
    cantidad = models.IntegerField("cantidad de producto", default=0)
    poblacion = models.IntegerField(u"población beneficiada", default=0)
    tipo_poblacion = models.ForeignKey(Tipo, verbose_name=u"tipo de población",related_name="+",
        limit_choices_to={'categoria__exact' : Tipo.TIPO_POBLACION},on_delete=models.PROTECT)
    propietario = models.ForeignKey(User, verbose_name="creado por",null=True,on_delete=models.PROTECT,related_name="+")
    modifica = models.ForeignKey(User, verbose_name="modificado por",null=True,on_delete=models.PROTECT,editable=False,related_name="+")
    creado = models.DateField("fecha de creacion",editable=False)
    actualizado = models.DateField(u"fecha de actualización",editable=False)
    objects = gismodels.GeoManager()

    def save(self, *args, **kwargs):
        ahora = datetime.now()
        if self.codigo == "" and self.grupo_id is not None:
            self.codigo = "%s%03d" % (self.grupo.codigo,
                                      Obra.objects.filter(grupo_id__exact=self.grupo_id)
                                      .aggregate(models.Count("codigo"))["codigo__count"] + 1)
        elif self.grupo_id is None:
            self.codigo = "%d" % (Obra.objects.all().aggregate(models.Max("id"))["id__max"] + 1)
        if getattr(self, 'id', None) is None:
            self.creado = ahora
        self.actualizado = ahora
        super(Obra, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"[%s] (%d) %s" % (self.codigo, self.cantidad, self.producto.etiqueta)

    class Meta:
        db_table = "obra"
        verbose_name = "obra"
        verbose_name_plural = "obras"
        ordering = ('id',)
        permissions = (('view_obra','Can view obra'),)

class Estado(models.Model):
    descripcion = models.TextField(u"descripción",max_length=200)
    fecha_insercion = models.DateTimeField("insertado")
    fecha_actualizacion = models.DateTimeField("actualizado")
    autor = models.ForeignKey(User, verbose_name="autor",on_delete=models.PROTECT,related_name="+")
    obra = models.ForeignKey(Obra, verbose_name="obra",to_field="codigo",on_delete=models.CASCADE,related_name="+")

    def __unicode__(self):
        return u"[%d] %s" % (self.id, self.descripcion)

    def save(self, force_insert=False, force_update=False, using=None):
        self.autor = self.obra.modifica
        ahora = datetime.now()
        if getattr(self, 'id', None) is None:
            self.fecha_insercion = ahora
        self.fecha_actualizacion = ahora
        super(Estado, self).save(force_insert, force_update, using)

    class Meta:
        db_table = "estado"
        verbose_name = "historico de estado"
        verbose_name_plural = "historico de estados"
        permissions = (('view_estado','Can view estado'),)

class Contacto(models.Model):
    cedula = models.IntegerField(u"cédula de identidad",primary_key=True)
    nombres = models.CharField("nombres",max_length=60)
    apellidos = models.CharField("apellidos",max_length=80)
    telefono_celular = models.CharField("celular", max_length=15,validators=[RegexValidator("^09[6789]\d{7,7}$")],
        help_text=u"Introduzca el número de telefono. Ej 0981321123")
    obra = models.ForeignKey(Obra, verbose_name=u"obra",on_delete=models.SET_DEFAULT, null=True,blank=True,default=None)

    def __unicode__(self):
        return u"[%d] %s %s" % (self.cedula, self.nombres, self.apellidos)

    class Meta:
        verbose_name = "contacto"
        verbose_name_plural = "contactos"
        db_table = "contacto"
        permissions = (('view_contacto','Can view contacto'),)

class Comentario(models.Model):
    descripcion = models.TextField(u"descripción",max_length=200)
    fecha_insercion = models.DateTimeField("insertado")
    fecha_actualizacion = models.DateTimeField("actualizado")
    autor = models.ForeignKey(User, verbose_name="autor",on_delete=models.PROTECT,related_name="+")
    contacto = models.ForeignKey(Contacto, verbose_name="contacto",on_delete=models.CASCADE)

    def __unicode__(self):
        return u"[%d] %s" % (self.id, self.descripcion)

    def save(self, force_insert=False, force_update=False, using=None):
        self.autor = self.contacto.modifica
        ahora = datetime.now()
        if getattr(self, 'id', None) is None:
            self.fecha_insercion = ahora
        self.fecha_actualizacion = ahora
        super(Comentario, self).save(force_insert, force_update, using)

    class Meta:
        db_table = "comentario"
        verbose_name = "comentario"
        verbose_name_plural = "comentarios"
        permissions = (('view_comentario','Can view comentario'),)