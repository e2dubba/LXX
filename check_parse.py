#!/usr/in/env python3

import sqlite3
import json
conn = sqlite3.connect('/home/echindod3/strongs.db')
c = conn.cursor()
from perseus import perseus
from betacode import greek


def create_etym_tab():
    c.execute('CREATE TABLE IF NOT EXISTS etymology_lexical '
            '(etymology TEXT NOT NULL, '
            'part_of_speech TEXT NOT NULL, '
            'lexical TEXT NOT NULL)')
    conn.commit()


def up_etym_to_lex(etymology, part_of_speech, lexical):
    c.execute('INSERT INTO etymology_lexical VALUES (?, ?, ?)',
            (etymology, part_of_speech, lexical))
    conn.commit() 


def check_parse(row, packard):
    '''
    This sets the variable in the beginning in order to facilitate json look
    up. I still need to finish the part where the json look up writes the
    Lexical form and returns the proper varibles. The issue is, if there are
    still more viable lexical forms after the first sorting, what is the next
    best delimiter? 
    '''
    dicty = perseus(row[0].lower())
    part_of_speech = row[1][0]
    etymology = row[2]

    if len(dicty) == 1:
        for key in dicty.keys():
            lexical = key
        return etymology, part_of_speech, lexical 
    
    elif not dicty:
        pass
        #writeError

    else: 
       packd_speech = posgen(row[1], num=1)
       lexical = dicty_sorter(dicty, packd_speech)
       return etymology, part_of_speech, lexical 


def dicty_sorter(dicty, packd_speech):
    if len(dicty) == 1:
        for key in dicty.keys():
            lexical = key
        return lexical 
    
    elif not dicty:
        lexical = ''
        return lexical 
        #write this to error file

    else: 
        dicty_one = dicty_narrow(dicty, packd_speech)
        if len(dicty_one) == 1:
            for lex in dicty:
                lexical = lex
                return lexical
        
        elif not dicty_one:
            # writeError
            print('Error with 1 Dicty!')

        else:
            dicty_two = {}
            for lex in dicty_one:
                num = 1
                packd_speech = posgen(row[1], num)
                new_less = [x for x in dicty[lex] if packd_speech in x]
                if not new_less:
                    print('Not New Less!')
                else:
                    dicty_two[lex] = new_less

            if not dicty_two: 
                lexical = ''
                return lexical 
            
            elif len(dicty_two) == 1:
                for key in dicty_two:
                    lexical = key
                return lexical
            
            else:
                for lex in dicty_two:
                    num += 1
                    packd_speech = posgen(row[1], num)
                    new_dicty = dicty_narrow(plex, packd_speech)
                    if not new_dicty:
                        # writeError
                        print('No new Dicty')
                    elif len(new_dicty) == 1:
                        for lex in new_dicty:
                            lexical = lex
                        return lexical
                    else:
                        num += 1
                        packd_speech = posgen(row[1], num)
                        third_dicty = dicty_narrow(new_dicty, packd_speech)
                        if len(third_dicty) == 1:
                            for lex in third_dicty:
                                lexical = lex
                            return lexical
                        else:
                            print('No third dicty')
                            lexical = ''
                            return lexical
                            # writeError


def dicty_narrow(dicty, packd_speech):
    new_dicty = {}
    for lex in dicty:
        new_less = [x for x in dicty[lex] if packd_speech in x]
        new_dicty[lex] = new_less
    return new_dicty


def posgen(packard, num):
    '''
    This will cycle through the packard.json file with different values for the
    index in order to help limit the number of valid lexical items. 
    '''
    col = 'col.' + str(num)
    p = num - 1 
    packing = packard.split()
    pospeech = packing[0]
    if pospeech[0] == 'V':
        packd_speech = packard['Column2']['Verb2'][col][packing[1][p]] 
        
    if pospeech[0] == 'N':
        packd_speech = packard['Column2']['Noun2'][col][packing[1][p]] 
        
    if pospeech[0] == 'A': 
        packd_speech = packard['Column2']['Adj2'][col][packing[1][p]]

    if pospeech[0] == 'C':
        packd_speech = 'conj'
    
    if pospeech[0] == 'D':
        packd_speech = 'adv'
    return packd_speech


if __name__ == '__main__':
    fp = open('packard.json')
    packard = json.load(fp)
    c.execute('select * from row_value')
    tupylist = c.fetchall()
    error_file = open('ErrorFile.txt', 'w')
    create_etym_tab()

    for row in tupylist:
        print(greek.decode(row[0]))
        try: 
            etymology, part_of_speech, lexical = check_parse(row, packard)
            up_etym_to_lex(etymology, part_of_speech, lexical)
        except TypeError: 
            error_file.write(', '.join(row))
            print('  Type Error ' + row[0])
            pass
        #up_etym_to_lex(etymology, part_of_speech, lexical)
    
