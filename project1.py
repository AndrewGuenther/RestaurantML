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

   total = 0
   classifier = train_set.buildWordClassifier(langFeatures, 100, isValid)

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

   sum = 0
   for rms in rmss:
      sum += rms
   print "Average RMS error rate on validation set:", (sum / len(rmss))
   print

classifier = corpus.buildWordClassifier(langFeatures, 100, isValid)

for f, rev in testcorpus.items():
   print "Now showing predictions for", f
   prediction = []
   for reviewer, score, para in rev.paras():
      vals = {}
      for word in para:
         if isValid(word.lower()): 
            output = classifier.classify(langFeatures(word.lower()))
            vals[output] = vals.get(output, 0) + 1
      prediction.append(int(sorted(vals.items(), key=lambda (key, val): val)[-1][0]))
   print "Paragraph ratings:", prediction
   print
