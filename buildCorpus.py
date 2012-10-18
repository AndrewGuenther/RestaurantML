from nltk import clean_html
import sys, os, re
from reviews import Review, ReviewSet, ReviewItem
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

   corpus = ReviewSet() 
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
            rawReview.append(ReviewItem(para, ratings[j][i]))

         if corpus.get(filename) is None:
            corpus[filename] = Review(ratings[-1][i], rawReview)
         else:
            i = 1 
            while corpus.get(filename + "-" + str(i)) is not None:
               i += 1
            corpus[filename + "-" + str(i)] = Review(ratings[-1][i], rawReview)

   return corpus


def initCorpora():
   for root, dirs, files in os.walk("./training-clean"):
      corpus = buildCorpus(["./training-clean/" + f for f in files])
      
   for root, dirs, files in os.walk("./test-clean"):
      testcorpus = buildCorpus(["./test-clean/" + f for f in files])

   return corpus, testcorpus
   
def main():
   corpus = buildCorpus(sys.argv[1:])

   for (f, rev) in corpus.items():
      print f
      print rev.reviewer
      for section in rev:
         print section.rating
         print section.sents()
      print

if __name__ == '__main__':
   main()
