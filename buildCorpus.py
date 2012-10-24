from nltk import clean_html
import sys, os, re
from reviews import Review, ReviewSet, ReviewItem

def buildCorpus(filepaths):

   corpus = ReviewSet() 
   for path in filepaths:
      filename = re.findall(r'.*\/(.*)', path)[0]
      raw = open(path).read()
      rawReview = []
#      print filename
      
      reviewer = re.findall(r'REVIEWER:\W*([ \w]*)', raw)
      food = re.findall(r'FOOD:\s*(.)', raw)
      service = re.findall(r'SERVICE:\s*(.)', raw)
      venue = re.findall(r'VENUE:\s*(.)', raw)
      rating = re.findall(r'(?:RATING|OVERALL):\s*(.)', raw)
      ratings = [food, service, venue, rating, reviewer]
      
#      print '\t',ratings

      rawreviews = re.findall(r'WRITTEN REVIEW:((?:.|\n|\r)*?)(?:REVIEWER|\Z)', raw)

      for i, rawreview in enumerate(rawreviews):
         #review = re.sub("(<.*?span[^>]*>)", "", review)
         review = re.findall(r'(.{10,})', rawreview)
         review = [clean_html(section) for section in review if len(clean_html(section)) > 10]
         if len(review) != 4:
            review = re.findall(r'(?:<br.*?>)?([^<]*)', rawreview)
            review = [clean_html(section) for section in review if len(clean_html(section)) > 10]

         if len(review) != 4:
            review = re.split(r'<br \/><br \/>', rawreview) 
            review = [clean_html(section) for section in review if len(clean_html(section)) > 10]

         if len(review) != 4:
            print "Failed to parse review in", filename

         sections = []
         for j, section in enumerate(review):
            sections.append(ReviewItem(section, ratings[j][i]))

         if corpus.get(filename) is None:
            corpus[filename] = Review(ratings[-1][i], sections)
         else:
            k = 1 
            while corpus.get(filename + "-" + str(k)) is not None:
               k += 1
            corpus[filename + "-" + str(k)] = Review(ratings[-1][i], sections)
   return corpus

def initCorpora():
   for root, dirs, files in os.walk("./training"):
      corpus = buildCorpus(["./training/" + f for f in files if f[0] != '.'])
      
   for root, dirs, files in os.walk("./test"):
      testcorpus = buildCorpus(["./test/" + f for f in files if f[0] != '.'])

   return corpus, testcorpus
   
def main():
   initCorpora()

 
if __name__ == '__main__':
   main()
