#coding:utf-8
from bs4 import BeautifulSoup
import bs4,math
from publicsettings import useridRange,dbconn,tempDir
from datetime import datetime

actypeDict = {}
res = dbconn.query("select * from mfwactype")
for r in res:
    actypeDict.update({r.name:r.id})

    
def hasMoreFeedPage(html):
    soup = BeautifulSoup(html, from_encoding="utf8")
    page = soup.find("div","f_turnpage")
    pages = page.get_text()
    if pages.find(u"末页") > -1:
        return True
    else:
        return False

def getPagesAndCal(userid,lastpage):
    actDictList = []
    for pagenumber in range(1,lastpage+1):
        html = open(tempDir + "/" + str(userid) + "_" + str(pagenumber) + ".html").read()
        actDictList.extend( getFeed(html) )
    if len(actDictList) == 0:
        return
    ##registryTime = getRegistryTime()
    sumCount = len(actDictList)
    firstAct = actDictList[0][0]
    firstActTime = actDictList[0][1]
    actSummary,dateSummary = getActDateSummary(actDictList)
    mostAct = actSummary[0]
    actSummaryString = summaryToString(actSummary)
    actDense = calDense(actSummary)
    dateDense = calDense(dateSummary)
    longestPeriod, mostPeriod, deviation = calRate(dateSummary)
    print "sumCount:" + sumCount
    print "firstAct:" + firstAct
    print "firstActTime:" + firstActTime
    print "mostAct:" + mostAct
    print "actSummaryString:" + actSummaryString
    print "actDense:" + actDense
    print "dateDense:" + dateDense
    print "longestPeriod:" + longestPeriod
    print "mostPeriod:" + mostPeriod
    print "deviation:" + deviation

def summaryToString(tList):
    summaryString = ""
    for t in tList:
        summaryString = summaryString + "$" + str(t[0]) + "|" + str(t[1])

unknownActType = []

def getFeed(html):
    feedList = []
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
            if actypeDict.has_key(text):
                actDate = None
                dateSpan = con.find("span","date")
                if dateSpan:
                    actDate = datetime.strptime(dateSpan.string,"%Y-%m-%d %H:%M:%S").date()
                feedList.append((actypeDict[text],actDate))
            else:
                unknownActType.append(text)
    return feedList

def getActDateSummary(actDictList):
    actSummaryDict = {}
    dateSummaryDict = {}
    for actDict in actDictList:
        act = actDict[0]
        actDate = actDict[1]
        if actSummaryDict.has_key(act):
            actSummaryDict[act] = actSummaryDict[act] + 1
        else:
            actSummaryDict.update({act:1})

        if dateSummaryDict.has_key(actDate):
            dateSummaryDict[actDate] = dateSummaryDict[actDate] + 1
        else:
            dateSummaryDict.update({actDate:1})
    return dictToOrderList(actSummaryDict), dictToOrderList(dateSummaryDict)

def dictToOrderList(tDict):
    dictList = []
    for key, value in tDict.iteritems():
        temp = (key,value)
        dictList.append(temp)
    return sorted(dictList,key=lambda t: t[1],reverse=True)

def calDense(tList):
    listsum = 0
    dense = 0
    for t in tList:
        listsum = listsum + t[1]
    for t in tList:
        dense = dense + (t[1]/listsum)^2
    return math.sqrt(dense)


def calRate(tList):
    ##longestPeriod, mostPeriod, deviation
    perdSummaryDict = {}
    sumPerd = 0
    segPerd = 0
    dateList = sorted(tList,key=lambda t: t[0],reverse=False)
    for i in range(1,len(dateList)):
        perd = (dateList[i][0] - dateList[i-1][0]).days
##most and longest
        if perdSummaryDict.has_key(perd):
            perdSummaryDict[perd] = perdSummaryDict[perd] + 1
        else:
            perdSummaryDict.update({perd:1})
        sumPerd = sumPerd + perd
        segPerd = segPerd + perd^2
    longestPerd = max(perdSummaryDict.keys())
    mostPerd = max(perdSummaryDict.values())
    avgPerd = sumPerd/(len(tList)-1)
    print "segPerd:" + str(segPerd)
    print "avgPerd" + str(avgPerd)
    deviaiion = math.sqrt(1/(len(tList)-1)*segPerd-avgPerd^2)
    return longestPerd, mostPerd, deviaiion







def insertIntoDB(data):
    pass

def genUserIds():
    for userid in useridRange:
        yield userid


def main():
    getPagesAndCal(768689,2)

if __name__ == "__main__":
    main()

