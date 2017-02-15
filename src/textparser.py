#!/usr/bin/env python3
'''
This app is for taking the plain text mlxx files and diogenese 
output to create speciall objects to import into lxx.py
'''

class MlxxWords:
    def __init__(self, reference, words):
        self.reference = reference 
        self.book, self.number = reference.split()
        self.chapter, self.verse = map(int, self.number.split(':'))
        self.data = words 


class DlxxWords:
    def __init__(self, verse):
        def verse_spliter(verse):
            book_chap, verse, text = verse.split(':', 3)
            text = text.replace('(', '')
            words = text.split(')')
            words = [x.split() for x in words]
            book_chap = book_chap.split()
            chap = book_chap.pop()
            book = ' '.join(book_chap)
            return book, chap, verse, words 
        self.book, self.chap, self.verse, self.words = verse_spliter(verse)




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
