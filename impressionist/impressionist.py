from PIL import Image, ImageDraw, ImageFile, ImageChops
from time import sleep
from random import randint
import math, operator

#constants
LINES = 800
IMG_WIDTH = 120
IMG_HEIGHT = 154
GENERATIONS = 10000000
MUTATION_RANGE = 100
POPULATION_SIZE = 100
SELECTION_CUTOFF = 10

class Line():
  def __init__(self):
    self.start = (randint(0,IMG_WIDTH), randint(0,IMG_HEIGHT))
    self.end   = (randint(0,IMG_WIDTH), randint(0,IMG_HEIGHT))
    self.color = (randint(0,255),randint(0,255),randint(0,255))
    self.width = randint(1,4)

  def draw(drawer):
    drawer.line(self.start()+self.end(),fill=self.color,width=self.width)


def diff_img(i1,i2):
  #h1 = i1.histogram()
  #h2 = i2.histogram()
  #return math.sqrt(reduce(operator.add, [(a-b)**2 for a,b in zip(h1,h2)])/len(h1))
  diff = ImageChops.difference(i1.convert('RGB'),i2.convert('RGB')).resize((IMG_WIDTH/8,IMG_HEIGHT/8),Image.CUBIC).getdata()
  return sum([sum(e) for e in diff])

def main():
  target = Image.open('Self-Portrait-with-Straw-Hat.png')
  #generate
  pop = [{'p':[Line() for f in xrange(LINES)],'f':0} for e in xrange(POPULATION_SIZE)]

  for g in xrange(GENERATIONS):
    for c in pop:
      img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), (255, 255, 255)) 
      drawer = ImageDraw.Draw(img)  
      for l in xrange(LINES):
        line = c['p'][l]
        drawer.line(line.start+line.end,fill=line.color,width=line.width) 
      c['f'] = diff_img(img,target)
      if c['f']<10:
        img.save("./out/gen_%d.jpg"%g, "JPEG", quality=100, optimize=True)
        print "close match!"
        img.show()
        return 0
    #selection
    pop = sorted(pop, key=lambda k: k['f'])[:SELECTION_CUTOFF]
    left = len(pop)
    #crossover
    newgen = [{'p':pop[randint(0,left-1)]['p'][:LINES]+pop[randint(0,left-1)]['p'][LINES:],'f':0} for e in xrange(POPULATION_SIZE-SELECTION_CUTOFF)]
    pop = pop+newgen
    
    #logging
    if g%100==0:
      out = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), (255, 255, 255)) 
      logger = ImageDraw.Draw(out)  
      for l in xrange(LINES):
        line = pop[0]['p'][l]
        logger.line(line.start+line.end,fill=line.color,width=line.width) 
      out.save("./out/gen_%d.png"%g, "PNG")
      print "generation %d saved with f: %d"%(g,pop[0]['f'])
    else: 
      print "generation %d"%g

    #mutation
    for e in xrange(MUTATION_RANGE):
      pop[randint(0,99)]['p'][randint(0,LINES-1)] = Line()
    
    #sleep(0.1)
  
if __name__=='__main__': main()
