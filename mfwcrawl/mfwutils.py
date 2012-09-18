#coding:utf-8
from bs4 import BeautifulSoup
    
def hasMoreFeedPage(html):
    soup = BeautifulSoup(html, from_encoding="utf8")
    page = soup.find("div","f_turnpage")
    pages = page.get_text()
    if pages.find(u"末页") > -1:
        return True
    else:
        return False

def getPagesAndCal(userid):
    pass

def insertIntoDB(data):
    pass

def genUserIds():
    for userid in range(768800,768801):
        yield userid


def main():
    html = open("/Users/macbookpro/lvping/temp/test1.html")
    hasMoreFeedPage(html)




