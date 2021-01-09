import scrapy
import json
import time
import pathlib
from scrapy import signals

# from crochet import setup
# setup()

class ImageSpider(scrapy.Spider):

    name = 'image'

    def __init__(self,profil):
        self.profil = profil
        self.start_urls = ["https://www.instagram.com/"+self.profil+"/?__a=1"]

    def parse(self,response):
        graphql = json.loads(response.text)
        print(graphql['graphql']['user']['profile_pic_url'])
        time.sleep(2)
        yield graphql['graphql']['user']['profile_pic_url']


        

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

def launch(user,**kwargs):
    if ('json_parser' in kwargs) and kwargs['json_parser']:
        json_parser = kwargs['json_parser']
    else :
        json_parser = False
        
    if ('csv_parser' in kwargs) and kwargs['csv_parser']:
        csv_parser = kwargs['csv_parser']
    else :
        csv_parser = False    


    settings = get_project_settings()
    if (json_parser==True) and (csv_parser==True):
        settings.set("FEEDS",{
            "%s_posts.json" % user: {'format': 'json' ,'encoding': 'utf8'},
            pathlib.Path('%s_posts.csv' % user) : {'format': 'csv'},
        })
    elif (json_parser == True) and (csv_parser == False):
        settings.set("FEEDS",{
            "%s_posts.json" % user: {"format": "json"},
        })
    elif(csv_parser == True) and (json_parser == False) : 
        settings.set("FEEDS" ,{
            pathlib.Path('%s_posts.csv' % user) : {'format': 'csv'},
        })  
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner(settings)

    d = runner.crawl(ImageSpider , profil= user )
    d.addBoth(lambda _: reactor.stop())
    reactor.run() # the script will block here until the crawling is finished

