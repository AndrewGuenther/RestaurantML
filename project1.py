from buildSenti import buildSenti
import random, operator, nltk
import sys, os
from buildCorpus import buildCorpus
from crossval import crossval
from math import pow, sqrt

senti = buildSenti()

ml = 2

def isValid(w):
   if len(w) > ml and w.isalpha():
      return True
   return False

def langFeatures(word):
   sent = senti.get(word, (0, 0))[0] - senti.get(word, (0, 0))[1] 
   return { 'sent': sent}
#   return {'sent': sent, 'word':word, 'first': word[0], 'last 2': word[-2:]}

for root, dirs, files in os.walk("./training-clean"):
   corpus = buildCorpus(["./training-clean/" + f for f in files])
   
for root, dirs, files in os.walk("./test-clean"):
   testcorpus = buildCorpus(["./test-clean/" + f for f in files])

crosses = crossval(corpus, 4)

rmss = []
for idx, (train_set, test_set) in enumerate(crosses):
   print "Random Validation Set", idx + 1, ":", test_set.keys()
   words = [w for rev in train_set.values() for w in rev.words()]

   random.shuffle(words)
   featureSets = [(langFeatures(w.lower()), rank) for (reviwer, rank, w) in words if isValid(w)]

   limit = {'5':0, '4':0, '3':0, '2':0, '1':0}
   for feature, rank in featureSets:
      if limit[rank] > 100:
         featureSets.remove((feature, rank))
      limit[rank] += 1

   s = len(featureSets)
   train = featureSets

   total = 0
   classifier = nltk.NaiveBayesClassifier.train(train)

   for f, rev in test_set.items():
      for reviewer, score, para in rev.paras():
         vals = {}
         for word in para:
            if isValid(word.lower()):
               output = classifier.classify(langFeatures(word.lower()))
               vals[output] = vals.get(output, 0) + 1
         diff = int(score) - int(sorted(vals.items(), key=lambda (key, val): val)[-1][0])
         total += pow(diff, 2)

      rms = sqrt(total / (len(test_set) * 4))
      rmss.append(rms)
#      print f
#      print "RMS:\t\t", rms

   sum = 0
   for rms in rmss:
      sum += rms
   print "Average RMS error rate on validation set:", (sum / len(rmss))
   print

#now, it is tested on the test set and the accuracy reported
#print "Accuracy: ",nltk.classify.accuracy(classifier,test)

#this is a nice function that reports the top most impactful features the NB classifier found
#print classifier.show_most_informative_features(10) 
