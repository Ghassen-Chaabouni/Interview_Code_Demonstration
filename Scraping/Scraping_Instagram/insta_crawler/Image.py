
import os 
import json
import time
from selenium import webdriver
# from .crawler.media import login
from .crawler.media import getimages
# from .crawler.media import getcomments
# from .crawler.crawler.spiders.profil import launch
# from webdriver_manager.chrome import ChromeDriverManager

username = 'jawherbouhouch75'
password = '123456789pilote@'

class Image():
    def __init__(self):
        pass
        
    def get_images(self, user='', starttime='', keys=[], download_img=False, **kwargs):
        for dict in kwargs.values(): 
            for key in dict.keys(): 
                if (key == 'post_scroll_down'):
                    post_scroll_down = int(dict[key])       
     
						
        gt = getimages.Getimages(user, post_scroll_down, starttime, keys, download_img)
        links, images_url = gt.get_links()
        posts = gt.get_images(links, images_url)
        return posts
