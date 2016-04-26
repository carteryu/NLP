import nltk
# presume select statement
input = raw_input('What are you looking for?\n')

tokens = nltk.word_tokenize(input)
tagged_tokens = nltk.pos_tag(tokens)
print(tagged_tokens)

retrieval = None
target = None
verbs = 0
nouns = 0
for i in range(len(tagged_tokens)):
    if 'NNP' in tagged_tokens[i]:
        print('yes')
    else:
        print('no')
        
# assuming the user writes proper english
# else throw some error
# one table attribute will always be there in the query
# if one table attribute in query and nothing else then likely a select *

