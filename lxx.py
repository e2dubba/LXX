#!/usr/bin/env python3

from betacode import greek

import lxml.etree as et
from xml.dom import minidom
import sqlite3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('document', nargs='*')
args = parser.parse_args()
document = ' '.join(args.document)

conn = sqlite3.connect('/home/svg/Documents/GreekReader/strongs-dictionary-xml-master/strongs.db')
c = conn.cursor()

error_file = open('error_test', 'w')
comp_words_file = open('comp_words_file', 'w')

gen = et.Element('book')
word_num = 1


def verse_assign(chap_ele, verse):
    verse_ele = et.SubElement(chap_ele, 'verse')
    verse_ele.attrib['sID'] = verse
    verse_ele.attrib['osisID'] = verse  
    return verse_ele 


def get_strongs(value):
    '''
    fetch strongs number from db. 
    returns data as a string. Throws IndexError if there is no result. 
    '''
    c.execute('SELECT strongs FROM new_strong_combined WHERE BETA=?',
            value) 
    data = c.fetchall()
    data = data[0][0]
    return data


def get_compound(value):
    c.execute('SELECT strongs FROM new_strong_combined WHERE stnumbers=?',
            (value))
    data = c.fetchall()
    return data


def beta2_strong_list(list_of_beta_words):
    '''
    takes a list of betacode words, and returns a list of strongs numbers
    '''
    comp_strong = []
    for word in list_of_beta_words:
        word = (word ,)
        try:
            strong = get_strongs(word).lstrip('0')
        except IndexError:
            print('\n' + verse + '\n' + ','.join(list_of_beta_words))
            from xtermcolor import colorize 
            print(colorize("IndexError!!!", ansi=1))
            strong = ''
            write_error('No Strong Number for Compound Word')
        comp_strong.append(strong)
    return comp_strong 


def dual_root(lemma):
    '''
    '''
    comp_strong = []
    for word in lemma:
        word = (word ,)
        try:

        
def get_comp_uni(value):
    value = (value ,)
    c.execute('SELECT greek FROM new_strong_combined WHERE strongs = ?',
            (value))
    data = c.fetchall()
    return data[0][0]


def multi_word(list_of_num):
    first_try = (','.join(list_of_num) ,)
    word = get_compound(first_try)
    if not word:
        second_try = (','.join(list_of_num[::-1]) ,)
        word = get_compound(second_try)
    return word[0][0]


def write_error(error_type, lemma):
    c.execute('SELECT * FROM extra_word WHERE beta = ?', 
            (lemma ,))
    if not c.fetchall():
        error_file.write(verse + '\t' + greek.decode(row[:24]) + row[24:36] + \
                greek.decode(row[36:]))
        error_file.write(verse + ': wn={} '.format(str(word_num)) + row + \
              'Problem: {}\n\n'.format(error_type)) 
        c.execute('INSERT INTO extra_word VALUES (?)', 
                (lemma ,)) 
        c.execute('INSERT INTO extra_word_count VALUES (?, ?, ?)',
                (verse, lemma, word_num))
        conn.commit()


def norm_compounds(row):
    lemma = row[36:].split()
    brth_word = lemma[0]
    if brth_word[0] == '*': # this section moves the breathing mark
        if brth_word[2] in '()':
           breather = brth_word[2]
           brth_word = brth_word.replace(')', '').replace('(', '')
           lemma[0] = brth_word[0] + breather + brth_word[1:]
    if len(lemma) == 1:
        '''
        This works for the words that only have one lexeme 
        '''
        #lemma = (lemma[0] ,)
        try:
            lemmata = get_strongs((lemma[0] ,))
        except IndexError:
            if lemma[0] == '*':
                write_error('No corresponding Strongs Number', str(lemma))
            lemmata = ''
        try:
            lexical = greek.decode(lemma[0])
        except IndexError:
            wrte_error('Betacode decode error')
            lexical = ''

    elif len(lemma) == 2:
        '''
        This is for the words that have two lexemes. This shouldn't be a
        problem, most of these words will be in the db. 
        '''
        lemma.append(lemma.pop(0))
        lemma, lexical = dual_root(lemma)
        comp_strong = beta2_strong_list(lemma)
        print(comp_strong)
        if not comp_strong:
            lemmata = ','.join(greek.decode(word) for word in lemma)
            from xtermcolor import colorize
            print(colorize(lemmata, ansi=3))
        else:
            try:
                lemmata = multi_word(comp_strong)
                lexical = get_comp_uni(lemmata)
            except IndexError:
                write_error('Compound Strongs Not Found', str(lemma))
                lexical = ','.join(greek.decode(word) for word in lemma)
                lemmata = ' '
            if not lexical:
                try:
                    lexical = ','.join(greek.decode(word) for word in lemma)
                except IndexError:
                    write_error('No Lexical Entry')
        
    elif len(lemma) == 3:
        lemma.append(lemma.pop(0))
        lemmar = beta2_strong_list(lemma[-2:])
        ini_lemmata = multi_word(lemmar).lstrip('0')
        try:
            lemmata = [get_strongs((lemma[0] ,)), ini_lemmata]
        except IndexError:
            write_error('No Stongs number for Root')
            lemmata = ''
        try:
            lemmata = multi_word(lemmata)
        except IndexError:
            write_error('multi_word() Index Error')
        try:
            lexical = get_comp_uni(lemmata) 
        except sqlite3.InterfaceError:
            write_error('sqlite3 Interface Error')
            lexical = ''
        if not lexical:
            try:
                lexical = ','.join(greek.decode(word) for word in lemma)
            except IndexError:
                write_error('No Lexical Entry')

    elif len(lemma) == 0:
        '''
        Write to error file
        '''
        write_error('No Lexical Given in CATSS')
        lemmata = None
        lexical = None
    return lemmata, lexical  


for row in open(document):
    #try:
    element = gen 
    if len(row) >= 20:
        word_ele = et.SubElement(chap_ele, 'w')
        try:
            lemma, lexical = norm_compounds(row)
            if lemma == '':
                lemma = ''
                word_ele.attrib['lemma'] = 'Strong:' + lexical 
            else:
                word_ele.attrib['lemma'] = 'Strong:' + lexical + \
                       ' lemma.strong:G' + lemma  
            # word_ele.attrib['lexical'] = lexical
        except TypeError:
            continue
            # write_error('TypeError Raised from `norm_compounds()`')
        word_ele.attrib['morph'] = 'packard:' + row[24:35].strip()
        word_ele.attrib['wn'] = '%0.3d' % word_num
        word_ele.text = greek.decode(row[:24].strip())
        word_num += 1 
    else:
        if row == '\n':
            word_num = 1
            verse_ele = et.SubElement(chap_ele, 'verse')
            verse_ele.attrib['eID'] = verse 
            continue 
        else: 
            verse = row.strip('\n')
            ref = verse.split(' ')
            verse = verse.replace(' ', '.').replace(':', '.')
            book = ref[0]
            chap_verse = ref[1].strip('\n').split(':')
            chapter = book + '.' + chap_verse[0]
            try: 
                if chapter == chap_ele.attrib['osisID']:
                    verse_ele = verse_assign(chap_ele, verse)
                else: 
                    chap_ele = et.SubElement(element, 'chapter')
                    chap_ele.attrib['osisID'] = chapter
                    verse_ele = verse_assign(chap_ele, verse)
            except:
                chap_ele = et.SubElement(element, 'chapter')
                chap_ele.attrib['osisID'] = chapter
                verse_ele = verse_assign(chap_ele, verse)
'''
            verse_ele = et.SubElement(chap_ele, 'verse')
            verse_ele.attrib['osisID'] = verse
'''

tree = et.ElementTree(element)
tree.write('%s.xml' % document, encoding='unicode', pretty_print=True)
comp_words_file.close()
error_file.close()

'''
trying to set this up in git
for xml milestones: 
    see http://stackoverflow.com/a/5089707/5547025
    I think the format i need is 
    verse_ele = et.Element("verse osisID='%s'", verse)
NOTES:
    lang code: grc

    possible func:
    def get_2word_compound(lemma):
    lemma.append(lemma.pop(0))
    comp_strong = []
    for word in lemma:
        word = (word ,)
        try:
            strong = get_strongs(word)
        except IndexError:
            error_file.write(verse + row)
            strong = None
        comp_strong.append(strong[0].lstrip('0'))
    if len(comp_strong) == 2:
        comp_words_file.write(comp_strong)
    comp_words = (','.join(comp_strong) ,)
    strong_number = get_compound(comp_words) 
    lemmata = 'strong:G' + strong_number 
    lexical = get_comp_uni(comp_words)
    return lemmata, lexical 

i need to make sure this ends up somehow in the final code:
        lemmata = 'strong:G' + strong_number 
'''
