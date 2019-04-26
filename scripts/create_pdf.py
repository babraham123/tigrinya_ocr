#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to create Tigrinya PDFs from the corpus

# pip install reportlab

from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont 
import sys

# font_dir = '/Users/babraham/Library/Fonts/'
font_dir = '/home/babraham/tigrinya_ocr/fonts/'
lines_per_page = 50

fonts = {
    'Abyssinica SIL': 'AbyssinicaSIL-R.ttf',
    'Abyssinica SIL Sebatbeit': 'AbyssinicaSIL-Sebatbeit-with-gwa.ttf',  # AbyssinicaSIL-Sebatbeit.ttf
    'Abyssinica SIL Ximtanga': 'AbyssinicaSIL-R-designsource-20130811-Khimtanga.ttf',
    'Abyssinica SIL Zaima': 'AbyssinicaSIL-R-designsource-zaima-extensions.ttf',
    'Code2003': 'Code200365k.ttf',
    'Ethiopia Jiret': 'jiret.ttf',
    'Ethiopic Fantuwua': 'fantuwua.ttf',
    'Ethiopic Hiwua': 'hiwua.ttf',
    'Ethiopic Tint': 'tint.ttf',
    'Ethiopic WashRa Bold': 'washrab.ttf',
    'Ethiopic WashRa SemiBold': 'washrasb.ttf',
    'Ethiopic Wookianos': 'wookianos.ttf',
    'Ethiopic Yebse': 'yebse.ttf',
    'Ethiopic Yigezu Bisrat Goffer': 'goffer.ttf',
    'Ethiopic Yigezu Bisrat Gothic': 'yigezubisratgothic.ttf',
    'Ethiopic Zelan': 'zelan.ttf',
    'GF Zemen Unicode': 'gfzemenu.ttf'
}

max_fonts = len(fonts)

def create_pdf(filename_in, filename_out, filename_txt):
    for f1 in fonts:
        pdfmetrics.registerFont(TTFont(f1, font_dir + fonts[f1]))

    with open(filename_in) as f:
        content = f.readlines()
    content = [x.decode('utf-8') for x in content]

    styles = {}  # getSampleStyleSheet()
    # leading = fontize * 1.2
    styles['Ethiopic'] = ParagraphStyle(
        name='Ethiopic',
        fontName='Abyssinica SIL',
        fontSize=12,
        leading=14,
        firstLineIndent=0,
        alignment=TA_LEFT,
        textColor=black,
        backColor=None,
        splitLongWords=0
    )

    pdf = SimpleDocTemplate(filename_out, pagesize=letter)

    groundtruth = u''
    story = []
    styles['Ethiopic_i'] = styles['Ethiopic']
    for i in range(lines_per_page * max_fonts):
        line = content[i % len(content)]
        groundtruth = groundtruth + line + u'\n'
        story.append(Paragraph(line.encode('utf-8'), styles['Ethiopic_i']))
        story.append(Spacer(inch * 0.05, inch * 0.05))
        if i > 0 and i % lines_per_page == 0:
            groundtruth = groundtruth + u'\n'
            story.append(PageBreak())
            styles['Ethiopic_i'] = ParagraphStyle(
                name='Ethiopic_i',
                fontName=fonts.keys()[i / lines_per_page])

    pdf.build(story)
    print('Wrote new pdf ' + filename_out)

    with open(filename_txt, 'w') as f:
        f.write(groundtruth.encode('utf-8'))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Incorrect arguments!')
        exit()

    filename_in = sys.argv[1]
    filename_out = sys.argv[2]
    filename_txt = sys.argv[3]
    
    create_pdf(filename_in, filename_out, filename_txt)

