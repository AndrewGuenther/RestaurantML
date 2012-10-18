from nltk import NaiveBayesClassifier
import random

#All reviews are held in this review class
class Review:
   def __init__(self, reviewer, ratings):
      self.reviewer = reviewer
      self.ratings = ratings

   #All getters return a tuple (reviewer, rating, content) where content is either
   #the list of paragraphs or list of sentences or list of words
   def scores(self):
      return [rating for rating, sents in self.ratings]

   def paras(self):
      ret = []
      for rating, sents in self.ratings:
         para = [word for sent in sents for word in sent]
         ret.append((self.reviewer, rating, para))
      return ret

   def sents(self):
      ret = []
      for rating, sents in self.ratings:
         for sent in sents:
            ret.append((self.reviewer, rating, sent))
      return ret

   def words(self):
      ret = []
      for rating, sents in self.ratings:
         for sent in sents:
            for word in sent:
               ret.append((self.reviewer, rating, word))
      return ret

class ReviewSet(dict):
   def __init__(self, *args, **kw):
      super(ReviewSet,self).__init__(*args, **kw)

   def buildWordClassifier(self, features, normalize, validity):
      words = [w for rev in self.values() for w in rev.words()]

      random.shuffle(words)
      featureSets = [(features(w.lower()), rank) for (reviwer, rank, w) in words if validity(w)]

      limit = {'5':0, '4':0, '3':0, '2':0, '1':0}
      for feature, rank in featureSets:
         if limit[rank] > normalize:
            featureSets.remove((feature, rank))
         limit[rank] += 1

      return NaiveBayesClassifier.train(featureSets)

   def buildSentClassifier(self, features, normalize, validity):
      sents = [s for rev in self.values() for s in rev.sents()]

      random.shuffle(sents)

      featureSets = [(features(sent), rank) for (reviwer, rank, sent) in sents if validity(sent)]

      limit = {'5':0, '4':0, '3':0, '2':0, '1':0}
      for feature, rank in featureSets:
         if limit[rank] > normalize:
            featureSets.remove((feature, rank))
         limit[rank] += 1

      return NaiveBayesClassifier.train(featureSets)

   def buildParaClassifier(self, features, normalize, validity):
      paras = [p for rev in self.values() for p in rev.paras()]

      random.shuffle(paras)

      featureSets = [(features(para), rank) for (reviwer, rank, para) in paras if validity(para)]

      limit = {'5':0, '4':0, '3':0, '2':0, '1':0}
      for feature, rank in featureSets:
         if limit[rank] > normalize:
            featureSets.remove((feature, rank))
         limit[rank] += 1

      return NaiveBayesClassifier.train(featureSets)
