#coding:utf-8
from bs4 import BeautifulSoup
import bs4,math,re,os
from publicsettings import useridRange,dbconn,tempDir,articleidRange
from datetime import datetime

actypeDict = {}
res = dbconn.query("select * from mfwactype")
for r in res:
    actypeDict.update({r.name:r.id})

    
def hasMoreFeedPage(html):
    soup = BeautifulSoup(html, from_encoding="utf8")
    page = soup.find("div","f_turnpage")
    if not page:
        return False
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
        dbconn.insert("mfwuserfeed",
                userid = userid,
                pageCount=lastpage,
                sumCount=0
        )
        return
    if len(actDictList) == 1:
        dbconn.insert("mfwuserfeed",
                userid = userid,
                pageCount=lastpage,
                sumCount=1,
                firstAct = actDictList[-1][0],
                firstActTime = actDictList[-1][1],
                mostAct = actDictList[-1][0],
                actSummaryString = "$" + str(actDictList[-1][0]) + "|1",
                actDense = 1,
                dateDense = 1
        )
        return
    ##registryTime = getRegistryTime()
    sumCount = len(actDictList)
    firstAct = actDictList[-1][0]
    firstActTime = actDictList[-1][1]
    actSummary,dateSummary = getActDateSummary(actDictList)
    mostAct = actSummary[0][0]
    actSummaryString = summaryToString(actSummary)
    actDense = calDense(actSummary)
    dateDense = calDense(dateSummary)
    longestPeriod, mostPeriod, deviation, avgPerd, middlePerd = calRate(dateSummary)
    print "sumCount:" + str(sumCount)
    print "firstAct:" + str(firstAct)
    print "firstActTime:" + str(firstActTime)
    print "mostAct:" + str(mostAct)
    print "actSummaryString:" + str(actSummaryString)
    print "actDense:" + str(actDense)
    print "dateDense:" + str(dateDense)
    print "longestPeriod:" + str(longestPeriod)
    print "mostPeriod:" + str(mostPeriod)
    print "deviation:" + str(deviation)
    print "avgPerd:" + str(avgPerd)
    print "middlePerd:" + str(middlePerd)
    dbconn.insert("mfwuserfeed",
                userid = userid,
                pageCount=lastpage,
                sumCount=sumCount,
                firstAct=firstAct,
                firstActTime = firstActTime,
                mostAct = mostAct,
                actSummaryString = actSummaryString,
                actDense = actDense,
                dateDense = dateDense,
                longestPeriod = longestPeriod,
                mostPeriod = mostPeriod,
                deviation = deviation,
                avgPerd = avgPerd,
                middlePerd = middlePerd
    )

def summaryToString(tList):
    summaryString = ""
    for t in tList:
        summaryString = summaryString + "$" + str(t[0]) + "|" + str(t[1])
    return summaryString

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
                    actDate = datetime.strptime(dateSpan.string,"%Y-%m-%d %H:%M:%S")
                feedList.append((actypeDict[text],actDate))
            else:
                unknownActType.append(text)
    return feedList

def getActDateSummary(actDictList):
    actSummaryDict = {}
    dateSummaryDict = {}
    for actDict in actDictList:
        act = actDict[0]
        actDate = actDict[1].date()
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
        dense = dense + (t[1]*1.0/listsum)**2
    return math.sqrt(dense)


def calRate(tList):
    if len(tList) == 1:
        return 0,0,0,0,0
    ##longestPeriod, mostPeriod, deviation
    perdSummaryDict = {}
    sumPerd = 0
    segPerd = 0
    perdList = []
    dateList = sorted(tList,key=lambda t: t[0],reverse=False)
    for i in range(1,len(dateList)):
        perd = (dateList[i][0] - dateList[i-1][0]).days
        perdList.append(perd)
##most and longest
        if perdSummaryDict.has_key(perd):
            perdSummaryDict[perd] = perdSummaryDict[perd] + 1
        else:
            perdSummaryDict.update({perd:1})
        sumPerd = sumPerd + perd
        segPerd = segPerd + perd**2
    longestPerd = max(perdSummaryDict.keys())
    mostPerd = dictToOrderList(perdSummaryDict)
    mostPerd = mostPerd[0][0]
    avgPerd = sumPerd*1.0/(len(tList)-1)
    ##print "segPerd:" + str(segPerd)
    ##print "avgPerd:" + str(avgPerd)
    deviaiion = math.sqrt(1.0/(len(tList)-1)*segPerd-avgPerd**2)
    perdList = sorted(perdList,key=lambda t: t,reverse=False)
    middlePerd = perdList[len(perdList)/2]
    return longestPerd, mostPerd, deviaiion, avgPerd, middlePerd







def getNickName(userid):
    html = open(tempDir + "/" + str(userid) + "_1.html").read()
    soup = BeautifulSoup(html,from_encoding="utf8")
    div = soup.find("div","top_lab")
    name = div.find("div","lab_on").string
    return name[0:-4]


def hasMoreWaa(filepath):
    if os.path.getsize(filepath) < 35000:
        return False
    return hasMoreFeedPage(open(filepath).read())


def genUserIds():
    feedRange = []
    for userid in useridRange:
        feedRange.append(userid)
    ##print feedRange
    comp = re.compile("(\d+)_(\d+).html")
    for dir in os.listdir(tempDir):
        feedDir = tempDir + "/" + dir
        if not os.path.isdir(feedDir):
            continue
        tempid = 0
        temppage = 0
        for feedFilename in os.listdir(feedDir):
            m = comp.search(feedFilename)
            if m:
                userid = int(m.group(1))
                pagenum = int(m.group(2))
                if tempid == 0:
                    tempid = userid
                if temppage == 0:
                    temppage = pagenum
                if  userid <> tempid:
                    if hasMoreWaa(feedDir+"/"+str(tempid) + "_" + str(temppage) + ".html") and not tempid in feedRange:
                        feedRange.append(tempid)
                    elif tempid in feedRange:
                        feedRange.remove(tempid)
                    tempid = userid
                temppage = pagenum

    for userid in feedRange:
        yield userid

def getArticleIds():
    for articleid in articleidRange:
        yield articleid


def fileToFeed():
    comp = re.compile(u"(\d+)_(\d+).html")
    userid = 0
    pagenumber = 0
    for filename in os.listdir(tempDir):
        print filename
        m = comp.search(filename)
        if not m:
            continue
        if userid == int(m.group(1)):
            pagenumber = int(m.group(2))
        else:
            if userid <> 0:
                getPagesAndCal(userid,pagenumber)
            userid = int(m.group(1))
            pagenumber = int(m.group(2))

def main():
    comp = re.compile(u"(\d+)_(\d+).html")
    for filename in os.listdir(tempDir):
        m = comp.search(filename)
        if not m:
            continue
        if int(m.group(2)) == 1:
            userid = int(m.group(1))
            nickname = getNickName(userid)
            dbconn.insert("mfwuser",userid=userid,nickname=nickname)



if __name__ == "__main__":
    main()

