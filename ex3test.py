from buildSenti import buildSenti
from math import sqrt
import re
from nltk import bigrams
from nltk import pos_tag
class Method:
   def isValid(self):
      return True

   def langFeatures(self, rev):
      wordReuse = {}
      wordCnt, sentCnt, aveSentLength, aveWordLength = 0, 0, 0.0, 0.0
      iCnt = 0.0
      adjCount = 0

      for para in rev:
         for word in para.words():
            if len(word) > 3:
               wordReuse[word] = 1
            aveWordLength += len(word)
            wordCnt += 1

         for sent in para.sents():
            aveSentLength += len(sent)
            sentCnt += 1
         
         iCnt += len(re.findall(r"((\s+|^)I(\s+|'))", para.review))
         tagged = pos_tag(para.words())

         for (word, tag) in tagged:
            if (tag == 'RB' or tag == 'JJ') is True:
               adjCount += 1 

      adjCount = adjCount/wordCnt
      iCnt = iCnt/wordCnt

      if adjCount < .02:
         adjCount = 1
      elif adjCount < .04:
         adjCount = 2
      elif adjCount < .06:
         adjCount = 3
      elif adjCount < .08:
         adjCount = 4
      elif adjCount < .1:
         adjCount = 5
      elif adjCount < .12:
         adjCount = 6
      elif adjCount < .14:
         adjCount = 7
      else:
         adjCount = 8

      wordList = wordReuse.items()
      wordList = sorted(wordList, key=lambda x: x[1])

      aveWordLength = aveWordLength / wordCnt
      aveSentLength = aveSentLength / sentCnt
      aveSentLength = int(aveSentLength / 3)


      features = {'adj': adjCount, 'sentLen': aveSentLength}
      features = dict(features.items() + wordReuse.items())        
      return features
 
   def test(self, rev):
      name = self.classifier.classify(self.langFeatures(rev))
      return name

   def __init__(self, corpus):
      self.senti = buildSenti()
      self.classifier = corpus.buildRevClassifier(self.langFeatures, 100, self.isValid)
