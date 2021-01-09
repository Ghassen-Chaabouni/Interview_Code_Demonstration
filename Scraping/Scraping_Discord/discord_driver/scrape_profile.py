#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from bs4 import BeautifulSoup as soup
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys 
from IPython.display import display
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import re


# Scraping 

class ScrapeProfile:
    def __init__(self, driver, username, json_parser=False):

        '''
        Reads the value of driver, and username
        '''

        self.driver = driver
        self.username = username
        self.json_parser = json_parser
       
    def clean_html(self, raw_html):

        ''' 
        Remove any html tag.
        '''

        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext        
		
    def extract_image(self, data):
        final_data = []
        for i in range (len(data['profile_image'])):
            matches = re.search('src="([^"]+)"', data['profile_image'][i])
            final_data.append(matches[0][len('src="'):-1])  
  
        return final_data

    def extract_acc_name(self, data, account_type_text_x):    
	
        ''' 
        Extract the usernames of the other accounts (like Facebook username).
        This function returns a list of the usernames.
        '''

        final_data = []
        for i in range (len(data['info'])):
            account_name_list = (data['info'][i].split(','))     # account_name_list has this structure: [acc_type1, acc_name1, acc_type2, acc_name2, ... ]

            account_type=[]
            account_name=[]
            for j in range(0, len(account_name_list), 2):        # Get the types of the accounts.
                account_type.append(account_name_list[j])
            for j in range(1, len(account_name_list), 2):        # Get the names of the accounts.
                account_name.append(account_name_list[j])

            test = 0
            for j in range(len(account_type)):
                if(account_type_text_x in account_type[j]):
                    final_data.append(account_name[j].split('">')[1][:-len("</div>")])     # The account type is stored in a div tag.
                    test = 1
                    break
                    
            if(not test):
                final_data.append("")     # If there is no account name, we append 'No account name'.

        return final_data
		
    def extract_acc_link(self, data, acc_link_structure): 
	
        ''' 
        Extract the links of the accounts from column 'acc_link_info' (like a Facebook link).
        This function returns a list of the accounts corresponding to a 
        structure 'acc_link_structure'.
        '''

        acc_link = []
        for i in range (len(data['acc_link_info'])):
            account_link_list = (data['acc_link_info'][i].split(' '))
            acc_verif = 0
            for account_link in account_link_list:            # Search for an account link structure in account_link.
                if(acc_link_structure in account_link):       # If account link structure exists in account_link.
                    acc_link.append(account_link)             # Append the link to acc_link.
                    acc_verif = 1
                    break

            if (not acc_verif):         # If account link structure doesn't exist in account_link.
                acc_link.append("")     # Append 'No Account link' to acc_link.

        return acc_link
    
    def scrape(self):   

            ''' 
            Scrape the profile.
            '''   

            acc_link_info = []
            info = [] 
            profile_image = []
			
            try:
                search = self.driver.find_element_by_class_name("close-hZ94c6")   # Search for the close button of a pop up.
                search.click()     # Close the pop up.
            except:
                pass
			
            #time.sleep(3)
            timeout = 5

            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'searchBar-6Kv8R2'))
            WebDriverWait(self.driver, timeout).until(element_present)
            search = self.driver.find_element_by_class_name("searchBar-6Kv8R2")    # Search for the search box.
            search.click()    # Click on the search box.
			
            #time.sleep(2)
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'input-2VB9rf'))
            WebDriverWait(self.driver, timeout).until(element_present)
            search = self.driver.find_element_by_class_name("input-2VB9rf")        # Find the input box.
            search.send_keys("@" + self.username)     # Write the username.
			
            time.sleep(5)
            webdriver.ActionChains(self.driver).send_keys(Keys.ENTER).perform()    # Click on ENTER.
			
            #time.sleep(2)
            try:
                element_present = EC.presence_of_element_located((By.CLASS_NAME, 'cursorPonter-YEp76E'))
                WebDriverWait(self.driver, timeout).until(element_present)
                profile = self.driver.find_element_by_class_name('cursorPonter-YEp76E')    # Find the search result.
                profile.click()      # Click on the search result.

                element_present = EC.presence_of_element_located((By.CLASS_NAME, 'connectedAccountName-f8AEe2'))
                WebDriverWait(self.driver, timeout).until(element_present)
                profile_info_html = soup(self.driver.page_source, 'html.parser')   # Contains the html code of the name and the accounts.
                icon = (profile_info_html.find_all("img", class_="connectedAccountIcon-3P3V6F"))      # Get the types of the accounts.
                acc_name = (profile_info_html.find_all("div", class_="connectedAccountName-f8AEe2"))  # Get the usernames of the accounts. 
                acc_link = (profile_info_html.find_all("a", class_="anchor-3Z-8Bb"))                  # Get the links of the accounts.

                profile_image.append(str(profile_info_html.find_all("div", class_="avatar-3EQepX")[0]))
				
                if(len(acc_link)>0):  # Store the links of the accounts.
                    acc_link_info.append(acc_link)
                else:
                    acc_link_info.append("No links")

                if (len(icon)>0):    # Store the usernames and the types of the accounts.
                    x=[]
                    for j in range (len(icon)):
                        x=x+([icon[j], acc_name[j]])
                    info.append(x)
                else:
                    info.append("No info")

                webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()    # Click on ESCAPE.
                data = pd.DataFrame()
                data['name'] = [self.username]
                data['profile_image'] = profile_image
               
                data['role'] = ''
                data['info'] = info
                data['acc_link_info'] = acc_link_info

                data['info'] = data['info'].astype(str)
                data['acc_link_info'] = data['acc_link_info'].astype(str)
                data['acc_link_info'] = data['acc_link_info'].str.replace('href=','')
                data['acc_link_info'] = data['acc_link_info'].str.replace('"','')

                data['info'] = data['info'].str.replace(']','')
                data['info'] = data['info'].str.replace('[','')

                # Accounts links.
                data["steam_link"] = self.extract_acc_link(data, "https://steamcommunity.com/profiles/")
                data["twitch_link"] = self.extract_acc_link(data, "https://www.twitch.tv/")
                data["spotify_link"] = self.extract_acc_link(data, "https://open.spotify.com/user/")
                data["reddit_link"] = self.extract_acc_link(data, "https://www.reddit.com/u/")
                data["youtube_link"] = self.extract_acc_link(data, "https://www.youtube.com/channel/")

                # Accounts usernames.
                data["steam_name"] = self.extract_acc_name(data, "Steam")
                data["twitch_name"] = self.extract_acc_name(data, "Twitch")
                data["spotify_name"] = self.extract_acc_name(data, "Spotify")
                data["reddit_name"] = self.extract_acc_name(data, "Reddit")
                data["youtube_name"] = self.extract_acc_name(data, "YouTube")
                data["battle_net_name"] = self.extract_acc_name(data, "Battle.net")
                data["facebook_name"] = self.extract_acc_name(data, "Facebook")
                data["twitter_name"] = self.extract_acc_name(data, "Twitter")
                data["xbox_live_name"] = self.extract_acc_name(data, "Xbox")

                data['profile_image'] = self.extract_image(data)
				
                data = data.replace(',',';')
                data = data.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r", ","], value=["","", ";"], regex=True)
			
                # Rename two columns.
                data = data.rename(columns={'info': 'names_data', 'acc_link_info': 'links_data'})

                # Save the data.
                if(self.json_parser):
                    if(os.path.exists("./discord_data_profile.csv")):         # If an old dataset exists, we concatenate it with the new data.
                        data2 = pd.read_csv("./discord_data_profile.csv")
                        full_data = pd.concat([data2, data], axis=0)
                        full_data.to_csv("./discord_data_profile.csv", index=False)

                    else:   # Else, we create a new dataset.
                        data.to_csv("./discord_data_profile.csv", index=False)
                else:
                    data_json = {}
                    full_data = []
                    for i in range (len(data)):
                        data_json['name'] = data['name'].iloc[i]
                        data_json['profile_image'] = data['profile_image'].iloc[i]
                        data_json['names_data'] = data['names_data'].iloc[i]
                        data_json['links_data'] = data['links_data'].iloc[i]
                        data_json['steam_link'] = data['steam_link'].iloc[i]
                        data_json['twitch_link'] = data['twitch_link'].iloc[i]
                        data_json['spotify_link'] = data['spotify_link'].iloc[i]
                        data_json['reddit_link'] = data['reddit_link'].iloc[i]
                        data_json['youtube_link'] = data['youtube_link'].iloc[i]
                        data_json['steam_name'] = data['steam_name'].iloc[i]
                        data_json['twitch_name'] = data['twitch_name'].iloc[i]
                        data_json['spotify_name'] = data['spotify_name'].iloc[i]
                        data_json['reddit_name'] = data['reddit_name'].iloc[i]
                        data_json['youtube_name'] = data['youtube_name'].iloc[i]
                        data_json['battle_net_name'] = data['battle_net_name'].iloc[i]
                        data_json['facebook_name'] = data['facebook_name'].iloc[i]
                        data_json['twitter_name'] = data['twitter_name'].iloc[i]
                        data_json['xbox_live_name'] = data['xbox_live_name'].iloc[i]

                        full_data.append(data_json)
                        data_json = {}
                    return full_data
            except:
                print('***Error***')

            
			
