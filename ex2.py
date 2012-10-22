from buildSenti import buildSenti
from math import sqrt

class Method:
   def isValid(self, w):
      return True

   def langFeatures(self, rev):
      pos = 0
      neg = 0
      for section in rev:
         for word in section.words():
            sent = self.senti.get(word, (0, 0)) 
            pos += sent[0]
            neg += sent[1]
      return {'pos': pos, 'neg': neg}

   def test(self, rev):
      output = self.classifier.classify(self.langFeatures(rev))
      return float(output)

   def __init__(self, corpus):
      self.ml = 2
      self.senti = buildSenti()
      self.classifier = corpus.buildRevClassifier(self.langFeatures, 100000, self.isValid)
      self.classifier.show_most_informative_features(5)
