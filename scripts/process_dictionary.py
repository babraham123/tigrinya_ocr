#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to create Tigrinya wordlist list

import sys


charstart = 0x1200
charend = 0x135a


def splitTir(word):
    start = ""
    end = ""

    for i in range(len(word)):
        if charstart <= ord(word[i]) <= charend:
            start = word[i:]
            break

    for j in range(len(start), 0, -1):
        if charstart <= ord(start[j - 1]) <= charend:
            end = start[:j]
            break

    return end


filename = '../raw_data/dictionary.txt'
with open(filename) as f:
    content = f.readlines()

content = [x.decode('utf-8').strip().split(' ') for x in content]
print 'read file, %s lines' % len(content)
sys.stdout.flush()

dic = []
for line in content:
    for word in line:
        w = splitTir(word)
        if w and len(w) <= 10:
            dic.append(w)

print 'processed dic, %s words' % len(dic)
sys.stdout.flush()
dic = list(set(dic))
dic.sort()
print 'sorted dic, %s uniq words' % len(dic)
sys.stdout.flush()

filename = '../tesseract/tir/tir.wordlist'
with open(filename, 'w') as f:
    for w in dic:
        f.write(w.encode('utf-8') + '\n')

print 'wrote to file'
sys.stdout.flush()
