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
    dicty = perseus(row[0].lower())
    packing = row[1].split()[0][:2]
    for lex in dicty:
        '''
        the following comprehension will check to see which dictionary key
        parses like the Packard notation indicates. This needs to be narrowed a
        bit. I need to narrow it down if their is more than one lexical item
        that agrees with the parsings. 
        '''
        less = [x for x in dicty[lex] if packard['Column1'][packing] in x]
        # less = filter(lambda x: packard['Column1'][packing] in x, dicty[lex])
        print(less)


if __name__ == '__main__':
    import sys
    import json 
    dicty = perseus(sys.argv[1])
    fp = open('packard.json')
    packard = json.load(fp)
    pretty_print(dicty)
    
