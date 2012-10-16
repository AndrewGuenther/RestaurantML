def buildSenti():
   import re
   from string import atof

   senti = {}
   f = open('not_stolen.txt','r')
   raw = f.readlines()
   for line in raw:
      base = re.findall(r'(\S*)\s*(\S*)\s*(\S*)\s', line)[0]
      senti[base[2]] = (atof(base[0]), atof(base[1]))
   f.close()
   return senti

if __name__ == '__main__':
   senti = buildSenti()
