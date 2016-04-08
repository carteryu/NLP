# Good luck

import nltk
import sys

text = sys.argv[1]
tokens = nltk.word_tokenize(text)
tags = nltk.pos_tag(tokens)
print(tags)
