from buildSenti import buildSenti
from math import pow, sqrt
import operator

ml = 2
senti = buildSenti()

def isValid(w):
   return True

def langFeatures(sent):
   pos, neg = 0, 0
   for word in sent:
      sent = senti.get(word, (0, 0))
      pos += sent[0]
      neg += sent[1]
   tot = pos / (pow(neg, 4) + 0.00001)
   #return {'pos': pos, 'neg': pow(neg, 2)}
   return {'sent': tot, 'length': len(sent)}

def getClassifier(corpus):
   return corpus.buildSentClassifier(langFeatures, 100, isValid)

def test(rev, classifier):
   predictions = []
   for section in rev:
      output = []
      for sent in section.sents():
         output.append(int(classifier.classify(langFeatures(sent))))
      out = reduce(operator.add, output) / len(output)
      predictions.append(out)

   return predictions
