#!/usr/bin/env python
# coding: utf-8


# Search for a game

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import discord_driver.scrape_chosen_messages as ScrapeChosenMessages
import discord_driver.login as Login
from datetime import datetime as dt
from bs4 import BeautifulSoup as soup
import json 
import os, sys
import re

class ScrapeRooms:
    def __init__(self, driver, game = "", start_date = "", end_date = "", key = ""):

        '''
        Reads "start_date_(dd/mm/yyyy)", "end_date_(dd/mm/yyyy)" and "game_name" 
        values from config.json file or from the function inputs. Also, reads the value of the driver.
        '''

        self.driver = driver 
        self.key = key
        if(len(game)>0 and len(start_date)>0 and len(end_date)>0):    # If game, start_date and end_date are specified.
            self.game = game
            self.start_date = dt.strptime(start_date, "%d/%m/%Y")
            self.end_date = dt.strptime(end_date, "%d/%m/%Y")
            f = open(self.determine_path () + '/config/config.json',)     # Open config.json
            data = json.load(f)          # Load the configurations from config.json
            data['game_name'] = game     # Store the new game name.
            data['start_date_(dd/mm/yyyy)'] = start_date   # Store the new start date.
            data['end_date_(dd/mm/yyyy)'] = end_date       # Store the new end date.
            f.close()		
            
            with open(self.determine_path () + '/config/config.json', 'w', encoding='utf-8') as f:    # Save the new data in config.json
                json.dump(data, f, ensure_ascii=False, indent=4)
	
        else:		# If game or start_date or end_date aren't specified, we use the configurations from config.json
            f = open(self.determine_path () + '/config/config.json',)    # Open config.json
            data = json.load(f)        # Load the configurations from config.json
		
            self.start_date = dt.strptime(data['start_date_(dd/mm/yyyy)'], "%d/%m/%Y")   # Store the start_date.
            self.end_date = dt.strptime(data['end_date_(dd/mm/yyyy)'], "%d/%m/%Y")       # Store the end_date.

            self.game = data['game_name']    # Store the game name.

            f.close() 		

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
			
    def clean_html(self, raw_html):

        ''' 
        Remove any html tag.
        '''

        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext 
			
    def scrape(self):

        ''' 
        Search for a game and opens the discord's rooms.
        '''

        self.driver.get("https://discord.com/guild-discovery")     # Open search discord channel.
        time.sleep(5)
        search = self.driver.find_element_by_class_name('inputDefault-_djjkz')    # Find the input box.
        search.send_keys(self.game)     # Type the game name.
        webdriver.ActionChains(self.driver).send_keys(Keys.ENTER).perform()       # Press enter.
        time.sleep(5)

        # open a chat group

        group = self.driver.find_elements_by_class_name('card-Lnpy-k')    # Find the containers of the rooms. 
        while(1):
            for i in range (len(group)):
                
                self.driver.execute_script("return arguments[0].scrollIntoView(true);", group[i])    # Scroll into view.

                page = soup(self.driver.page_source, 'html.parser')         # Get the html code.
                room_name = page.find_all("h3", class_="name-2S4ebg")[0]    # Get the room name.
                print('room name = ' + self.clean_html(str(room_name)))

                group[i].click()    # Click on the room.
                time.sleep(10)
                try:
                    close = self.driver.find_element_by_class_name('close-hZ94c6')    # Find the close button of a pop up.
                    close.click()    # Close the pop up.
                    time.sleep(3)
                except:
                    pass
				
                try:
                    join = self.driver.find_elements_by_class_name("button-2PWmas")[1]    # Find the join button.
                    join.click()    # Click on the join button.
                    time.sleep(3)
                    try:
                        close = self.driver.find_elements_by_class_name("sizeMedium-1AC_Sl")[0]    # find a button to close a pop up.
                        close.click()    # click on the button.
                        time.sleep(3)
                    except:
                        pass
                except:
                    pass

                scrape_chosen_message = ScrapeChosenMessages.ScrapeChosenMessages(self.driver, self.start_date, self.end_date, room_name, self.key)   # Search for words and scrape conversations
                scrape_chosen_message.scrape()
                
                back = self.driver.find_element_by_class_name("back-1Ess-_")    # Find the back button to return to the rooms search.
                back.click()    # Click on the back button.
                time.sleep(3)

                group = self.driver.find_elements_by_class_name('card-Lnpy-k')    # Reload the rooms list.

            try:
                next_page = self.driver.find_elements_by_class_name('endButtonInner-7u9q7X')[1]       # Find the next page button.
                self.driver.execute_script("return arguments[0].scrollIntoView(true);", next_page)    # Scroll into view.
                next_page.click()    # Click on the next button.
                time.sleep(3)
                group = self.driver.find_elements_by_class_name('card-Lnpy-k')    # Reload the rooms list.
            except:
                break

if __name__ == "__main__":
    #   email = "ghassen1302@live.com"
    #   password = "Ghassen123"
    #   start_date = "01/07/2020"
    #   end_date = "02/07/2020"

    discord_login = Login()
    driver = discord_login.login_to_discord()
    
    scrape_rooms = ScrapeRooms(driver)
    scrape_rooms.scrape()
