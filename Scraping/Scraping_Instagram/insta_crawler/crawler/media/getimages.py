from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
import time , threading
from urllib.request import urlopen
# import getcomments
from dateutil.parser import parse
from . import login
from webdriver_manager.chrome import ChromeDriverManager
import os
import requests

username = 'ghassen13021302@gmail.com'
password = 'Ghassen123'



class Getimages:
    def __init__(self, profil='', post_scroll_down=0, start_time='', keys=[], download_img=False):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        op.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(ChromeDriverManager().install() , options= op, service_log_path='NUL')
        #self.driver = webdriver.Chrome(ChromeDriverManager().install() , service_log_path='NUL')

        self.profil = profil
        self.post_scroll_down = post_scroll_down
        self.driver_list = []
        self.download_img = download_img
        if (keys==[]):
            l = login.Login(self.driver, username, password)
            l.signin()
            self.driver.get('https://www.instagram.com/'+ profil+ '/?hl=fr')
            time.sleep(2)
            self.driver_list = [self.driver]
        else:
            timeout = 5
            
            for key in keys:
                #driver = webdriver.Chrome(ChromeDriverManager().install() , service_log_path='NUL')
                driver = webdriver.Chrome(ChromeDriverManager().install() , options= op, service_log_path='NUL')
                l = login.Login(driver, username, password)
                driver = l.signin()
                driver.get('https://www.instagram.com/explore/tags/'+str(key)+'/')
                self.driver_list.append(driver)
                time.sleep(2)

        self.keys = keys
        self.dt=''
        if start_time != '':
            self.dt = parse(start_time)


    def get_links(self):
        links = []	
        img_url = []
        for driver in self.driver_list:
            time.sleep(2)
            self.popup = WebDriverWait(driver, 10). until(EC.presence_of_element_located((By.CSS_SELECTOR, 'html')))
            posts = driver.find_elements_by_css_selector('.v1Nh3.kIKUG._bz0w')
            posts = []
            for h in range(11):
                time.sleep(1)
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight/{}'.format(str(11-h)), self.popup)
                if h == 5:
                    break
            	
            for i in range(self.post_scroll_down):
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', self.popup)
                time.sleep(2)
                posts.append(driver.find_elements_by_css_selector('.v1Nh3.kIKUG._bz0w'))
                for p in posts:

                    try:
                        if (type(p)== list):
                            for sub_p in p :
                                txt = soup(sub_p.get_attribute('innerHTML'),'html.parser')
                                links.append('https://www.instagram.com' + txt.a['href'])
                                img_url.append(txt.img['src'])
                                
                        else:
                            txt = soup(p.get_attribute('innerHTML'),'html.parser')
                            links.append('https://www.instagram.com' + txt.a['href'])
                            img_url.append(txt.img['src'])
                        
                        time.sleep(1)
                    except:
                        pass			
                        
            driver.quit()
              
        return list(dict.fromkeys(links)), list(dict.fromkeys(img_url))
        

    def get_link(self, i, links, img_url):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        op.add_argument("--log-level=3")
        op.add_argument("--no-sandbox")
        driver = webdriver.Chrome(ChromeDriverManager().install() , options= op,  service_log_path='NUL')
        #driver = webdriver.Chrome(ChromeDriverManager().install() , service_log_path='NUL')
        driver.get(links[i])

        date = driver.find_element_by_css_selector('.Nzb55').get_attribute('datetime')
        datetime = parse(date)
        print(date)
        if self.dt != '':
            if datetime.date() > self.dt.date():
                if datetime.time() > self.dt.time():
                    print("scraping: "+str(date)) 
                    self.img.append({'img_link':img_url[i]})
                    time.sleep(2)
                    
        driver.quit()        


    def get_images(self, links, img_url):
        self.img = []
        
        for i in range(len(links)):
            if (self.dt!=''):
                self.get_link(i, links, img_url)
            else:
                self.img.append({'img_link':img_url[i]})
            
        if (not self.download_img):
            return self.img
        else:
            if not os.path.exists('images'):
                os.makedirs('images')
                
            list = os.listdir('images') 
            number_images = len(list)
                
            for i in range(len(self.img)):
                img_link = self.img[i]['img_link']
                name="images/image"+str(number_images + i)+".jpg"
                with open(name, 'wb') as handler:
                    img_data = requests.get(img_link).content
                    handler.write(img_data)
            


def convert(f):        

    f = f.replace(',','.').replace(' ','')
    if 'k' in f:
        f = float(f[:-1]) * 10**3
        return f
    elif 'm' in f:
        f = float(f[:-1]) * 10**6
        return f
    else:
        return float(f)