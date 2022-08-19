import string
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import sent_tokenize

tknzr = TweetTokenizer()
s0 = "what? it is! No thanks: okay!"

print(tknzr.tokenize(s0))
print(s0.split())
print(set(sent_tokenize(s0)))