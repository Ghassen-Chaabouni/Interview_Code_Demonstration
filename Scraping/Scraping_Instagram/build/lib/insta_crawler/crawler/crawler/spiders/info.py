# importing libraries
import scrapy
from scrapy.crawler import CrawlerProcess  
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
from scrapy import signals
import json 
import pathlib

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from items import CrawlerItem


class InfoSpider(scrapy.Spider):
    '''
        A spider to extract general info on a profil:
        **name
        **profile_pic
        **biography
        **followed
        **follow
    '''

    name = 'info'
    output = {}
    def __init__(self, profil):
        self.profil = profil
        self.start_urls = ["https://www.instagram.com/"+self.profil+"/?__a=1"]

    def parse(self,response):
        graphql = json.loads(response.text)
        
        global output 
        output =  CrawlerItem(
            name = graphql['graphql']['user']['full_name'],
            profile_pic = graphql['graphql']['user']['profile_pic_url'],
            biography = graphql['graphql']['user']['biography'],
            followed = graphql['graphql']['user']['edge_followed_by']['count'],
            follow = graphql['graphql']['user']['edge_follow']['count']
        )
        return output


from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

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
            pathlib.Path('%s.csv' % user) : {'format': 'csv'},
        })
    elif (json_parser == True) and (csv_parser == False):
        settings.set("FEEDS",{
            "%s.json" % user: {"format": "json"},
        })
    elif(csv_parser == True) and (json_parser == False) : 
        settings.set("FEEDS" ,{
            pathlib.Path('%s.csv' % user) : {'format': 'csv'},
        })    

    logging.getLogger('scrapy').propagate = False
    runner = CrawlerRunner(settings)

    d = runner.crawl(InfoSpider,profil= user )
    d.addBoth(lambda _: reactor.stop())
    reactor.run() # the script will block here until the crawling is finished
