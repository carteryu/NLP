import nltk, string, math
from nltk import word_tokenize

def main():
	new_tokens = []
	word_hash = {}
	query_hash = {}
	tfidf_vector = []

	abstract_new_tokens = []
	abstract_word_hash  = {}
	abstract_query_hash = {}
	abstract_tfidf_vector = []


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
	file = open('cran/cran.qry', 'r')
	raw = file.read()
	abstract_file = open('cran/cran.all.1400')
	abstract_raw = abstract_file.read()

	sentences = clean(raw, closed_class_stop_words, new_tokens)
	term_count(sentences, tfidf_vector, word_hash)
	query_count(sentences, query_hash)
	calc_tfidf(sentences, tfidf_vector, word_hash, query_hash, 225)

	abstract_sentences = abstract_clean(abstract_raw, closed_class_stop_words, abstract_new_tokens)
	abstract_term_count(abstract_sentences, abstract_tfidf_vector, abstract_word_hash)
	abstract_query_count(abstract_sentences, abstract_query_hash)
	abstract_calc_tfidf(abstract_sentences, abstract_tfidf_vector, abstract_word_hash, abstract_query_hash, 1400)                           

def clean(text, closed_class_stop_words, new_tokens):
	tokens = word_tokenize(text)
	for token in tokens:
		if token in closed_class_stop_words or token in string.punctuation or token == '.I' or token == '.W':
			continue
		if token.isdigit() and len(token) == 3:
			new_tokens.append([])
		else:
			new_tokens[-1].append(token)
	return new_tokens

def abstract_clean(text, closed_class_stop_words, new_tokens):
	tokens = word_tokenize(text)
	for token in tokens:
		for token in tokens:
			return None

# tfidf = term frequency (how many times it appears in query) x idf (total number of queries / number of queries where term occurs)

# separate: queries with term

# tfidf_vector = 
#[
#	{
#		# query 1
#		word: [tf, idf, tfidf],
#		word: [tf, idf, tfidf],
#		word: [tf, idf, tfidf]
#	},
#	{
#		# query 2
#		word: [tf, idf, tfidf],
#		word: [tf, idf, tfidf],
#		word: [tf, idf, tfidf]
#	},
#	# etc
#]

# these modularized functions aren't time-efficient, but this is currently a brute force method to get some functionality whilst staying somewhat bug-free

def term_count(sentences, tfidf_vector, word_hash):
	for sentence in sentences:
		for word in sentence:
			word = word.lower()
			if word_hash.get(word):
				word_hash[word] += 1
			else:
				word_hash[word] = 1

def abstract_term_count(sentences, tfidf_vector, word_hash):
	return None
def query_count(sentences, query_hash):
	for sentence in sentences:
		word_vector = []
		for word in sentence:
			word = word.lower()
			if word in word_vector:
				continue
			word_vector.append(word)
			if query_hash.get(word):
				query_hash[word] += 1
			else:
				query_hash[word] = 1

def abstract_query_count(sentences, query_hash):
	return None

def calc_tfidf(sentences, tfidf_vector, word_hash, query_hash, total_queries):
	for sentence in sentences:
		tfidf_vector.append({})
		word_vector = []
		for word in sentence:
			word = word.lower()
			# calculate tf, idf, tfidf, and round to three decimal places
			if word in word_vector:
				tfidf_vector[-1][word][0] += 1
				tfidf_vector[-1][word][1] = math.floor(float(total_queries) / float(query_hash[word]) * 1000) / 1000
				tfidf_vector[-1][word][2] = math.floor(tfidf_vector[-1][word][0] * tfidf_vector[-1][word][1] * 1000) / 1000
			else:
				word_vector.append(word)
				tfidf_vector[-1][word] = [None, None, None]
				tfidf_vector[-1][word][0] = 1
				tfidf_vector[-1][word][1] = math.floor(float(total_queries) / float(query_hash[word]) * 1000) / 1000
				tfidf_vector[-1][word][2] = math.floor(tfidf_vector[-1][word][0] * tfidf_vector[-1][word][1] * 1000) / 1000
	print tfidf_vector

def abstract_calc_tfidf(sentences, tfidf_vector, word_hash, query_hash, total_queries):
	return None

main()
