#coding:utf-8
from publicsettings import dbconn
from mfwutils import dictToOrderList

def calActSummary(sql):
    res = dbconn.query(sql)

    summary = {}

    for r in res:
        actSummaryString = r.actSummaryString
        actStrings = actSummaryString[1:].split(u"$")
        for actString in actStrings:
            act,count = actString.split(u"|")[0], actString.split(u"|")[1]
            if summary.has_key(act):
                summary[act] = summary[act] + 1
            else:
                summary.update({act:1})

    summaryOrder = dictToOrderList(summary)

    return summaryOrder

def main():
    sql =   """
            select actSummaryString from mfwuserfeed
            where sumcount = 2 and datedense = 1 and actdense <> 1
            limit 1
            """
    print calActSummary(sql)

if __name__ == "__main__":
    main()

