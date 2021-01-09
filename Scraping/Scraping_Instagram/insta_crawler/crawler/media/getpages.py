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

username = 'ghassen13021302@gmail.com'
password = 'Ghassen123'


class getReplies :
    def __init__(self,driver):
        self.driver = driver

class Getcomments :

    def __init__(self,driver,profil, comment_scroll_down=0):
        self.driver = driver 
        self.profil = profil
        self.comment_scroll_down = comment_scroll_down

    def getcomments_from_pub(self,link) :
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        op.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(ChromeDriverManager().install() , options= op, service_log_path='NUL')
        #self.driver = webdriver.Chrome(ChromeDriverManager().install() , service_log_path='NUL')
        l = login.Login(self.driver, username, password)
        l.signin()
        self.driver.get('https://www.instagram.com/p/'+ link)

        result =[]
        for i in range(30):
            try :
                button = self.driver.find_element_by_css_selector('.u-__7')
                button.click()
            except:
                break

            comments = self.driver.find_elements_by_css_selector('.Mr508')

            for c in comments:
                text = soup(c.get_attribute('innerHTML'),'html.parser')
                # print(text)
                # print(text.findAll('div',{'class':'ZyFrc'}))

                try:
                    commentator = text.find('a',{'class':['Mr508' ,'ZIAjV']}).get_text()
                
                    comment = text.select_one('.C4VMK > span').get_text()

                    likes = text.select_one('button.FH9sR').text.replace(" mentions J’aime",'').replace(" mention J’aime",'')
                    date = text.select_one('.Nzb55').text
                    result.append({'commentator':commentator,'comment':comment,'likes': likes, 'date':date})
                except :
                    pass
            time.sleep(1)
        # text = self.profil + '/' +link[-11:-2] + '.xls'
        # s = pd.DataFrame(result,columns=['commentator','comment','likes','date']).to_json(orient = "records")
        return result




    def getcomment(self, link):
        
        result =[]
        for i in range(self.comment_scroll_down):
            comments = self.driver.find_elements_by_css_selector('.Mr508')
            for c in comments:
                 					
                text = soup(c.get_attribute('innerHTML'),'html.parser')

                try:
                    commentator = text.find('a',{'class':['Mr508' ,'ZIAjV']}).get_text()
                
                    comment = text.select_one('.C4VMK > span').get_text()

                    likes = text.select_one('button.FH9sR').text
                    date = text.select_one('.Nzb55').text
                    result.append({'commentator':commentator,'comment':comment,'likes': likes, 'date':date})
                except :
                    pass
            time.sleep(1)
            try :
                button = self.driver.find_element_by_css_selector('.glyphsSpriteCircle_add__outline__24__grey_9.u-__7')
                button.click()
            except:
                break

        return result




class Getpages:
    def __init__(self,profil='', post_scroll_down=0, comment_scroll_down=0, start_time='' , comments = False, keys=[]):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        op.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(ChromeDriverManager().install() , options= op, service_log_path='NUL')
        #self.driver = webdriver.Chrome(ChromeDriverManager().install() , service_log_path='NUL')

        self.profil = profil
        self.comments = comments
        self.post_scroll_down = post_scroll_down
        self.comment_scroll_down = comment_scroll_down
        self.driver_list = []
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
                                
                        else:
                            txt = soup(p.get_attribute('innerHTML'),'html.parser')
                            links.append('https://www.instagram.com' + txt.a['href'])
                        
                        time.sleep(1)
                    except:
                        pass			
                        
            driver.quit()
              
        return set(links)
        
    def get_link(self, link):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        op.add_argument("--log-level=3")
        op.add_argument("--no-sandbox")
        driver = webdriver.Chrome(ChromeDriverManager().install() , options= op,  service_log_path='NUL')
        #driver = webdriver.Chrome(ChromeDriverManager().install() , service_log_path='NUL')
        driver.get(link)
        
        date = driver.find_element_by_css_selector('.Nzb55').get_attribute('datetime')
        datetime = parse(date)
        print(date)
        if self.dt != '':
            if datetime.date() > self.dt.date():
                if datetime.time() > self.dt.time():
                    print("scraping: "+str(date)) 
                    if self.comments == True :
                        gcom = Getcomments(driver, self.profil, self.comment_scroll_down)
                        comments = gcom.getcomment(link)

                    try :
                        post = driver.find_element_by_css_selector('#react-root > section > main > div > div > article > div.eo2As > div.EtaWk > ul > div > li > div > div > div.C4VMK > span').text
                    except:
                        post = ''
                    try:	
                        likes = int(driver.find_element_by_css_selector('._8A5w5 span').text.replace(' ',''))
                    except:
                        likes = ''
                    try:	
                        location = driver.find_element_by_css_selector('.O4GlU').text
                    except:
                        location = ''
                    
                    try:
                        img = driver.find_element_by_css_selector('.wKWK0')
                        desc_img = img.find_element_by_css_selector('img').get_attribute('alt')
                    except:
                        desc_img = ''
                    

                    shortcode = link[-11:-2]
                    if self.comments ==True :			
                        self.posts.append({'profil':self.profil, 'post':post, 'id':shortcode , 'location':location, 
                                            'desc_img':desc_img ,'date': date, 'likes': likes,'comments':comments })
                    else :
                        self.posts.append({'profil':self.profil, 'post':post, 'id':shortcode ,'likes': likes,
                                           'location':location, 'desc_img':desc_img ,'date': date})
                    time.sleep(2)
        else:
            print("scraping: "+str(date)) 
            if self.comments == True :
                gcom = Getcomments(driver, self.profil, self.comment_scroll_down)
                comments = gcom.getcomment(link)

            try :
                post = driver.find_element_by_css_selector('#react-root > section > main > div > div > article > div.eo2As > div.EtaWk > ul > div > li > div > div > div.C4VMK > span').text
            except:
                post = ''
            try:	
                likes = int(driver.find_element_by_css_selector('._8A5w5 span').text.replace(' ',''))
            except:
                likes = ''
            try:	
                location = driver.find_element_by_css_selector('.O4GlU').text
            except:
                location = ''
            
            try:
                img = driver.find_element_by_css_selector('.wKWK0')
                desc_img = img.find_element_by_css_selector('img').get_attribute('alt')
            except:
                desc_img = ''
            

            shortcode = link[-11:-2]
            if self.comments ==True :			
                self.posts.append({'profil':self.profil, 'post':post, 'id':shortcode , 'location':location, 
                                    'desc_img':desc_img ,'date': date, 'likes': likes,'comments':comments })
            else :
                self.posts.append({'profil':self.profil, 'post':post, 'id':shortcode ,'likes': likes,
                                   'location':location, 'desc_img':desc_img ,'date': date})
            time.sleep(2)
        driver.quit()

    def get_posts(self, links):
        self.posts = []
 
        for link in links:
            self.get_link(link)
            
        return self.posts


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