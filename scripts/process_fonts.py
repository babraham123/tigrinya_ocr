#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to create Tigrinya wordlist and *gram files from corpus

import sys
import subprocess


def sendCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (stdout, stderr) = p.communicate()
    if stderr:
        print stderr
        sys.stdout.flush()
    return stdout.strip()


def main():
    # fonts = sendCmd('fc-list').split('\n')
    fonts = sendCmd('text2image --list_available_fonts --fonts_dir /usr/local/share/fonts/tir_fonts').split('\n')

    xheight_tool = '~/grctraining/tools/xheight'
    xheights = []
    for font in fonts:
        if font: # and 'tir_fonts' in font:
            font = font.strip().split(':')[1][1:]
            xheights.append(sendCmd(xheight_tool + ' "' + font + '"'))

    xheights = list(set(xheights))
    xheights.sort()
    print xheights
    sys.stdout.flush()

    filename = 'Ethiopic.xheights'
    with open(filename, 'w') as f:
        for x in xheights:
            f.write(x.encode('utf-8') + '\n')

    print 'wrote to file'
    sys.stdout.flush()


if __name__ == "__main__":
    main()
