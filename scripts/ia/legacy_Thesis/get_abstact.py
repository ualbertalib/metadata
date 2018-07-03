'''import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
#nltk.download('stopwords')
string =''
with open('absorptionbyairw00pinn_djvu.txt', 'r') as file:
	for line in file:
		line = line.replace('\n', '')
		string = string + line
tokens = RegexpTokenizer(r'\w+')
tokens = tokens.tokenize(string)
tagged = nltk.pos_tag(tokens)
tok = []
for w in tokens:
	if w not in stopwords.words('english'):
		tok.append(w)
print (tok)


import uts
string =''
with open('absorptionbyairw00pinn_djvu.txt', 'r') as file:
	for i, line in enumerate(file):
		if i < 1000:
			line = line.replace('\n', '')
			string = string + line
model = uts.C99(window=2)
boundary = model.segment(string)
# output: [1, 0, 1, 0]
print(boundary)'''

from os import listdir, getcwd, chdir, makedirs
from os.path import isfile, join, exists
import nltk
import nltk.data
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import math
sentencer = nltk.data.load('tokenizers/punkt/english.pickle')
#nltk.download('stopwords')

mypath = "/home/danydvd/git/remote/metadata/scripts/ia/files/txt/"
docs ={}
docs['tokens'] = {}
docs['sentences'] = {}
tf = {}
for i, filename in enumerate([f for f in listdir(mypath) if isfile(join(mypath, f))]):
	print ('processing %s' %(str(i+1))) 
	with open(join(mypath, filename), 'r') as file:
		filen = filename.replace('_djvu.txt', '')
		string = ''
		for line in file:
			line = line.replace('\n', '')
			string = string + line
		if string != '':
			docs['tokens'][filen] = []
			tokens = RegexpTokenizer(r'\w+')
			tokens = tokens.tokenize(string)
			for w in tokens:
				if w not in stopwords.words('english') and len(w) > 1:
					docs['tokens'][filen].append(w)
			sentence = sent_tokenize(string)
			docs['sentences'][filen] = sentence
	file.close()
print (docs['sentences'])

def get_TF(docs, word, tf):
	if word in tf.keys():
		pass
	else:
		count = 0
		for key in docs.keys():
			for w in docs[key]:
				if w == word:
					count +=1
		tf[word] = count
	return (tf)

def get_freq(tf):
	freq = 0 
	for key in tf.keys():
		freq = freq + tf[key]
	return (freq)

def get_IC(docs, word, tf):
	tf = get_TF(docs, word, tf)
	freq = get_freq(tf)
	freq_prime = freq - tf[word]
	ic = -math.log10((tf[word]+1)/(freq + freq_prime))
	return (ic)

for key in docs.keys():
	for word in docs[key]:
		get_TF(docs, word, tf)

for key in docs.keys():
	for word in docs[key]:
		ic = get_IC(docs, word, tf)		
		print (word, ic)