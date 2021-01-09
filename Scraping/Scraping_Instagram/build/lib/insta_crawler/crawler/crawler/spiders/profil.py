#importing libraries
import scrapy
from scrapy.crawler import CrawlerProcess  
from scrapy.signalmanager import dispatcher
from scrapy import signals
import json 
from datetime import datetime
import pathlib
from contextlib import suppress

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from items import Post

from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import logging


class ProfilSpider(scrapy.Spider):
    '''
        A spider to extract posts of a profil:
        **shortcode
        **comments[ {owner,comment,likes} ]
        **likes
        **taken_at
    '''

    name = 'profil'
    def __init__(self, profil='' , time = ''):
        #the profil to scrape from
        self.profil = profil
        if profil == '':
            self.profil = input('type the profil : ')

        self.start_urls = ["https://www.instagram.com/"+self.profil+"/?__a=1"]

        self.start_time = time
        if(time != ''):
            self.start_time = datetime.strptime(time,"%m/%d/%Y")
            self.start_time = datetime.timestamp(self.start_time)



    def parse(self,response):
        """
            scraping the shortcodes of the first 12 pages
        """

        graphql = json.loads(response.text)
        edges = graphql['graphql']['user']['edge_owner_to_timeline_media']['edges']

        # has_next helps to find if we have a next page or not 
        # end_cursor is the variable that links us to the next page  
        has_next = graphql['graphql']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        end_cursor = graphql['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']

        self.id = graphql['graphql']['user']['id']

        for edge in edges :
            yield scrapy.Request('https://instagram.com/p/'+ edge['node']['shortcode'] + '/?__a=1' , callback= self.parse_post)

        if has_next :
            yield scrapy.Request('https://instagram.com/graphql/query/?query_id=17888483320059182&id='+ self.id +'&first=12&after=' + end_cursor , callback= self.parse_profil)



    def parse_profil(self,response):
        """
            scraping the shortcodes of the other pages 
        """
        data = json.loads(response.text)
        edges = data['data']['user']['edge_owner_to_timeline_media']['edges']
        has_next = data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        end_cursor = data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'] 

        for edge in edges : 
            yield scrapy.Request(url= 'https://instagram.com/p/'+ edge['node']['shortcode']+'/?__a=1', callback= self.parse_post) 

        
        if has_next :
            yield scrapy.Request('https://instagram.com/graphql/query/?query_id=17888483320059182&id='+ self.id +'&first=12&after=' + end_cursor , callback= self.parse_profil)


    def parse_post(self,response):
        graphql = json.loads(response.text)
        shortcode = graphql['graphql']['shortcode_media']['shortcode']
        has_next = graphql['graphql']['shortcode_media']['edge_media_to_parent_comment']['page_info']['has_next_page']
        end_cursor = graphql['graphql']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor']

        edges = graphql['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges']
        likes_on_post = graphql['graphql']['shortcode_media']['edge_media_preview_like']['count']
        taken_at = graphql['graphql']['shortcode_media']['taken_at_timestamp']

        try:
            text = graphql['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
        except:
            text = ' '

        try:
            location = graphql['graphql']['shortcode_media']['location']['name']
        except:
            location = ' '

        comments = []
        for edge in edges :
            try:
                owner = edge['node']['owner']['username']
                comment = edge['node']['text']
                likes_comment = edge['node']['edge_liked_by']['count']
                comments.append({'owner': owner , 'comment': comment , 'likes' : likes_comment})
            except:
                pass
        
        if (self.start_time == ''):
            yield Post(
                    shortcode= shortcode,
                    comments= comments,
                    text= text,
                    location= location,
                    likes= likes_on_post,
                    taken_at_timestamp= datetime.fromtimestamp(taken_at)
                )
        elif (taken_at > self.start_time):
            yield Post(
                    shortcode= shortcode,
                    comments= comments,
                    text= text,
                    location= location,
                    likes= likes_on_post,
                    taken_at_timestamp= datetime.fromtimestamp(taken_at)
                )
        else:
            pass

        # if has_next :
        #     yield scrapy.Request('https://instagram.com/p/' + shortcode + '/?__a=1&max_id='+ end_cursor, callback= self.parse_post)


# def launch(user,**kwargs):

    
#     if ('json_parser' in kwargs) and kwargs['json_parser']:
#         json_parser = kwargs['json_parser']
#     else :
#         json_parser = False
        
#     if ('csv_parser' in kwargs) and kwargs['csv_parser']:
#         csv_parser = kwargs['csv_parser']
#     else :
#         csv_parser = False

#     if ('start_time' in kwargs) and kwargs['start_time']:
#         start_time = kwargs['start_time']
#     else :
#         start_time = ''    


#     settings = get_project_settings()
#     if (json_parser==True) and (csv_parser==True):
#         settings.set("FEEDS",{
#             "%s_posts.json" % user: {'format': 'json' ,'encoding': 'utf8'},
#             pathlib.Path('%s_posts.csv' % user) : {'format': 'csv'},
#         })
#     elif (json_parser == True) and (csv_parser == False):
#         settings.set("FEEDS",{
#             "%s_posts.json" % user: {"format": "json"},
#         })
#     elif(csv_parser == True) and (json_parser == False) : 
#         settings.set("FEEDS" ,{
#             pathlib.Path('%s_posts.csv' % user) : {'format': 'csv'},
#         })

#     process = CrawlerProcess(settings)

#     process.crawl(ProfilSpider, profil= user , time = start_time)
#     process.start()


# launch('realdonaldtrump')

from multiprocessing import Process, Queue


def prelaunch(user,**kwargs):
    if ('json_parser' in kwargs) and kwargs['json_parser']:
        json_parser = kwargs['json_parser']
    else :
        json_parser = False
        
    if ('csv_parser' in kwargs) and kwargs['csv_parser']:
        csv_parser = kwargs['csv_parser']
    else :
        csv_parser = False

    if ('start_time' in kwargs) and kwargs['start_time']:
        start_time = kwargs['start_time']
    else :
        start_time = ''    


    settings = get_project_settings()
    if (json_parser==True) and (csv_parser==True):
        settings.set("FEEDS",{
            "%s_posts.json" % user: {'format': 'json' ,'encoding': 'utf8'},
            pathlib.Path('%s_posts.csv' % user) : {'format': 'csv'},
        })
    elif ((json_parser == True) and (csv_parser == False)) or ((json_parser == False) and (csv_parser == False)):
        settings.set("FEEDS",{
            "%s_posts.json" % user: {"format": "json",'encoding': 'utf8'},
        })
    elif(csv_parser == True) and (json_parser == False) : 
        settings.set("FEEDS" ,{
            pathlib.Path('%s_posts.csv' % user) : {'format': 'csv'},
        })    

    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s' })
    # logging.getLogger('scrapy').propagate = False
    runner = CrawlerRunner(settings)

    d = runner.crawl(ProfilSpider,profil= user , time = start_time)
    d.addBoth(lambda _: reactor.stop())
    reactor.run() # the script will block here until the crawling is finished
    
    


    if (json_parser == False) and (csv_parser == False) :
        try :
            with open("%s_posts.json" % user , encoding= 'UTF-8') as f:
                data = json.load(f)

            # os.remove("%s_posts.json" % user)
            
            return data
        except :
            return 'cannot parse data'
    




def launch(user, **kwargs):
    x= 'cannot parse data'
    with suppress(OSError):
        while (x == 'cannot parse data' ):
            x = prelaunch(user,**kwargs)

    os.remove("%s_posts.json" % user)
    return x    
