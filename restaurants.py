import operator, sys
from math import pow, sqrt
from buildCorpus import buildCorpus, initCorpora
from crossval import crossval

def main(method1, method2, method3):
   corpus, testcorpus = initCorpora()

   crosses = crossval(corpus, 4)

   print "Cross validation"
   rmss = []
   for idx, (train_set, test_set) in enumerate(crosses):
      print "Random validation set", idx + 1, ":", test_set.keys()

      #classifier = method.getClassifier(train_set)
      ex1 = method1.Method(train_set)
      ex2 = method2.Method(train_set)
      ex3 = method3.Method(train_set)

      for f, rev in test_set.items():
         results = ex1.test(rev)
         diffs = [pow(a - int(b), 2) for a, b in zip(results, rev.scores())]
         total = reduce(operator.add, diffs)
         rms = sqrt(total / 4)

         rmss.append(rms)

      sum = 0
      for rms in rmss:
         sum += rms
      print "Average RMS error rate on validation set:"
      print "\tExercise 1:", round(sum / len(rmss), 2)
      print "\tExercise 2:"
      print "\tExercise 3:"
      print

   ex1 = method1.Method(corpus)
   ex2 = method2.Method(corpus)
   ex3 = method3.Method(corpus)

   print "Begin processing test set"
   for f, rev in testcorpus.items():
      results1 = ex1.test(rev)
      results2 = ex2.test(rev)
      results3 = ex3.test(rev)

      print "Now showing predictions for", f
      print "Paragraph ratings:", [round(r, 2) for r in results1]
      print "Overall rating:", round(results2, 2)
      print "Author:", results3
      print

if __name__ == '__main__':
   method1 = __import__(sys.argv[1])
   method2 = __import__(sys.argv[2])
   method3 = __import__(sys.argv[3])
   main(method1, method2, method3)
