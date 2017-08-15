#!/usr/bin/env python3
'''
This app is for taking the plain text mlxx files and diogenese 
output to create speciall objects to import into lxx.py
'''


import re 
from betacode import greek
from perseus import perseus
import lxml.etree as et



BIBLEBOOKS = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
	'Joshua', 'Judges', 'Ruth', 'I Samuel', 'II Samuel', 'I Kings', 
	'II Kings', 'I Chronicles ', 'II Chronicles', 'Ezra', 'Nehemiah', 'Esther',
	'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song', 'Isaiah',
	'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel',
	'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah',
	'Haggai', 'Zechariah', 'Malachi', 'Matthew', 'Mark', 'Luke', 'John',
	'Acts', 'Romans', 'I Corinthians', 'II Corinthians', 'Galatians',
	'Ephesians', 'Philippians', 'Colossians', 'I Timothy', 'II Timothy', 
	'I Thessalonians', 'II Thessalonians', 'Titus', 'Philemon', 'Hebrews',
	'James', 'I Peter', 'II Peter', 'I John', 'II John', 'III John', 'Jude',
	'Revelation']


BETACODE_STRIP = re.compile(r'[^A-Z]*')

PHRASE_JSON = {}
perseus_regex = re.compile('doric|aeolic|attic|epic|doric|contr')


def quick_perseus(lemma, packard):
    perseus_dict = perseus(lemma)
    if len(perseus_dict) == 1:
        if len(perseus_dict.values()) == 1:
            PHRASE_JSON[packard] = re.sub(perseus_regex, '', perseus_dict[0])


class WordParsings:
    def __init__(self, word_list):
        self.word = word_list[0]
        self.word_un = word_list[1]
        self.parsing = word_list[2]
        self.lexical = word_list[3]
        self.strongs = word_list[4]


    def deroma_lex(self):
        if self.word == '':
            plaintxt = self.word_un
        else:
            plaintxt = re.sub(BETACODE_STRIP, '', self.word)
            plaintxt = greek.decode(plaintxt)
        return plaintxt

    def osis_output(self, chap_ele, word_num):
        word_ele = et.SubElement(chap_ele, 'w')
        if not self.strongs:
            word_ele.attrib['lemma'] = 'Strong:' + self.lexical
        else:
            word_ele.attrib['lemma'] = 'Strong:' + self.lexical + \
                    ' lemma.strong:G' + self.strongs
        word_ele.attrib['morph'] = 'packard:' + self.parsing
        word_ele.attrib['wn'] = '%0.3d'% word_num
        word_ele.text = greek.decode(self.word)
        

    def __eq__(self, other_WordParsings):
        truth_value = self.deroma_lex == other_WordParsings.deroma_lex 
        if truth_value: 
           quick_perseus(self.word, packard) 
        return truth_value
                

class LxxWords: 
    def __init__(self, book, chap, verse, words_parsing_tuple):
        self.book = book
        self.chap = chap 
        self.verse = verse 
        self.words_list_tuple = words_parsing_tuple
        self.numb = 0



def split_mlxx(line):
    return line




def split_diogenese_gen(diogenese_lxx_file):
    for line in diogenese_lxx_file:
        book_chap, verse, text = line.split(':', 3)
        text = text.replace('(', '')
        words = text.split(')')
        words = [x.split() for x in words]
        book, chap = book_chap.split()
        yield LxxWords(book, chap, verse, words_list)


'''
def fuzzy_matcher(term):
'''    

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

            
def main():
    print('hello world')


if __name__ == '__main__':
    main()



'''
class MlxxWords:

    def __init__(self, reference, words):
        self.reference = reference 
        self.book, self.number = reference.split()
        self.chapter, self.verse = map(int, self.number.split(':'))
        self.data = words 


class DlxxWords:

    def __init__(self, verse):
        book_chap, verse, text = verse.split(':', 3)
        text = text.replace('(', '')
        words = text.split(')')
        self.words = [x.split() for x in words]
        book_chap = book_chap.split()
        self.chap = book_chap.pop()
        self.book = ' '.join(book_chap)
'''
