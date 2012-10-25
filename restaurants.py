import operator, sys
from math import pow, sqrt
from buildCorpus import buildCorpus, initCorpora
from crossval import crossval

def main(method1, method2, method3):
   corpus, testcorpus = initCorpora()

   crosses = crossval(corpus, 4)

   print "Cross validation"

   avg = [[], [], []]
   rmss = [[], [], []]
   for idx, (train_set, test_set) in enumerate(crosses):
      print "Random validation set", idx + 1, ":", test_set.keys()

      #classifier = method.getClassifier(train_set)
      ex1 = method1.Method(train_set)
      ex2 = method2.Method(train_set)
      ex3 = method3.Method(train_set)

      diffs1, diffs2, diffs3 = [], [], []
      for f, rev in test_set.items():
         results1 = ex1.test(rev)
         diffs1 += [pow(a - int(b), 2) for a, b in zip(results1, rev.scores())]
        
         result2 = ex2.test(rev)
         diffs2.append(pow(result2 - int(rev.overall()), 2))

         result3 = ex3.test(rev)
         diffs3.append(0.0 if result3 == rev.reviewer else 1.0)
     
      total1 = reduce(operator.add, diffs1)
      rms1 = sqrt(total1 / (len(test_set.items()) * 4))
      rmss[0] += [rms1]

      total2 = reduce(operator.add, diffs2)
      rms2 = sqrt(total2 / len(test_set.items()))
      rmss[1] += [rms2]

      total3 = reduce(operator.add, diffs3)
      rms3 = sqrt(total3 / len(test_set.items()))
      rmss[2] += [rms3]

      print "Average RMS error rate on validation set:"
      print "\tExercise 1:", round(rms1, 2)
      print "\tExercise 2:", round(rms2, 2)
      print "\tExercise 3:", round(rms3, 2)
      print

   print "Average RMS error rate on all validation sets:"
   print "\tExercise 1:", round(float(reduce(operator.add, rmss[0])) / len(rmss[0]), 2)
   print "\tExercise 2:", round(float(reduce(operator.add, rmss[1])) / len(rmss[1]), 2)
   print "\tExercise 3:", round(float(reduce(operator.add, rmss[2])) / len(rmss[2]), 2)
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
   method1 = __import__('ex1')
   method2 = __import__('ex2')
   method3 = __import__('ex3')
   main(method1, method2, method3)
