#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import re
from datetime import datetime as dt
import discord_driver.scrape_messages as ScrapeMessages
import discord_driver.login as Login
from datetime import timedelta
from bs4 import BeautifulSoup as soup
import os, sys
from tqdm import tqdm


class ScrapeChosenMessages:
    
    def __init__(self, driver, start_date, end_date, room_name, key=""):

        ''' 
        Reads the value of driver, start_date, end_date, room_name and key.
        '''
		
        self.key = key
        self.driver = driver
        self.start_date = start_date
        self.end_date = end_date
        self.room_name = room_name

    def clean_html(self, raw_html):
	
        ''' 
        Remove any html tag.
        '''

        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    def determine_path (self):

        '''
        Find the path of config folder.
		'''

        try:
            root = __file__
            if os.path.islink (root):
                root = os.path.realpath (root)
            return os.path.dirname (os.path.abspath (root))
        except:
            print ("I'm sorry, but something is wrong.")
            print ("There is no __file__ variable. Please contact the author.")
            sys.exit ()
			
    def scrape(self):
	
        ''' 
        Search for the words in the words_data.txt file.
        '''
		
        if len(self.key) == 0:   # If no key is entered, config.json is used.
            f = open(self.determine_path () + '/config/words_data.txt', "r")    # Open config.json
            mess_list = f.readlines()
            f.close()
        else:     # If a key is entered.
            if (type(self.key) == str):       # If the key is a single string value.
                mess_list = [self.key]
            elif  (type(self.key) == list):   # If the key is a list.
                mess_list = self.key
		
        for mess in mess_list:
            mess = re.sub('\n', '', mess)     # Remove '\n'.
            try:
                exit_search = self.driver.find_element_by_class_name('iconContainer-O4O2CN')     # Find the exit button of a pop up.
                exit_search.location_once_scrolled_into_view            # Scroll into view.
                exit_search.click()                   # Click on the exit button.
            except:
                pass

            search_word = self.driver.find_element_by_class_name('public-DraftEditor-content')     # Find the search box.
            search_word.click()     # Click on the search box.
            time.sleep(1)
            search_word.send_keys(mess)    # Type the key.
            webdriver.ActionChains(self.driver).send_keys(Keys.ENTER).perform()   # Press ENTER.
            time.sleep(5)

            today_date = dt.today().strftime("%d/%m/%Y")       # Get today's date.
            yesterday_date = (dt.today() - timedelta(days=1)).strftime("%d/%m/%Y")    # Get yesterday's date.

            while(1):
                page = soup(self.driver.page_source, 'html.parser')              # Get the html code.
                search_result = page.find_all("div", class_="hit-1fVM9e")        # Get the result of the search.
                if(len(search_result)>0):     # If there is a match.
                    for i in tqdm(range(len(search_result))):                 
                        dates = search_result[i].find_all("span", class_="timestamp-3ZCmNB")    # Get the date.
                        tt = self.clean_html(str(dates[0]))    # Clean the date.

                        if("Aujourd’hui" in tt):
                            tt = dt.strptime(today_date, "%d/%m/%Y")
                        elif("Hier" in tt):
                            tt = dt.strptime(yesterday_date, "%d/%m/%Y")
                        else:
                            tt = dt.strptime(tt, "%d/%m/%Y")

                        print(tt)

                        if((tt >= self.start_date) and (tt <= self.end_date)):    # If the search results date is between the start date and the end date.
                            container = self.driver.find_elements_by_class_name("jumpButton-JkYoYK")[i]        # html container that we want to get rid of.
                            self.driver.execute_script("arguments[0].style.display = 'inline';", container)    # Change its css display to none.

                            jump_word = self.driver.find_elements_by_class_name('jumpButton-JkYoYK')[i]         # find the jump button to open the conversation.
                            self.driver.execute_script("return arguments[0].scrollIntoView(true);", jump_word)  # Scroll into view.
                            jump_word.click()    # Click on the jump button
                            time.sleep(2)
                            scrape_message = ScrapeMessages.ScrapeMessages(self.driver, self.start_date, self.end_date, self.room_name)    # Scrape the conversation.
                            scrape_message.scrape()
                    if(tt < self.start_date):    # If a search result got a date < start_date then we start searching for the next key.
                        break

                    try:
                        next_page = self.driver.find_elements_by_class_name('paginationButton-3u4jo8')[1]   # Find the next button.
                        next_page.location_once_scrolled_into_view    # Scroll into view.
                        next_page.click()    # Click on the nex button.
                        time.sleep(5)

                    except:   # if there are no more pages, we start searching for the next key.
                        break    
                else:         # If there is no match, we start searching for the next key. 
                    break

if __name__ == "__main__":
    #   email = "ghassen1302@live.com"
    #   password = "Ghassen123"
    #   start_date = "01/07/2020"
    #   end_date = "02/07/2020"

    discord_login = Login()
    driver = discord_login.login_to_discord()
	
    while(1):
        try:
            start_date = dt.strptime(input('Start date (dd/mm/yyyy): '), "%d/%m/%Y")
            break
        except:
            print ("Wrong date")

    while(1):
        try:
            end_date = dt.strptime(input('End date (dd/mm/yyyy): '), "%d/%m/%Y")
            break
        except:
            print ("Wrong date")
  
    scrape_chosen_message = ScrapeChosenMessages(driver, start_date, end_date)
    scrape_chosen_message.scrape()
