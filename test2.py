from buildSenti import buildSenti
from math import pow, sqrt

class Method:
   def isValid(self, w):
      return True

   def langFeatures(self, para):
      pos, neg = 0, 0
      for idx, word in enumerate(para):
         sent = self.senti.get(word, (0, 0))
         pos += sent[0]
         neg += sent[1]
      tot = pos / (pow(neg, 3) + 0.000001)
      #return {'pos': pos, 'neg': pow(neg, 2)}
      return {'sent': tot}

   def __init__(self, corpus):
      self.senti = buildSenti()
      self.ml = 2
      self.classifier = corpus.buildParaClassifier(self.langFeatures, 100, self.isValid)

   def test(self, rev):
      predictions = []
      for section in rev:
         vals = {}
         output = int(self.classifier.classify(self.langFeatures(section.words())))
         predictions.append(output)

      return predictions
