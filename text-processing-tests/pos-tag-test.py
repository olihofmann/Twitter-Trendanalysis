import nltk

def extract_noun(text):
    is_noun = lambda pos: pos[:2] == "NN"
    tokens = nltk.word_tokenize(text)
    return [word for (word, pos) in nltk.pos_tag(tokens) if is_noun(pos)]

print(extract_noun("Can you please buy me a Arizona Ice Tea?"))