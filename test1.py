from buildSenti import buildSenti
from math import sqrt

class Method:
   def isValid(self, w):
      if len(w) > 2 and w.isalpha():
         return True
      return False

   def langFeatures(self, word):
      sent = self.senti.get(word, (0, 0))[0] - self.senti.get(word, (0, 0))[1]
      return {'sent': sent}

   def test(self, rev):
      predictions = []
      for section in rev:
         vals = {}
         for word in section.words():
            if self.isValid(word.lower()):
               output = self.classifier.classify(self.langFeatures(word.lower()))
               vals[output] = vals.get(output, 0) + 1
         predictions.append(int(sorted(vals.items(), key=lambda (key, val): val)[-1][0]))

      return predictions

   def __init__(self, corpus):
      self.ml = 2
      self.senti = buildSenti()
      self.classifier = corpus.buildWordClassifier(self.langFeatures, 100, self.isValid)
