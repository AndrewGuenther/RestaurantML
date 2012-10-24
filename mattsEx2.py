from buildSenti import buildSenti
from nltk.corpus import stopwords
from math import sqrt

class Method:
   def isValid(self, w):
      if len(w) > 3 and w.isalpha():
         return True
      return False

   def langFeatures(self, word):
      sent = self.senti.get(word, (0, 0))[0] - self.senti.get(word, (0, 0))[1]
      if sent < 0:
          neg = True
      else:
          neg = False
      return {'sent':sent,'Negative': neg, word:True, "word":word}

   def test(self, rev):
      vals = {}
      stopset = set(stopwords.words('english'))
      for section in rev:
         for word in section.words():
            if word not in stopset:
                if self.isValid(word.lower()):
                    output = self.classifier.classify(self.langFeatures(word.lower()))
                    vals[output] = vals.get(output, 0) + 1

      prediction, count = 0.0, 0.0
      for (output, occurances) in vals.items():
      	count += occurances
      	prediction += int(output) * occurances
      prediction = prediction/count 
      return prediction

   def __init__(self, corpus):
      self.ml = 2
      self.senti = buildSenti()
      self.classifier = corpus.buildWordClassifier(self.langFeatures, 100, self.isValid)
