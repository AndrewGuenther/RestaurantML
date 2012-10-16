import random
from reviews import Review, ReviewSet
 
def crossval(corpus, n):
   size = len(corpus.keys()) 
   hold = range(0, size)
   random.shuffle(hold)

   holds = []
   fold = int(size / n) + 1
   for i in range(0, n):
      holds.append(hold[:fold])
      hold = hold[fold:]

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
