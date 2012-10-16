from buildSenti import buildSenti
import random, operator, nltk
import sys, os
from buildCorpus import buildCorpus
from crossval import crossval
from math import pow, sqrt

senti = buildSenti()

ml = 2

def isValid(w):
   if len(w) > ml and w in senti and w.isalpha():
      return True
   return False

def langFeatures(word):
   sent = 1 if senti.get(word, (0, 0))[0] > senti.get(word, (0, 0))[1] else -1 
#   return { 'sent': sent}
   return {'sent': sent, 'word':word, 'first': word[0], 'last 2': word[-2:]}

for root, dirs, files in os.walk("./training-clean"):
   corpus = buildCorpus(["./training-clean/" + f for f in files])
   
#for root, dirs, files in os.walk("./test-clean"):
#   testcorpus = buildCorpus(["./test-clean/" + f for f in files], '/tmp/test/')
crosses = crossval(corpus, 4)

for train_set, test_set in crosses:
   print "Cross:"

#   wordthings = {5: [w.lower() for w in train_set.get(5, []) if isValid(w)][:100],
#                 4: [w.lower() for w in train_set.get(4, []) if isValid(w)][:100],
#                 3: [w.lower() for w in train_set.get(3, []) if isValid(w)][:100],
#                 2: [w.lower() for w in train_set.get(2, []) if isValid(w)][:100],
#                 1: [w.lower() for w in train_set.get(1, []) if isValid(w)][:100]}

#   words = reduce(operator.add, map(lambda L: ([(w.lower(),L) for w in wordthings[L]]),wordthings.keys()),[])
   words = [w for rev in train_set.values() for w in rev.words()]

   random.shuffle(words)
   featureSets = [(langFeatures(w.lower()), rank) for (reviwer, rank, w) in words if isValid(w)]

   s = len(featureSets)
   train = featureSets

   total = 0
   classifier = nltk.NaiveBayesClassifier.train(train)
   for rev in test_set.values():
      for reviewer, score, para in rev.paras():
         vals = {}
         for word in para:
            if isValid(word.lower()):
               output = classifier.classify(langFeatures(word.lower()))
               vals[output] = vals.get(output, 0) + 1
         diff = int(score) - int(sorted(vals.items(), key=lambda (key, val): val)[-1][0])
         total += pow(diff, 2)

   print sqrt(total / (len(test_set) * 4))

#now, it is tested on the test set and the accuracy reported
#print "Accuracy: ",nltk.classify.accuracy(classifier,test)

#this is a nice function that reports the top most impactful features the NB classifier found
#print classifier.show_most_informative_features(10) 
