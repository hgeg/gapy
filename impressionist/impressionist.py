from PIL import Image, ImageDraw, ImageFile, ImageChops
from time import sleep
from random import randint
import math, operator,thread


#constants
POLYGONS = 50
IMG_WIDTH = 120
IMG_HEIGHT = 154
GENERATIONS = 10000000
MUTATION_RANGE = 5
POPULATION_SIZE = 5
SELECTION_CUTOFF = 1

class Polygon():
  def __init__(self):
    self.vertices = ((randint(0,IMG_WIDTH), randint(0,IMG_HEIGHT)),(randint(0,IMG_WIDTH), randint(0,IMG_HEIGHT)),(randint(0,IMG_WIDTH), randint(0,IMG_HEIGHT)),(randint(0,IMG_WIDTH), randint(0,IMG_HEIGHT)))
    self.color = (randint(0,255),randint(0,255),randint(0,255),randint(0,255))

  def draw(self,drawer):
    drawer.polygon(self.vertices,fill=self.color)

def diff_img(i1,i2):
  diff = ImageChops.difference(i1.convert('RGB'),i2.convert('RGB')).resize((IMG_WIDTH/8,IMG_HEIGHT/8),Image.CUBIC).getdata()
  return ((141372-sum([sum(e) for e in diff]))/141372.0)*100

def main():
  target = Image.open('Self-Portrait-with-Straw-Hat.png')
  #generate
  pop = [{'p':[Polygon() for f in xrange(POLYGONS)],'f':0} for e in xrange(POPULATION_SIZE)]

  for g in xrange(GENERATIONS):
    for c in pop:
      img = Image.new('RGBA', (IMG_WIDTH, IMG_HEIGHT), (0, 0, 0, 255)) 
      for p in xrange(POLYGONS):
        ipa = Image.new('RGBA', (IMG_WIDTH, IMG_HEIGHT)) 
        drawer = ImageDraw.Draw(ipa,'RGBA')  
        polygon = c['p'][p]
        polygon.draw(drawer)
        img.paste(ipa,mask=ipa)
      c['f'] = diff_img(img,target)
      if c['f']>95:
        img.save("./out/gen_%d_f_%d%%.png"%(g,c['f']), "PNG")
        print "close match!"
        return 0
    #selection
    pop = sorted(pop, key=lambda k: -k['f'])[:SELECTION_CUTOFF]
    left = len(pop)
    #crossover
    newgen = [{'p':pop[randint(0,left-1)]['p'][:POLYGONS]+pop[randint(0,left-1)]['p'][POLYGONS:],'f':0} for e in xrange(POPULATION_SIZE-SELECTION_CUTOFF)]
    pop = pop+newgen
    
    #logging
    if g%100==0:
      out = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), (0, 0, 0, 255)) 
      for p in xrange(POLYGONS):
        pha = Image.new('RGBA', (IMG_WIDTH, IMG_HEIGHT)) 
        logger = ImageDraw.Draw(pha,'RGBA')  
        polygon = pop[0]['p'][p]
        polygon.draw(logger)
        out.paste(pha,mask=pha)
      out.save("./out/gen_%d_f_%d%%.png"%(g,pop[0]['f']), "PNG")
      print "generation %d saved with f: %d%%"%(g,pop[0]['f'])
    else: 
      print "generation %d"%g

    #mutation
    for e in xrange(MUTATION_RANGE):
      pop[randint(0,POPULATION_SIZE-1)]['p'][randint(0,POLYGONS-1)] = Polygon()
    
    sleep(0.5)
  
if __name__=='__main__': main()
