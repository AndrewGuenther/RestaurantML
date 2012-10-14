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
   from nltk.corpus import PlaintextCorpusReader

   corpus_root = 'C:\\Users\\Matthew\\AppData\\Local\Temp\\restaurantcorpus\\'
   temp1 = open(corpus_root + "temp1.txt", 'w')
   temp2 = open(corpus_root + "temp2.txt", 'w')
   temp3 = open(corpus_root + "temp3.txt", 'w')
   temp4 = open(corpus_root + "temp4.txt", 'w')
   temp5 = open(corpus_root + "temp5.txt", 'w')
   temps = [temp1, temp2, temp3, temp4, temp5]

   for path in filepaths:
      raw = open(path).read()
      
      food = re.findall(r'FOOD: *(\d)', raw)
      service = re.findall(r'SERVICE: *(\d)', raw)
      venue = re.findall(r'VENUE: *(\d)', raw)
      rating = re.findall(r'RATING: *(\d)', raw)
      ratings = [food, service, venue, rating]

      reviews = re.findall(r'WRITTEN REVIEW:\s*(.*\n)(.*\n)(.*\n)(.*\n)', raw)
      i = 0
      for review in reviews:
         #print "Review:"
         j = 0
         for para in review:
            temps[int(ratings[j][i])-1].write(para)
            temps[int(ratings[j][i])-1].write('\n')
            j += 1
            #print para
         i += 1

   newcorpus = PlaintextCorpusReader(corpus_root, '.*')
   return newcorpus
   
def main():
   buildCorpus(sys.argv[1:])

if __name__ == '__main__':
   main()
