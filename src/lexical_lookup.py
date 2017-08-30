#!/usr/bin/env python3

import sqlite3
import json
from perseus import perseus
from betacode import greek

conn = sqlite3.connect('strongs.db')
c = conn.cursor()


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


def perseus_dict_sorter(per_dict, packd_speech):
    '''
    This needs to take the raw perseus dictionary, scraped from the web, and 
    then go through each of the lexemes to see if it can be narrowed down to 
    just one. 
    see line 52 in check_parse.py
    '''
    


def check_parse(infl_form, part_of_speech, etymology, packard):
    '''
    packard is the json file, loaded. 
    This sets the variable in the beginning in order to facilitate json look
    up. I still need to finish the part where the json look up writes the
    Lexical form and returns the proper varibles. The issue is, if there are
    still more viable lexical forms after the first sorting, what is the next
    best delimiter? 
    '''
    perseus_dict = perseus(infl_form.lower())

    if len(perseus_dict) == 1:
        for key in perseus_dict.keys():
            lexical = key
        return etymology, part_of_speech, lexical 
    
    elif not perseus_dict:
        
        pass
        #writeError

    else: 
       packd_speech = posgen(part_of_speech, num=1)
       lexical = dicty_sorter(dicty, packd_speech)
       return etymology, part_of_speech, lexical 


def main():
    print('hello world')


if __name__ == '__main__':
    main()

