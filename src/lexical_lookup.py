#!/usr/bin/env python3

import sqlite3
import json
from perseus import perseus
from betacode import greek

conn = sqlite3.connect('strongs.db')
c = conn.cursor()



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

