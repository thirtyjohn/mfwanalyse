#coding:utf-8
from publicsettings import dbconn
from mfwutils import dictToOrderList

sumcount_con = ["0","1","2","between 3 and 10",">10"]

class Condition:
    def __init__(self,condition):
        self.conditon = condition
        self.firstact = self.calAct("firstact",condition)
        self.mostact = self.calAct("mostact",condition)
        self.actDense = self.calDense("actDense",condition)
        self.dataDense = self.calDense("dateDense",condition)
        
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
    print dif_res

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
    print res_d



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
            where 
            sumcount > 10
            and mostact = 5
            """
    print calActSummary(sql)

if __name__ == "__main__":
    calDif("sumcount =2","sumcount = 2 and mostact = 1")

