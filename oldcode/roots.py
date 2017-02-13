#!/usr/bin/env python3

import sqlite3
import os 
import collections as coll 
import subprocess as sp
from xtermcolor import colorize
import re 

conn = sqlite3.connect('../strongs.db')
c = conn.cursor()


def create_row_table():
	c.execute('CREATE TABLE IF NOT EXISTS row_value ' 
			'(inflected_form TEXT NOT NULL, '
			'packard TEXT NOT NULL, ' 
			'etymology TEXT NOT NULL,  '
			'PRIMARY KEY (packard, etymology) )')


def create_phrase_book():
    c.execute('CREATE TABLE IF NOT EXISTS phrase_book '
            '(packard TEXT NOT NULL, '
            'perseus TEXT PRIMARY KEY)') 


def create_lexical():
    c.execute('CREATE TABLE IF NOT EXISTS compound_lexical '
            '(eytmology TEXT NOT NULL, '
            'lexical TEXT PRIMARY KEY)')


def create_roots_table():
    c.execute('CREATE TABLE IF NOT EXISTS roots_table '
            '(lexical TEX NOT NULL, '
            'perseus TEXT NOT NULL, ' 
            'form TEXT NOT NULL)')


def update_row_value_tabledb(row):
    infl = row[:24].strip()
    morph = row[24:36].strip()
    etym_roots = row[36:].strip()
    updating = (infl, morph, etym_roots)
    c.execute('INSERT INTO row_value VALUES (?, ?, ?)',
                    updating)
    conn.commit()
	

def up_phrase_book(form, perseus):
    c.execute('SELECT packard FROM row_value WHERE inflected_form = ?',
            (form, ))
    packard = c.fetchall()
    if len(packard) == 1:
        c.execute('INSERT INTO phrase_book (packard, perseus) '
            'VALUES (?, ?)', (packard[0], perseus) )
        conn.commit()
    

def lexdb(etymology, lexical):
    updating = (etymology, lexical)
    try:
        c.execute('INSERT INTO compound_lexical VALUES (?, ?)', updating)
        conn.commit()
    except sqlite3.IntegrityError:
        pass


def roots_table(lexical, perseus_morph, form):
    c.execute('INSERT INTO roots_table VALUES (?, ?, ?)', 
            (lexical, persus_morph, form))
    conn.commit()


def cruncher(form):
    poss_roots = sp.run(['cruncher'], input=form, stderr=sp.DEVNULL, 
            stdout=sp.PIPE, universal_newlines=True, env=os.environ).stdout
    poss_roots = poss_roots.split('\n')
    try: 
        poss_roots = poss_roots[1].replace('<NL>', '').split('</NL>')
    except IndexError:
        error_file.write(form + '\n')
    if not poss_roots[-1]:
        del poss_roots[-1]
    parsing_list = []
    for item in poss_roots:
        templist = item[2:].split(maxsplit=1)
        temptup = (templist[0],
                templist[1].split('\t', maxsplit=1)[0])
        parsing_list.append(temptup)

    return parsing_list


def packard_def(packard):
    cmd = 'diatheke -b Packard -k %s' % (packard)
    definition = sp.getoutput(cmd)
    definition = definition.split(':', maxsplit=1)[1].split(':', maxsplit=1)
    defi2 = re.split(r'([A-Z][a-z]*):', definition[1])
    defi2.insert(0, definition[0].strip())
    def_dict = coll.OrderedDict(zip(defi2[0::2], defi2[1::2]))
    print(def_dict)
    return def_dict


def man_up_phrase_book(form, parsing_list, root_set):
    '''
    User interface for adding entries into the morphology phrase_book
    '''
    form = (form.upper(), )
    c.execute('SELECT * FROM row_value WHERE inflected_form '
            '= ?', (form))
    rows = c.fetchall()
    parsing_dict = coll.OrderedDict((str(x), y) for x, y in
            enumerate(parsing_list) )
    for lex in root_set:
        for row in rows:
            #try:
            c.execute('SELECT perseus FROM phrase_book WHERE '
                    'packard = ?', (row[1], ))
            perseus = c.fetchall()
            try:
                perseus = c.fetchall().pop()
                for tup in parsing_list:
                    if tup[1] == perseus:
                        lexdb(row[2], tup[0])
            except IndexError: #Catch's perseus = c.fetchall().pop() error
                # provide a user interface to fill out index 
                # I need to provide a way of selecting none of the above

                print('\n\nRow: ' + ', '.join(row))
                #print(packard_def(row[1]))
                def_dict = packard_def(row[1])
                for key, value in def_dict.items():
                    print('\t' + key + ':\t' + value)
                
                print('Which tupple agrees with the row?\n')
                for key, value in parsing_dict.items():
                    print(key + ': ' + str(value))
                print(str(len(parsing_dict)) + ': ' + 'None')
                index_num = input('Type index number: ')
                try:
                    correct_parsing = parsing_dict[str(index_num)]
                    perseus = correct_parsing[1]
                    try:
                        c.execute('INSERT INTO phrase_book (packard, perseus) '
                            'VALUES (?, ?)', (row[1], perseus) )
                        conn.commit()
                        break
                    except sqlite3.IntegrityError:
                        break
                    lexdb(row[2], correct_parsing[0]) 
                except KeyError:
                    continue


def read_cruncher():
    '''
    This takes the full list of unparsed forms from the databse and runs it
    through the cruncher, returning the form and its possible parsings
    '''
    error_file = open('ErrorList', 'w') # this is for testing purposes
    c.execute('SELECT inflected_form FROM row_value')
    parse_set = set(tup for tup in c.fetchall())
    num_forms = len(parse_set)
    num = 1
    for form in parse_set:
            print(num, 'of ', num_forms)
            form = form[0].lower()
            parsing_list = cruncher(form)
                        
            if not parsing_list:
                error_file.write(form + '\n')
                continue
            if len(parsing_list) == 1:
                try:
                    up_phrase_book(form, parsing_list[0][1])
                    c.execute('SELECT etymology FROM row_value '
                            'WHERE inflected_form = ?', (form.upper(), ))
                    etymology = c.fetchone()
                    lexdb(etymology[0], parsing_list[0][0])
                except sqlite3.IntegrityError:
                    continue
            root_set = set(i[0] for i in parsing_list)
            if len(root_set) == 1:
                # Should I look up the value of packard morphology? And how?
                c.execute('SELECT etymology FROM row_value '
                        'WHERE inflected_form = ?', (form, ))
                etym = c.fetchone()
                try:
                    print(colorize(etym[0] + root_set.pop(), ansi=3))
                    lexdb(etym[0], root_set.pop())
                except TypeError:
                    error_file.write(form + '\n')
            else:
                man_up_phrase_book(form, parsing_list, root_set)

            num += 1


if __name__ == '__main__':
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
    1) inflect forms, packard parsing, roots (one to many; 
       for this one the primary key is going to be the combination of parsing and roots)
    2) inflect forms, lexical forms (many to many)
    3) Packard Parsing, cruncher parsing (many to many)
    4) lexical forms, cruncher parsing (many to many)
    '''
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('argus', nargs='*') 
    args = parser.parse_args()
    books =  args.argus

    error_file = open('../ErrorList', 'w')

    create_row_table()
    create_phrase_book()
    create_lexical()
    create_roots_table()


    for book in books:
        print(book)
        for row in open(book):
            if len(row[36:].strip().split()) >= 2:
                try:
                    update_row_value_tabledb(row)
                except sqlite3.IntegrityError: 
                    continue 
            #else: 
              #  continue 
    
    read_cruncher()
    error_file.close()
