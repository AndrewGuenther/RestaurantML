#Returns a dictionary representing a subset of the SentiWordnet corpus
#Values in the dictionary are represented as tuples of (posValue, negValue)
def buildSenti():
   import re
   from string import atof

   #Open and read in SentiWordnet file
   f = open('senti_wordnet.txt','r')
   raw = f.read()

   #Pull records from raw text
   r = re.compile('(\S*)\s*(\S*)\s*(\S*)\s')
   results = r.findall(raw)

   #Build Dictionary
   senti = dict((res[2], (atof(res[0]), atof(res[1]))) for res in results)

   #Close SentiWordnet file
   f.close()

   #Return dictionary
   return senti

if __name__ == '__main__':
   senti = buildSenti()
   print senti
