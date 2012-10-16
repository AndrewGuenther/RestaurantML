from nltk import clean_html
import sys, re

'''
def buildCorpus(filepaths):
   for path in filepaths:
      raw = open(path).read()
      raw = re.sub(r'< *br *\/?> *', "\n", raw)
      review = clean_html(raw)
      
      review = review.split('\n')
      for idx, line in enumerate(review):
         review[idx] = re.sub(r'\r|\xc2|\xa0', ' ', line)

      print review
'''

def buildCorpus(filepaths):
   from nltk import word_tokenize
   from nltk.tokenize.punkt import PunktSentenceTokenizer

   tok = PunktSentenceTokenizer()

   #All reviews are held in this review class
   class Review:
      def __init__(self, reviewer, ratings):
         self.reviewer = reviewer
         self.ratings = ratings

      #All getters return a tuple (reviewer, rating, content) where content is either
      #the list of paragraphs or list of sentences or list of words
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

   corpus = {}
   for path in filepaths:
      filename = re.findall(r'.*\/(.*)', path)[0]
      raw = open(path).read()
      rawReview = []
     
      reviewer = re.findall(r'REVIEWER: *(\S* \S*)', raw)
      food = re.findall(r'FOOD: *(\d)', raw)
      service = re.findall(r'SERVICE: *(\d)', raw)
      venue = re.findall(r'VENUE: *(\d)', raw)
      rating = re.findall(r'RATING: *(\d)', raw)
      ratings = [food, service, venue, rating, reviewer]

      reviews = re.findall(r'WRITTEN REVIEW:\s*(.*\n)(.*\n)(.*\n)(.*\n)', raw)
      for i, review in enumerate(reviews):
         rawReview = []
         for j, para in enumerate(review):
            rawReview.append((ratings[j][i], 
                              [word_tokenize(sent) for sent in tok.tokenize(para)]))

         if corpus.get(filename) is None:
            corpus[filename] = Review(ratings[-1][i], rawReview)
         else:
            i = 1 
            while corpus.get(filename + "-" + str(i)) is not None:
               i += 1
            corpus[filename + "-" + str(i)] = Review(ratings[-1][i], rawReview)

   return corpus
   
def main():
   corpus = buildCorpus(sys.argv[1:])

   for (f, rev) in corpus.items():
      print f
      print rev.reviewer
      print rev.paras()[0]
      print rev.sents()[0]
      print rev.words()[0]
      print

if __name__ == '__main__':
   main()
