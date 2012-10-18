import operator, sys
from math import pow, sqrt
from buildCorpus import buildCorpus, initCorpora
from crossval import crossval

method = __import__(sys.argv[1])

corpus, testcorpus = initCorpora()

crosses = crossval(corpus, 4)

print "Exercise 1 validation"
rmss = []
for idx, (train_set, test_set) in enumerate(crosses):
   print "Random validation set", idx + 1, ":", test_set.keys()

   classifier = method.getClassifier(train_set)

   for f, rev in test_set.items():
      results = method.test(rev, classifier)
      #print results
      diffs = [pow(a - int(b), 2) for a, b in zip(results, rev.scores())]
      total = reduce(operator.add, diffs)
      rms = sqrt(total / 4)

      rmss.append(rms)

   sum = 0
   for rms in rmss:
      sum += rms
   print "Average RMS error rate on validation set:", round(sum / len(rmss), 2)
   print

classifier = method.getClassifier(corpus)

print "Begin processing test set"
for f, rev in testcorpus.items():
   results = method.test(rev, classifier)

   print "Now showing predictions for", f
   print "Paragraph ratings:", [round(r, 2) for r in results]
   print
