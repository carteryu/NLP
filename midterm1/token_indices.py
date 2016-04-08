import nltk
import sys
import string

text = sys.argv[1]
tokens = nltk.word_tokenize(text)

index = 0

# Header
print("{0:10} \t|\t {1:10} \t|\t {2:10} \t|".format("Token","Start Index","End Index"))
print("-" * 65)

# Cycle through and print all our words
for word in tokens:
  line = ""
  
  # Undo our postorder increment if we've got a comma/semicolon/etc.
  if word in string.punctuation:
    index -= 1

  # Account for if a string starts with a punctuation
  if index == -1 and word in string.punctuation:
    index += 1

  # Add our word and starting index to our line
  line += "{0:10} \t\t {1:5} \t\t ".format(word, index)
  index += len(word)

  # Add our incremented index to our line, print, and assume we 
  # increment by 1 (space)
  line += "{0:14}".format(index)
  print(line)
  index += 1
