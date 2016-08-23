#!/usr/bin/env python3

import sqlite3
import os 


conn = sqlite3.connect('strongs.db')
c = conn.cursor()

<<<<<<< HEAD
c.execute('CREATE TABLE row_value (
		inflected_form TEXT NOT NULL,
		morphology TEXT NOT NULL,
		etymology TEXT NOT NULL,
		PRIMARY KEY (morphology, etymology) )')
=======
def create_row_table():
	c.execute('CREATE TABLE IF NOT EXISTS row_value (
			inflected_form TEXT NOT NULL,
			morphology TEXT NOT NULL,
			etymology TEXT NOT NULL,
			PRIMARY KEY (morphology, etymology) )')

>>>>>>> bb82e5ebb983d7e9453b9d45b80a8ad66b43440c

def update_db(row):
	infl = row[:24].strip()
	morph = row[24:36].strip()
	etym_roots = row[36:].strip()
	c.execute('INSERT INTO row_value VALUES (?, ?, ?)',
			(infl, morph, etym_roots))
	conn.commit()
	

def read_cruncher():
	c.execute('SELECT inflected_form FROM row_values')
	parse_set = set(tup for tup in c.fetchall())
	num_forms = len(parse_set)
	num = 1
	for form in parse_set:
		form = form.lower()
		print("Forms to be parsed:", num, 'of', num_forms)
		poss_roots = sp.run(['cruncher'], input=form, stdout=sp.PIPE,
				universal_newlines=True, env=os.environ).stdout
		poss_roots = poss_roots.replace('<NL>', '').replace('</NL>',
				'\n').split('\n')
		try:
			del poss_roots[0]
			del poss_roots[-2]
		except IndexError:
			error_doc.write(greek.decode(form))
		


	





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
                
    



