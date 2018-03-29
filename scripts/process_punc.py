#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to create Tigrinya alphabet list

filename = '../tesseract/tir/tir.punc'
with open(filename) as f:
    content = f.readlines()

rows = []
for x in content:
    if not any(sub in x for sub in [",", ".", ":", ";", "?"]):
        continue

    if any(x.count(sub) > 1 for sub in [",", ".", ":", ";", "?"]):
        continue

    if any(sub in x for sub in ["¿", "¡"]):
        continue

    y = x.decode('utf-8')
    y = y.replace(",", "፡".decode('utf-8'))
    y = y.replace(".", "።".decode('utf-8'))
    y = y.replace(":", "፥".decode('utf-8'))
    y = y.replace(";", "፤".decode('utf-8'))
    y = y.replace("?", "፧".decode('utf-8'))
    rows.append(y)

print rows

filename = '../raw_data/new_punc.txt'
with open(filename, 'w') as f:
    for l in rows:
        f.write(l.encode('utf-8'))
