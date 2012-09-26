# Scrapy settings for mfwcrawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

from publicsettings import logDir

BOT_NAME = 'mfwcrawl'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['mfwcrawl.spiders']
NEWSPIDER_MODULE = 'mfwcrawl.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
STATS_ENABLED = True
LOG_FILE = logDir
LOG_STDOUT = True
DOWNLOAD_DELAY = 0


"""
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': None,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware':None,
    'scrapy.contrib.downloadermiddleware.redirect.MyRedirectMiddleware':501,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentRotateMiddleware': 502,
}
"""
