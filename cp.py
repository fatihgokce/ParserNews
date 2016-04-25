#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cherrypy
import urllib2
from bs4 import BeautifulSoup
import json
import time
import requests
import json
import re
class RootServer:
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def index(self,**keyword):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def getData(self,url):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"
        #self.userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"
        url2 ='http://www.hurriyet.com.tr/olu-yunus-karaya-vurdu-40090917'
            #http://www.sabah.com.tr/'  ##headline > .news > a
            #'http://www.haber7.com/'  ##headline > .news > a
            #'http://www.hurriyet.com.tr/' .mansetSlider > li > a
        #print url2
        req = urllib2.Request(url, headers={'User-Agent':userAgent})
        html = urllib2.urlopen(req, timeout=5).read()
         #resp = urllib2.urlopen('http://www.hurriyet.com.tr/',headers={'User-Agent':self.userAgent})
        #and read the normal way ie
         #newsTitle
         #print(html)
         #page = resp.read()
        criter=".news-box > p"
        msj=""
        soup = BeautifulSoup(html,"html.parser")
        letters = soup.select(criter) #.mansetSlider > li > a#sliderPager > li > a #find_all("li", class_="sliderPager")
        img=soup.select(".news-image > img")[0]
        res={}
        res["img"]=img['src']
        for l in letters:
            msj = msj + str(l)#.getText()
        #x = re.compile(r'</?[aA]\>[^>]*?/?>')
        x = re.compile(r'''</?a((s+w+(s*=s*(?:".*?"|'.*?'|[^'">s]+))?)+s*|s*)/?>w+</a>''')
            #compile(r'<[aA][^>]*>([^<]+)</[aA]>')
        res["pr"]=x.sub('', msj)
        #json_obj = cherrypy.request.json
        res["url"]=cherrypy.request.params["url"]
        #print letters[0];
        #cherrypy.response.headers['Content-Type'] = 'application/json'
        return res
def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
if __name__ == '__main__':

    #cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)

    site_config = {
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "/home/ubuntu/my_website/static"
        },
        '/support': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': "/home/ubuntu/my_website/templates/support.html"
        }
    }
    #cherrypy.quickstart(RootServer(), '/d/', conf)
    cherrypy.tree.mount(RootServer())

    cherrypy.server.unsubscribe()



    server2 = cherrypy._cpserver.Server()
    server2.socket_port=8081
    server2._socket_host='127.0.0.1'
    server2.thread_pool=30
    server2.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()
