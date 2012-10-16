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

def buildCorpus(filepaths, corpus_root):
#   from nltk.corpus import PlaintextCorpusReader
   from nltk import word_tokenize

#   temps = [open(corpus_root + str(i) + ".txt", 'w') for i in range(1, 6)]

   corpus = {5:[], 4:[], 3:[], 2:[], 1:[]}

   for path in filepaths:
      raw = open(path).read()
      
      food = re.findall(r'FOOD: *(\d)', raw)
      service = re.findall(r'SERVICE: *(\d)', raw)
      venue = re.findall(r'VENUE: *(\d)', raw)
      rating = re.findall(r'RATING: *(\d)', raw)
      ratings = [food, service, venue, rating]

      reviews = re.findall(r'WRITTEN REVIEW:\s*(.*\n)(.*\n)(.*\n)(.*\n)', raw)
      for i, review in enumerate(reviews):
         for j, para in enumerate(review):
            corpus[int(ratings[j][i])] += [word_tokenize(para)]
#            temps[int(ratings[j][i])-1].write(para + '\n')

#   newcorpus = PlaintextCorpusReader(corpus_root, '.*')
   return corpus
   
def main():
   print buildCorpus(sys.argv[1:], '/tmp/train/')

if __name__ == '__main__':
   main()
