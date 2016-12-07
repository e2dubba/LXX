#!/usr/bin/env python3

import requests, bs4, webbrowser
import collections as coll 


def perseus(lemma):
    url = 'http://www.perseus.tufts.edu/hopper/morph?l=' + lemma + '&la=greek'
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    lexical = [x.get_text() for x in soup.select('div > h4')]
    parse_tables = soup.select('div > table')
    parsing = []
    for table in parse_tables:
        tempy = [x.get_text() for x in table.findAll('td')[1::3]]
        parsing.append(tempy)
    analysis_dict = coll.OrderedDict(zip(lexical, parsing))
    return analysis_dict


def pretty_print(dicty):
    for x, y in dicty.items():
        print(x)
        for i in y:
            print('\t' + i)


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
    for lex in dicty:
	    new_less = [x for x in dicty[lex] if packd_speech in x]
	    if len(new_less) == 1:
		    new_less = new_less.pop()
	    if len(new_less) != 1:
		    print('Error!!!\t' + lex)
	    print(new_less)
	    plex[lex] = new_less
    return plex


if __name__ == '__main__':
    import sys
    import json 
    dicty = perseus(sys.argv[1])
    fp = open('packard.json')
    packard = json.load(fp)
    pretty_print(dicty)



        
'''
if packing[0][0] == 'V':
        pospeech = packing[1][0]
    else:
        pospeech = packing[0][:2]
    new_lex = {}
    for lex in dicty:
        less = [x for x in dicty[lex] if packard['Column2']['Verb2'][pospeech] in x]
        new_lex[lex] = less 

    if len(new_lex) == 1:
        lexical = new_lex.popitem()[0]
        part_of_speech = pospeech[0] 
        etymology = row[2] 
        return lexical, part_of_speech, etymology

    if len(new_lex) >= 2:
        plex = {}
        for lex in new_lex:
            if pospeech[0] == 'V':
                packing_data = packard['Column2']['Verb2']['col.2'][packing[1][1]] 
                
            if pospeech[0] == 'N':
                packing_data = packard['Column2']['Noun2']['col.1'][packing[1][0]] 
                
            if pospeech[0] == 'A': 
                packing_data = packard['Column2']['Adj2']['col.1'][packing[1][0]]

            new_less = [x for x in dicty[lex] if packing_data in x]
            plex[new_less] = lex

        if len(plex) >= 2:
            if pospeech[0] == 'V':
                pack2_data = packard['Column2']['Verb2']['col.4'][packing[1][3]] 
                
            if pospeech[0] == 'N':
                pack2_data = packard['Column2']['Noun2']['col.1'][packing[1][0]] 
                
            if pospeech[0] == 'A': 
                pack2_data = packard['Column2']['Adj2']['col.1'][packing[1][0]]

            
        if len(plex) == 1:
            lexical = plex.popitem(0)[0] 
            part_of_speech = pospeech[0]
            etymology = row[2]
            return lexical, part_of_speech, etymology 
        
        if not len(plex):
            #write error
            print('Error!')


    if len(new_lex) == 0:
          # write error
          print('Error!')


if __name__ == '__main__':
    import sys
    import json 
    dicty = perseus(sys.argv[1])
    fp = open('packard.json')
    packard = json.load(fp)
    pretty_print(dicty)

'''
