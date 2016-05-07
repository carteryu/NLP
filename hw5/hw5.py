import nltk, re, string, math
from nltk import word_tokenize

def main():
	word_hash = {}
	query_hash = {}
	tfidf_vector = []
	final_query_vector = []

	abstract_word_hash  = {}
	abstract_query_hash = {}
	abstract_tfidf_vector = []
	final_abstract_vector = []

	final_total_vector = []
	ranked_list = []

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

	sentences = clean(raw, closed_class_stop_words)
	term_count(sentences, word_hash)
	query_count(sentences, query_hash)
	calc_tfidf(sentences, tfidf_vector, word_hash, query_hash, 225)
	print 'query tfidf calculated'

	abstract_sentences = abstract_clean(abstract_file, closed_class_stop_words)
	term_count(abstract_sentences, abstract_word_hash)
	query_count(abstract_sentences, abstract_query_hash)
	calc_tfidf(abstract_sentences, abstract_tfidf_vector, abstract_word_hash, abstract_query_hash, 1400)
	print 'abstract tfidf calculated' 

	query_vector(sentences, tfidf_vector, final_query_vector)
	abstract_vector(sentences, abstract_tfidf_vector, final_query_vector, final_abstract_vector)
	create_final_vector(final_query_vector, final_abstract_vector, final_total_vector)
	print 'cosine similarity calculated'  

	cosine_rank(final_total_vector, ranked_list)
	print 'ranking finished. results outputted to ranks.txt'
	                        

def clean(text, closed_class_stop_words):
	line_array = []
	tokens = word_tokenize(text)
	for token in tokens:
		if token in closed_class_stop_words or token in string.punctuation or token == '.I' or token == '.W':
			continue
		if token.isdigit() and len(token) == 3:
			line_array.append([])
		elif not re.search(r'\d|\W', token):
			line_array[-1].append(token)
	return line_array

def abstract_clean(file, closed_class_stop_words):
	delete_flag = True
	line_array = []
	with file as f:
		abstract_concat = []
		for line in f:
			if line[:2] == ('.W'):
				delete_flag = False
			elif line[:2] == '.I' and abstract_concat:
				line_array.append(abstract_concat)
				abstract_concat = []
				delete_flag = True
			elif delete_flag == False:
				tokens = word_tokenize(line)
				for token in tokens:
					new_token = strip(token, closed_class_stop_words)
					if new_token:
						abstract_concat.append(new_token)
	return line_array

def strip(token, closed_class_stop_words):
	if not (token in closed_class_stop_words or re.search(r'\d|\W', token)):
		return token

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

def term_count(sentences, word_hash):
	for sentence in sentences:
		for word in sentence:
			word = word.lower()
			if word_hash.get(word):
				word_hash[word] += 1
			else:
				word_hash[word] = 1

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

def calc_tfidf(sentences, tfidf_vector, word_hash, query_hash, total_queries):
	for sentence in sentences:
		tfidf_vector.append({})
		word_vector = []
		for word in sentence:
			word = word.lower()
			# calculate tf, idf, tfidf, and round to three decimal places
			if word in word_vector:
				# consider normalizing the term frequencies
				tfidf_vector[-1][word][0] += 1
			else:
				word_vector.append(word)
				tfidf_vector[-1][word] = [None, None, None]
				tfidf_vector[-1][word][0] = 1
			# normalizing with respect to the length of the sentence
			tfidf_vector[-1][word][0] = float(tfidf_vector[-1][word][0]) / float(len(sentence))
			tfidf_vector[-1][word][1] = math.floor(math.log(float(total_queries) / float(query_hash[word])) * 1000) / 1000
			tfidf_vector[-1][word][2] = math.floor(tfidf_vector[-1][word][0] * tfidf_vector[-1][word][1] * 1000) / 1000

# final query vector = 
#[
#	[tfidf value 1, tfidf value 2, tfidf value 3, etc], 
#	[tfidf value 1, tfidf value 2, tfidf value 3, etc],
#	[tfidf value 1, tfidf value 2, tfidf value 3, etc],
#	etc
#]

def query_vector(sentences, tfidf_vector, final_query_vector):
	counter = 0
	for sentence in sentences:
		final_query_vector.append([])
		for word in sentence:
			if tfidf_vector[counter].get(word):
				final_query_vector[-1].append(tfidf_vector[counter].get(word)[2])
		counter += 1

# final abstract vector = 
#[
#	[
#		[tfidf value 1, tfidf value 2, tfidf value 3, etc], 
#		[tfidf value 1, tfidf value 2, tfidf value 3, etc],
#		[tfidf value 1, tfidf value 2, tfidf value 3, etc],
#		etc
#	],
#	[
#		[tfidf value 1, tfidf value 2, tfidf value 3, etc], 
#		[tfidf value 1, tfidf value 2, tfidf value 3, etc],
#		[tfidf value 1, tfidf value 2, tfidf value 3, etc],
#		etc
#	],
#	etc
#]

def abstract_vector(sentences, abstract_tfidf_vector, final_query_vector, final_abstract_vector):
	counter = 0
	tencount = 0
	gtencount = 0
	for sentence in sentences:
		final_abstract_vector.append([])
		for abstract in abstract_tfidf_vector:
		 	final_abstract_vector[-1].append([])
		 	for word in sentence:
		 		if abstract.get(word):
					final_abstract_vector[-1][-1].append(abstract.get(word)[2])
		 		else:
		 			final_abstract_vector[-1][-1].append(0)
		 	counter += 1

# cosine similarity (d1, d2) =  dot product(d1, d2) / ||d1|| * ||d2||

# final total vector = 
#[
#	[
#		[query number, abstract number, cosine similarity],
#		[query number, abstract number, cosine similarity],
#		[query number, abstract number, cosine similarity],
#		etc
#	],
#	[
#		[query number, abstract number, cosine similarity],
#		[query number, abstract number, cosine similarity],
#		[query number, abstract number, cosine similarity],
#		etc
#	],
#	etc
#]

def create_final_vector(final_query_vector, final_abstract_vector, final_total_vector):
	query_num = 0
	for query in final_query_vector:
		final_total_vector.append([])
		abstract_num = 0
		for abstract in final_abstract_vector[query_num]:
			final_total_vector[-1].append([])
			final_total_vector[-1][-1].append(query_num)
			final_total_vector[-1][-1].append(abstract_num)
			cosine_num = cosine_similarity(query, abstract)
			final_total_vector[-1][-1].append(cosine_num)
			abstract_num += 1
			if cosine_num == 0:
				final_total_vector[-1].pop()
		query_num += 1

def cosine_similarity(query, abstract):
	dot_product = 0
	query_magnitude = 0
	abstract_magnitude = 0
	for i in range(len(query)):
		dot_product += (query[i] * abstract[i])
		query_magnitude += query[i] ** 2
		abstract_magnitude += abstract[i] ** 2
	query_magnitude = query_magnitude ** 0.5
	abstract_magnitude = abstract_magnitude ** 0.5
	if not (query_magnitude * abstract_magnitude == 0):
		cosine_similarity = math.floor(dot_product / (query_magnitude * abstract_magnitude) * 1000) / 1000
	else:
		# returning a cosine similarity of zero if denominator is zero
		cosine_similarity = 0
	return cosine_similarity

def cosine_rank(vector, ranked_list):
	for cluster in vector:
		cluster.sort(key=lambda x: x[2])
		cluster.reverse()
		ranked_list.append(cluster)
	f = open('ranks.txt','w')
	for cluster in ranked_list:
		for rank in cluster:
			rank_one = rank[0] + 1
			rank_two = rank[1] + 1
			rank_three = rank[2]
			line = str(rank_one) + ' ' + str(rank_two) + ' '  + str(rank_three)
			f.write(line + '\n')
	
main()




































