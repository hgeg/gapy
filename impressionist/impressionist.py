from PIL import Image, ImageDraw, ImageFile, ImageChops
from time import sleep
from random import randint
import math, operator,thread


#constants
POLYGONS = 100
IMG_WIDTH = 120
IMG_HEIGHT = 154
GENERATIONS = 10000000
MUTATION_RANGE = 10
POPULATION_SIZE = 25
SELECTION_CUTOFF = 5

class Polygon():
  def __init__(self):
    p0 = (randint(0,IMG_WIDTH), randint(0,IMG_HEIGHT))
    p1 = (randint(0,IMG_WIDTH), randint(0,IMG_HEIGHT))
    p2 = (randint(min(p0[0],p1[0]),max(p0[0],p1[0])), randint(0,IMG_HEIGHT))
    self.vertices = (p0,p1,p2)
    self.color = (randint(0,255),randint(0,255),randint(0,255),randint(0,200))

  def draw(self,drawer):
    drawer.polygon(self.vertices,fill=self.color)

def diff_img(i1,i2):
  diff = ImageChops.difference(i1.convert('RGB'),i2.convert('RGB')).resize((IMG_WIDTH/8,IMG_HEIGHT/8),Image.CUBIC).getdata()
  return ((141372-sum([sum(e) for e in diff]))/141372.0)*100

def main():
  global POLYGONS
  polygons = int(POLYGONS)
  target = Image.open('Self-Portrait-with-Straw-Hat.png')
  #generate
  pop = [{'p':[Polygon() for f in xrange(polygons)],'f':0} for e in xrange(POPULATION_SIZE)]

  for g in xrange(GENERATIONS):
    POLYGONS += 0.01
    for c in pop:
      img = Image.new('RGBA', (IMG_WIDTH, IMG_HEIGHT), (220, 230, 225, 255)) 
      for p in xrange(polygons):
        ipa = Image.new('RGBA', (IMG_WIDTH, IMG_HEIGHT)) 
        drawer = ImageDraw.Draw(ipa,'RGBA')  
        polygon = c['p'][p]
        polygon.draw(drawer)
        img.paste(ipa,mask=ipa)
      c['f'] = diff_img(img,target)
      if c['f']>95:
        img.save("./out/gen_%d_f_%d.png"%(g,c['f']), "PNG")
        print "close match!"
        return 0
    #selection
    pop = sorted(pop, key=lambda k: -k['f'])[:SELECTION_CUTOFF]
    left = len(pop)
    #crossover
    newgen = [{'p':pop[randint(0,left-1)]['p'][:polygons]+pop[randint(0,left-1)]['p'][polygons:],'f':0} for e in xrange(POPULATION_SIZE-SELECTION_CUTOFF)]
    pop = pop+newgen
    
    #logging
    if g>=0:
      out = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), (220, 230, 225, 255)) 
      for p in xrange(polygons):
        pha = Image.new('RGBA', (IMG_WIDTH, IMG_HEIGHT)) 
        logger = ImageDraw.Draw(pha,'RGBA')  
        polygon = pop[0]['p'][p]
        polygon.draw(logger)
        out.paste(pha,mask=pha)
      out.save("./out/output.png", "PNG")
      print "generation %d saved with f: %d"%(g,pop[0]['f'])
    else: 
      print "generation %d"%g

    #mutation
    for e in xrange(MUTATION_RANGE):
      pop[randint(0,POPULATION_SIZE-1)]['p'][randint(0,polygons-1)] = Polygon()
    
    sleep(1)
  
if __name__=='__main__': main()
