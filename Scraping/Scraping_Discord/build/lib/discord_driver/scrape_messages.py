#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from bs4 import BeautifulSoup as soup
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys 
import os.path
import re
from datetime import datetime as dt
from datetime import timedelta
import discord_driver.login as Login


class ScrapeMessages:
    def __init__(self, driver, start_date, end_date, room_name):

        '''
        Reads the value of driver, start_date, end_date and room_name.
        '''

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
    
    def store_data(self, message, name, time_info, role, info, acc_link_info): 
	
        ''' 
        Store the data in a csv file called discord_data_uncleaned.csv.
        If the file exists, it uses the old one and concatinates it with the new data.
        '''

        data = pd.DataFrame()
        data['message'] = message
        data['name'] = name
        data['time'] = time_info
        data['room_name'] = [self.room_name] * len(time_info)
        data['role'] = role
        data['info'] = info
        data['acc_link_info'] = acc_link_info
        
        # Save the data.
        if(os.path.exists("./discord_data_uncleaned.csv")):   # If an old dataset exists, we concatenate it with the new data.
            data2 = pd.read_csv("./discord_data_uncleaned.csv")
            full_data = pd.concat([data2, data], axis=0)
            full_data.to_csv("./discord_data_uncleaned.csv", index=False)

        else:   # Else, we create a new dataset.
            data.to_csv("./discord_data_uncleaned.csv", index=False)
        
    
    def scrape(self):   

            ''' 
            Scrape the conversations.
            '''   

            acc_link_info = []
            info = [] 
            name = []
            message = []
            role = []
            time_info = []
            k = 0
        
            time.sleep(5)
                       
            l = (self.driver.find_elements_by_class_name("contents-2mQqc9"))  # Get the messages containers.
            today_date = dt.today().strftime("%d/%m/%Y")
            yesterday_date = (dt.today() - timedelta(days=1)).strftime("%d/%m/%Y")
            for i in range((len(l))):

                    try:   # Remove a html code that interferes with the scraping procedure.
                        container = self.driver.find_element_by_class_name("newMessagesBar-mujexs")      # html container that we want to get rid of.
                        self.driver.execute_script("arguments[0].style.display = 'none';", container)    # Change its css display to none.
                    except:
                        pass
                    
                    profile_info_html = soup(self.driver.page_source, 'html.parser')     # Get the html code.
               
                    try:
                        tt = self.clean_html(str(profile_info_html.find_all("span", class_="timestamp-3ZCmNB")[i]))    # Get the time.
                        if("Aujourd’hui" in tt):
                            tt = today_date
                        if("Hier" in tt):
                            tt = yesterday_date

                        tt = dt.strptime(tt, "%d/%m/%Y")
                        tt_copy = tt
                       
                    except:
                        tt = tt_copy     # If there is an error, we store the last date.
                        
                    try:  
                        link = l[i].find_elements_by_class_name("username-1A8OIy")[0]   # Get the profile link.
                        link.location_once_scrolled_into_view     # Scroll into view.
                        profile_info_html = soup(self.driver.page_source, 'html.parser')     # Get the html code.
                        message.append(str(profile_info_html.find_all("div", class_="messageContent-2qWWxC")[i]))    # Get the message.

                    except:
                        message[k-1] = message[k-1] + "; " + (str(profile_info_html.find_all("div", class_="messageContent-2qWWxC")[i]))    # Get the message.
                        print(message[k-1])
                        continue
                            
                    profile_info_html = soup(self.driver.page_source, 'html.parser')     # Get the html code.

                    time_info.append(str(profile_info_html.find_all("span", class_="timestamp-3ZCmNB")[i]))    # Get the time of the message.
                        
                    time.sleep(1)
                    try:    
                        link.click()    # Click on the name of the person who wrote the message.
                    except:
                        time_info.pop()
                        message.pop()
                        break
                           
                    profile_info_html = soup(self.driver.page_source, 'html.parser')   # Contains the html code of the roles.

                    try:   # Get the roles of the person who wrote the message.
                        role.append(profile_info_html.find_all("div", class_="roleName-32vpEy"))    
                    except:
                        role.append("No role")

                    time.sleep(3)

                    try:
                        profile_pic_link = '/html/body/div/div[6]/div/div/div/div[1]/div/div[1]/div'
                        self.driver.find_elements_by_xpath(profile_pic_link)[0].click()    # Click on the picture to open the profile.
                    except:    # If there is an error, we pop what we scraped last and then we scrape the next message.
                        role.pop()
                        time_info.pop()
                        message.pop()
                        continue

                    time.sleep(3)

                    profile_info_html = soup(self.driver.page_source, 'html.parser')   # Contains the html code of the name and the accounts. 

                    icon = (profile_info_html.find_all("img", class_="connectedAccountIcon-3P3V6F"))      # Get the accounts types.
                    acc_name = (profile_info_html.find_all("div", class_="connectedAccountName-f8AEe2"))  # Get the usernames of the accounts. 
                    acc_link = (profile_info_html.find_all("a", class_="anchor-3Z-8Bb"))                  # Get the accounts links.

                    if(len(acc_link)>0):  # Get the accounts links.
                        acc_link_info.append(acc_link)
                    else:
                        acc_link_info.append("No links")

                    if (len(icon)>0):    # Get the usernames of the accounts and the accounts types.
                        x=[]
                        for j in range (len(icon)):
                            x=x+([icon[j], acc_name[j]])
                        info.append(x)
                    else:
                        info.append("No info")

                    name.append(str(profile_info_html.find_all("span", class_="username-2b1r56")[0]))    # Get the discord name.

                    webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()    # Close the pop up.
                    time.sleep(3)

                    print ("name = " + self.clean_html(str(name[k])))
                    print ("message = " + self.clean_html(str(message[k])))
                    print ("role = " + self.clean_html(str(role[k])))
                    print ("accounts = " + self.clean_html(str(info[k])))
                    print ("time = " + self.clean_html(str(time_info[k])))
                    print ("--------------------------------")
                    k=k+1
                                                      
            self.store_data(message, name, time_info, role, info, acc_link_info)     # Store the data in discord_data_uncleaned.csv
            
            
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
    
    ScrapeMessage = ScrapeMessages(driver, start_date, end_date)
    ScrapeMessage.scrape()
