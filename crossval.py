import random
from reviews import Review, ReviewSet
 
def crossval(corpus, n):
   size = len(corpus.keys()) 
   hold = range(0, size)
   random.shuffle(hold)

   avg = len(corpus) / float(n)
   holds = []
   last = 0.0

   while last < len(hold):
      holds.append(hold[int(last):int(last + avg)])
      last += avg

   crosses = []

   for hold in holds:
      test_set = ReviewSet() 
      train_set = ReviewSet()
      for idx, f in enumerate(corpus.keys()):
         if idx not in hold:
            train_set[f] = corpus[f]
         else:
            test_set[f] = corpus[f]

      crosses.append((train_set, test_set))

   return crosses
