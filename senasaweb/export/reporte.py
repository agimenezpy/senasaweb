# -*- coding: iso-8859-1
from re import match

from geraldo.generators import PDFGenerator
from geraldo import Report, ReportBand, Label, ObjectValue, SystemField,\
FIELD_ACTION_COUNT, FIELD_ACTION_SUM, BAND_WIDTH, Line, ReportGroup, landscape
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm,inch
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY

from producto.exporter import get_field

class ReporteObras(Report):
    title = u"SENASA: Reporte de Obras"
    page_size = landscape(A4)

    class band_summary(ReportBand):
        height = 0.8*cm
        elements = [
            Label(text=u"Cantidad de obras:", top=0.1*cm, left=0),
            ObjectValue(attribute_name='id', top=0.1*cm, left=4*cm,
                action=FIELD_ACTION_COUNT, display_format='%s obras encontradas'),
            ]
        borders = {'all': True}

    class band_page_header(ReportBand):
        height = 1.6*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 18, 'alignment': TA_CENTER}),
            Label(text=u"Localidad", top=0.8*cm, left=0, width=1.1*inch),
            Label(text=u"Nombre programa", top=0.8*cm, left=1.1*inch,width=0.7*inch),
            Label(text=u"Inicio", top=0.8*cm, left=1.8*inch,width=0.8*inch),
            Label(text=u"Fin", top=0.8*cm, left=2.6*inch,width=0.8*inch),
            Label(text=u"Proceso", top=0.8*cm, left=3.4*inch,width=0.7*inch),
            Label(text=u"Estado Actual", top=0.8*cm, left=4.1*inch, width=0.7*inch),
            Label(text=u"Porcentaje", top=0.8*cm, left=4.8*inch,width=1.5*inch),
            Label(text=u"Coord. X", top=0.8*cm, left=6.3*inch,width=0.8*inch),
            Label(text=u"Coord. Y", top=0.8*cm, left=7.1*inch,width=0.8*inch),
            Label(text=u"Tipo de organización", top=0.8*cm, left=7.9*inch,width=0.8*inch),
            Label(text=u"Situación de junta", top=0.8*cm, left=8.7*inch,width=0.8*inch),
            Label(text=u"Grupo de obras", top=0.8*cm, left=9.5*inch,width=0.8*inch),
            Label(text=u"Nombre producto", top=0.8*cm, left=10.3*inch,width=1.3*inch),
            Label(text=u"Cantidad de producto", top=0.8*cm, left=11.6*inch,width=1*inch),
            Label(text=u"Tipo de población", top=0.8*cm, left=12.6*inch,width=0.8*inch),
            Label(text=u"Población beneficiada", top=0.8*cm, left=13.4*inch,width=0.8*inch),
            Label(text=u"Observación", top=0.8*cm, left=14.2*inch,width=0.8*inch),
            ]
        #borders = {'bottom': Line(stroke_color=red, stroke_width=3)}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            SystemField(expression=u"Página # %(page_number)d de %(page_count)d", top=0.8*cm,
                width=BAND_WIDTH, style={'alignment': TA_CENTER}),
            ]
        #borders = {'top': Line(stroke_color=navy)}

    class band_detail(ReportBand):
        height = 0.7*cm
        auto_expand_height = True
        elements = [
            ObjectValue(attribute_name='locacion', top=0, width=1.1*inch),
            ObjectValue(attribute_name='proyecto_nombre', top=0, width=0.7*inch),
            ObjectValue(attribute_name='inicio', top=0, width=0.8*inch,
                get_value=lambda inst: inst.inicio.strftime('%d/%m/%Y')),
            ObjectValue(attribute_name='fin', top=0, width=0.8*inch,
                get_value=lambda inst: inst.fin.strftime('%d/%m/%Y')),
            ObjectValue(attribute_name='proceso_id', top=0, width=0.7*inch,
                get_value=lambda inst: get_field(inst,"proceso_id")),
            ObjectValue(attribute_name='estado_descripcion', top=0, left=0.7*inch),
            ObjectValue(attribute_name='procentaje', top=0, left=1.5*inch,
                get_value=lambda inst: "%d %%" % inst.porcentaje),
            ObjectValue(attribute_name='coordenada_x', top=0, left=0.8*inch),
            ObjectValue(attribute_name='coordenada_y', top=0, left=0.8*inch),
            ObjectValue(attribute_name='organizacion_id', top=0, left=0.8*inch,
                get_value=lambda inst: get_field(inst,"organizacion_id")),
            ObjectValue(attribute_name='tipo_junta_id', top=0, left=0.8*inch,
                get_value=lambda inst: get_field(inst,"tipo_junta_id")),
            ObjectValue(attribute_name='grupo_descripcion', top=0, left=0.8*inch),
            ObjectValue(attribute_name='producto_id', top=0, left=1.3*inch,
                get_value=lambda inst: get_field(inst,"producto_id")),
            ObjectValue(attribute_name='cantidad', top=0, left=1*inch),
            ObjectValue(attribute_name='tipo_poblacion_id', top=0, left=0.8*inch,
                get_value=lambda inst: get_field(inst,"tipo_poblacion_id")),
            ObjectValue(attribute_name='poblacion', top=0, left=0.8*inch),
            ObjectValue(attribute_name='observacion', top=0, left=0.8*inch)
            ]

    groups = [
        ReportGroup(attribute_name='departamento_nombre',
            band_header=ReportBand(
                height=1.3*cm,
                elements=[
                    ObjectValue(attribute_name='departamento_nombre', left=0, top=0.1*cm,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 24})
                ],
                #borders={'bottom': True},
            ),
            band_footer=ReportBand(
                height=0.7*cm,
                elements=[
                    ObjectValue(attribute_name='id', action=FIELD_ACTION_COUNT,
                        display_format='%s departamentos', left=0*cm, top=0.1*cm),
                    ObjectValue(attribute_name='cantidad', action=FIELD_ACTION_SUM,
                        display_format=u"%s población beneficiada", left=4*cm, top=0.1*cm),
                    ],
                borders={'top': True},
            ),
        ),
        ReportGroup(attribute_name='distrito_nombre',
            band_header=ReportBand(
                height=0.7*cm,
                elements=[
                    ObjectValue(attribute_name='distrito_nombre', left=0.5*cm, top=0.1*cm)
                ],
                borders={'bottom': True},
            ),
            band_footer=ReportBand(
                height=0.7*cm,
                elements=[
                    ObjectValue(attribute_name='id', action=FIELD_ACTION_COUNT,
                        display_format='%s distritos', left=0.5*cm, top=0.1*cm),
                    ObjectValue(attribute_name='cantidad', action=FIELD_ACTION_SUM,
                        display_format=u"%s población beneficiada", left=4*cm, top=0.1*cm),
                ],
                borders={'top': True},
            ),
        ),
        ]

    def generar(self,filename):
        self.generate_by(PDFGenerator,filename=filename)