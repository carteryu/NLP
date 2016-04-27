import nltk
# presume select statement
input = raw_input('What are you looking for?\n')

def parse(input):
    tokens = nltk.word_tokenize(input)
    tagged_tokens = nltk.pos_tag(tokens)
    print tagged_tokens 

    retrieval = None
    target = None
    nouns = 0
    n_types = ['NN', 'NNS', 'NNP', 'NNPS']
    n_list = []
    v_types = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    v_list = []
    for i in range(len(tagged_tokens)):
        token_list = list(tagged_tokens[i])
        if token_list[1] in n_types: 
            n_list.append(token_list[0])
    print n_list
parse(input)
# assuming the user writes proper english
# else throw some error
# one table attribute will always be there in the query
# if one table attribute in query and nothing else then likely a select *
# db schema:
# table students, columns: first name, last name, ID, major
# if NNS then column, if not check whether every NN-derivative is a table name
# if not NNP, it won't be in the form [VB] [NNP] [POS], therefore if there is POS, the format will be [function] [target] [retrieval]
# otherwise, must be in the form [function] [retrieval] [target]
# stripped of 's', target will always be a row
# with 'computer science majors', last term will match the column after being stripped
# then do a search of 'computer' and then 'computer science' in major column
# with 'students majoring in computer science', 'NNS' means last noun phrase is a row
