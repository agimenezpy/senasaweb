# -*- coding: iso-8859-1
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Line
from reportlab.rl_config import defaultPageSize
from reportlab.platypus.flowables import Flowable
from reportlab.platypus import Table, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from os.path import join

PAGE_WIDTH, PAGE_HEIGHT = defaultPageSize
STILO = [('ALIGN', (0, 0), (-1, 0), 'CENTER'),
         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
         ('ALIGN', (-2, 1), (-1, -1), 'RIGHT'),
         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
         ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
         ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
         ('FONTSIZE', (0, 0), (-1, -1), 8)]
MEDIDAS = [1 * inch, 1.1 * inch, 1 * inch, 0.7 * inch, 0.7 * inch, 1.5 * inch, 0.8 * inch, 1.3 * inch, 1 * inch,
           0.8 * inch, 0.8 * inch]
STYLESHEET = ParagraphStyle(name='ItemRow', fontSize=8)


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        self.drawCentredString(self._pagesize[0] / 2.0, 20 * mm,
                               u"Página %d de %d" % (self._pageNumber, page_count))


class Caratula(Flowable):
    def __init__(self, title, filedir):
        self.title = title
        self.filedir = filedir

    def wrap(self, availWidth, availHeight):
        return availWidth, availHeight

    def draw(self):
        canvas = self.canv
        canvas.setPageSize((PAGE_WIDTH, PAGE_HEIGHT))
        canvas.setFont('Helvetica-Bold', 30)
        wdth = canvas.stringWidth(self.title, canvas._fontname, canvas._fontsize)
        canvas.drawImage(join(self.filedir, "static/img/vivapy.png"), 0, PAGE_WIDTH, width=2.63 * cm,
                         preserveAspectRatio=True)
        canvas.drawImage(join(self.filedir, "static/img/senasa.png"), PAGE_WIDTH / 2 - 3 * cm, PAGE_WIDTH + 2.54 * cm,
                         width=2.73 * cm, preserveAspectRatio=True)
        canvas.drawImage(join(self.filedir, "static/img/ministerio.png"), PAGE_WIDTH - 6.5 * cm, PAGE_WIDTH + 1.27 * cm,
                         width=3.1 * cm, preserveAspectRatio=True)
        canvas.line(0, PAGE_WIDTH + 2.54 * cm, PAGE_WIDTH - 3.4 * cm, PAGE_WIDTH + 2.54 * cm)
        canvas.drawCentredString((PAGE_WIDTH - 2.5 * cm) / 2.0, PAGE_HEIGHT / 2.0, self.title)


def Parrafo(val):
    if type(val) == type(1):
        val = u"%d" % val
    return Paragraph(val, style=STYLESHEET)


def Tabla(datos, rows, cols):
    return Table(datos, MEDIDAS, repeatRows=1, style=STILO)