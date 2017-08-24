#!/user/bin/env python3
'''
For nlxx: I need to split the line, then split line[2] by -.
But this will give me a list within a list. 
For mlxx: I need to remove all of the diacritics (as well as split it
like I did in roots.py. 
'''

import sqlite3
import os
import re 
from betacode import greek
import collections

BETACODE_STRIP = re.compile(r'[^A-Z]*')


def split_line(line):
    line = line.split()
    oinfl = line[0]
    if re.match('<G\d+', line[1]):
        strongs = line[1].replace('<', '').replace('>', '')
    else:
        strongs = ''
    omorph = line[2].split('-')
    return oinfl, strongs, omorph


def iter_mlxx(path):
    '''
    This is a generator function that goes through a specified directory,
    openining the mlxx files and returning a verse reference and a list of the
    the words. 
    '''
    listing = os.listdir(path)
    for l in listing:
        mfile = open(path + l)
        for line in mfile:
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
    '''
    Split's mlxx rows.
    '''
    infl = row[:24].strip()
    morph = row[24:36].strip()
    etym_roots = row[36:].strip()
    return [infl, morph, etym_roots]


Word = collections.namedtuple('Word', ['text', 'morph', 'lemma'])


class Verse(collections.UserList):
    def __init__(self, reference, words):
        self.reference = reference
        self.book, self.number = reference.split()
        self.chapter, self.verse = map(int, self.number.split(':'))

        self.data = words


'''
#This needs to change
for v in verses:
    # do some regex or whatever here and get your verse chopped up
    this_verse = Verse(reference, *(Word(text, morph, lemma) 
                                    for text morph lemma in words))
'''
    

def strip_acc(betacode_word):
    '''
    strip accents out of betacode strings.
    '''
    plaintxt = re.sub(BETACODE_STRIP, '', betacode_word)
    plaintxt = greek.decode(plaintxt)
    return plaintxt


def split_dlxx(verse):
    '''
    The verse is on its own line and strongs numbers are id'd by <> and the
    morph codes by (). This splits the string manually.
    '''
    book_chap, verse, text = verse.split(':', 3)
    text = text.replace('(', '')
    words = text.split(')')
    words = (x.split() for x in words)
    book_chap = book_chap.split()
    chap = book_chap.pop()
    book = ' '.join(book_chap)
    return book, chap, verse, words


def mlxx_file_cycle(path, files_list):
    for mlxx_file in files_list:
        try:
            verse, word_buffer = next(iter_mlxx(path + mfiles))
            return verse, word_buffer
        except StopIteration:
            continue


            
if __name__ == '__main__':
    path = '/home/echindod3/lxx2'
    mlxx = iter_mlxx(path)
    dlxx = open('/home/echindod3/files/nlxx')
    comblxx = open('/home/echindod3/files/comblxx')
    for line in dlxx:
        book, chap, verse, words = split_dlxx(line)
        mlxx_verse, mlxx_words = next(mlxx)
        dref = book + ' ' + chap + ':' + verse
        if re.search(mlxx_verse.split()[0], dref) and
            re.search(mlxx_verse.split()[1], dref):
                for mword in mlxx_words:
                    dword = next(words)
                    if strip_acc(mword[0]) == dword[0]:
                        if re.match('<G[0-9]*>', dword[1]):
                            strongs = dword[0]
                        else:
                             strongs = ''
                         comblxx.append('|'.join([mword[0], mword[1]. strongs,
                             '-'.join(mword[2].split())]))
                    else:
                        #raise error for human eyeballs
                        


                     
'''

The books in mlxx aren't just shortened forms of the dlxx, they can also be
different kinds of abbrefviations like "Kgs" and "PsSol".

'''
