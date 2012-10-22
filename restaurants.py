import operator, sys
from math import pow, sqrt
from buildCorpus import buildCorpus, initCorpora
from crossval import crossval

def main(method1, method2, method3):
   corpus, testcorpus = initCorpora()

   crosses = crossval(corpus, 4)

   print "Cross validation"
   rmss = [[], [], []]

   for idx, (train_set, test_set) in enumerate(crosses):
      print "Random validation set", idx + 1, ":", test_set.keys()

      #classifier = method.getClassifier(train_set)
      ex1 = method1.Method(train_set)
      ex2 = method2.Method(train_set)
      ex3 = method3.Method(train_set)

      for f, rev in test_set.items():
         results1 = ex1.test(rev)
         diffs1 = [pow(a - int(b), 2) for a, b in zip(results1, rev.scores())]
         total1 = reduce(operator.add, diffs1)
         rms1 = sqrt(total1 / 4)
         rmss[0].append(rms1)
         
         result2 = ex2.test(rev)
         rms2 = sqrt(pow(result2 - int(rev.overall()), 2))       
         rmss[1].append(rms2)

         result3 = ex3.test(rev)
         #print result3 + ", " + rev.reviewer
         rms3 = 0

         if (result3 == rev.reviewer):
            rms3 = 1
         rmss[2].append(rms3)

      sum1 = 0
      for rms in rmss[0]:
         sum1 += rms

      sum2 = 0
      for rms in rmss[1]:
         sum2 += rms

      sum3 = 0
      for rms in rmss[2]:
         sum3 += rms
      print "Average RMS error rate on validation set:"
      print "\tExercise 1:", round(sum1 / len(rmss[0]), 2)
      print "\tExercise 2:", round(sum2 / len(rmss[1]), 2)
      print "\tExercise 3:", round(sum3 / len(rmss[2]), 2)
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
