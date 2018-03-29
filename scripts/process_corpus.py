#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to create Tigrinya wordlist and *gram files from corpus

import sys

charstart = 0x1200
charend = 0x135a


def inRange(letter):
    return (len(letter) == 1 and (charstart <= ord(letter) <= charend))


def isWord(word):
    return (word and len(word) <= 10)


def hashInsert(hashmap, entry):
    if entry in hashmap:
        hashmap[entry] = hashmap[entry] + 1
    else:
        hashmap[entry] = 1


def splitTir(word):
    start = u''
    end = u''

    for i in range(len(word)):
        if inRange(word[i]):
            start = word[i:]
            break

    for j in range(len(start), 0, -1):
        if inRange(start[j - 1]):
            end = start[:j]
            break

    return end


def writeFreq(freqmap, filename, include_freqs=False):
    sortedKeys = sorted(freqmap, key=freqmap.get, reverse=True)

    with open(filename, 'w') as f:
        for entry in sortedKeys:
            if include_freqs:
                entry = entry + u' ' + unicode(freqmap[entry])
            f.write(entry.encode('utf-8') + '\n')

    print 'wrote ' + filename
    sys.stdout.flush()
    return


def main():
    print 'Starting ...'
    sys.stdout.flush()

    filename = '../raw_data/corpus.txt'
    with open(filename) as f:
        content = f.readlines()

    content = [x.decode('utf-8').strip().split(' ') for x in content]
    print 'read file, %s lines' % len(content)
    sys.stdout.flush()

    dic = []
    wordlist = {}
    unigrams = {}
    bigrams = {}
    biwordlist = {}
    for line in content:
        prev_word = u''
        prev_w = u''
        for word in line:
            prev_letter = u''
            for letter in word:
                if inRange(letter):
                    hashInsert(unigrams, letter)
                    if inRange(prev_letter):
                        hashInsert(bigrams, prev_letter + letter)

                prev_letter = letter

            w = splitTir(word)
            if isWord(w):
                dic.append(w)
                hashInsert(wordlist, w)
                # no punc in previous word
                if isWord(prev_w) and prev_w == prev_word:
                    hashInsert(biwordlist, prev_w + u' ' + w)

            prev_w = w
            prev_word = word

    print 'processed %d lines, %d words' % (len(content), len(dic))
    sys.stdout.flush()
    dic = list(set(dic))
    dic.sort()
    if len(dic) != len(wordlist):
        print 'dic and wordlist don\'t match!!'
        sys.stdout.flush()

    writeFreq(wordlist, '../tesseract/tir/tir.wordlist')
    writeFreq(biwordlist, '../tesseract/tir/tir.word.bigrams')
    writeFreq(bigrams, '../tesseract/tir/tir.training_text.bigram_freqs', True)
    writeFreq(unigrams, '../tesseract/tir/tir.training_text.unigram_freqs', True)

    print '... Finished'
    sys.stdout.flush()


if __name__ == "__main__":
    main()
