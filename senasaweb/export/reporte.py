# -*- coding: iso-8859-1
from re import match

from geraldo.generators import PDFGenerator
from geraldo import Report, ReportBand, Label, ObjectValue, SystemField,\
FIELD_ACTION_COUNT, FIELD_ACTION_SUM, BAND_WIDTH, Line, ReportGroup, landscape
from reportlab.lib.pagesizes import A4,LEGAL
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY,TA_RIGHT

from producto.exporter import get_field

PORC = (
    0.07,0.055,0.04,0.04,0.055,0.055,0.04,0.055,0.055,0.06,0.06,0.07,0.07,0.04,0.04,0.04,0.10
)
PGW = LEGAL[1]
WS = map(lambda i: i*PGW, PORC)
LS = [0]
LS.extend([sum(WS[:i]) for i in range(1,len(WS))])
styb = {'fontSize':8,'fontName':'Helvetica-Bold'}
styr = {'fontSize':8,'alignment':TA_CENTER}
styww = {'fontSize':8,'wordWrap':True}
sty = {'fontSize':8}
class ReporteObras(Report):
    title = u"SENASA: Reporte de Obras"
    page_size = landscape(LEGAL)

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
            Label(text=u"Localidad", top=0.8*cm, left=LS[0], width=WS[0],style=styb),
            Label(text=u"Nombre programa", top=0.8*cm, left=LS[1],width=WS[1],style=styb),
            Label(text=u"Inicio", top=0.8*cm, left=LS[2],width=WS[2],style=styb),
            Label(text=u"Fin", top=0.8*cm, left=LS[3],width=WS[3],style=styb),
            Label(text=u"Proceso", top=0.8*cm, left=LS[4],width=WS[4],style=styb),
            Label(text=u"Estado Actual", top=0.8*cm, left=LS[5],width=WS[5],style=styb),
            Label(text=u"Porcentaje", top=0.8*cm, left=LS[6],width=WS[6],style=styb),
            Label(text=u"Coord. X", top=0.8*cm, left=LS[7],width=WS[7],style=styb),
            Label(text=u"Coord. Y", top=0.8*cm, left=LS[8],width=WS[8],style=styb),
            Label(text=u"Tipo de organización", top=0.8*cm, left=LS[9],width=WS[9],style=styb),
            Label(text=u"Situación de junta", top=0.8*cm, left=LS[10],width=WS[10],style=styb),
            Label(text=u"Grupo de obras", top=0.8*cm, left=LS[11],width=WS[11],style=styb),
            Label(text=u"Nombre producto", top=0.8*cm, left=LS[12],width=WS[12],style=styb),
            Label(text=u"Cantidad de producto", top=0.8*cm, left=LS[13],width=WS[13],style=styb),
            Label(text=u"Tipo de población", top=0.8*cm, left=LS[14],width=WS[14],style=styb),
            Label(text=u"Población beneficiada", top=0.8*cm, left=LS[15],width=WS[15],style=styb),
            Label(text=u"Observación", top=0.8*cm, left=LS[16],width=WS[16],style=styb),
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
            ObjectValue(attribute_name='locacion', top=0, left=LS[0],width=WS[0],style=sty),
            ObjectValue(attribute_name='proyecto_nombre', top=0, left=LS[1],width=WS[1],style=sty),
            ObjectValue(attribute_name='inicio', top=0, left=LS[2],width=WS[2],style=sty,
                get_value=lambda inst: inst.inicio.strftime('%d/%m/%y')),
            ObjectValue(attribute_name='fin', top=0, left=LS[3],width=WS[3],style=sty,
                get_value=lambda inst: inst.fin.strftime('%d/%m/%y')),
            ObjectValue(attribute_name='proceso_id', top=0, left=LS[4],width=WS[4],style=sty,
                get_value=lambda inst: get_field(inst,"proceso_id")),
            ObjectValue(attribute_name='estado_descripcion', top=0, left=LS[5],width=WS[5],style=styww),
            ObjectValue(attribute_name='procentaje', top=0, left=LS[6],width=WS[6],style=styr,
                get_value=lambda inst: "%d %%" % inst.porcentaje),
            ObjectValue(attribute_name='coordenada_x', top=0, left=LS[7],width=WS[7],style=styr),
            ObjectValue(attribute_name='coordenada_y', top=0, left=LS[8],width=WS[8],style=styr),
            ObjectValue(attribute_name='organizacion_id', top=0, left=LS[9],width=WS[9],style=styww,
                get_value=lambda inst: get_field(inst,"organizacion_id")),
            ObjectValue(attribute_name='tipo_junta_id', top=0, left=LS[10],width=WS[10],style=sty,
                get_value=lambda inst: get_field(inst,"tipo_junta_id")),
            ObjectValue(attribute_name='grupo_descripcion', top=0, left=LS[11],width=WS[11],style=styww),
            ObjectValue(attribute_name='producto_id', top=0, left=LS[12],width=WS[12],style=sty,
                get_value=lambda inst: get_field(inst,"producto_id")),
            ObjectValue(attribute_name='cantidad', top=0, left=LS[13],width=WS[13],style=styr),
            ObjectValue(attribute_name='tipo_poblacion_id', top=0, left=LS[14],width=WS[14],style=sty,
                get_value=lambda inst: get_field(inst,"tipo_poblacion_id")),
            ObjectValue(attribute_name='poblacion', top=0, left=LS[15],width=WS[15],style=styr),
            ObjectValue(attribute_name='observacion', top=0, left=LS[16],width=WS[16],style=styww)
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
                    ObjectValue(attribute_name='distrito_nombre', left=0, top=0.1*cm)
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