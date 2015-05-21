# -*- coding: iso-8859-1 -*-
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User
from parametros.models import *
from datetime import datetime
from django.core.validators import RegexValidator, MinValueValidator
from django.conf import settings


class Obra(gismodels.Model):
    codigo = models.CharField("codigo", max_length=20, unique=True, editable=False)
    distrito = models.ForeignKey(Distrito, verbose_name="distrito", to_field="codigo", on_delete=models.PROTECT)
    localidad = models.ForeignKey(Localidad, verbose_name=u"barrio/compañia", to_field="codigo",
                                  on_delete=models.PROTECT, null=True, blank=True)
    locacion = models.CharField(u"localidad", max_length=150)
    fecha_inicio = models.DateField("inicio de obra")
    inicio = models.DateField("inicio de actividades")
    fin = models.DateField("fin de las actividades")
    proceso = models.ForeignKey(Tipo, verbose_name="proceso", related_name="+",
                                limit_choices_to={'categoria__exact': Tipo.TIPO_PROCESO})
    estado = models.CharField("estado actual", max_length=200)
    porcentaje = models.IntegerField("porcentaje de avance", default=0)
    coordenada_x = models.FloatField("coordenada x", default=0)
    coordenada_y = models.FloatField("coordenada y", default=0)
    ubicacion = gismodels.PointField(u"ubicación geográfica", srid=32721, null=True, blank=True)
    tipo_junta = models.ForeignKey(Tipo, verbose_name=u"situación de junta", related_name="+",
                                   limit_choices_to={'categoria__exact': Tipo.TIPO_SITUACION}, on_delete=models.PROTECT)
    junta = models.ForeignKey('Junta', verbose_name="nombre de junta", null=True, blank=True)
    organizacion = models.ForeignKey(Tipo, verbose_name=u"tipo de organización", related_name="+",
                                     limit_choices_to={'categoria__exact': Tipo.TIPO_ORGANIZACION},
                                     on_delete=models.PROTECT)
    grupo = models.ForeignKey(Grupo, verbose_name="grupo de obras", to_field='codigo', on_delete=models.PROTECT,
                              null=True, blank=True)
    producto = models.ForeignKey(Tipo, verbose_name="nombre de producto", related_name="+",
                                 limit_choices_to={'categoria__exact': Tipo.TIPO_PRODUCTO}, on_delete=models.PROTECT)
    cantidad = models.IntegerField("cantidad de producto", default=0)
    poblacion = models.IntegerField(u"población beneficiada", default=0)
    conexion = models.IntegerField("cantidad de conexiones", default=0)
    tipo_poblacion = models.ForeignKey(Tipo, verbose_name=u"tipo de población", related_name="+",
                                       limit_choices_to={'categoria__exact': Tipo.TIPO_POBLACION},
                                       on_delete=models.PROTECT)
    propietario = models.ForeignKey(User, verbose_name="creado por", null=True, on_delete=models.PROTECT,
                                    related_name="+")
    modifica = models.ForeignKey(User, verbose_name="modificado por", null=True, on_delete=models.PROTECT,
                                 editable=False, related_name="+")
    creado = models.DateField("fecha de creacion", editable=False, auto_now_add=True)
    actualizado = models.DateField(u"fecha de actualización", editable=False, auto_now=True)
    presupuesto = models.DecimalField("presupuesto", max_digits=12, decimal_places=2, default=0)
    objects = gismodels.GeoManager()

    def save(self, *args, **kwargs):
        if self.grupo_id is None:
            self.codigo = "%d" % (Obra.objects.all().aggregate(models.Max("id"))["id__max"] + 1)
        elif self.codigo == "" or self.codigo.find(self.grupo.codigo) == -1:
            qty = Obra.objects.raw(
                "SELECT 0 as id, MAX(cast(regexp_replace(codigo, '" + self.grupo.codigo +
                "', '') as int)) as secuencia__max FROM " +
                self._meta.db_table
                + " WHERE grupo_id = %s", [self.grupo.codigo])[0].secuencia__max
            if qty is None:
                qty = 0
            else:
                qty += 1
            self.codigo = "%s%03d" % (self.grupo.codigo, qty)
        super(Obra, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"[%s] (%d) %s" % (self.codigo, self.cantidad, self.producto.etiqueta)

    class Meta:
        db_table = "obra"
        verbose_name = "obra"
        verbose_name_plural = "obras"
        ordering = ('id',)
        permissions = (('view_obra', 'Can view obra'),)


class Estado(models.Model):
    descripcion = models.TextField(u"descripción", max_length=200)
    fecha_insercion = models.DateTimeField("insertado", auto_now_add=True)
    fecha_actualizacion = models.DateTimeField("actualizado", auto_now=True)
    autor = models.ForeignKey(User, verbose_name="autor", on_delete=models.PROTECT, related_name="+")
    obra = models.ForeignKey(Obra, verbose_name="obra", to_field="codigo", on_delete=models.CASCADE, related_name="+")

    def __unicode__(self):
        return u"[%d] %s" % (self.id, self.descripcion)

    def save(self, force_insert=False, force_update=False, using=None):
        self.autor = self.obra.modifica
        super(Estado, self).save(force_insert, force_update, using)

    class Meta:
        db_table = "estado"
        verbose_name = "historico de estado"
        verbose_name_plural = "historico de estados"
        permissions = (('view_estado', 'Can view estado'),)


class Contacto(models.Model):
    cedula = models.IntegerField(u"cédula de identidad", primary_key=True)
    nombres = models.CharField("nombres", max_length=60)
    apellidos = models.CharField("apellidos", max_length=80)
    telefono_celular = models.CharField("celular", max_length=15, validators=[RegexValidator("^09[6789]\d{7,7}$")],
                                        help_text=u"Introduzca el número de telefono. Ej 0981321123")

    @staticmethod
    def autocomplete_search_fields():
        return ("nombres__icontains", "apellidos__icontains")

    @property
    def id(self):
        return self.cedula

    def __unicode__(self):
        return u"[%d] %s %s" % (self.cedula, self.nombres, self.apellidos)

    class Meta:
        verbose_name = "contacto"
        verbose_name_plural = "contactos"
        db_table = "contacto"
        permissions = (('view_contacto', 'Can view contacto'),)


class Comentario(models.Model):
    descripcion = models.TextField(u"descripción", max_length=200)
    fecha_insercion = models.DateTimeField("insertado", auto_now_add=True)
    fecha_actualizacion = models.DateTimeField("actualizado", auto_now=True)
    autor = models.ForeignKey(User, verbose_name="autor", on_delete=models.PROTECT, related_name="+")
    junta = models.ForeignKey('Junta', verbose_name="junta", on_delete=models.CASCADE)

    def __unicode__(self):
        return u"[%d] %s" % (self.id, self.descripcion)

    def save(self, force_insert=False, force_update=False, using=None):
        self.autor = self.junta.modifica
        super(Comentario, self).save(force_insert, force_update, using)

    class Meta:
        db_table = "comentario"
        verbose_name = "comentario"
        verbose_name_plural = "comentarios"
        permissions = (('view_comentario', 'Can view comentario'),)


class Junta(models.Model):
    nombre = models.CharField("nombre de junta", max_length=100)
    direccion = models.CharField("direccion", null=True, blank=True, max_length=100)
    telefono = models.CharField(u"teléfono", max_length=15, validators=[RegexValidator("^09[6789]\d{7,7}$")],
                                help_text=u"Introduzca el número de telefono. Ej 0981321123", null=True, blank=True)
    distrito = models.ForeignKey(Distrito, verbose_name="distrito", to_field="codigo", on_delete=models.PROTECT)
    localidad = models.ForeignKey(Localidad, verbose_name="localidad", to_field="codigo", on_delete=models.PROTECT,
                                  null=True, blank=True)
    proyecto = models.ManyToManyField(Proyecto, verbose_name="Proyectos", blank=True)
    organizacion = models.ForeignKey(Tipo, verbose_name=u"tipo de organización", related_name="+",
                                     limit_choices_to={'categoria__exact': Tipo.TIPO_ORGANIZACION},
                                     on_delete=models.PROTECT)
    tipo_junta = models.ForeignKey(Tipo, verbose_name=u"situación de junta", related_name="+",
                                   limit_choices_to={'categoria__exact': Tipo.TIPO_SITUACION}, on_delete=models.PROTECT)
    fecha_asamblea = models.DateField("fecha de asamblea constitutiva", null=True, blank=True)
    fecha_habilita = models.DateField(u"fecha de habilitación", null=True, blank=True)
    fecha_ignagura = models.DateField(u"fecha de ignaguración", null=True, blank=True)
    personeria = models.IntegerField(u"Personería Jurídica Nro", null=True, blank=True)
    miembro = models.ManyToManyField(Contacto, through='Miembro')

    @staticmethod
    def autocomplete_search_fields():
        return ("nombre__icontains",)

    def __unicode__(self):
        return u"[%d] %s" % (self.id, self.nombre)

    def related_label(self):
        return u"[%d] %s (%s - %s)" % (self.id, self.nombre, self.distrito.nombre, self.distrito.departamento.nombre)

    class Meta:
        db_table = "junta"
        verbose_name = "junta de saneamiento"
        verbose_name_plural = "juntas de saneamiento"
        permissions = (('view_junta', 'Can view junta'),)
        ordering = ('id',)


class Miembro(models.Model):
    TIPO_CARGO = ((1, "Presidente"),
                  (2, "Vice Presidente"),
                  (3, "Secretario/a"),
                  (4, "Tesorero/a"),
                  (5, "Vocal"),
                  (6, "Sindico Titular"),
                  (7, "Sindico Suplente"),
                  (8, "Vocal Titular"),
                  (9, "Vocal Suplente"))
    TIPO_GRUPO = ((1, "COMISION DIRECTIVA"),
                  (2, "SINDICATURA"),
                  (3, "T.E.I."))
    contacto = models.ForeignKey(Contacto, verbose_name="contacto")
    junta = models.ForeignKey(Junta, verbose_name="junta de saneamiento", related_name="comision_set")
    cargo = models.IntegerField("cargo", choices=TIPO_CARGO)
    grupo = models.IntegerField("grupo", choices=TIPO_GRUPO)

    def __unicode__(self):
        return u"[%d,%d] %s - %s" % (self.contacto_id, self.junta_id,
                                     self.TIPO_CARGO[self.cargo - 1][1], self.TIPO_GRUPO[self.grupo - 1][1])

    class Meta:
        db_table = "miembro_junta"
        verbose_name = "miembro de junta"
        verbose_name_plural = "miembros de junta"
        unique_together = ('junta', 'contacto')
        permissions = (('view_miembrojunta', 'Can view miembro junta'),)


class LocacionManager(models.Manager):
    def get_query_set(self):
        return super(LocacionManager, self).get_query_set() \
            .only("locacion") \
            .order_by("locacion") \
            .distinct("locacion")


class Locacion(Obra):
    objects = LocacionManager()

    def related_label(self):
        return self.locacion

    @staticmethod
    def autocomplete_search_fields():
        return ("locacion__icontains",)

    class Meta:
        proxy = True


class Hitos(models.Model):
    obra = models.OneToOneField(Obra, verbose_name="obra",
                                on_delete=models.CASCADE, editable=False, primary_key=True)
    por_hito_a = models.IntegerField("% real (1)", default=0, null=True, validators=[MinValueValidator(0)],
                                     help_text="%s (%d)" % settings.HITOS[0])
    fecha_hito_a = models.DateField("fecha de entrega (1)", null=True, blank=True)
    por_hito_b = models.IntegerField("% real (2)", default=0, null=True, validators=[MinValueValidator(0)],
                                     help_text="%s (%d)" % settings.HITOS[1])
    fecha_hito_b = models.DateField("fecha de entrega (2)", null=True, blank=True)
    por_hito_c = models.IntegerField("% real (3)", default=0, null=True, validators=[MinValueValidator(0)],
                                     help_text="%s (%d)" % settings.HITOS[2])
    fecha_hito_c = models.DateField("fecha de entrega (3)", null=True, blank=True)

    def __unicode__(self):
        return u"[%d] Hitos %d, %d, %d" % (self.obra_id, self.por_hito_a, self.por_hito_b, self.por_hito_c)

    class Meta:
        db_table = "obra_hitos"
        verbose_name = "hito"
        verbose_name_plural = "hitos"