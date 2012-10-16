def crossval(corpus, n):
   import random
   from copy import deepcopy

#   hold = range(0, len(corpus.paras()))
   size = 0
   for val in corpus.values():
      size += len(val)
   hold = range(0, size)
   random.shuffle(hold)

   holds = []
   fold = int(size / n) + 1
   for i in range(0, n):
      holds.append(hold[:fold])
      hold = hold[fold:]

   idx = 0
   crosses = []
   for hold in holds:
      idx = 0
      test_set = []
      train_set = {}
   #   for f in corpus.fileids():
      for f in corpus.keys():
   #      for para in corpus.paras(f):
         for para in corpus[f]:
            if idx not in hold:
               train_set[f] = train_set.get(f, []) + para 
            else:
               test_set.append(([para], f))
            idx += 1

      crosses.append((train_set, test_set))

   return crosses
