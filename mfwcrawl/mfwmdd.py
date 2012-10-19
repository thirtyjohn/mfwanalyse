#coding:utf-8
import re,os
from bs4 import BeautifulSoup
from publicsettings import tempMddDir,dbconn

stdDict = {
    "post_main":"post_main",
    "box box_photo":"box_box_photo",
    "box master":"box_master",
    "box box_map":"box_box_map",
    "box baike":"box_baike",
    "box box_discuss":"box_box_discuss",
    "box box_plan":"box_box_plan",
    "box other_city":"box_other_city",
    "box box_book":"box_box_book",
    "box box_tips":"box_box_tips",
    "poi_nav":"poi_nav",
    "box postBox":"box_postBox",
    "city_hd":"city_hd",
    "box mb10":"box_mb10",
    "box mod_rec":"box_mod_rec",
    "box hotBox2":"box_hotBox2",
    "box pathBox2":"box_pathBox2",
    "box pathBox1":"box_pathBox1",
    "box hotBox1":"box_hotBox1",
    "info_cate":"info_cate",
    "box other_mdd":"box_other_mdd"
    }

comp = re.compile("(\d+).html")
comp_title = re.compile(u"2012(.+)旅游攻略")

def anaMdd(mddid,html):
    box_dict = findHtml(html)
    soup = BeautifulSoup(html,from_encoding="utf8")
    title = unicode(soup.title)
    name = comp_title.search(title).group(1)
    insert(mddid,name,box_dict)

def re_find(html,text):
    m = re.search(u'class="'+text+'( *)"',html)
    if m:
        return True
    return False

def findHtml(html):
    box_dict = {}
    for k in stdDict.keys():
        if re_find(html,k):
            box_dict.update({stdDict[k]:1})
        else:
            box_dict.update({stdDict[k]:0})
    return box_dict

def insert(mddid,name,box_dict):
    dbconn.insert("mfwmdd",
        mddid = mddid,
        name = name,
        post_main = box_dict["post_main"],
        box_box_photo = box_dict["box_box_photo"],
        box_master = box_dict["box_master"],
        box_box_map = box_dict["box_box_map"],
        box_baike = box_dict["box_baike"],
        box_box_discuss = box_dict["box_box_discuss"],
        box_box_plan = box_dict["box_box_plan"],
        box_other_city = box_dict["box_other_city"],
        box_box_book = box_dict["box_box_book"],
        box_box_tips = box_dict["box_box_tips"],
        poi_nav = box_dict["poi_nav"],
        box_postBox = box_dict["box_postBox"],
        city_hd = box_dict["city_hd"],
        box_mb10 = box_dict["box_mb10"],
        box_mod_rec = box_dict["box_mod_rec"],
        box_hotBox2 = box_dict["box_hotBox2"],
        box_pathBox2 = box_dict["box_pathBox2"],
        box_pathBox1 = box_dict["box_pathBox1"],
        box_hotBox1 = box_dict["box_hotBox1"],
        info_cate = box_dict["info_cate"],
        box_other_mdd = box_dict["box_other_mdd"]
    )

def main():
    for mdddir in os.listdir(tempMddDir):
        if not os.path.isdir(tempMddDir+"/"+mdddir):
            continue
        for filename in os.listdir(tempMddDir +"/"+mdddir):
            print filename
            mddid = int(comp.search(filename).group(1))
            html = open(tempMddDir+"/"+mdddir+"/"+filename,"r").read()
            if html == "":
                continue
            mmdlevel(mddid,html)


complevel = re.compile("mddid=(\d*)")
def mmdlevel(mddid,html):
    soup = BeautifulSoup(html,from_encoding="utf8")
    crumbs = soup.find("div","crumb").find_all("a")
    href = crumbs[1]["href"]
    pid = complevel.search(href).group(1)
    if pid == "":
        pid = None
    else:
        pid = int(pid)
    dbconn.update("mfwmdd",where="mddid = $mddid",vars=locals(),pid=pid)
    

if __name__ == "__main__":
    main()
