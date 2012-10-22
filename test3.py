from buildSenti import buildSenti
from math import pow, sqrt
import operator
from nltk import word_tokenize

class Method:
   def isValid(self, w):
      return True

   def langFeatures(self, sent):
      pos, neg = 0, 0
      for word in sent: 
         sentiment = self.senti.get(word.lower(), (0, 0))
         #pos += sent[0]
         #neg += sent[1]
         pos += 1 if sentiment[0] > sentiment[1] else 0
         neg += 1 if sentiment[1] > sentiment[0] else 0
      tot = pos / (pow(neg, 2) if pow(neg, 2) > 0 else 1)
      return {'neg': pow(neg, 2), 'length': len(sent)}
#      return {'sentiment': tot, 'length': len(sent)}
#      return {"length": len(sent)}

   def __init__(self, corpus):
      self.senti = buildSenti()
      self.ml = 2
      self.classifier = corpus.buildSentClassifier(self.langFeatures, 1000, self.isValid)
#      self.classifier.show_most_informative_features(20)

   def test(self, rev):
      predictions = []
      for section in rev:
         output = []
         for sent in section.sents():
            output.append(int(self.classifier.classify(self.langFeatures(sent))))
         out = reduce(operator.add, output) / len(output)
         predictions.append(out)

      return predictions
