# python script to create Tigrinya alphabet list

filename = '../raw_data/characters.txt'

letters = []
for cval in range(0x1200, 0x1380):
    try:
        letters.append(unichr(cval))
    except ValueError:
        continue

print letters

with open(filename, 'w') as f:
    for l in letters:
        f.write(l.encode('utf-8') + '\n')
