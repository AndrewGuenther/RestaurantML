#Language classification demo using NLTK and python
#uses the Universal Declaration of Human Rights (udhr) corpus, and Naive Bayes classifier from NLTK
#by Foaad Khosmood / Cal Poly / Oct 5, 2012
#Updated by Matthew Parker to work on word sentiment analysis
# Oct 14 2012

#First define a function that produces features from a given object, in this case one word
#Three string features are extracted per word: first two letters, last letter and last three letters
#Note that featuresets are dictionaries. That's what the classifier takes as input
def langFeatures(word):
	return {'word':word, 'last 2': word[-2:]}

#minimum word length we want to consider
ml = 0

#languages we are interested in (over 300 available in the udhr corpus) MUST be "Latin1" coding
scores = range(1, 6)

#importing standard packages + NLTK
import random,operator, nltk
from nltk.corpus import udhr
import sys, os
from buildCorpus import buildCorpus

for root, dirs, files in os.walk("./training-clean"):
   corpus = buildCorpus(["./training-clean/" + f for f in files])

wordthings = {5: corpus.words('5.txt'), 4: corpus.words('4.txt'), 3: corpus.words('3.txt'), 2: corpus.words('2.txt'), 1: corpus.words('1.txt')}

#use Python's functional features to get a big list of (word,Langauge) from languages, we are interested in
words = reduce(operator.add, map(lambda L: ([(w.lower(),L) for w in wordthings[L] if len(w) > ml]),scores),[])

#next three lines do the same thing without using lambda, map() or reduce()
#engWords, afrWords, itaWords = udhr.words('English-Latin1'), udhr.words('Afrikaans-Latin1'), udhr.words('Italian-Latin1')
#words = [(w,'English') for w in engWords] + [(w,'Afrikaans') for w in afrWords] + [(w,'Italian') for w in itaWords]
#words = [(w,l) for (w,l) in words if len(w) >= ml]

#(word, Langauge) tuples are still in file access order. This randomizes them
random.shuffle(words)

#convert the (word,L) -> (features(word),L)
featureSets = [(langFeatures(w),l) for (w,l) in words]

#splits training and test sets, it's about 1/5 test
s = len(featureSets)
train, test = featureSets[:int(s * 0.8)], featureSets[int(s * 0.8):]

#NLTK's built-in implementation of the Naive Bayes classifier is trained
classifier = nltk.NaiveBayesClassifier.train(train)

'''
for paras in test:
   total = 0.0
   count = 0.0
   #print paras
   for sents in paras:
      #print sents
      for words in sents:
         #print "Pairing: " ,
         #print words,
         #print " Score: ",
         count = count + 1
         total = total + classifier.classify(langFeatures(words))
   print "First word in paragraph is: ",
   print paras[0],
   print " aggregate score is: ",
   print total/count
'''   
#now, it is tested on the test set and the accuracy reported
print "Accuracy: ",nltk.classify.accuracy(classifier,test)

#this is a nice function that reports the top most impactful features the NB classifier found
print classifier.show_most_informative_features(10) 
