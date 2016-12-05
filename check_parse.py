#!/usr/in/env python3


import sqlite3
import json
conn = sqlite3.connect('/home/echindod3/strongs.db')
c = conn.cursor()
from perseus import perseus


def check_parse(row, packard):
    '''
    This sets the variable in the beginning in order to facilitate json look
    up. I still need to finish the part where the json look up writes the
    Lexical form and returns the proper varibles. The issue is, if there are
    still more viable lexical forms after the first sorting, what is the next
    best delimiter? 
    '''
    dicty = perseus(row[0].lower())
    packing = row[1].split()
    pospeech = packing[0]
    plex ={}
    if pospeech[0] == 'V':
        packd_speech = packard['Column2']['Verb2']['col.1'][packing[1][0]] 
        
    if pospeech[0] == 'N':
        packd_speech = packard['Column2']['Noun2']['col.1'][packing[1][0]] 
        
    if pospeech[0] == 'A': 
        packd_speech = packard['Column2']['Adj2']['col.1'][packing[1][0]]

    #What about C? 
    if len(dicty) == 1:
	    for key in dicty.keys():
		    lexical = key
		    part_of_speech = pospeech[0]
		    etymology = row[2]
	    return lexical, part_of_speech, etymology
    
    if len(dicty) >= 2: 
    for lex in dicty:
	    new_less = [x for x in dicty[lex] if packd_speech in x]
	    print(len(new_less))
	    if len(new_less) == 1:
		    new_less = new_less.pop()
	    else:
		    print(row[0] + '\n Error!!!\t' + lex)
	    plex[lex] = new_less
    return plex

if __name__ == '__main__':
	fp = open('packard.json')
	packard = json.load(fp)
	c.execute('select * from row_value')
	tupylist = c.fetchmany(5)
	for row in tupylist:
		dict = check_parse(row, packard)
		print(row[0] + '\n\t' + str(len(dict)) + ': '+ str(dict))
	
