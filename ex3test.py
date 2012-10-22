from buildSenti import buildSenti
from math import sqrt
import re
from nltk import bigrams

class Method:
   def isValid(self):
      return True

   def langFeatures(self, rev):
      wordReuse = {}
      wordCnt, sentCnt, aveSentLength, aveWordLength = 0, 0, 0.0, 0.0
      iCnt = 0.0
      bigramList = []
      for para in rev:
         for word in para.words():
            if len(word) > 3:
               wordReuse[word] = wordReuse.get(word, 0) + 1
            aveWordLength += len(word)
            wordCnt += 1

         for sent in para.sents():
            aveSentLength += len(sent)
            sentCnt += 1
         iCnt += len(re.findall(r"((\s+|^)I(\s+|'))", para.review))
         bigramList.append(bigrams(para.words()))
      iCnt = iCnt/wordCnt

      wordList = wordReuse.items()
      wordList = sorted(wordList, key=lambda x: x[1])

      aveWordLength = aveWordLength / wordCnt
      aveSentLength = aveSentLength / sentCnt

      features = {'len': wordCnt, 'wordLen': aveWordLength, 'richness': len(wordList), 
      'sentLen': aveSentLength, 'popWord': wordList[0], 'popWord2': wordList[1], 
      'iCnt': iCnt}

      #for bigram in bigramList:
         #features[tuple(bigram)]= 1
                  
      return features
 
   def test(self, rev):
      name = self.classifier.classify(self.langFeatures(rev))
      return name

   def __init__(self, corpus):
      self.senti = buildSenti()
      self.classifier = corpus.buildRevClassifier(self.langFeatures, 100, self.isValid)
