def iter_mlxx(path):
    '''
    This is a generator function that goes through a specified directory,
    openining the mlxx files and returning a verse reference and a list of the
    the words. 
    '''
    listing = os.listdir(path)
    for l in listing:
        mfile = open(path + l)
        for line in mfile:
            for line in map(str.rstrip, mlxx_file):
                if len(line.split()) == 2:
                    word_buffer = []
                    verse = line
                elif line == '':
                    yield (verse, word_buffer)
                else:
                    word_buffer.append(split_row(line))

            yield (verse, word_buffer)
