# -*- coding: iso-8859-1 -*-
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User as Usuario
from django.core.validators import RegexValidator

class Departamento(gismodels.Model):
    codigo = models.IntegerField(u"c�digo",primary_key=True)
    nombre = models.CharField(u"nombre",max_length=150)
    geom = gismodels.PolygonField(u"ubicaci�n geogr�fica",srid=32721)
    objects = gismodels.GeoManager()

    def get_extent(self):
        return self.geom.extent

    def __unicode__(self):
        return u"[%d] %s" % (self.codigo, self.nombre)

    class Meta:
        verbose_name = "departamento"
        verbose_name_plural = "departamentos"
        db_table = "departamento"
        ordering = ["codigo"]

class Distrito(gismodels.Model):
    codigo = models.CharField(u"c�digo",primary_key=True,max_length=4,editable=False)
    nombre = models.CharField(u"nombre",max_length=150)
    geom = gismodels.PolygonField(u"ubicaci�n geogr�fica",srid=32721)
    departamento = models.ForeignKey(Departamento, verbose_name="departamento",on_delete=models.PROTECT)
    objects = gismodels.GeoManager()

    def get_extent(self):
        return self.geom.extent

    def __unicode__(self):
        return u"[%s] %s" % (self.codigo, self.nombre)

    class Meta:
        verbose_name = "distrito"
        verbose_name_plural = "distritos"
        db_table = "distrito"
        ordering = ["codigo"]

    def save(self, *args, **kwargs):
        if self.codigo == None:
            self.codigo = "%02d%02d" % (self.departamento_id,
                                        self.objects.filter(departamento_id__exact=self.departamento_id)
                                                    .aggregate(models.Count("codigo"))["codigo_count"] + 1)
        super(Distrito, self).save(*args, **kwargs)

class Localidad(gismodels.Model):
    codigo = models.CharField(u"c�digo",primary_key=True,max_length=8,editable=False)
    nombre = models.CharField(u"nombre",max_length=150)
    geom = gismodels.PolygonField(u"ubicaci�n geogr�fica",srid=32721)
    distrito = models.ForeignKey(Distrito, verbose_name="distrito",on_delete=models.PROTECT)
    objects = gismodels.GeoManager()

    def get_extent(self):
        return self.geom.extent

    def __unicode__(self):
        return u"[%s] %s" % (self.codigo, self.nombre)

    class Meta:
        verbose_name = "localidad"
        verbose_name_plural = "localidades"
        db_table = "localidad"
        ordering = ["codigo"]

    def save(self, *args, **kwargs):
        if self.codigo == None:
            self.codigo = "%s%03d" % (self.distrito_id,
                                      self.objects.filter(distrito_id__exact=self.distrito_id)
                                                  .aggregate(models.Count("codigo"))["codigo_count"] + 1)
        super(Localidad, self).save(*args, **kwargs)

class Proyecto(models.Model):
    nombre = models.CharField(u"nombre de programa", max_length=30)
    descripcion = models.TextField(u"descripci�n",null=True,max_length=200,help_text="Resumen descriptivo del proyecto")
    presupuesto = models.DecimalField(u"presupuesto previsto",max_digits=15,decimal_places=2,default=0)
    ejecutado = models.DecimalField(u"presupuesto ejecutado",max_digits=15,decimal_places=2,default=0)
    moneda = models.CharField(u"moneda",max_length=3,choices=(("USD",u"Dolares"),("PYG",u"Guaran�es")),default="USD",null=True)

    def __unicode__(self):
        return u"[%d] %s" % (self.id, self.nombre)

    class Meta:
        verbose_name = u"proyecto de inversi�n"
        verbose_name_plural = u"proyectos de inversi�n"
        db_table = "proyecto"

class Contacto(models.Model):
    cedula = models.IntegerField(u"c�dula de identidad",primary_key=True)
    nombres = models.CharField("nombres",max_length=60)
    apellidos = models.CharField("apellidos",max_length=80)
    telefono_celular = models.CharField("celular", max_length=15,validators=[RegexValidator("09[6789]\d{7,7}")],
        help_text=u"introduzca el n�mero de telefono. Ej 0981321123")

    def __unicode__(self):
        return u"[%d] %s %s" % (self.cedula, self.nombres, self.apellidos)

    class Meta:
        verbose_name = "contacto"
        verbose_name_plural = "contactos"
        db_table = "contacto"

class Grupo(models.Model):
    codigo = models.CharField(u"c�digo",max_length=30,null=True,blank=True)
    descripcion = models.TextField(u"descripci�n",max_length=200,help_text="Resumen descriptivo del grupo")
    llamado = models.IntegerField("identificador de llamado",null=True,blank=True)
    proyecto = models.ForeignKey(Proyecto, verbose_name=u"proyecto de inversi�n",on_delete=models.PROTECT)
    contacto = models.ForeignKey(Contacto, verbose_name=u"contacto",on_delete=models.PROTECT, null=True,blank=True)

    def __unicode__(self):
        return u"[%d] %s" % (self.id, self.descripcion)

    class Meta:
        verbose_name = u"grupo de obras"
        verbose_name_plural = u"grupos de obras"
        db_table = "grupo_obra"
        ordering = ('id',)

class Miembro(models.Model):
    grupo = models.ForeignKey(Grupo,verbose_name=u"grupo de obras",on_delete=models.PROTECT)
    usuario = models.ForeignKey(Usuario, verbose_name=u"miembro",on_delete=models.PROTECT)
    responsable = models.BooleanField(u"responsable del grupo",default=False)

    def __unicode__(self):
        return u"Relaci�n miembro (%d, %d)" % (self.grupo_id, self.usuario_id)

    class Meta:
        verbose_name = u"miembro"
        verbose_name_plural = u"miembros"
        db_table = "miembro"
        unique_together = ('grupo', 'usuario')

class Categoria(models.Model):
    codigo = models.CharField(u"c�digo",max_length=3,primary_key=True)
    nombre = models.CharField(u"nombre de categor�a", max_length=80)

    def __unicode__(self):
        return u"[%s] %s" % (self.codigo, self.nombre)

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"
        db_table = "categoria"

class Tipo(models.Model):
    (TIPO_SITUACION,
     TIPO_PROCESO,
     TIPO_ORGANIZACION,
     TIPO_PRODUCTO,
     TIPO_POBLACION,
        ) = ("SJS","PRO","ORG","PRD","POB")
    etiqueta = models.CharField(u"etiqueta",max_length=50)
    orden = models.SmallIntegerField(u"secuencia")
    categoria = models.ForeignKey(Categoria, verbose_name=u"categor�a",on_delete=models.PROTECT)

    def __unicode__(self):
        return u"[%d] %s - %s " % (self.id, self.etiqueta, self.categoria_id)

    class Meta:
        verbose_name = "tipo"
        verbose_name_plural = "tipos"
        db_table = "tipo"
        ordering = ['orden','categoria']
