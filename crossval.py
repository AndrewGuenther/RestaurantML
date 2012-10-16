def crossval(corpus, n):
   import random
   
   size = 0
   hold = range(0, len(corpus.keys()))
   random.shuffle(hold)

   holds = []
   fold = int(size / n) + 1
   for i in range(0, n):
      holds.append(hold[:fold])
      hold = hold[fold:]

   idx = 0
   crosses = []
   for hold in holds:
      test_set = {} 
      train_set = {}
      for idx, f in enumerate(corpus.keys()):
         if idx not in hold:
            train_set[f] = corpus[f]
         else:
            test_set[f] = corpus[f]

      crosses.append((train_set, test_set))

   return crosses
