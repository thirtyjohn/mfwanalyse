#coding:utf-8
from bs4 import BeautifulSoup
import urllib2,bs4

##html = urllib2.urlopen("http://www.mafengwo.cn/home/feedlist.php?uid=768689&page=1").read()
html = open("/Users/macbookpro/lvping/test.html")
moveList = list()

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
    if not text in moveList and text <> "":
        moveList.append(text)
for m in moveList:
    print m
    

