#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python lib to evaluate Tesseract models

# sudo apt-get install pandoc python-pythonmagick
# pip install reportlab pytesseract Pillow pypandoc pdfminer

from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from PIL import Image
from wand.image import Image as Img
from wand.color import Color
import pytesseract

lines_per_page = 25
logging = True

def register_fonts(fonts_by_level, font_dir=''):
    for level, fonts in fonts_by_level.iteritems():
        for font_name, font_file in fonts.iteritems():
            pdfmetrics.registerFont(TTFont(font_name, font_dir + font_file))

def pdf_to_text(filename):
    pdf_file = filename + '.pdf'
    pass

def pdf_to_tif(filename):
    pdf = filename + '.pdf'
    tif = filename + '.tif'
    with Img(filename=pdf, resolution=300) as img:
        img.compression_quality = 99
        img.type = 'grayscale'
        img.save(filename=tif)
    return tif

def print_ocr(filename, lang):
    # text image to string
    ocr_output = pytesseract.image_to_string(Image.open(filename), lang=lang)
    print(ocr_output)
    # Get bounding box estimates
    print(pytesseract.image_to_boxes(Image.open(filename), lang=lang))
    # Get verbose data including boxes, confidences, line and page numbers
    print(pytesseract.image_to_data(Image.open(filename), lang=lang))
    # Get information about orientation and script detection
    print(pytesseract.image_to_osd(Image.open(filename), lang=lang))

def run_ocr(filename, lang):
    # text image to string
    return pytesseract.image_to_string(Image.open(filename), lang=lang)

def post_processing(text):
    lines = [line.strip(' \n') for line in text.split('\n')]
    lines[:] = [line for line in lines if line]
    return '\n'.join(lines)

def remove_ext(filename):
    parts = filename.split('.')
    if len(parts) < 2:
        return filename, ''
    return '.'.join(parts[:-1])

def create_pdf(filename, text, font):
    styles = {}  # getSampleStyleSheet()
    # leading = fontize * 1.2
    styles['Ethiopic'] = ParagraphStyle(
        name='Ethiopic',
        fontName=font,
        fontSize=12,
        leading=14,
        firstLineIndent=0,
        alignment=TA_LEFT,
        textColor=black,
        backColor=None,
        splitLongWords=0
    )

    filename = filename + '-' + font.replace(' ', '_') + '.pdf'
    pdf = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles['Ethiopic_i'] = styles['Ethiopic']
    for i in range(len(text)):
        line = text[i]
        story.append(Paragraph(line.encode('utf-8'), styles['Ethiopic_i']))
        story.append(Spacer(inch * 0.1, inch * 0.1))
        if i > 0 and i % lines_per_page == 0:
            story.append(PageBreak())
    
    pdf.build(story)
    # print('Wrote ' + filename)
    return filename

def eval_langs(filename, text, fonts_by_level, langs, cleanup_files=True):
    groundtruth = '\n'.join(text)
    if logging:
        print('groundtruth:\n' + groundtruth)

    results = {}
    for level, fonts in fonts_by_level.iteritems():
        print('Level: ' + level)
        f_res = {}
        for font in fonts:
            print('  Font: ' + font)
            pdf_file = create_pdf(filename, text, font)
            img_file = pdf_to_tif(remove_ext(pdf_file))

            l_res = {}
            for lang in langs:
                output = run_ocr(img_file, lang)
                output = post_processing(output)
                if logging:
                    print('output [' + font + ', '+ lang +']:\n' + output)
                stats = check_accuracy(groundtruth, output)
                l_res[lang] = stats

            f_res[font] = l_res

            if cleanup_files:
                os.remove(pdf_file)
                os.remove(img_file)

        results[level] = f_res
    return results

def check_accuracy(truth, output_raw):
    truth = truth.split('\n')
    output_raw = output_raw.split('\n')
    output = []
    for out in output_raw:
        out = out.strip()
        if out:
            output.append(out)
    del output_raw

    correct_words = 0
    words = 0
    correct_letters = 0
    letters = 0
    for l_truth, l_out in zip(truth, output):
        l_truth = l_truth.strip().split(' ')
        l_out = l_out.strip().split(' ')
        words += len(l_truth)

        for i, w_truth in enumerate(l_truth):
            letters += len(w_truth)
            if not w_truth:
                continue

            if i >= len(l_out):
                continue
            w_out = l_out[i]

            if w_truth == w_out:
                correct_words += 1
                correct_letters += len(w_truth)
                continue

            for j, ll_truth in enumerate(w_truth):
                if j < len(w_out) and ll_truth == w_out[j]:
                    correct_letters += 1

    if logging and (words == 0 or letters == 0):
        print('Divide by zero will happen in stats!')

    return [correct_words, words, correct_letters, letters]

def sum_stats(stats_a, stats_b):
    for level in stats_a:
        for font in stats_a[level]:
            for lang in stats_a[level][font]:
                for i in range(4):
                    stats_a[level][font][lang][i] += stats_b[level][font][lang][i]
    return stats_a

def calc_stats(stats):
    for level in stats:
        for font in stats[level]:
            for lang in stats[level][font]:
                words = 100.0 * stats[level][font][lang][0] / stats[level][font][lang][1]
                letters = 100.0 * stats[level][font][lang][2] / stats[level][font][lang][3]
                stats[level][font][lang] = [words, letters]
    return stats

def pick_best(stats):
    picks = {}
    for level in ['easy', 'medium']:
        if level not in stats:
            continue
        for font in stats[level]:
            for lang in stats[level][font]:
                picks[lang] += picks.get(lang, 0) + sum(stats[level][font][lang])
    return max(picks, key=picks.get)

def mean_stats(stats, lang):
    words = {}
    letters = {}
    calcs = {}
    for level in stats:
        words[level] = []
        letters[level] = []
        for font in stats[level]:
            words[level].append(stats[level][font][lang][0])
            letters[level].append(stats[level][font][lang][1])
    
        mwords = sum(words[level]) / len(words[level])
        mletters = sum(letters[level]) / len(letters[level])
        vwords = sum([(w - mwords)**2 / len(w) for w in words[level]])
        vletters = sum([(l - mletters)**2 / len(l) for l in letters[level]])
        # mean and variance for the % of correct words and letters
        calcs[level] = [mwords, vwords, mletters, vletters]
    return calcs

def eval_sample(filename, text, font, lang):
    pdf_file = create_pdf(filename + '_sample', text, font)
    img_file = pdf_to_tif(remove_ext(pdf_file))
    print_ocr(img_file, lang)
    print('\n')
    os.remove(pdf_file)
    os.remove(img_file)

def eval_all(filename, text, fonts_by_level, langs, cleanup_files=True):
    results = []
    for i in range(0, len(text), lines_per_page):
        page_results = eval_langs(filename + str(i), text[i:i+lines_per_page], fonts_by_level, langs, cleanup_files)
        results.append(page_results)

    if logging:
        print('%d pages' % len(results))

    stats_raw = results[0]
    for j in range(1, len(results)):
        stats_raw = sum_stats(stats_raw, results[j])

    if logging:
        print('Raw stats: ' + str(stats_raw))

    stats_full = calc_stats(stats_raw)
    print('Full stats: ' + str(stats_full))
    lang = pick_best(stats_full)
    print('Best lang: ' + lang)
    stats = mean_stats(stats_full, lang)
    print('Stats (mean, variance): ' + str(stats))

