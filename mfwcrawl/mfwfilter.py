#coding:utf-8
import os,re
from scrapy.exceptions import IgnoreRequest
from publicsettings import tempArticleDir


class sche_dupli_article(object):
    def __init__(self):
        self.fingerprints = {}

    def open_spider(self, spider):
        comp = re.compile("(\d+).html")
        self.fingerprints[spider] = set()
        for dir in os.listdir(tempArticleDir):
            for articleFilename in os.listdir(tempArticleDir+"/"+dir):
                m = comp.search(articleFilename)
                if m:
                    self.fingerprints[spider].add(m.group(1))
                
    def close_spider(self, spider):
        del self.fingerprints[spider]

    def enqueue_request(self, spider, request):
        seen = self.request_seenn(spider, request)
        if seen and not request.dont_filter:
            raise IgnoreRequest('Skipped (request already seen)')

    def request_seenn(self, spider, request, dont_record=False):
        m = re.search("(\d+).html",request.url)
        if not m:
            return False
        articleid = m.group(1)
        if articleid in self.fingerprints[spider]:
            return True
        if not dont_record:
            self.fingerprints[spider].add(articleid)
        return False
