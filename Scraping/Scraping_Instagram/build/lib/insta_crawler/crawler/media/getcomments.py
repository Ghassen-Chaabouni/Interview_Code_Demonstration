from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time
import pandas as pd
from bs4 import BeautifulSoup as b

class Getcomments :

    def __init__(self,driver,profil):
        self.driver = driver 
        self.profil = profil

    def getcomment(self,link):
        
        # button = self.driver.find_element_by_css_selector('.u-__7')
        # scroll = self.driver.find_element_by_css_selector('.RxcQ6')
        result =[]
        for i in range(30):
            # scroll = self.driver.find_element_by_css_selector('.RxcQ6')
            # self.driver.execute_script("document.getElementsByClassName('RxcQ6').scrollTop=document.getElementsByClassName('RxcQ6').scrollHeight",scroll)
            # k = self.driver.find_element_by_css_selector('.RxcQ6')
            # button = WebDriverWait(k, 10). until(EC.presence_of_element_located((By.CSS_SELECTOR, '.u-__7')))
            try :
                button = self.driver.find_element_by_css_selector('.u-__7')
                button.click()
            except:
                break

            comments = self.driver.find_elements_by_css_selector('.Mr508')

            for c in comments:
                text = b(c.get_attribute('innerHTML'),'html.parser')
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