#!/usr/bin/env python3

from betacode import greek

import lxml.etree as et
from xml.dom import minidom
import sqlite3
import os 
import subprocess as sp 
import webbrowser 
import requests, bs4
import betacode

from xtermcolor import colorize

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
            comp_strong = []
            print('No Strong Number for Compound Word ' + str(list_of_beta_words
                ))
            return comp_strong
        comp_strong.append(strong)
    return comp_strong 


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


def pcruncher(row, verse):
    '''
    Uses perseus's cruncher which can be installed from the website, but if
    there are any errors to what the cruncher produces it calls the perseus website. 
    '''
    inf_form = row[:24].strip()
    lemma = inf_form.lower()
    poss_roots = sp.run(['cruncher'], input=lemma, stdout=sp.PIPE,
            universal_newlines=True, env=os.environ).stdout 
    poss_roots = poss_roots.replace('<NL>', '').replace('</NL>', '\n').split('\n')
    try:
        del poss_roots[0]
        del poss_roots[-2:]
    except IndexError:
        # This IndexError will hapen when perseus returns no values, so it need
        # s to find that info somewhere, should have it look up something on
        # the perseus website.
        lexical = ff_parser(lemma)
        # write that lemma = lexical in a db somewhere 
        return lexical 
    try:
        roots_set = set(greek.decode(root.split()[1].upper().replace('-', '')) for root in poss_roots)  
    except betacode.greek.BetacodeError:
        # This betacode error is often from one value with a comma in it. 
        roots_set = set(root.split()[1].upper() for root in poss_roots)
        try:
            roots_list = [ word.split(',')[1] for word in roots_set]
        except IndexError:
            roots_list = []
            for root in roots_set:
                try:
                    roots_list.append(greek.decode(root))
                except betacode.greek.BetacodeError:
                    # some timess there is an IndexError in handeling this
                    # exception I probably should send it to ff_parser
                    roots_list.append(greek.decode(root.split(',')[1]))
            roots_set = set(roots_list)
        print(colorize("\nUser Input!\n", ansi=3) + \
                greek.decode(row[:24]) + row[24:36] + greek.decode(row[36:])+ \
                "Possible Roots " + str(roots_list))
        if len(roots_list) == 1:
            try:
                lexical = roots_list.pop()
                var = input("Is this the correct word: %s? (y/n)" % lexical)
                if var == 'y':
                    return lexical
                if var == 'n':
                    lexical = ff_parser(lemma)
                return lexical 
            except betacode.greek.BetacodeError:
                print("What is the correct root for this misparsed item?")
                lexical = ff_parser(lemma)
                return lexical  
    if len(roots_set) == 0:
        lexical = ff_parser(lemma)
        return lexical
    elif len(roots_set) == 1:
        lexical = roots_set.pop()
        return lexical
    else:
        menu = {str(k): v for k, v in enumerate(roots_set)}
        print(colorize("User Input!\n", ansi=3) + \
                greek.decode(row[:24]) + row[24:36] + greek.decode(row[36:]))
        for key, value in menu.items():
            print(key, ':', value)
        print(str(len(menu)), ':', 'Other')
        usr_ans = input("Which is the lexical form of %s?\n" % lemma)
        if usr_ans == str(len(menu)):
            lexical = ff_parser(lemma)
            return lexical
        else:
            lexical = menu[str(usr_ans)]
            return lexical 


def ff_parser(lemma):
    url ='http://www.perseus.tufts.edu/hopper/morph?l=' + lemma + \
    '&la=greek'
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "lxml")
    elems = soup.select('div > h4')
    web_words = {str(x): y.get_text().replace('-', '') for x, y in enumerate(elems)}
    if len(web_words) == 1:
        lexical = web_words[str(0)]
        return lexical 
    elif len(web_words) == 0:
        lexical = input("\nThe Computer failed.\n \
                Please enter the lexical form of %s." % lemma)
        try:
            lexical = greek.decode(lexical)
        except betacode.greek.BetacodeError:
            pass
        return lexical 
    else:
        webbrowser.open(url) 
        for key, value in web_words.items():
            print(key, ':', value)
        var = input("What is the Lexical form of %s?\n" % lemma )
        lexical = web_words[str(var)]
        return lexical
    

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
                print('No corresponding Strongs Number', str(lemma))
            lemmata = ''
        try:
            lexical = greek.decode(lemma[0])
        except IndexError:
            wrte_error('Betacode decode error')
            lexical = pcruncher(row, verse) 
        
    elif len(lemma) == 2:
        '''
        This is for the words that have two lexemes. This shouldn't be a
        problem, most of these words will be in the db. 
        '''
        lemma.append(lemma.pop(0))
        #lemma, lexical = dual_root(lemma)
        comp_strong = beta2_strong_list(lemma)
        if not comp_strong:
            #lexical = ','.join(greek.decode(word) for word in lemma)
            lexical = pcruncher(row, verse) 
            lemmata = ''
        else:
            try:
                lemmata = multi_word(comp_strong)
                lexical = get_comp_uni(lemmata)
            except IndexError:
                #print('Compound Strongs Not Found ', str(lemma))
                # lexical = ','.join(greek.decode(word) for word in lemma)
                lexical = pcruncher(row, verse)
                lemmata = ''
            if not lexical:
                try:
                    #lexical = ','.join(greek.decode(word) for word in lemma)
                    lexical = pcruncher(row, verse)
                except IndexError:
                    print('No Lexical Entry')
        
    elif len(lemma) == 3:
        print(row)
        lemma.append(lemma.pop(0))
        lemmar = beta2_strong_list(lemma[-2:])
        ini_lemmata = multi_word(lemmar).lstrip('0')
        try:
            lemmata = [get_strongs((lemma[0] ,)), ini_lemmata]
        except IndexError:
            print('No Stongs number for Root')
            lemmata = ''
        try:
            lemmata = multi_word(lemmata)
        except IndexError:
            print('multi_word() Index Error')
            lemmata = ''
        try:
            lexical = get_comp_uni(lemmata) 
        except (sqlite3.InterfaceError, IndexError):
            print('sqlite3 Interface Error or IndexError')
            #lexical = ','.join(greek.decode(word) for word in lemma)
            lexical = pcruncher(row, verse)
            lemmata = ''
        if not lexical:
            lexical = ','.join(greek.decode(word) for word in lemma)

    elif len(lemma) == 0:
        '''
        Write to error file
        '''
        print('No Lexical Given in CATSS')
        lemmata = None
        lexical = None
    return lemmata, lexical  


for row in open(document):
    #try:
    element = gen 
    if len(row) >= 20:
        word_ele = et.SubElement(chap_ele, 'w')
        lemmata, lexical = norm_compounds(row)
        if not lemmata: 
            word_ele.attrib['lemma'] = 'Strong:' + lexical 
        else:
            word_ele.attrib['lemma'] = 'Strong:' + lexical + \
                   ' lemma.strong:G' + lemmata
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
