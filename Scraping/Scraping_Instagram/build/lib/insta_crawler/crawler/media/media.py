from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as b
import time
from urllib.request import urlopen
import urllib.request
from webdriver_manager.chrome import ChromeDriverManager
from . import login

username = 'jawherbouhouch75'
password = '123456789pilote@'

class Media():
    def __init__(self , profil):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        op.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(ChromeDriverManager().install() , options= op, service_log_path='NUL')
        l = login.Login(self.driver, username, password)
        l.signin()
        self.profil = profil
        self.driver.get('https://www.instagram.com/'+ self.profil+ '/?hl=fr')
        time.sleep(2)

    def get_profile_image(self, **kwargs):
        img = self.driver.find_element_by_css_selector('._6q-tv').get_attribute('src')
        if ('download' in kwargs) and (kwargs['download']==True or kwargs['download']==1) :
            urllib.request.urlretrieve(img, "%s.jpg" % self.profil)      
        return img

    def get_last_image(self, **kwargs):
        img = self.driver.find_element_by_css_selector('.FFVAD').get_attribute('src')
        if ('download' in kwargs) and (kwargs['download']==True or kwargs['download']==1):
            urllib.request.urlretrieve(img, "%s_last_image.jpg" % self.profil)
        return img

    def get_last_location(self):
        scroll = 1
        while True:
            self.popup = WebDriverWait(self.driver, 10). until(EC.presence_of_element_located((By.CSS_SELECTOR, 'html')))
            for i in range(scroll):
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', self.popup)
                posts = self.driver.find_elements_by_css_selector('.v1Nh3.kIKUG._bz0w')
            for p in posts:
                try:
                    if (type(p)== list):
                        for sub_p in p :
                            txt = b(sub_p.get_attribute('innerHTML'),'html.parser')
                    else:
                        txt = b(p.get_attribute('innerHTML'),'html.parser')
                    link = 'https://www.instagram.com' + txt.a['href']
                    self.driver.get(link)
                    location = self.driver.find_element_by_css_selector('.O4GlU').text
                    if location != '':
                        self.driver.get('https://www.instagram.com/'+ self.profil+ '/?hl=fr')
                        return location
                    time.sleep(1)
                except:
                    pass	
            self.driver.get('https://www.instagram.com/'+ self.profil+ '/?hl=fr')
            scroll = scroll + 1
            if scroll >10:
                break
        return ' '

    def get_number_publications(self):
        number = self.driver.find_elements_by_css_selector('a .g47SY')[0].text
        return number 

    def get_number_followers(self):
        number = self.driver.find_elements_by_css_selector('a .g47SY')[1].text
        return convert(number)

    def get_number_followed(self):
        number = self.driver.find_element_by_css_selector('.Y8-fY~ .Y8-fY+ .Y8-fY .g47SY').text
        return convert(number)

    def get_last_post_date(self):
        try :
            date = self.driver.find_element_by_css_selector('.Nzb55').text
            return date
        except :
            return None

    def get_last_post_likes(self):
        try :
            likes = self.driver.find_element_by_css_selector('._8A5w5 span').text
            return likes
        except :
            return 0

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


