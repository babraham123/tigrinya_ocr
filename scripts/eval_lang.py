#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to create Tigrinya PDFs from the corpus

# sudo apt-get install pandoc python-pythonmagick
# pip install reportlab pypandoc pytesseract Pillow

from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pypandoc
import PythonMagick
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

filename_in = '../raw_data/corpus.txt'
filename_out = '../tesseract/eval/tir_testdata.pdf'
filename_txt = '../tesseract/eval/tir_groundtruth.txt'
# font_dir = '/Users/babraham/Library/Fonts/'
font_dir = ''

fonts_by_level = {
    'easy': {
        'Abyssinica SIL': 'AbyssinicaSIL-R.ttf',
        'Abyssinica SIL Sebatbeit': 'AbyssinicaSIL-Sebatbeit-with-gwa.ttf',  # AbyssinicaSIL-Sebatbeit.ttf
        'Ethiopia Jiret': 'jiret.ttf',
        'Ethiopic Hiwua': 'hiwua.ttf',
        'Ethiopic Tint': 'tint.ttf',
        'Ethiopic WashRa Bold': 'washrab.ttf',
        'Ethiopic WashRa SemiBold': 'washrasb.ttf',
        'Ethiopic Yebse': 'yebse.ttf',
        'Ethiopic Zelan': 'zelan.ttf',
    },
    'medium': {
        'Code2003': 'Code200365k.ttf',
        'Ethiopic Fantuwua': 'fantuwua.ttf',
        'Ethiopic Wookianos': 'wookianos.ttf',
        'Ethiopic Yigezu Bisrat Goffer': 'goffer.ttf',
    },
    'hard': {
        'Abyssinica SIL Ximtanga': 'AbyssinicaSIL-R-designsource-20130811-Khimtanga.ttf',
        'Abyssinica SIL Zaima': 'AbyssinicaSIL-R-designsource-zaima-extensions.ttf',
        'Ethiopic Yigezu Bisrat Gothic': 'yigezubisratgothic.ttf',
        'GF Zemen Unicode': 'gfzemenu.ttf'
    },
}

def pdf_to_tiff(filename):
    img = PythonMagick.Image()
    img.density('600')  # you have to set this here if the initial dpi are > 72
    img.read(filename + '.pdf') # the pdf is rendered at 600 dpi
    img.write(filename + '.tif')

def run_ocr(lang, filename):
    # text image to string
    ocr_output = pytesseract.image_to_string(Image.open(filename + '.tif'), lang=lang)
    # Get bounding box estimates
    print(pytesseract.image_to_boxes(Image.open(filename + '.tif'), lang=lang))
    # Get verbose data including boxes, confidences, line and page numbers
    print(pytesseract.image_to_data(Image.open(filename + '.tif'), lang=lang))
    # Get information about orientation and script detection
    print(pytesseract.image_to_osd(Image.open(filename + '.tif'), lang=lang))
    return ocr_output

def main():
    for level, fonts in fonts_by_level
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
        story.append(Spacer(inch * 0.1, inch * 0.1))
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
    main()
