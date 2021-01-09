from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json

from webdriver_manager.chrome import ChromeDriverManager
from . import login

username = 'jawherbouhouch75'
password = '123456789pilote@'

class Profil() :
    def __init__(self , profil):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        op.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options= op )
        l = login.Login(self.driver, username, password)
        l.signin()
        self.profil = profil
        self.driver.get('https://www.instagram.com/'+ self.profil+ '/?hl=fr')

    def get_info(self):
        """
            a function to extract all infos about a profil such :
            number of publications; number of followers and following 
            profil description and photos
            verified account or not and its stories
        """
        result = {}

        publications = self.driver.find_element_by_css_selector('span.g47SY').text
        followers = self.driver.find_elements_by_css_selector('span.g47SY')[1].text
        following = self.driver.find_elements_by_css_selector('span.g47SY')[2].text
        result['publications'] = convert(publications)
        result['followers'] = convert(followers)
        result['following'] = convert(following)

        try : 
            profil = self.driver.find_element_by_css_selector('.rhpdm').text
        except:
            profil = ''

        try :    
            description = self.driver.find_element_by_css_selector('br+ span').text
        except:
            description = ''
        result['profil description '] = profil + ' '  + description
        
        try :
            stories = []
            story = self.driver.find_elements_by_css_selector('.eXle2')
            for s in story:
                stories.append(s.text)
        except :
            stories = ''
        result['stories'] = stories
        
        try:
            pdp = self.driver.find_element_by_css_selector('._6q-tv').get_attribute('src')
        except:
            pdp = ''
        result['pdp'] = pdp
            

        try:
            self.driver.find_element_by_css_selector('.coreSpriteVerifiedBadge')
            verified = True 
        except:
            verified = False
        result['verified'] = verified

        try :
            self.driver.find_element_by_css_selector('.QlxVY')
            private_account = True
        except:
            private_account = False
        result['private_account'] = private_account

        return(json.dumps(result))
        
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