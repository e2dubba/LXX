#!/usr/bin/env python3
'''
This app is for taking the plain text mlxx files and diogenese 
output to create speciall objects to import into lxx.py
'''


import re 
from betacode import greek



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


class WordParsings:
    def __init__(self, word_list):
        self.word = word_list[0]
        self.word_un = word_list[1]
        self.parsing = word_list[2]
        self.lexical = word_list[3]
        self.strongs = word_list[4]


    def deroma_lex(self):
        if self.word != '':
            plaintxt = re.sub(BETACODE_STRIP, '', self.word)
            plaintxt = greek.decode(plaintxt)
        else:
            plaintxt = self.word_un
        return plaintxt

    
    def word_check(self):
        
               



    def __eq__(self, other_WordParsings):

        

class LxxWords: 
    def __init__(self, book, chap, verse, words_list_tuple):
        self.book = book
        self.chap = chap 
        self.verse = verse 
        self.words_list_tuple = words_list_tuple
        self.numb = 0

    def __eq__(self, other_LxxWords):

    def word_check(compare_word):
        return compare_word


def split_mlxx




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
