#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to create Tigrinya word list

filename = '../raw_data/alphabet.txt'
with open(filename) as f:
    letters = f.readlines()

letters = [l.decode('utf-8').strip() for l in letters]

filename = '../raw_data/dictionary.txt'
with open(filename) as f:
    content = f.readlines()

content = [x.decode('utf-8').strip().split(' ') for x in content]
content = [item for sublist in content for item in sublist]
content = list(set(content))
content.sort()

words = []
unknown = []
for word in content:
    subword = u''
    for letter in word:
        if letter in letters:
            subword += letter
        else:
            unknown.append(letter)

    if subword and subword in word:
        words.append(subword)

unknown = list(set(unknown))
unknown.sort()
print unknown
words = list(set(words))
words.sort()

filename = '../raw_data/wordlist.txt'
with open(filename, 'w') as f:
    for w in words:
        f.write(w.encode('utf-8') + '\n')
