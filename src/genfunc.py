#!/usr/bin/env python3


def iter_mlxx(mlxx_file):
    for line in map(str.rstrip, mlxx_file):
        if len(line.split()) == 2:
            word_buffer = []
            verse = line
        elif line == '':
            yield (verse, word_buffer)
        else:
            word_buffer.append(split_row(line))

    yield (verse, word_buffer)


def split_row(row):
    infl = row[:24].strip()
    morph = row[24:36].strip()
    etym_roots = row[36:].strip()
    return [infl, morph, etym_roots]



if __name__ == '__main__':
    mlxx_file = open('/home/echindod3/lxx2/01.Gen.1.mlxx')
    olxx = open('/home/echindod3/files/LXX')
    for line in olxx:
        mllx = iter_mlxx(mlxx_file)
        print(line, str(mllx))




