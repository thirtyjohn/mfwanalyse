#!/usr/bin/env python
#coding:utf-8
from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
import re,os
from scrapy import log
from mfwutils import hasMoreFeedPage,getPagesAndCal,genUserIds,getArticleIds
from publicsettings import tempDir,tempArticleDir



class Tbshop_Spider(BaseSpider):
    name = "mfwfeed"
    allowed_domains = ["mafengwo.cn"]

    def start_requests(self):
        return [FormRequest("http://www.mafengwo.cn//login/ajax.php",
                        formdata={'action':'login','code':'','login_from':'1','mail': 'karen198832@126.com', 'ps': '123456','mem':'1'},
                        callback=self.logged_in)]

    def logged_in(self,response):
        log.msg("========response=====")
        log.msg(response.body)
        for userId in genUserIds():
            yield self.make_requests_from_url("http://www.mafengwo.cn/home/feedlist.php?uid="+ str(userId) +"&page=1")
        ## make request
        
    def parse(self, response):
       m = re.search("uid=(\d+)&page=(\d+)",response.url)
       if not m:
           return
       userId = m.group(1)
       pageNumber = m.group(2)
       open(tempDir+"/"+userId+ "_" + str(pageNumber)+".html",'wb').write(response.body)
       if hasMoreFeedPage(response.body):
           yield self.make_requests_from_url("http://www.mafengwo.cn/home/feedlist.php?uid="+ userId +"&page="+ str(int(pageNumber)+1))
       else:
           data = getPagesAndCal(userId)
           insertIntoDB(data)

class MfwArticle_Spider(BaseSpider):
    name = "mfwarticle"
    allowed_domains = ["mafengwo.cn"]

    def start_requests(self):
        for articleid in getArticleIds():
            yield self.make_requests_from_url("http://www.mafengwo.cn/i/"+str(articleid)+".html")

    def parse(self, response):
        m = re.search("http://www.mafengwo.cn/i/(\d+).html",response.url)
        if not m:
           return
        articleId = m.group(1)
        root = tempArticleDir + "/" + articleId[0:2]
        if not os.path.exists(root):
            os.mkdir(root)
        open(root+"/"+articleId+ ".html",'wb').write(response.body)







