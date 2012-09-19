#coding:utf-8
from bs4 import BeautifulSoup
import bs4,os
from publicsettings import tempDir,dbconn



moveDict = {}

htmlfiles = os.listdir(tempDir)
for htmlfile in htmlfiles:
    html = open(tempDir+"/"+htmlfile)
    soup = BeautifulSoup(html,from_encoding="utf8")
    news_lists = soup.find_all("div","news_list")
    for news_list in news_lists:
        con = news_list.find("div","con")
    ##print con.string
        text = ""
        for i in con.children:
            if isinstance(i,bs4.element.NavigableString):
                i = i.strip().encode("utf8")
                if i <> "":
                    text = text + "$" + i
        if text <> "":
            if moveDict.has_key(text):
                moveDict[text] = moveDict[text]+1
            else:
                moveDict.update({text:1})
for m in moveDict.keys():
    dbconn.insert("mfwaction",name=m,count=moveDict[m])

    

