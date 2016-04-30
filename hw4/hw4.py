import sys, re, itertools

from decimal import Decimal, getcontext

def print_dictionary(d):
	for key in d:
		print(key)
		print(d[key],'\n')

# when token not in dictionary
def min_in_dict(dictionary):
	minimum = 100000
	for key in dictionary:
		if key != 'num':
			if minimum > dictionary[key]:
				minimum = dictionary[key]
	return minimum

# calculate bigram probability
def eval_word(i,sent,freq_dict,tag_dict,tag,prev_tag):
	if tag in tag_dict[sent[i]]:
		num = tag_dict[sent[i]][tag]
		den = freq_dict[tag]['num']
	else:
		num = min_in_dict(tag_dict[sent])
		den = freq_dict[tag]['num']
	likelihood = Decimal(num) / Decimal(den)

	if prev_tag == None:
		return likelihood

	if tag in freq_dict[prev_tag]:
		num = freq_dict[prev_tag][tag]
		den = freq_dict[prev_tag]['num']
	else:
		num = min_in_dict(freq_dict[prev_tag])
		den = freq_dict[prev_tag]['num']
	prior_prob = num / den

	return likelihood * prior_prob


def tag_sent(i,val,sent,freq_dict,tag_dict, tag_seq):
	pos = ''
	best = 0
	prev_tag = ''
	if i == len(sent):
		return val
	if i == 0:
		if sent[i] not in tag_dict:
			tag_seq[i] = 'NN'
			#word_val = eval_word(i,sent,freq_dict,tag_dict,'NN',None)
			value = tag_sent(i+1,val,sent,freq_dict,tag_dict,tag_seq)
			return tag_seq
		for key in tag_dict[sent[i]]:
			# print('-----------------key----------------')
			# print(key)
			# print('-----------------key----------------')
			if key == 'num':
				continue
			tag_seq[i] = key
			# print('-----------------tagsq----------------')
			# print(tag_seq)
			# print('-----------------tagsq----------------')
			word_val = eval_word(i,sent,freq_dict,tag_dict,key,None) + val
			# print('-----------------wordval----------------')
			# print(word_val)
			# print('-----------------wordval----------------')
			value = tag_sent(i+1,word_val,sent,freq_dict,tag_dict,tag_seq)
			if value > best:
				best = value
				pos = key
		# print('-----------------pos----------------')
		# print(pos)
		# print('-----------------pos----------------')
		tag_seq[i] = pos
		return tag_seq
				
				
	else:
		if sent[i] not in tag_dict:
			tag_seq[i] = 'NN'
			#word_val = eval_word(i,sent,freq_dict,tag_dict,'NN',None)
			value = tag_sent(i+1,val,sent,freq_dict,tag_dict,tag_seq)
			return value
		for key in tag_dict[sent[i]]:
			# print('-----------------tagsq----------------')
			# print(tag_seq)
			# print('-----------------tagsq----------------')
			if key == 'num':
				continue
			tag_seq[i] = key
			word_val = eval_word(i,sent,freq_dict,tag_dict,key,tag_seq[i-1]) + val
			value = tag_sent(i+1,word_val,sent,freq_dict,tag_dict,tag_seq)
			if value > best:
				best = value
				pos = key
		tag_seq[i] = pos
		return best

print('start')

input_file = sys.argv[1]
corpus_file = open(input_file, "r")

tag_dict = {}
freq_dict = { 'VB':{'num':0}, 'VBP':{'num':0},'VBZ':{'num':0},'PRT':{'num':0},
			'VBD':{'num':0},'VBG':{'num':0},'VBN':{'num':0},'NNP':{'num':0}, 
			'NNPS':{'num':0},'NN':{'num':0},'NNS':{'num':0},'JJ':{'num':0},
			'JJR':{'num':0},'JJS':{'num':0},'RB':{'num':0},'RBR':{'num':0},
			'RBS':{'num':0},'RP':{'num':0},'PRP':{'num':0}, 'PRP$':{'num':0}, 
			'PP$':{'num':0}, 'WP':{'num':0},'WP$':{'num':0},'WDT':{'num':0},
			'WRB':{'num':0},'CC':{'num':0},'CD':{'num':0},'DT':{'num':0},
			'PDT':{'num':0},'IN':{'num':0},'MD':{'num':0}, 'TO':{'num':0},
			'POS':{'num':0},'UH':{'num':0},'EX':{'num':0},'$':{'num':0},
			'FW':{'num':0},'SYM':{'num':0}, 'LS':{'num':0},'AFX':{'num':0},
			'ADVP-MNR':{'num':0},'HV':{'num':0}, 'NNS-4':{'num':0}}

num_words = 0
prev_tag = None
for line in corpus_file:
	sline = line.split()
	if (len(sline) == 2):
		if sline[1]=='COMMA' or sline[1]==',' or sline[1]=='#' or sline[1]=='(' or sline[1]==')' or sline[1]=='.' or sline[0]=='\"' or sline[0]=='(' or \
				sline[0]==')' or sline[1]==':' or sline[1]=='HYPH' or sline[1]=="``"\
				or sline[0]=='-LSB-' or sline[0]=='-RSB-' or sline[1]=='\'\'':
			continue
		if (sline[0].lower() not in tag_dict):
			tag_dict[sline[0].lower()] = {'num':0}
		pos_dict = tag_dict[sline[0].lower()]
		if (sline[1] not in pos_dict) :
			pos_dict[sline[1]] = 1
		else:
			pos_dict[sline[1]] += 1
		pos_dict['num'] += 1
		
		if prev_tag in freq_dict:
			bi_dict = freq_dict[prev_tag]
			if sline[1] not in bi_dict:
				bi_dict[sline[1]] = 1
			else:
				bi_dict[sline[1]] += 1

		freq_dict[sline[1]]['num'] += 1
		prev_tag = sline[1]
		num_words += 1

	elif (len(sline) == 0):
 		prev_tag = None

corpus_file.close()

print(freq_dict)

print('after training')


# normalize probabilities
for key in freq_dict:
	for  k in freq_dict[key]:
		freq_dict[key][k] = Decimal(freq_dict[key][k]) / (num_words)

dev_file = sys.argv[2]
text_file = open(dev_file,"r")


# hmm tagging
tags = []
sentence = []
for line in text_file:
	sline = line.split()
	if len(sline) == 0:
		if len(sentence) > 0:
			tag_seq = [None]*len(sentence)
			tag_seq = tag_sent(0,0,sentence,freq_dict,tag_dict,tag_seq)
			print(sentence)
			print(tag_seq)
			tags.append(tag_seq)
		sentence = []
		continue
	
	elif sline[0]==',' or sline[0]=='.' or sline[0]=='\"' or sline[0]=='(' or \
				sline[0]==')' or sline[0]==':' or sline[0]=='-' or sline[0]=="``"\
				or sline[0]=='\'\'' or sline[0] == 'COMMA':
			continue
	sentence.append(sline[0].lower())

print('done tagging')

print(tags)
merged = list(itertools.chain(*tags))

dev_file = sys.argv[2]
text_file = open(dev_file,"r")

# write output to output.pos
out = ''
for line in text_file:
	sline = line.split()
	if len(sline) == 0:
		out = out + '\n'
		continue
	if sline[0]==',' or sline[0]=='.' or sline[0]=='\"' or sline[0]=='(' or \
				sline[0]==')' or sline[0]==':' or sline[0]=='-' or sline[0]=="``"\
				or sline[0]=='\'\'' or sline[0] == 'COMMA':
		out = out + sline[0] + '\n'
		continue
	if merged:
		out = out + sline[0] + '\t' + merged.pop(0) + '\n'

text_file.close()

print('finished. tagged words should be contained in output.pos')

output = open("output.pos","w")
output.write(out)
output.close()

