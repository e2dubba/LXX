#!/usr/bin/env python3




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
    '''
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('passage', nargs='*') 
    args = parser.parse_args()
    key = args.passage 
    for doc in keys:
        opr en(doc)
        for row in doc:
            if len(row[36:].split()) >= 1:
                
    


