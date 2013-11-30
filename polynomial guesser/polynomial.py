from random import randint
import re, sys

#CONSTANTS
GENERATIONS = 10000
MUTATION_RANGE = 16
POPULATION_SIZE = 100
SELECTION_CUTOFF = 30

#polynomial object class
class Polynomial:
  def __init__(self,a,b,c):
    self.a, self.b, self.c = a, b, c
  #evaluate value for given x
  def eval(self,x):
    return self.a*x*x+self.b*x+self.c
  #pretty printing
  def __str__(self):
    return "%dx^2 + %dx + %d"%(self.a,self.b,self.c)
  #parsing
  def parse(self,text):
    m = re.match(r"(-*\d*)x\^2\ *\+\ *(-*\d*)x\ *\+\ *(-*\d*)",text)
    self.a = int(m.group(1))
    self.b = int(m.group(2))
    self.c = int(m.group(3))

#generator function
def generate(n):
  return [{'p':Polynomial(randint(1,10),randint(1,10),randint(1,10)),'f':0} for i in xrange(n)]

#fitness function
def diff(i,target):
  f = 0
  for x in xrange(-10,11):
    f += abs(i['p'].eval(x)-target.eval(x))
  return f

def main():
  #create evolutionary target
  target = Polynomial(0,0,0)
  target.parse(sys.argv[1])
  print "target polynomial: %s"%target
  #generate initial population
  pop = generate(POPULATION_SIZE)
  for g in xrange(GENERATIONS):

    #fitness test
    for i in pop:
      f = diff(i,target)
      if f==0:
        print "exact match: %s"%(i['p'])
        return
      i['f'] = f

    #selection
    pop = sorted(pop, key=lambda k: k['f'])[:SELECTION_CUTOFF]

    #crossover
    newgen = [{'p': Polynomial(pop[randint(0,4)]['p'].a,pop[randint(0,4)]['p'].b,pop[randint(0,4)]['p'].c),'f':0} for e in xrange(POPULATION_SIZE-SELECTION_CUTOFF)] 
    pop += newgen
    
    #log the fittest
    print "best guess: %s  f:%d  gen:%d"%(pop[0]['p'],pop[0]['f'],g)

    #mutation
    for i in pop:
      p = i['p']
      p.a += randint(-MUTATION_RANGE,MUTATION_RANGE)
      p.b += randint(-MUTATION_RANGE,MUTATION_RANGE)
      p.c += randint(-MUTATION_RANGE,MUTATION_RANGE)

if __name__ == '__main__': main()
