#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import sys
import urllib2,urllib
from bs4 import BeautifulSoup
import pyodbc
import time
import json
import datetime
import requests
import re

from HTMLParser import HTMLParser
class UserComment:
    def __init__(self,un,cm):
        self.userName=un
        self.comment =cm

class post:



    def __init__(self):
        self.comments=[]
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



class ParseSiteDb:
     orders={
     'cell_name_order':{'db':0,'file':0}
     }
     cell_name_order={'db_column_name':'CELL_NAME','file':11}
     cell_type_order={'db_column_name':'CELL_TYPE','file':5}
     lati_order={'db_column_name':'LATITUDE','file':2}
     longi_order={'db_column_name':'LONGITUDE','file':1}
     cell_id_order={'db_column_name':'GSM_CELL_ID','file':12}
     direction_order={'db_column_name':'ANTENNA_DIRECTION','file':9}
     cell_number_order={'db_column_name':'CELL_NUMBER','file':7}
     system_type_order={'db_column_name':'SYSTEM_TYPE','file':13}
     ary_script={'2g_type':[],'3g_type':[]}
     def readSetting(self):
         json_data=open('settings.json',"r").read()
         data = json.loads(json_data)
         self.settings["dbCs"]=data["dbCs"]

     def writeLog(self,msj):
         f = open("tel.txt", "a")
         f.write("date:{0}".format(datetime.datetime.now()) + " "+msj+'\n')
         f.close()
     def callStoredProc(self,conn, procName, *args):
         sql = """SET NOCOUNT ON;
         DECLARE @ret int
         EXEC @ret = %s %s
         SELECT @ret""" % (procName, ','.join(['?'] * len(args)))
         return int(conn.execute(sql, args).fetchone()[0])
     def getFacebookCount(self,url):
        try:
            resp = urllib2.urlopen('http://api.facebook.com/method/links.getStats?urls=%s&format=json' % url, timeout=5).read()
            cf = json.loads(resp)[0]['total_count']
            return cf
        except Exception as e:
            print(e)
            return -1
     def readdetailJson(self):
          json_data=open('detail.json',"r").read()
          self.detailJson = json.loads(json_data)

     def writeLog(self,msj):
        f = open("logs.txt", "a")
        f.write("date:{0}".format(datetime.datetime.now()) + " "+msj+'\n')
        f.close()
     def __init__(self):

         #for arg in sys.argv:
         #    print(sys.argv[0])
         #c=self.getFacebookCount('http://www.hurriyet.com.tr/esi-ve-cocuklari-evdeyken-ogrencisiyle-birlikte-olan-abdli-ogretmen-tutuklandi-40084737')
         #time.sleep(1000)
         #print("after:%s" % c)
         #self.writeLog("err")
         self.settings={}
         self.detailJson={}
         self.readSetting()
         self.readdetailJson()
         print 'starting..:',str(datetime.datetime.now())
         dict={}
         dict["facebook"]="ffff"
         dict["twitter"]="teee"
         #print(dict["facebook"])
         self.userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"
         url ='http://www.ntvspor.net/haber/haber-t/154475/yonetimden-kombine-indirimi'
            #http://www.sabah.com.tr/'  ##headline > .news > a
            #'http://www.haber7.com/'  ##headline > .news > a
            #'http://www.hurriyet.com.tr/' .mansetSlider > li > a

         req = urllib2.Request(url, headers={'User-Agent':self.userAgent})
         html = urllib2.urlopen(req, timeout=5).read()
         host_name=str.split(url,".")[1]

         criter= self.detailJson[host_name]["criter_paragraph"] #".news-box > p"
         soup = BeautifulSoup(html,"html.parser")
         letters = soup.select(criter) #.mansetSlider > li > a#sliderPager > li > a #find_all("li", class_="sliderPager")
         img=soup.select(self.detailJson[host_name]["criter_image"])[0]
         print("img:%s pr:%s" %(img,letters[0]) )




         #for link in letters:
             #print(link.get("title"))
             #print(link.select("img")[0]["alt"])
        #      if(l.find("http://") == -1 or l.find("https://") == -1):
        #          l=url+l;
        #      print("%s" %l)
             #self.callStoredProc(cnxn,"dbo.SetDb",l,link.get("title"),'spor')
             #cursor.execute("exec SetDb(?,?)","dd","rff")
             #link.get("href"),link.get("title")
             #if(link.get("href")=="/felipe-meloya-la-ligadan-talip-var-40084499"):
            #     print("buldu")


             #print("fff")
             #self.writeLog(link.get("href"))

             #if(link.get("href")=="/kirikkale-mkede-operasyon-40083836"):
            #        print(link)
        #ghost = Ghost()


#         with ghost.start() as session:
#            page, extra_resources = session.open("http://www.hurriyet.com.tr/")
#            #assert page.http_status == 200 and 'jeanphix' in page.content
#            print "fff",page.content
#            soup = BeautifulSoup(page.content,"html.parser")
#            letters = soup.select("#sliderPager > li > a") #find_all("li", class_="sliderPager")
#            for link in letters:
#                print(link)

         #"/kirikkale-mkede-operasyon-40083836"
    #assert page.http_status == 200 and 'jeanphix' in page.content
         #assert page.http_status==200 and 'jeanphix' in ghost.content

         ##print(soup.prettify())
         ##ary1=soup.select("newsTitle")

##select("#_MiddleLeft1 > .manset >  a")
         #for link in soup.find_all('a'):
         # print(link.get('href'))
         #print(letters)


         #print("calling",letters)
         #self.path2g='VF_2G_SITES.txt'
         #self.path3g='VF_3G_SITES.txt'
         ##self.ary_script={'2g_type':[],'3g_type':[]}
         #print "before call"
         #cnxn.close()
         #self.sayHello()
         #print(len(letters))
     def sayHello(self):
         print ('hello:',self.cell_number_order["file"])
     def callStoredProc(self,conn, procName, *args):
         sql = """SET NOCOUNT ON;

         EXEC  %s %s
         """ % (procName, ','.join(['?'] * len(args)))
         return conn.execute(sql, args)
def main():

    demo=ParseSiteDb()
    #demo.sayHello()
    #db = cx_Oracle.connect('SXQM_VF/SXQM_VF@178.233.4.223:1521/orcl')
    #curs = db.cursor()
    #print 'begin delete'
    #try:
    #    curs.execute('delete from GEO_SITE_DB')
    #    db.commit()
    #except Exception as e:
    #    db.rollback()
    #    print 'error delete:',e
    #print 'delete site db'
    #print 'starting..:',demo.writeDb(100)
    #print 'starting..:',str(datetime.datetime.now())
    #print '{0}, {1}, {2}'.format('a', 'b', 'c')

    #print(sys.argv)

if __name__ == '__main__':

    main()
