from buildSenti import buildSenti
from math import pow, sqrt
import operator
from nltk import word_tokenize, FreqDist

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
      tot = pos - neg 
      self.tots.inc(tot)
      self.pos.inc(pos)
      self.negs.inc(neg)

      return {'length': len(sent)}

   def __init__(self, corpus):
      self.tots = FreqDist()
      self.pos = FreqDist()
      self.negs = FreqDist()

      self.senti = buildSenti()
      self.ml = 2
      self.classifier = corpus.buildSentClassifier(self.langFeatures, 1000, self.isValid)

#      print "tots"
#      self.tots.tabulate()
#      print "pos"
#      self.pos.tabulate()
#      print "negs"
#      self.negs.tabulate()
      self.classifier.show_most_informative_features(5)

   def test(self, rev):
      predictions = []
      for section in rev:
         output = []
         for sent in section.sents():
            output.append(int(self.classifier.classify(self.langFeatures(sent))))
         out = reduce(operator.add, output) / len(output)
         predictions.append(out)

      return sum(predictions) / len(predictions)

#      return predictions
