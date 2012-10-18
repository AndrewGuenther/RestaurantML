from buildSenti import buildSenti
from math import sqrt

ml = 2
senti = buildSenti()

def isValid(w):
   if len(w) > ml and w.isalpha():
      return True
   return False

def langFeatures(word):
   sent = senti.get(word, (0, 0))[0] - senti.get(word, (0, 0))[1]
   return {'sent': sent}

def getClassifier(corpus):
   return corpus.buildWordClassifier(langFeatures, 100, isValid)

def test(rev, classifier):
   predictions = []
   for section in rev:
      vals = {}
      for word in section.words():
         if isValid(word.lower()):
            output = classifier.classify(langFeatures(word.lower()))
            vals[output] = vals.get(output, 0) + 1
      predictions.append(int(sorted(vals.items(), key=lambda (key, val): val)[-1][0]))
      #predictions.append(3.8)

   return predictions
