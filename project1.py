
def langFeatures(word):
	return {'word':word, 'first': word[0], 'last 2': word[-2:]}

ml = 3

scores = range(1, 6)

import random, operator, nltk
import sys, os
from buildCorpus import buildCorpus

for root, dirs, files in os.walk("./training-clean"):
   corpus = buildCorpus(["./training-clean/" + f for f in files], '/tmp/train/')
   
for root, dirs, files in os.walk("./test-clean"):
   testcorpus = buildCorpus(["./test-clean/" + f for f in files], '/tmp/test/')

wordthings = {5: corpus.words('5.txt'), 4: corpus.words('4.txt'), 3: corpus.words('3.txt'), 2: corpus.words('2.txt'), 1: corpus.words('1.txt')}

words = reduce(operator.add, map(lambda L: ([(w.lower(),L) for w in wordthings[L] if len(w) > ml]),scores),[])

random.shuffle(words)

featureSets = [(langFeatures(w),l) for (w,l) in words]

s = len(featureSets)
train = featureSets

classifier = nltk.NaiveBayesClassifier.train(train)
for id in testcorpus.fileids():
   print id
   for para in testcorpus.paras(id):
      vals = {1:0, 2:0, 3:0, 4:0, 5:0}
      for sent in para:
         for word in [w.lower() for w in sent if len(w) > ml]:
            output = classifier.classify(langFeatures(word))
            vals[output] = vals[output]+1
      print "Predicted Rating: ",
      print sorted(vals.items(), key=lambda (key, val): val)[-1][0]

#now, it is tested on the test set and the accuracy reported
#print "Accuracy: ",nltk.classify.accuracy(classifier,test)

#this is a nice function that reports the top most impactful features the NB classifier found
#print classifier.show_most_informative_features(10) 
