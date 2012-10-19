#coding:utf-8

from publicsettings import dbconn,tempDir,tempDataDir,tempMddDir
from mfwutils import dictToOrderList
from bs4 import BeautifulSoup
import bs4,os,re

"""

actypeDict = {}
res = dbconn.query("select * from mfwactype")
for r in res:
    actypeDict.update({r.name:r.id})

unknownActType = {}

for userid in range(400000,440000):
    html = open(tempDir+"/"+str(userid)[0:2]+"/"+str(userid)+"_1.html")
    soup = BeautifulSoup(html,from_encoding="utf8")
    news_lists = soup.find_all("div","news_list")
    for news_list in news_lists:
        con = news_list.find("div","con")
    ##print con.string
        text = ""
        for i in con.children:
            if isinstance(i,bs4.element.NavigableString):
                i = i.strip()
                if i <> u"":
                    text = text + u"$" + i
        if text <> u"":
            ##print text
            if not actypeDict.has_key(text):
                if unknownActType.has_key(text):
                    unknownActType[text] = unknownActType[text] + 1
                else:
                    unknownActType.update({text:0})
dlist = dictToOrderList(unknownActType)
f = open(tempDataDir,"wb")
for d in dlist:
    f.write(d[0].encode("utf8")+ "," +str(d[1])+"\n")

"""
"""
class_dict = {}
def ana(html):
    soup = BeautifulSoup(html,from_encoding="utf8")
    city_sides = soup.find_all("div","city_side")
    for city_side in city_sides:
        for div in city_side.children:
            if isinstance(div,bs4.element.NavigableString):
                continue
            if div.name <> "div":
                continue
            cal(div['class'])

    city_conts = soup.find_all("div","city_cont")
    for city_cont in city_conts:
        for div in city_cont.children:
            if isinstance(div,bs4.element.NavigableString):
                continue
            if div.name <> "div":
                continue
            cal(div['class'])


def cal(className):
    if isinstance(className,list):
        tempName = ""
        for c in className:
            tempName = tempName + " " +c
        className = tempName
    if class_dict.has_key(className):
        class_dict[className] = class_dict[className] + 1
    else:
        class_dict.update({className:1})

##for mddDir in os.listdir(tempMddDir):
##    if not os.path.isdir(tempMddDir +"/"+ mddDir):
##        continue
for filename in os.listdir(tempMddDir +"/1"):
    ana(open(tempMddDir+"/1/"+filename,"r").read())

f = open("d:/log/mmd.log","wb")
for d in dictToOrderList(class_dict):
    f.write(d[0] + "," + str(d[1])+ "\r\n")
"""
res = dbconn.query("select distinct pid from mfwmdd where pid is not null")
comp = re.compile(u"<title>(.+)地区旅游地图")
for r in res:
    pid = r.pid
    html = open(tempMddDir+"/"+str(pid)[0]+"/"+str(pid)+".html","r").read()
    soup = BeautifulSoup(html,from_encoding="utf8")
    name = comp.search(unicode(soup.title)).group(1)
    dbconn.insert("mfwpid",pid=pid,name=name)
    
