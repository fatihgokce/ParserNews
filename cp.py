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
from HTMLParser import HTMLParser
import pyodbc
class UserComment:
    def __init__(self,un,cm):
        self.userName=un
        self.comment =cm

class post:


    def default(self, o):
        return o.__dict__
    def __init__(self):

        self.link=""
        self.title = ""
        self.sourceName = ""

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    parser = HTMLParser()
    html = parser.unescape(html)
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def toJson(posts):

    js ='{"posts":['

    for j in posts:
        js1=""
        js1+='{ "title":"'+j.title+'","sourceName":"'+j.sourceName+'","link":"'+j.link+'"'

        js1+="},"

        js+=js1
    js=js[:-1]
    js +=']}'
    return js
class RootServer:
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def getByCategory(self,ct):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        posts=[]
        cnxn = pyodbc.connect("DRIVER={SQL Server};SERVER=198.38.92.235;DATABASE=FeedNews;UID=sa;PWD=Sapass..123")
        cursor = cnxn.cursor()


         #cursor.execute("insert into test_tb values(6, 'name')")
         #print("gündem".encode("utf-8","ignore"))
         #print("EXEC  %s" % ("gündem"))
        cursor =  cursor.execute(" EXEC [dbo].[GetDataByCategory] @category = N'%s' " % (ct))
        rows = cursor.fetchall()
        for row in rows:
            p1={}
            p1["link"]=row.url
            p1["title"]=row.title
            p1["sourceName"]=str.split(str(p1["link"]),".")[1]
            posts.append(p1)

        #res =toJson(posts)  #json.dumps([ob.__dict__ for ob in posts]) #toJson(posts)
        cnxn.close()
        return posts
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

        host_name=str.split(str(url),".")[1]
        print("c:" + host_name) #detailJson[host_name]["criter_paragraph"])
        criter=self.detailJson[host_name]["criter_paragraph"] #".news-box > p"
        msj=""
        soup = BeautifulSoup(html,"html.parser")
        letters = soup.select(criter) #.mansetSlider > li > a#sliderPager > li > a #find_all("li", class_="sliderPager")
        img=soup.select(self.detailJson[host_name]["criter_image"])[0]
        res={}
        res["img"]=img['src']
        if(res["img"].find("http://") < 0):
            res["img"]="http:" + res["img"]
        pr = ""
        for p in letters:
            str1 = str(p).replace("</p>","\n[#pp#]").replace("<br>","\n").replace('"',"##")
            str1 = str1.replace("[#pp#]","</p>")
            pr += strip_tags(str1)

        res["pr"] = pr #.encode("utf-8")  #html.encode('latin1')
        #json_obj = cherrypy.request.json
        res["url"]=cherrypy.request.params["url"]
        #print letters[0];
        #cherrypy.response.headers['Content-Type'] = 'application/json'
        return res
    def __init__(self):
        self.detailJson={}
        self.readdetailJson()
    def readdetailJson(self):
        json_data=open('detail.json',"r").read()
        self.detailJson = json.loads(json_data)

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
    cherrypy.config["tools.encode.on"] = True
    cherrypy.config["tools.encode.encoding"] = "utf-8"
    cherrypy.server.unsubscribe()



    server2 = cherrypy._cpserver.Server()
    server2.socket_port=8081
    server2._socket_host='127.0.0.1'
    server2.thread_pool=30
    server2.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()
