#!/usr/bin/env python3

import sqlite3
import os 


conn = sqlite3.connect('strongs.db')
c = conn.cursor()

c.execute('CREATE TABLE row_value (
		inflected_form TEXT NOT NULL,
		morphology TEXT NOT NULL,
		etymology TEXT NOT NULL,
		PRIMARY KEY (morphology, etymology) )')

def update_db(row):
	infl = row[:24].strip()
	morph = row[24:36].strip()
	etym_roots = row[36:].strip()
	c.execute('INSERT INTO row_value VALUES (?, ?, ?)',
			(infl, morph, etym_roots))





if __name__ = "__main__":
    '''
    The purpose of this script is going to be to read through the entire
    LXX files and create a database  of all of the multiword compounds, 
    and their inflected forms. Then it will take those inflected forms and 
    run them through perseus's cruncher, or perseus online, to find all of 
    the possible roots for each inflected form. The idea is to narrow down a
    list of the compound words and their respective lexical forms. Hopefully 
    reducing the number of ambiguous forms. For those compounds that only have 
    ambiguous forms a phrase book needs to be established so that User interaction
    need only occur once, or after given, can be queried to answer other ambiguities. 

    Database construction:
    1) inflect forms, packard parsing, roots (one to many; for this one the primary key is going to be the combination of parsing and roots)
    2) inflect forms, lexical forms (many to many)
    3) Packard Parsing, cruncher parsing (many to many)
    4) lexical forms, cruncher parsing (many to many)
    '''
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('passage', nargs='*') 
    args = parser.parse_args()
    key = args.passage 
    for doc in keys:
        open(doc)
        for row in doc:
            if len(row[36:].split()) >= 1:
                
    



