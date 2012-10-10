#coding:utf-8
from publicsettings import dbconn,tempDataDir
from mfwutils import dictToOrderList

sumcount_con = ["0","1","2","between 3 and 10",">10"]

class Condition:
    def __init__(self,condition):
        self.conditon = condition
        self.sumCount = self.calAct("sumcount",condition)
        self.firstact = self.calAct("firstact",condition)
        self.mostact = self.calAct("mostact",condition)
        self.actDense = self.calDense("actDense",condition)
        self.dateDense = self.calDense("dateDense",condition)
        
    def calAct(self,col,cond):
        r_dict = {}
        res = dbconn.query(
        "select " + col + " as act,count(*) as count from mfwuserfeed where "+ cond +" group by " + col
        )
        for r in res:
            r_dict.update({r.act:r.count})

        r_dict = self.calDictRate(r_dict)
        return r_dict

    def calDense(self,col,cond):
        r_dict = {}
        res = dbconn.query(
        "select floor("+ col +"*10) as dense,count(*) as count from mfwuserfeed where "+ cond +" group by floor("+ col +"*10) "
        )

        for r in res:
            r_dict.update({r.dense:r.count})

        r_dict = self.calDictRate(r_dict)
        return r_dict

    def calDictRate(self,r_dict):
        v_sum = 0
        for v in r_dict.values():
            v_sum = v_sum + v
        for k in r_dict.keys():
            r_dict[k] = r_dict[k]*1.0/v_sum
        return r_dict

def calDif(con1,con2):
    con1 = Condition(con1)
    con2 = Condition(con2)
    dif_res = calDictDif(con1.firstact,con2.firstact)
    f = open(tempDataDir,"wb")
    for k,v in dif_res.items():
        f.write(str(k)+","+str(v) +"\n")

def calDictDif(dict1,dict2):
    res_d = {}
    for k in dict1.keys():
        if dict2.has_key(k):
            res_d.update({
                k:(dict2[k]-dict1[k])/(dict1[k] if dict1[k]>dict2[k] else dict2[k])
                })
        else:
            res_d.update({k:-1})
    for k in dict2.keys():
        if not dict1.has_key(k):
            res_d.update({k:1})
    return res_d



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

def anaySumcount():
    sumDict = {}
    for i in range(10000,900000,10000):
        con = Condition("userid between "+str(i)+" and "+str(i+10000))
        sumDict.update({str(i):(con.sumCount[0],con.sumCount[1] if con.sumCount.has_key(1) else 0)})

    f = open(tempDataDir,"wb")
    for k,v in sumDict.items():
        f.write(str(k)+","+str(v[0])+ "," + str(v[1]) +"\n")

def anayAct():
    f = open(tempDataDir,"wb")
    for i in range(10000,900000,10000):
        con = Condition("userid between "+str(i)+" and "+str(i+10000))
        actdenseList = dictToOrderList(con.actDense)
        datedenseList = dictToOrderList(con.dateDense)
        f.write(str(i)+","+str(actdenseList[0])+ "," + str(datedenseList[0]) +"\n")


def ana(condition):
    cons = [
        condition,
        condition + " and sumcount = 1",
        condition + " and sumcount = 2",
        condition + " and sumcount between 3 and 10",
        condition + " and sumcount > 10"
    ]
    
    f = open(tempDataDir,"wb")
    for c in cons:
        con = Condition(c)
        flist = dictToOrderList(con.firstact)
        ##mlist = dictToOrderList(con.mostact)
        f.write(c+"\n")
        for v in flist:
            f.write(str(v[0])+","+str(v[1])+"\n")



def main():
    sql =   """
            select actSummaryString from mfwuserfeed
            where 
            sumcount > 10
            and mostact = 5
            """
    print calActSummary(sql)

if __name__ == "__main__":
    ana("userid between 500000 and 600000 and firstact is not null")

