import nltk

response = input("What word do you want tagged? (q = quit) ")
while response != "q":
  token = nltk.word_tokenize(response)
  tag = nltk.pos_tag(token)
  print("Your tagged word is: {}".format(tag))
  print("-" * 40)
  response = input("What word do you want tagged? (q = quit) ")
