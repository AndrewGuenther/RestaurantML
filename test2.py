from buildSenti import buildSenti
from math import pow, sqrt

ml = 2
senti = buildSenti()

def isValid(w):
   return True

def langFeatures(para):
   pos, neg = 0, 0
   for idx, word in enumerate(para):
      sent = senti.get(word, (0, 0))
      pos += sent[0]
      neg += sent[1]
   tot = pos / pow(neg, 3)
   #return {'pos': pos, 'neg': pow(neg, 2)}
   return {'sent': tot}

def getClassifier(corpus):
   return corpus.buildParaClassifier(langFeatures, 100, isValid)

def test(rev, classifier):
   predictions = []
   for reviewer, score, para in rev.paras():
      vals = {}
      output = int(classifier.classify(langFeatures(para)))
      predictions.append(output)

   return predictions
