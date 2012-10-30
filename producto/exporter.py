# -*- coding: iso-8859-1 -*-
from django.core.exceptions import PermissionDenied
import os
import pyExcelerator as pycel
from senasaweb.export.excel import xl_write
from senasaweb.export.pdf import Caratula,NumberedCanvas,PAGE_WIDTH,PAGE_HEIGHT,Tabla,Parrafo
from parametros.models import Tipo
from types import FunctionType
from django.conf import settings
from django.template.response import TemplateResponse
from datetime import datetime
from re import match
from reportlab.platypus import SimpleDocTemplate,PageBreak
from django.db import connection

def get_field(obj,fieldname):
    global TIPOS
    traverse = fieldname.split("__")
    result = obj
    while traverse:
        result = getattr(result,traverse[0])
        traverse.remove(traverse[0])
    if match("[a-z]+_id",fieldname):
        result = TIPOS[result]
    return result if result is not None else ""

TIPOS = {}

def export_obras(modeladmin, request, queryset,processor):
    """
    Exportar productos
    """
    global TIPOS
    for row in Tipo.objects.all():
        TIPOS[row.id] = row.etiqueta

    #selected = request.POST.getlist(ACTION_CHECKBOX_NAME)

    filtro  = ""
    params = []
    if queryset is not None:
        w,params = queryset.query.where.as_sql(connection.ops.quote_name,connection)
        filtro = "WHERE " + w

    sql = (r"""
SELECT obra.id,
departamento.nombre as departamento_nombre,
obra.locacion,
distrito.codigo as distrito_id,
distrito.nombre as distrito_nombre,
proyecto.nombre as proyecto_nombre,
proceso_id,
organizacion_id,
grupo.codigo as grupo_id,
grupo.descripcion as grupo_descripcion,
producto_id,
cantidad,
poblacion,
estado as estado_descripcion
FROM obra
JOIN distrito ON distrito.codigo = obra.distrito_id
JOIN departamento ON departamento.codigo = distrito.departamento_id
JOIN grupo_obra grupo ON grupo.codigo = grupo_id
JOIN proyecto ON proyecto.id = grupo.proyecto_id
%s
ORDER BY distrito.codigo,grupo.codigo
""" % filtro)
    fields = ((u"Departamento","departamento_nombre"),
              (u"Localidad","locacion"),
              (u"Distrito","distrito_nombre"),
              (u"Nombre programa","proyecto_nombre"),
              (u"Proceso","proceso_id"),
              (u"Estado Actual","estado_descripcion"),
              (u"Tipo de organización", "organizacion_id"),
              (u"Grupo de obras","grupo_descripcion"),
              (u"Nombre producto", "producto_id"),
              (u"Cantidad de producto","cantidad"),
              (u"Población beneficiada","poblacion")
        )
    return processor(modeladmin,request,queryset,fields,sql,params)

def save_xls(modeladmin,request,queryset,fields,sql,params):
    opts = modeladmin.model._meta
    model = modeladmin.model
    wb = pycel.Workbook()
    ws = wb.add_sheet("BASE DE DATOS")
    col = 0
    rowi = 2
    # write header row
    hedsty = {"font":(("height", 260),("bold",True)),
              "border": (("bottom",pycel.Formatting.Borders.MEDIUM),
                         ("top",pycel.Formatting.Borders.MEDIUM),
                         ("right",pycel.Formatting.Borders.MEDIUM),
                         ("left",pycel.Formatting.Borders.MEDIUM)),
              "alignment":(("wrap", pycel.Alignment.WRAP_AT_RIGHT),
                           ("horz", pycel.Alignment.HORZ_CENTER),
                           ("vert", pycel.Alignment.VERT_CENTER)),
              "background":(("pattern",pycel.Formatting.Pattern.SOLID_PATTERN),
                            ("pattern_fore_colour", 24))}
    for field in fields:
        xl_write(ws,rowi,col,field[0],hedsty)
        ws.col(col).width = (25+2)*256
        col += 1

    row = rowi+1
    # Write data rows
    rwsty = {"font":(("height", 200),),
              "border": (("bottom",pycel.Formatting.Borders.THIN),
                         #("top",pycel.Formatting.Borders.THIN),
                         ("right",pycel.Formatting.Borders.THIN),
                         ("left",pycel.Formatting.Borders.THIN)),
              "alignment":(("wrap", pycel.Alignment.WRAP_AT_RIGHT),
                           ("horz", pycel.Alignment.HORZ_LEFT),
                           ("vert", pycel.Alignment.VERT_TOP))}
    for obj in model.objects.raw(sql,params):
        col = 0
        for field in fields:
            if type(field[1]) == FunctionType:
                xl_write(ws,row,col,field[1](obj),rwsty)
            else:
                xl_write(ws,row,col,get_field(obj,field[1]),rwsty)
            col += 1
        row += 1

    now = datetime.now()
    filename = "%s_%s.xls" % (unicode(opts).replace(".","_"),now.strftime("%d-%m-%Y_%H%M%S"))
    wb.save(os.path.join(settings.DOWNLOAD_DIR,filename))
    return {'filename':filename,'type':'xls'}

def save_pdf(modeladmin,request,queryset,fields,sql,params):
    opts = modeladmin.model._meta
    model = modeladmin.model
    hData = []
    for field in fields:
        hData.append(Parrafo(field[0]))
    lastDpto = ""
    data = []
    elements = []
    rows = 1
    fistDpto = ""
    for obj in model.objects.raw(sql,params):
        rwData = []
        for field in fields:
            if type(field[1]) == FunctionType:
                valor = field[1](obj)
            else:
                valor = get_field(obj,field[1])
            rwData.append(valor)
        if lastDpto != rwData[0]:
            if lastDpto != "":
                if lastDpto != fistDpto:
                    elements.append(PageBreak())
                elements.append(Caratula(lastDpto,settings.CONFIG_DIR))
                elements.append(PageBreak())
                elements.append(Tabla(data,rows,len(fields)))
            else:
                fistDpto = rwData[0]
            data = [hData]
            lastDpto = rwData[0]
            rows = 1
        data.append(map(lambda i : Parrafo(i), rwData))
        rows += 1
    if lastDpto != fistDpto and fistDpto != "":
        elements.append(PageBreak())
    elements.append(Caratula(lastDpto,settings.CONFIG_DIR))
    elements.append(PageBreak())
    elements.append(Tabla(data,rows,len(fields)))
    now = datetime.now()
    filename = "%s_%s.pdf" % (unicode(opts).replace(".","_"),now.strftime("%d-%m-%Y_%H%M%S"))
    doc = SimpleDocTemplate(os.path.join(settings.DOWNLOAD_DIR,filename),pagesize=(PAGE_HEIGHT,PAGE_WIDTH))
    doc.build(elements,canvasmaker=NumberedCanvas)
    return {'filename':filename,'type':'pdf'}


def export_obras_xls(modeladmin, request, queryset):
    if not request.user.is_staff or not modeladmin.has_change_permission(request):
        raise PermissionDenied
    ctx = export_obras(modeladmin,request,queryset,save_xls)
    ctx['title'] = 'Descarga de archivos'
    return TemplateResponse(request, "admin/descargas.html",ctx,current_app=modeladmin.admin_site.name)
export_obras_xls.short_description = "Exportar seleccionados a Excel"

def export_obras_pdf(modeladmin, request, queryset):
    if not request.user.is_staff or not modeladmin.has_change_permission(request):
        raise PermissionDenied
    ctx = export_obras(modeladmin,request,queryset,save_pdf)
    ctx['title'] = 'Descarga de archivos'
    return TemplateResponse(request, "admin/descargas.html",ctx,current_app=modeladmin.admin_site.name)
export_obras_pdf.short_description = "Exportar seleccionados a PDF"