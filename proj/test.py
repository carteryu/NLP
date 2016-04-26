import nltk
# presume select statement
input = raw_input('What are you looking for?\n')

tokens = nltk.word_tokenize(input)
tagged_tokens = nltk.pos_tag(tokens)
print(tagged_tokens)

retrieval = None
target = None
nouns = 0
n_types = ['NN', 'NNS', 'NNP', 'NNPS']
for i in range(len(tagged_tokens)):
    token_list = list(tagged_tokens[i])
    if token_list[1] in n_types: 
        print('yes')
    else:
        print('no')
        
# assuming the user writes proper english
# else throw some error
# one table attribute will always be there in the query
# if one table attribute in query and nothing else then likely a select *
