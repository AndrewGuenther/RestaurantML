from buildSenti import buildSenti
import random, operator, nltk
import sys, os
from buildCorpus import buildCorpus
from crossval import crossval

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
   corpus = buildCorpus(["./training-clean/" + f for f in files], '/tmp/train/')
   
#for root, dirs, files in os.walk("./test-clean"):
#   testcorpus = buildCorpus(["./test-clean/" + f for f in files], '/tmp/test/')
crosses = crossval(corpus, 4)

for train_set, test_set in crosses:

   wordthings = {5: [w.lower() for w in train_set[5] if isValid(w)][:100],
                 4: [w.lower() for w in train_set[4] if isValid(w)][:100],
                 3: [w.lower() for w in train_set[3] if isValid(w)][:100],
                 2: [w.lower() for w in train_set[2] if isValid(w)][:100],
                 1: [w.lower() for w in train_set[1] if isValid(w)][:100]}

   words = reduce(operator.add, map(lambda L: ([(w.lower(),L) for w in wordthings[L]]),wordthings.keys()),[])

   random.shuffle(words)

   featureSets = [(langFeatures(w),l) for (w,l) in words]

   s = len(featureSets)
   train = featureSets

   classifier = nltk.NaiveBayesClassifier.train(train)
   for para, id in test_set:
      vals = {1:0, 2:0, 3:0, 4:0, 5:0}
      for sent in para:
         for word in [w.lower() for w in sent if isValid(w)]:
            output = classifier.classify(langFeatures(word))
            vals[output] = vals[output]+1
      print str(id) + ": ",
      print sorted(vals.items(), key=lambda (key, val): val)[-1][0]

#now, it is tested on the test set and the accuracy reported
#print "Accuracy: ",nltk.classify.accuracy(classifier,test)

#this is a nice function that reports the top most impactful features the NB classifier found
#print classifier.show_most_informative_features(10) 
