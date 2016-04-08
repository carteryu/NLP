import nltk

def main():
    #commenting out for quicker testing purposes
    #input_file = input('Enter path of file to score (in single quotes):')
    #table(input_file)
    table('WSJ_24.pos')
    print 'finished'

def table(input_file):
    training_set = open(input_file, 'r')
    table = {} 
    for line in training_set:
        if line.strip():
            table_add(line, table)

def table_add(line, table):
    s = line.split()
    token = s[0].lower()
    pos = s[1]
    entry = table.get(token)
    if entry:
        entry_pos = table[token].get(pos)
        if entry_pos: 
            table[token][pos] += 1
        else:
            table[token][pos] = 1
    else:
        table[token] = {pos: 1}

main()
        
