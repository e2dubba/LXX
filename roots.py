#!/usr/bin/env python3

import sqlite3
import os 


conn = sqlite3.connect('strongs.db')
c = conn.cursor()

def create_row_table():
	c.execute('CREATE TABLE IF NOT EXISTS row_value ' 
			'(inflected_form TEXT NOT NULL, '
			'morphology TEXT NOT NULL, ' 
			'etymology TEXT NOT NULL,  '
			'PRIMARY KEY (morphology, etymology) )')


def create_phrase_book():
    c.execute('CREATE TABLE IF NOT EXISTS phrase_book ('
        'packard TEXT NOT NULL, '
        'perseus TEXT NOT NULL)') 


def create_lexical():
    c.execute('CREATE TABLE IF NOT EXISTS compound_lexical '
            '(form TEXT NOT NULL, '
            'lexical TEXT NOT NULL)')


def update_db(row):
	infl = row[:24].strip()
	morph = row[24:36].strip()
	etym_roots = row[36:].strip()
	c.execute('INSERT INTO row_value VALUES (?, ?, ?)',
			(infl, morph, etym_roots))
	conn.commit()
	

<<<<<<< HEAD
def parse_phrase_book(form, perseus):
    c.execute('SELECT morphology WHERE inflected_form = ?',
            (form))
    packard = c.fetchall()
    if len(packard) == 1:
        c.execute('INSERT INTO phrase_book (packard, perseus) '
            'VALUES (?, ?)', (packard, perseus) )
        conn.commit()
    

def lexdb(form, lexical):
    c.execute('INSERT INTO compound_lexical (form, lexical) '
            'VALUES (?, ?)', (form, lexical) )
    conn.commit()


def read_cruncher():
    '''
    This takes the full list of unparsed forms from the databse and runs it
    through the cruncher, returning the form and its possible parsings
    '''
    c.execute('SELECT inflected_form FROM row_values')
    parse_set = set(tup for tup in c.fetchall())
    num_forms = len(parse_set)
    num = 1
    for form in parse_set:
            form = form.lower()
            print("Forms to be parsed:", num, 'of', num_forms)
            poss_roots = sp.run(['cruncher'], input=form, stdout=sp.PIPE,
                            universal_newlines=True, env=os.environ).stdout
            poss_roots = poss_roots.split('\n')
            try: 
                poss_roots = poss_roots[1].replace('<NL>', '').split('</NL>')
            except IndexError:
                error_file.append(form, '\n')
            if not poss_roots[-1]:
                del poss_roots[-1]
            parsing_list = []
            for item in poss_roots:
                templist = item[2:].split(maxsplit=1)
                temptup = (templist[0],
                        templist[1].split('\t',maxsplit=1)[0])
                parsing_list.append(temptup)
            
            if len(parsing_list) == 1:
                    parse_phrase_book(form, parsing_list[0][1])
            root_set = set(i[0] for i in parsing_list)
            if len(root_set) == 1:
                lexdb(form, root_set.pop())
                

=======
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
                
>>>>>>> 88c423a5847581835a1a2af67775ee809ba28063


if __name__ == "__main__":
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
    error_file = open('ErrorList', 'w')
    for doc in keys:
        open(doc)
        for row in doc:
            if len(row[36:].split()) >= 1:
                
