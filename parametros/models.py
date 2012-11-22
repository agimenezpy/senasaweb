# -*- coding: iso-8859-1 -*-
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User as Usuario
from django.contrib.gis.gdal import SpatialReference

class Departamento(gismodels.Model):
    codigo = models.CharField(u"código",unique=True,max_length=2,editable=False)
    nombre = models.CharField(u"nombre de departamento",max_length=150)
    geom = gismodels.PolygonField(u"ubicación geográfica",srid=32721)
    objects = gismodels.GeoManager()

    def get_extent(self):
        wgs84 = SpatialReference('EPSG:4326')
        return self.geom.transform(wgs84,clone=True).extent

    def __unicode__(self):
        return u"[%s] %s" % (self.codigo, self.nombre)

    def save(self, *args, **kwargs):
        if self.codigo  == "":
            qty = Departamento.objects.raw("SELECT 0 as id,MAX(cast(codigo as int)) as secuencia__max FROM " +
                                        self._meta.db_table)[0].secuencia__max
            if qty is None:
                qty = 0
            else:
                qty += 1
            self.codigo= "%02d" % qty
        super(Departamento, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "departamento"
        verbose_name_plural = "departamentos"
        db_table = "departamento"
        ordering = ["codigo"]
        permissions = (('view_departamento','Can view departamento'),)

class Distrito(gismodels.Model):
    codigo = models.CharField(u"código",unique=True,max_length=4,editable=False)
    nombre = models.CharField(u"nombre de distrito",max_length=150)
    geom = gismodels.PolygonField(u"ubicación geográfica",srid=32721)
    departamento = models.ForeignKey(Departamento, verbose_name="departamento",to_field="codigo",on_delete=models.PROTECT)
    objects = gismodels.GeoManager()

    @staticmethod
    def autocomplete_search_fields():
        return ("nombre__icontains",)

    def get_extent(self):
        wgs84 = SpatialReference('EPSG:4326')
        return self.geom.transform(wgs84,clone=True).extent

    def __unicode__(self):
        return u"[%s] %s - %s" % (self.codigo, self.nombre, self.departamento.nombre)

    class Meta:
        verbose_name = "distrito"
        verbose_name_plural = "distritos"
        db_table = "distrito"
        ordering = ["codigo"]
        permissions = (('view_distrito','Can view distrito'),)

    def save(self, *args, **kwargs):
        if self.codigo  == "":
            self.codigo = "%s%02d" % (self.departamento_id,
                                        Distrito.objects.filter(departamento_id__exact=self.departamento_id)
                                                    .aggregate(models.Count("codigo"))["codigo__count"] + 1)
        super(Distrito, self).save(*args, **kwargs)

class Localidad(gismodels.Model):
    codigo = models.CharField(u"código",unique=True,max_length=8,editable=False)
    nombre = models.CharField(u"nombre",max_length=150)
    tipo = models.CharField(u"tipo",max_length=8,choices=(("RURAL","RURAL"),("URBANO","URBANO")),default="RURAL")
    geom = gismodels.PolygonField(u"ubicación geográfica",srid=32721)
    distrito = models.ForeignKey(Distrito, verbose_name="distrito",to_field="codigo",on_delete=models.PROTECT)
    objects = gismodels.GeoManager()

    @staticmethod
    def autocomplete_search_fields():
        return ("nombre__icontains",)

    def get_extent(self):
        wgs84 = SpatialReference('EPSG:4326')
        return self.geom.transform(wgs84,clone=True).extent

    def __unicode__(self):
        return u"[%s] %s" % (self.codigo, self.nombre)

    class Meta:
        verbose_name = "localidad"
        verbose_name_plural = "localidades"
        db_table = "localidad"
        ordering = ["codigo"]
        permissions = (('view_localidad','Can view localidad'),)

    def save(self, *args, **kwargs):
        if self.codigo is None or len(self.codigo) == 0:
            self.codigo = "%s%03d" % (self.distrito_id,
                                      Localidad.objects.filter(distrito_id__exact=self.distrito_id)
                                                  .aggregate(models.Count("codigo"))["codigo__count"] + 1)
        super(Localidad, self).save(*args, **kwargs)

class Proyecto(models.Model):
    codigo = models.CharField(u"código",max_length=10,unique=True)
    nombre = models.CharField(u"nombre de programa", max_length=30)
    descripcion = models.TextField(u"descripción",null=True,max_length=200,help_text="Resumen descriptivo del proyecto")
    presupuesto = models.DecimalField(u"presupuesto previsto",max_digits=15,decimal_places=2,default=0)
    ejecutado = models.DecimalField(u"presupuesto ejecutado",max_digits=15,decimal_places=2,default=0)
    moneda = models.CharField(u"moneda",max_length=3,choices=(("USD",u"Dolares"),("PYG",u"Guaraníes")),default="USD",null=True)

    def __unicode__(self):
        return u"[%d] %s" % (self.id, self.nombre)

    class Meta:
        verbose_name = u"proyecto de inversión"
        verbose_name_plural = u"proyectos de inversión"
        db_table = "proyecto"
        permissions = (('view_proyecto','Can view proyecto'),)

class Grupo(models.Model):
    codigo = models.CharField(u"código",max_length=30,unique=True)
    descripcion = models.TextField(u"descripción",max_length=200,help_text="Resumen descriptivo del grupo")
    llamado = models.IntegerField("identificador de llamado",null=True,blank=True)
    proyecto = models.ForeignKey(Proyecto, verbose_name=u"proyecto de inversión",on_delete=models.PROTECT)

    def __unicode__(self):
        return u"[%s] %s" % (self.codigo, self.descripcion)

    def save(self, *args, **kwargs):
        if self.codigo is None or len(self.codigo) == 0:
            self.codigo = "%s%02d" % (self.proyecto.codigo,
                                      Grupo.objects.filter(proyecto_id__exact=self.proyecto_id)
                                      .aggregate(models.Count("codigo"))["codigo__count"] + 1)
        super(Grupo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"grupo de obras"
        verbose_name_plural = u"grupos de obras"
        db_table = "grupo_obra"
        ordering = ['id']
        permissions = (('view_grupo','Can view grupo'),)

class Miembro(models.Model):
    proyecto = models.ForeignKey(Proyecto,verbose_name=u"proyecto",on_delete=models.PROTECT)
    usuario = models.ForeignKey(Usuario, verbose_name=u"miembro",on_delete=models.PROTECT)
    responsable = models.BooleanField(u"responsable del proyecto",default=False)

    def __unicode__(self):
        return u"Relación miembro (%d, %d)" % (self.proyecto_id, self.usuario_id)

    class Meta:
        verbose_name = u"miembro"
        verbose_name_plural = u"miembros"
        db_table = "miembro"
        unique_together = ('proyecto', 'usuario')
        permissions = (('view_miembro','Can view miembro'),)

class Categoria(models.Model):
    codigo = models.CharField(u"código",max_length=3,primary_key=True)
    nombre = models.CharField(u"nombre de categoría", max_length=80)

    def __unicode__(self):
        return u"[%s] %s" % (self.codigo, self.nombre)

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"
        db_table = "categoria"
        permissions = (('view_categoria','Can view categoria'),)

class Tipo(models.Model):
    (TIPO_SITUACION,
     TIPO_PROCESO,
     TIPO_ORGANIZACION,
     TIPO_PRODUCTO,
     TIPO_POBLACION,
     TIPO_CARGO,
     TIPO_GRMI
        ) = ("SJS","PRO","ORG","PRD","POB","CRG","GRM")
    etiqueta = models.CharField(u"etiqueta",max_length=50)
    orden = models.SmallIntegerField(u"secuencia")
    categoria = models.ForeignKey(Categoria, verbose_name=u"categoría",on_delete=models.PROTECT)

    def __unicode__(self):
        return u"[%d] %s - %s " % (self.id, self.etiqueta, self.categoria_id)

    class Meta:
        verbose_name = "tipo"
        verbose_name_plural = "tipos"
        db_table = "tipo"
        ordering = ['orden','categoria']
        permissions = (('view_tipo','Can view tipo'),)