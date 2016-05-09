import datetime
import sys
import urllib2
from bs4 import BeautifulSoup
import json
import pyodbc
import time
import requests
class ParserNews:
    settings={}
    def writeLog(self,msj):
        f = open("logs.txt", "a")
        f.write("date:{0}".format(datetime.datetime.now()) + " "+msj+'\n')
        f.close()
    def sayHello(self):
        print ('hello:',self.aa)
    def isOutLinks(self,criterArray,link):

        ret = 0
        for cr in criterArray:
            if(link.find(cr) > 0):
                return 1
        return ret
    def __init__(self):
        self.readSetting()
        print "Start : %s" % time.ctime()
        #time.sleep(float(self.settings["sleep"]))

        #self.settings={}

        self.userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"
        json_data=open('links.json',"r").read()
        data = json.loads(json_data)
        #print(self.settings["dbCs"])
        cnxn = pyodbc.connect(self.settings["dbCs"])
        #print(settings["dbCs"])
        outLinkCriters = data["out_link_criter"]
        #print(outLinkCriters)
        for c in data['categories']:
            category = c["name"]
            for l in c["links"]:
                print('name:'+ category + ' url:'+l["url"]+ ' criter:'+l["criter"] +'\n')
                url=l["url"]
                try:
                    req = urllib2.Request(url, headers={'User-Agent':self.userAgent})
                    html = urllib2.urlopen(req, timeout=10).read()
                    soup = BeautifulSoup(html,"html.parser")
                    letters = soup.select(l["criter"])
                    #print("category:"+category+" url:"+url+"\n")
                    for link in letters:

                        #print(link.get("href"))

                        ln=link.get("href")  #.decode("utf-8")
                        if ln is None:
                            continue
                        b = '%s' % str(ln)
                        ff = self.isOutLinks(outLinkCriters,b)
                        #print("ff:%s link:%s " % (ff,ln))

                        #ff=self.isOutLinks(outLinkCriters,ln)
                        #print(ff)
                        #print(str(ln.find(outLinkCriters[0])) + str(ln.find(outLinkCriters[1])))
                        if(ff==0):

                            if(ln.find("http://") < 0 and ln.find("https://") < 0):
                                ln=url+ln;
                                #print(l+"icerde\n")
                                #print("found:"+l+" ind:"+l.find(("http://").encode('utf-8').strip())+"\n")
                            cnt = self.getFacebookCount(ln)
                            tc=0#self.getTwitterCount(ln)
                            gc=self.getGoogleCount(ln)
                            title=""

                            if(l["title_in_img"]=="true"):
                                img=link.select("img")
                                if not(img is None):
                                    title=img[0]["alt"]
                            else:
                                title=link.get("title")
                            #self.writeLog(title.encode('utf-8') )
                            if title is not None:
                                self.callStoredProc(cnxn,"dbo.SetDb",ln,title,category,cnt,tc,gc)
                except Exception as e:
                    self.writeLog(str(e))

        #
        cnxn.close()
        print "End : %s" % time.ctime()
    def getGoogleCount(self,url):
        try:


            url = 'https://clients6.google.com/rpc'
            values = {
                 "method": "pos.plusones.get",
                 "id": "p",
                 "params": {
                            "nolog": True,
                            "id": url,
                            "source": "widget",
                            "userId": "@viewer",
                            "groupId": "@self"
                           },
                  "jsonrpc": "2.0",
                  "key": "p",
                  "apiVersion": "v1"
            }
            headers = {"content-type" : "application/json"}

            req = requests.post(url, data=json.dumps(values), headers=headers)
            jsn = json.loads(req.text)
            return int(jsn["result"]["metadata"]["globalCounts"]["count"])
        except Exception as e:
            print e
            return -1
    def getTwitterCount(self,url):
        try:
            html = urllib2.urlopen("http://urls.api.twitter.com/1/urls/count.json?url=%s" % url, timeout=5).read()
            ic = html.find('"count":') + len('"count":')
            ct = int(html[indexCount: html[indexCount:].find(',') + indexCount])
            return ct
        except Exception as e:
            #print(e)
            return -1
    def getFacebookCount(self,url):
        try:
            resp = urllib2.urlopen('http://api.facebook.com/method/links.getStats?urls=%s&format=json' % url, timeout=5).read()
            cf = json.loads(resp)[0]['total_count']
            return cf
        except Exception as e:
            return -1
    def readSetting(self):
        json_data=open('settings.json',"r").read()
        data = json.loads(json_data)
        self.settings["dbCs"]=data["dbCs"]
        self.settings["sleep"]=data["sleep"]
    def callStoredProc(self,conn, procName, *args):
        sql = """SET NOCOUNT ON;
        DECLARE @ret int
        EXEC @ret = %s %s
        SELECT @ret""" % (procName, ','.join(['?'] * len(args)))
        return int(conn.execute(sql, args).fetchone()[0])

def main():

    demo=ParserNews()
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
