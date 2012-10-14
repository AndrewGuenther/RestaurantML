from nltk import clean_html
import sys

def buildCorpus(filepaths):
   for path in filepaths:
      review = clean_html(open(path).read())
      print review      
      
   
def main():
   buildCorpus(sys.argv[1:])


if __name__ == '__main__':
   main()
