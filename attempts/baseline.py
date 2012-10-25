from buildSenti import buildSenti

ml = 2
senti = buildSenti()

def isValid(w):
   if len(w) > ml and w.isalpha():
      return True
   return False

def langFeatures(word):
   sent = senti.get(word, (0, 0))[0] - senti.get(word, (0, 0))[1] 
   return { 'sent': sent}

def getClassifier(corpus):
   return corpus.buildWordClassifier(langFeatures, 100, isValid)

def test(rev, classifier):
   predictions = []
   for section in rev:
      predictions.append(4)

   return predictions
