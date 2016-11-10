#!/usr/bin/env python3

import os
import subprocess as sp

def cruncher(form):
    poss_roots = sp.run(['cruncher'], input=form, stdout=sp.PIPE, 
            universal_newlines=True, env=os.environ).stdout
    poss_roots = poss_roots.split('\n')
    try: 
        poss_roots = poss_roots[1].replace('<NL>', '').split('</NL>')
    except IndexError:
        print('Error! ' + form + '\n')
        
    parsing_list = []
    for item in poss_roots:
        templist = item[2:].split(maxsplit=1)
        print(templist)
        temptup = (templist[0],
                templist[1].split('\t', maxsplit=1)[0])
        parsing_list.append(temptup)

    return parsing_list

if __name__ == '__main__':
    import sys
    print(cruncher(sys.argv[1]))
    
