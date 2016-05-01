import nltk, sys, os, string
from nltk import word_tokenize
from collections import defaultdict

closed_class_stop_words = ['a','the','an','and','or','but','about','above','after','along','amid','among',\
                           'as','at','by','for','from','in','into','like','minus','near','of','off','on',\
                           'onto','out','over','past','per','plus','since','till','to','under','until','up',\
                           'via','vs','with','that','can','cannot','could','may','might','must',\
                           'need','ought','shall','should','will','would','have','had','has','having','be',\
                           'is','am','are','was','were','being','been','get','gets','got','gotten',\
                           'getting','seem','seeming','seems','seemed',\
                           'enough', 'both', 'all', 'your' 'those', 'this', 'these', \
                           'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',\
                           'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',\
                           'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',\
                           'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',\
                           'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',\
                           'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',\
                           'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',\
                           'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', \
                           'anything', 'anytime' 'anywhere', 'everybody', 'everyday',\
                           'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',\
                           'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',\
                           'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',\
                           'you','your','yours','me','my','mine','I','we','us','much','and/or'
                           ]

new_tokens = []
tfidf_hash = []

def clean(text):
	tokens = word_tokenize(text)
	for token in tokens:
		if token in closed_class_stop_words or token in string.punctuation or token == '.I' or token == '.W':
			continue
		if token.isdigit() and len(token) == 3:
			new_tokens.append([])
		else:
			new_tokens[-1].append(token)
	return new_tokens

# [tf, total queries, queries with term, idf, tfidf]

def calc_tfidf(text):
	for sentence in text:
		for word in sentence:
			if tfidf_hash[word]:
				# need list of query lists
				tfidf_hash[word][0] += 1
				tfidf_hash[word][2]  
			else:
				tfidf_hash[word] = [1, 225, 1, 225, 225]

file = open('cran/cran.qry', 'r')
raw = file.read()
sentences = clean(raw)
print(sentences)
#calc_tfidf(sentences)

#use hashmap
#tfidf = term frequency (how many times it appears in query) x idf (total number of queries / number of queries where term occurs)

