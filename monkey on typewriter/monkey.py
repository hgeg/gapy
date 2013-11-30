#/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint,choice
from time import sleep

#CONSTANTS
GENERATIONS = 10000000000000
MUTATION_RANGE = 16
POPULATION_SIZE = 100
SELECTION_CUTOFF = 10
ALPHABET='ABCÇDEFGĞHIİJKLMNOÖPQRSŞTUÜVWXYZabcçdefgğhıijklmnoöpqrsştuüvwxyz.,;:!?-*"1234567890 \n\''

def diff(p1,p2):
  point = 0
  if not len(p1) == len(p2): point = 5000*abs(len(p1)-len(p2))
  for i in xrange(min(len(p1),len(p2))):
    if not p1[i] == p2[i]: point += 10*(len(p2)-i)+50
  return point

def randstring(n,alphabet=ALPHABET):
  return ''.join([choice(alphabet) for f in xrange(n)])

def generate(n):
  return [{'w':"".join(randstring(50)),'f':0} for e in xrange(n)]

def crossover(a,b):
  return "".join([a[i] if i%2==0 else b[i] for i in xrange(min(len(a),len(b)))])


def main():
  target = '''o kadar gereksiz tipe dahi yönetmen, dahi yazar dendi ki dahi kelimesinin çoku çıktı. dahi'yi ayrı yazalım. peki o zaman charlie'ye ne diyelim? iyi bir yaratıcı yazar, helikoptere özenen gökkuşaklı bir beyin, köstebeklerle dost bir albatros. ilk işini 31-32 yaşında gerçekleştirdiğini de belirterek bugünün genç irileri yarının senaristlerine gaz verelim.

"panik durumum, kendimden nefret etmem ve değersiz küçük varlığım dışında hiçbir şeyi anlayamıyorum, bir tek kendi hakkımda yazı yazma konusunda oldukça iyiyim, tamamen benim hakkımda*".
'''

  #generate
  pop = generate(POPULATION_SIZE)
  for g in xrange(GENERATIONS):
    #fitness
    for s in pop:
      s['f'] = diff(s['w'],target)
      if s['f'] == 0: 
        print "exact match:\n %s"%s['w']
        return
    #selection
    pop = sorted(pop, key=lambda k: k['f'])[:SELECTION_CUTOFF]
    #crossover  
    newgen = [{'w':crossover(pop[randint(0,len(pop)-1)]['w'],pop[randint(0,len(pop)-1)]['w']),'f':0} for e in xrange(POPULATION_SIZE-SELECTION_CUTOFF)]
    pop = pop + newgen

    #log best
    print "best match:\n",pop[0]['w'],"\nf:",pop[0]['f']," gen:",g,"\n"
    sleep(0.01)

    #mutation
    for i in pop:
      c = randint(0,3)
      if c==0:
        rl = list(i['w'])
        rl[randint(0,len(i['w'])-1)] = randstring(1)
        i['w'] = ''.join(rl)
      elif c==1:
        i['w'] +=randstring(randint(0,10))
      elif c==2:
        i['w'] = i['w'][0:randint(1,len(i['w']))]

if __name__ == '__main__': main()
