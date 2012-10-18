#coding:utf-8

from publicsettings import dbconn,tempDir,tempDataDir
from mfwutils import dictToOrderList
from bs4 import BeautifulSoup
import bs4

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
    