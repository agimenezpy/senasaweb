# -*- coding: iso-8859-1 -*-
from django.db import models
from django.contrib.gis.db import models as gismodels
from seguridad.models import Usuario

class Departamento(gismodels.Model):
    codigo = models.IntegerField(u"código",primary_key=True)
    nombre = models.CharField(u"nombre",max_length=150)
    geom = gismodels.PolygonField(u"ubicación geográfica",srid=32721)
    objects = gismodels.GeoManager()

    def __unicode__(self):
        return u"[%d] %s" % (self.codigo, self.nombre)

    class Meta:
        verbose_name = "departamento"
        verbose_name_plural = "departamentos"
        db_table = "departamento"
        ordering = ["codigo"]

class Distrito(gismodels.Model):
    codigo = models.CharField(u"código",primary_key=True,max_length=4)
    nombre = models.CharField(u"nombre",max_length=150)
    geom = gismodels.PolygonField(u"ubicación geográfica",srid=32721)
    departamento = models.ForeignKey(Departamento, verbose_name="departamento",on_delete=models.DO_NOTHING)
    objects = gismodels.GeoManager()

    def __unicode__(self):
        return u"[%s] %s" % (self.codigo, self.nombre)

    class Meta:
        verbose_name = "distrito"
        verbose_name_plural = "distritos"
        db_table = "distrito"
        ordering = ["codigo"]

    def save(self, *args, **kwargs):
        if self.codigo == None:
            self.codigo = "%02d%02d" % (self.departamento_id, self.objects.aggregate(models.Max("")) + 1)
        super(Distrito, self).save(*args, **kwargs)

class Localidad(gismodels.Model):
    codigo = models.CharField(u"código",primary_key=True,max_length=4)
    nombre = models.CharField(u"nombre",max_length=150)
    geom = gismodels.PolygonField(u"ubicación geográfica",srid=32721)
    distrito = models.ForeignKey(Distrito, verbose_name="distrito",on_delete=models.DO_NOTHING)
    objects = gismodels.GeoManager()

    def __unicode__(self):
        return u"[%s] %s" % (self.codigo, self.nombre)

    class Meta:
        verbose_name = "localidad"
        verbose_name_plural = "localidades"
        db_table = "localidad"
        ordering = ["codigo"]

    def save(self, *args, **kwargs):
        if self.codigo == None:
            self.codigo = "%s%03d" % (self.distrito_id, self.objects.filter(distrito_id__exact=self.distrito_id).count() + 1)
        super(Localidad, self).save(*args, **kwargs)

class Proyecto(models.Model):
    nombre = models.CharField(u"nombre de programa", max_length=30)
    descripcion = models.TextField(u"Descripción",null=True,max_length=200)
    presupuesto = models.DecimalField(u"presupuesto previsto",max_digits=15,decimal_places=2,default=0)
    ejecutado = models.DecimalField(u"presupuesto ejecutado",max_digits=15,decimal_places=2,default=0)
    moneda = models.CharField(u"moneda",max_length=3,choices=(("USD",u"Dolares"),("PYG",u"Guaraníes")),default="USD",null=True)
    lider = models.ForeignKey(Usuario, verbose_name=u"responsable de proyecto", null=True,on_delete=models.DO_NOTHING)

    def __unicode__(self):
        return u"[%d] %s" % (self.id, self.nombre)

    class Meta:
        verbose_name = u"proyecto de inversión"
        verbose_name_plural = u"proyectos de inversión"
        db_table = "proyecto"

class Grupo(models.Model):
    nombre = models.CharField(u"grupo de trabajo",max_length=50)
    presupuesto = models.DecimalField(u"presupuesto previsto",max_digits=15,decimal_places=2,default=0)
    ejecutado = models.DecimalField(u"presupuesto ejecutado",max_digits=15,decimal_places=2,default=0)
    proyecto = models.ForeignKey(Proyecto, verbose_name=u"proyecto de inversión",on_delete=models.DO_NOTHING)
    miembros = models.ManyToManyField(Usuario,through='Miembro')

    def __unicode__(self):
        return u"[%d] %s" % (self.id, self.nombre)

    def monto_proyecto(self):
        return "%s %.2f" % (self.proyecto.moneda, self.presupuesto)
    monto_proyecto.admin_order_field = 'presupuesto'

    class Meta:
        verbose_name = u"grupo de obras"
        verbose_name_plural = u"grupos de obras"
        db_table = "grupo_trabajo"

class Miembro(models.Model):
    grupo = models.ForeignKey(Grupo,verbose_name=u"grupo de obras",on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, verbose_name=u"miembro",on_delete=models.DO_NOTHING)
    responsable = models.BooleanField(u"responsable del grupo",default=False)

    def __unicode__(self):
        return u"Relación miembro (%d, %d)" % (self.grupo_id, self.usuario_id)

    class Meta:
        verbose_name = u"miembro"
        verbose_name_plural = u"miembros"
        db_table = "miembro"
        unique_together = ('grupo', 'usuario')

class Categoria(models.Model):
    codigo = models.CharField(u"código",max_length=3,primary_key=True)
    nombre = models.CharField(u"nombre de categoría", max_length=80)

    def __unicode__(self):
        return u"[%s] %s" % (self.codigo, self.nombre)

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"
        db_table = "categoria"

class Tipo(models.Model):
    (TIPO_SITUACION,
     TIPO_PROCESO,
     TIPO_ESTADO,
     TIPO_ORGANIZACION,
     TIPO_PRODUCTO,
     TIPO_POBLACION,
        ) = ("SJS","PRO","EST","ORG","PRO","POB")
    etiqueta = models.CharField(u"etiqueta",max_length=50)
    orden = models.SmallIntegerField(u"secuencia")
    categoria = models.ForeignKey(Categoria, verbose_name=u"categoría",on_delete=models.DO_NOTHING)

    def __unicode__(self):
        return u"[%d] %s = %s " % (self.id, self.nombre, self.categoria_id)

    class Meta:
        verbose_name = "tipo"
        verbose_name_plural = "tipos"
        db_table = "tipo"
        ordering = ['orden','categoria']
