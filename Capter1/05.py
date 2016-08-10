sentence="I am an NLPer"

#文字bi-gram
charGram=[sentence[i:i+2] for i in range(len(sentence)-1)]
print(charGram)

#単語bi-gram
words=[word.strip(".,") for word in sentence.split()] 
wordGram=["-".join(words[i:i+2]) for i in range(len(words)-1)]
print(wordGram)