#!/usr/bin/env python
#-*- coding: utf-8 -*-
import web,os,glob

url = ('/vangogh','Preview')
app = web.application(url,globals())
rnd = web.template.render('templates')

class Preview:
  def GET(self):
    #imgs = [p[2] for p in os.walk('/home/ubuntu/gapy/impressionist/out')][0]
    #imgs = sorted(imgs, key=lambda item:(len(item),item))
    imgs = ['output.png']
    return rnd.preview(imgs)

if __name__ == '__main__':
  web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
  app.run()




