
import os 
import json
import time
from selenium import webdriver
# from .crawler.media import login
from .crawler.media import getpages
# from .crawler.media import getcomments
# from .crawler.crawler.spiders.profil import launch
# from webdriver_manager.chrome import ChromeDriverManager

username = 'jawherbouhouch75'
password = '123456789pilote@'

class Post():
    def __init__(self):
        pass
        
        
    def get_posts(self, user='' , starttime='', comments='', keys=[], **kwargs):
        for dict in kwargs.values(): 
            for key in dict.keys(): 
                if (key == 'post_scroll_down'):
                    post_scroll_down = int(dict[key])       
                elif (key == 'comment_scroll_down'):
                    comment_scroll_down = int(dict[key])       
						
        gt = getpages.Getpages(user, post_scroll_down, comment_scroll_down, starttime, comments, keys)
        links = gt.get_links()
        posts = gt.get_posts(links)
        return posts

    def get_comment_by_publication(self , publication_id , **kwargs):
        gc = getpages.Getcomments('','')
        return gc.getcomments_from_pub(publication_id)