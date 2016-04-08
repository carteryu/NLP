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
            table_add(line)

def table_add(line):
    s = line.split()
    token = s[0]
    pos = s[1]
    entry = table[token]
    if entry:
        if entry[pos]:
            entry[pos] += 1
        else:
            entry[pos] = 1
    else:
        entry = {token, pos}

main()
        
