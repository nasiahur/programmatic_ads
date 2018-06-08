import os

from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from reportlab.platypus import Paragraph, Spacer, KeepTogether
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus.flowables import Image
from reportlab.platypus.tables import Table, TableStyle, LongTable

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart, HorizontalBarChart

H1, H2, H3, H4, H5, H6 = 1, 2, 3, 4, 5, 6
CENTER, LEFT, RIGHT = 'CENTER', 'LEFT', 'RIGHT'
CYAN = Color(float(54)/255, float(171)/255, float(177)/255)
VERYLIGHTCYAN = Color(float(234)/255, float(241)/255, float(247)/255)
BAR_COLORS = [ CYAN, colors.green, colors.black, colors.yellow, colors.brown, colors.red, colors.blue ]

class DefaultTheme:
    margins = {
        'left': 25,
        'right': 25,
        'top': 20,
        'bottom': 25
    }

    spacer_height = 0.2 * inch

    styleSheet = getSampleStyleSheet()

    paragraph = styleSheet['Normal'] 

    headers = {
         H1: styleSheet['Heading1'],
         H2: styleSheet['Heading2'],
         H3: styleSheet['Heading3'],
         H4: styleSheet['Heading4'],
         H5: styleSheet['Heading5'],
         H6: styleSheet['Heading6'],
    }
    
    table_style = [
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('LINEBELOW', (0,0), (-1,0), 1, CYAN),
        ('BACKGROUND', (0,0), (-1,0), CYAN),
        ('ROWBACKGROUNDS', (0,1), (-1, -1), [colors.white, VERYLIGHTCYAN])
    ]
    
    @classmethod    
    def header_by_level(c, level):
        return c.headers[level]   


class PdfReport:
    single_intend = "        "
    document_width = A4[0] 
    document_hight = A4[1]

    def __init__(self, title, meta, report_directory):
        self.theme = DefaultTheme
        self.report_directory = ""
        self.story = []    
        self.title = title
        self.author = "Diladele Web Safety"
        self.pageNumber = 1
        self.meta = meta
        self.report_directory = report_directory

    def content_width(self):
        return self.document_width - self.theme.margins['left'] - self.theme.margins['right']

    def content_hight(self):
        return self.document_hight - self.theme.margins['top'] - self.theme.margins['buttom']
    
    def set_theme(self, theme):
        self.theme = theme
        
    def add(self, flowable):
        self.story.append(flowable)

    def add_vertical_bar_chart(self, data, categories, dataLabel):
        if len(categories) == 0:
            return
        if len(data) == 0:
            return

        drawing = Drawing(self.content_width(), len(categories)*15 + 50)
        
        maxValue = 1
        for value in data:
            if value > maxValue:
                maxValue = value

        bc = HorizontalBarChart()
        bc.height = len(categories)*15
        bc.width = self.content_width() - 300
        bc.x = 150
        bc.y = 25
        bc.groupSpacing = 2

        bc.data = [data]
        bc.strokeColor = None
        bc.bars[0].fillColor = CYAN

        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = maxValue
        bc.valueAxis.valueStep = max(maxValue/5, 1)
        bc.valueAxis.labelTextFormat = dataLabel

        bc.categoryAxis.labels.boxAnchor = 'e'
        bc.categoryAxis.labels.dx = -8
        bc.categoryAxis.labels.dy = 0
        bc.categoryAxis.categoryNames = categories

        drawing.add(bc)
        self.add(drawing)

    def add_report_header(self):
        self.add_header("Diladele Web Safety Report : %s" % self.meta["name"])
        self.add_paragraph("Generated: %s" % self.meta["builtOnLocal"])
        self.add_paragraph("Time Range: from %s till %s" % (self.meta["start"], self.meta["end"]))
        self.add_spacer()
        self.add_spacer()
        self.add_spacer()

    def add_header(self, text, level=H1):
        p = Paragraph(text, self.theme.header_by_level(level))
        self.add(p)
    
    def add_spacer(self, height_inch=None):
        height_inch = height_inch or self.theme.spacer_height
        ignored = 1
        self.add(Spacer(ignored, height_inch))
        
    def add_paragraph(self, text, style=None):
        style = style or self.theme.paragraph
        p = Paragraph(text, style)
        self.add(p)
    
    def add_table(self, rows, percentage_col_widths, align=CENTER, extra_style=[]):
        real_column_width = []
        for w in percentage_col_widths:
            real_column_width.append((self.content_width() * w)/100)
        style = self.theme.table_style + extra_style
        table = LongTable(rows, real_column_width, style=style, hAlign=align, repeatRows=1)
        self.add(table)

    def general_table_header(self, rows, col_widths, align=CENTER, extra_style=[]):
        style = self.theme.table_header_style + extra_style
        table = Table(rows, col_widths, style=style, hAlign=align)
        self.add(table)
    
    def add_image(self, src, width, height, align=CENTER):
        img = Image(src, width, height)
        img.hAlign = align
        self.add(img)

    def draw_page_header(self, canvas):
        canvas.saveState()
        canvas.setStrokeColor(CYAN)
        canvas.setFillColor(CYAN)
        canvas.rect(0, self.document_hight - 95, self.document_width, self.document_hight, stroke=1, fill=1)
        canvas.setStrokeColor(colors.white)
        canvas.setFillColor(colors.white)
        canvas.restoreState()

    def draw_page_footer(self, canvas):
        canvas.saveState()
        canvas.setStrokeColor(CYAN)
        canvas.setFillColor(CYAN)
        canvas.rect(0, 0, self.document_width, 25, stroke=1, fill=1)
        canvas.setFont('Times-Roman',9)
        canvas.setStrokeColor(colors.white)
        canvas.setFillColor(colors.white)
        canvas.drawString(self.theme.margins['left'] + 10, 10, "Page %d" % self.pageNumber)
        canvas.setFont('Times-Roman',11)
        canvas.drawString(self.document_width - self.theme.margins['right'] - 95, 10, "Diladele Web Safety")
        self.pageNumber = self.pageNumber + 1
        canvas.restoreState()

    def first_page(self, canvas, doc):
        self.draw_page_header(canvas)
        self.draw_page_footer(canvas)

    def later_pages(self, canvas, doc):
        self.draw_page_footer(canvas)

    def build(self):
        doc = SimpleDocTemplate(
            os.path.join(self.report_directory, "report.pdf"),
            pagesize = A4,
            title=self.title,
            author=self.author,
            rightMargin=self.theme.margins['right'],
            leftMargin=self.theme.margins['left'],
            topMargin=self.theme.margins['top'],
            bottomMargin=self.theme.margins['bottom'])
        doc.build(self.story, onFirstPage=self.first_page, onLaterPages=self.later_pages)
