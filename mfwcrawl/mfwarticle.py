#!/usr/bin/env python
#coding:utf-8

#!/usr/bin/env python
#coding:utf-8
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import bs4,re,urllib2,os
from datetime import datetime
from publicsettings import tempArticleDir

def getImgTexts(html):
   soup = BeautifulSoup(html,"html5lib",from_encoding="utf8")##,parse_only=SoupStrainer("div",id="pnl_contentinfo"))
   txt = u""
   imgs = []
   texts = []
   for p in soup.find("div",id="pnl_contentinfo").contents:
       if not isinstance(p,bs4.element.Tag):
           continue
       print "==========="
       print p
       if p.find("img") and p.find("img").parent.name=="a":
           print p.img
           texts.append(txt.strip() if not isSpace(txt) else None)
           imgs.append(p.img["src"])
           txt = p.get_text()
       elif not isSpace(p.get_text()):
           txt = txt + p.get_text()
   texts.append(txt.strip() if not isSpace(txt) else None)
   return imgs,texts


def getMeta(html):
    meta = {}
    soup = BeautifulSoup(html,from_encoding="utf8")
##source
    meta.update({"source":2})
##title
    title = unicode(soup.find("div","post_title").h1.string)
    meta.update({"title":title})
##wdate
    wdate =  datetime.strptime(soup.find("span","date").string,"%Y-%m-%d %H:%M:%S")
    meta.update({"wdate":wdate})
##location
    location = None
    dl_location = soup.find("dl","related_mdd")
    if dl_location:
        location = unicode(dl_location.p.a.string)
    meta.update({"location":location}) 
##author
    author_div = soup.find("div","fl").a
    author = unicode(author_div.string)
    author_link = u"http://www.mafengwo.cn" + unicode(author_div["href"])
    meta.update({"author":author,"author_link":author_link})
    return meta

def getHtml(url):
    html = urllib2.urlopen(url).read()
    return html

comp = re.compile(u"^[\s\xc2\xa0]+$")
def isSpace(text):
    if text is None:
        return True
    if text == "":
        return True
    if comp.match(text):
        return True
    return False


def fileToArticle(aid):
    html = open(tempArticleDir +"/"+ str(aid)[0:2] + "/" + str(aid)).read()
    soup = BeautifulSoup(html,from_encoding="utf8")

    #aid

    atype = None 
    if html.find(u"btn_Addpost") > -1:
        atype = 1
    elif html.find(u"op_btn") > -1:
        atype = 2

    title = unicode(soup.find("div","post_title").h1.string)
    
    author_div = soup.find("div","fl").a
    author = unicode(author_div.string)
    author_link = u"http://www.mafengwo.cn" + unicode(author_div["href"])

    wdate =  datetime.strptime(soup.find("span","date").string,"%Y-%m-%d %H:%M:%S")

    #replyCount
    r_div = soup.findall("div","post_item")
    replyCount = len(r_div) - 1
    reply_div = soup.find("div","turn_page").find("div","paginator")
    if reply_div:
        findall("a")
        reply_page = int(a[-2].string)
        replyCount = replyCount + (reply_page-1)*50


    location = None
    dl_location = soup.find("dl","related_mdd")
    if dl_location:
        location = unicode(dl_location.p.a.string)


    imgs,txt = getImgTexts(html)
    imgCount = len(imgs)
    txtCount = 0
    for t in txt:
        txtCount = txtCount + len(t)
    

def main():
    comp = re.compile(u"(\d+).html")
    for articleDir in os.listdir(tempArticleDir):
        if os.path.isdir(tempArticleDir +"/"+ articleDir):
            for filename in os.listdir(tempArticleDir +"/"+ articleDir):
                m = comp.search(filename)
                if not m:
                    continue
                articleid = int(m.group(1))
                fileToArticle(articleid)




