from nltk import NaiveBayesClassifier, word_tokenize
import random
from nltk.tokenize.punkt import PunktSentenceTokenizer

class ReviewItem:
   def __init__(self, review, rating):
      self.tok = PunktSentenceTokenizer()
      self.rating = rating
      self.review = review

   def words(self):
      return word_tokenize(self.review)

   def sents(self):
      return self.tok.tokenize(self.review)

class Review:
   def __init__(self, reviewer, sections):
      self.reviewer = reviewer
      self.sections = sections

   def scores(self):
      return [section.rating for section in self.sections]

   def overall(self):
      return self.sections[-1].rating

   def __iter__(self):
      return iter(self.sections)

   def __getitem__(self, key):
      return self.sections[key]

class ReviewSet(dict):
   def __init__(self, *args, **kw):
      super(ReviewSet,self).__init__(*args, **kw)

   def buildWordClassifier(self, features, normalize, validity):
      words = []
      for rev in self.values():
         for section in rev:
            words += [(rev.reviewer, section.rating, w) for w in section.words()]
      random.shuffle(words)
      featureSets = [(features(w.lower()), rank) for (reviwer, rank, w) in words if validity(w)]

      limit = {'5':0, '4':0, '3':0, '2':0, '1':0}
      for feature, rank in featureSets:
         if limit[rank] > normalize:
            featureSets.remove((feature, rank))
         limit[rank] += 1

      return NaiveBayesClassifier.train(featureSets)

   def buildSentClassifier(self, features, normalize, validity):
      sents = []
      for rev in self.values():
         for section in rev:
            sents += [(rev.reviewer, section.rating, sent) for sent in section.sents()]

      random.shuffle(sents)

      featureSets = [(features(sent), rank) for (reviwer, rank, sent) in sents if validity(sent)]

      limit = {'5':0, '4':0, '3':0, '2':0, '1':0}
      for feature, rank in featureSets:
         if limit[rank] > normalize:
            featureSets.remove((feature, rank))
         limit[rank] += 1

      return NaiveBayesClassifier.train(featureSets)

   def buildParaClassifier(self, features, normalize, validity):
      paras = [] 
      for rev in self.values():
         for section in rev:
            paras.append((rev.reviewer, section.rating, section.words()))

      random.shuffle(paras)

      featureSets = [(features(para), rank) for (reviwer, rank, para) in paras if validity(para)]

      limit = {'5':0, '4':0, '3':0, '2':0, '1':0}
      for feature, rank in featureSets:
         if limit[rank] > normalize:
            featureSets.remove((feature, rank))
         limit[rank] += 1

      return NaiveBayesClassifier.train(featureSets)

   def buildParaClassifier(self, features, normalize, validity):
      revs = random.shuffle(self.values)

      featureSets = [(features(rev), rev.overall()) for rev in revs if validity(rev)]

      limit = {'5':0, '4':0, '3':0, '2':0, '1':0}
      for feature, rank in featureSets:
         if limit[rank] > normalize:
            featureSets.remove((feature, rank))
         limit[rank] += 1

      return NaiveBayesClassifier.train(featureSets)
