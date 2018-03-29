#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to create Tigrinya alphabet list

filename = '../raw_data/alphabet.txt'

with open(filename) as f:
    content = f.readlines()

content = [x.decode('utf-8').strip().split(' ') for x in content]
letters_a = []

for line in content:
    letters_a.extend(line[::2])

letters = []
for l in letters_a:
    if len(l) == 1:
        letters.append(l)
letters.sort()
print letters

with open(filename, 'w') as f:
    for l in letters:
        f.write(l.encode('utf-8') + '\n')
