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
    def __init__(self, driver, context_data, json_parser, start_date, end_date, room_name):

        '''
        Reads the value of driver, start_date, end_date and room_name.
        '''

        self.driver = driver
        self.start_date = start_date
        self.end_date = end_date
        self.room_name = room_name
        self.json_parser = json_parser
        self.context_data = context_data
                   
				   
    def extract_acc_link(self, data, acc_link_structure): 
	
        ''' 
        Extract the accounts links from the column 'acc_link_info' (like a Facebook link).
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

            if (not acc_verif):         # If account link structure doesn't exists in account_link.
                acc_link.append("No Account link")     # Append 'No Account link' to acc_link.

        return acc_link
    
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

    def extract_message(self, data):
	
        ''' 
        Extract the messages from the column "message". 
        This function returns a list of the messages.
        '''

        final_data = []
        for i in range (len(data['message'])):
            mess = self.clean_html(data['message'][i])     # Remove html tags.
            if(len(mess)>0):             
                final_data.append(mess)
            else:
                final_data.append("No message")
        
        return final_data
    
    def extract_role(self, data):
	
        ''' 
        Extract the roles from the column "role" 
        This function returns a list of the roles.
        '''

        final_data = []
        for i in range (len(data['role'])):
            role = self.clean_html(data['role'][i])      # Remove html tags.
            if(len(role)>0):
                final_data.append(role)
            else:
                final_data.append("No role")
        
        return final_data
    
    
    def extract_time(self, data):
	
        ''' 
        Extract the message time from the column "time" 
        This function returns a list of the times.
        '''

        final_data = []
        today_date = dt.today().strftime("%d/%m/%Y")    # Get today's date.
        yesterday_date = (dt.today() - timedelta(days=1)).strftime("%d/%m/%Y")   # Get yesterday's date.
        for i in range (len(data['time'])):
            tt = self.clean_html(data['time'][i])       # Remove html tags.
            if("Aujourd’hui" in tt):
                tt = today_date          # Change 'Aujourd’hui' to a dd/mm/yyyy representation. 
            elif("Hier" in tt):
                tt = yesterday_date      # Change 'Hier' to a dd/mm/yyyy representation.

            final_data.append(tt)
			       
        return final_data
    
    def extract_names(self, data):
	
        ''' 
        Extract the discord's accounts names from the column "name" 
        This function returns a list of the names.
        '''

        final_data = []
        for i in range (len(data['name'])):
            final_data.append(self.clean_html(data['name'][i]))   # Remove html tags.
        
        return final_data
		
    def extract_room_name(self, data):
	
        ''' 
        Extract the discord's rooms names from the column "room_name" 
        This function returns a list of the room names.
        '''

        final_data = []
        for i in range (len(data['room_name'])):
            room_name = self.clean_html(data['room_name'][i])   # Remove html tags.
            if(len(room_name)>0):
                final_data.append(room_name)
            else:
                final_data.append("No room name")
        
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
            for j in range(0, len(account_name_list), 2):        # Get the accounts types.
                account_type.append(account_name_list[j])
            for j in range(1, len(account_name_list), 2):        # Get the accounts names.
                account_name.append(account_name_list[j])

            test = 0
            for j in range(len(account_type)):
                if(account_type_text_x in account_type[j]):
                    final_data.append(account_name[j].split('">')[1][:-len("</div>")])     # The account type is stored in a div tag.
                    test = 1
                    break
                    
            if(not test):
                final_data.append("No account name")     # If there is no account name, we append 'No account name'.

        return final_data
    
    def clean_data_function(self, data):

        ''' 
        Clean the data from "discord_data_uncleaned.csv".
        This function creates a cleaned DataFrame called "discord_data.csv".
        '''

        # Change the data type to String.
        data['message'] = data['message'].astype(str)
        data['name'] = data['name'].astype(str)
        data['time'] = data['time'].astype(str)
        data['room_name'] = data['room_name'].astype(str)
        data['profile_image'] = data['profile_image'].astype(str)

        data['role'] = data['role'].astype(str)
        data['info'] = data['info'].astype(str)
        data['acc_link_info'] = data['acc_link_info'].astype(str)

        # Cleaning the data.
        data['role'] = data['role'].str.replace('[','')
        data['role'] = data['role'].str.replace(']','')

        data['acc_link_info'] = data['acc_link_info'].str.replace('href=','')
        data['acc_link_info'] = data['acc_link_info'].str.replace('"','')
        
        data['info'] = data['info'].str.replace(']','')
        data['info'] = data['info'].str.replace('[','')

        # To avoid an error, I removed the row that causes it.
        for i in range (len(data['acc_link_info'])):
            try:
                l=data['acc_link_info'][i].split(',')
            except:
                data = data.drop(data.index[[i]])
                data = data.reset_index(drop=True)
                
        # Extract message.
        data["message"] = self.extract_message(data)
    
        # Extract role.
        data["role"] = self.extract_role(data)
        
        # Extract time.
        data["time"] = self.extract_time(data)
    
        # Extract discord names.
        data["name"] = self.extract_names(data)
		
        # Extract room name.
        data["room_name"] = self.extract_room_name(data)
		
        # Extract Accounts links.
        data["steam_link"] = self.extract_acc_link(data, "https://steamcommunity.com/profiles/")
        data["twitch_link"] = self.extract_acc_link(data, "https://www.twitch.tv/")
        data["spotify_link"] = self.extract_acc_link(data, "https://open.spotify.com/user/")
        data["reddit_link"] = self.extract_acc_link(data, "https://www.reddit.com/u/")
        data["youtube_link"] = self.extract_acc_link(data, "https://www.youtube.com/channel/")

        # Extract Accounts usernames.
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

        data.drop_duplicates(keep='first', inplace=True)  # Remove duplicates
        data = data.reset_index(drop=True)                # Reset index of the dataframe

        return data
			
    
    def store_data(self, message, name, time_info, role, info, acc_link_info, profile_image): 
	
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
        data['profile_image'] = profile_image
        
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
            profile_image = []
            k = 0
        
            time.sleep(5)
                       
            l = (self.driver.find_elements_by_class_name("contents-2mQqc9"))  # Get the messages containers.
            today_date = dt.today().strftime("%d/%m/%Y")
            yesterday_date = (dt.today() - timedelta(days=1)).strftime("%d/%m/%Y")
            
            profile_info_html = soup(self.driver.page_source, 'html.parser')     # Get the html code.
                    
            for i in range((len(l))):

                    try:   # Remove a html code that interferes with the scraping procedure.
                        container = self.driver.find_element_by_class_name("newMessagesBar-265mhP")      # html container that we want to get rid of.
                        self.driver.execute_script("arguments[0].style.display = 'none';", container)    # Change its css display to none.
                    except:
                        pass
                    
                    
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
                        message.append(str(profile_info_html.find_all("div", class_="messageContent-2qWWxC")[i]))    # Get the message.
 
                    except:
                        try:
                            message[k-1] = message[k-1] + "; " + (str(profile_info_html.find_all("div", class_="messageContent-2qWWxC")[i]))    # Get the message.
                            print('*****************')
                            print(message[k-1])
                            print('*****************')
                        except:
                            continue
                        continue

                    time_info.append(str(profile_info_html.find_all("span", class_="timestamp-3ZCmNB")[i]))    # Get the time of the message.
					
                    try:   # Remove a html code that interferes with the scraping procedure.
                        container = self.driver.find_element_by_class_name("newMessagesBar-265mhP")      # html container that we want to get rid of.
                        self.driver.execute_script("arguments[0].style.display = 'none';", container)    # Change its css display to none.
                    except:
                        pass
					
                    time.sleep(1)
                    try:    
                        link.click()    # Click on the name of the person who wrote the message.
                    except:
                        time_info.pop()
                        message.pop()
                        break
                           
                    profile_info_html2 = soup(self.driver.page_source, 'html.parser')   # Contains the html code of the roles.

                    try:   # Get the roles of the person who wrote the message.
                        role.append(profile_info_html2.find_all("div", class_="roleName-32vpEy"))    
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

                    profile_info_html2 = soup(self.driver.page_source, 'html.parser')   # Contains the html code of the name and the accounts. 

                    icon = (profile_info_html2.find_all("img", class_="connectedAccountIcon-3P3V6F"))      # Get the accounts types.
                    acc_name = (profile_info_html2.find_all("div", class_="connectedAccountName-f8AEe2"))  # Get the usernames of the accounts. 
                    acc_link = (profile_info_html2.find_all("a", class_="anchor-3Z-8Bb"))     					# Get the accounts links.
                    
                    try:
                        profile_image.append(str(profile_info_html2.find_all("div", class_="avatar-3EQepX")[0]))
                    except:
                        profile_image.append("")

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

                    try:
                        name.append(str(profile_info_html2.find_all("span", class_="username-2b1r56")[0]))    # Get the discord name.
                    except:
                        name.append('')

                    webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()    # Close the pop up.
                    time.sleep(3)

                    print ("name = " + self.clean_html(str(name[k])))
                    print ("message = " + self.clean_html(str(message[k])))
                    print ("role = " + self.clean_html(str(role[k])))
                    print ("accounts = " + self.clean_html(str(info[k])))
                    print ("time = " + self.clean_html(str(time_info[k])))
                    print ("profile image = " + profile_image[k])
                    print ("--------------------------------")
                    k=k+1
                                               
            if(self.json_parser):											   
                self.store_data(message, name, time_info, role, info, acc_link_info, profile_image)     # Store the data in discord_data_uncleaned.csv
            else:
                data = pd.DataFrame()
                data['message'] = message
                data['name'] = name
                data['time'] = time_info
                data['room_name'] = [self.room_name] * len(time_info)
                data['role'] = role
                data['info'] = info
                data['acc_link_info'] = acc_link_info
                data['profile_image'] = profile_image
                data = self.clean_data_function(data)

                data_json_context = {}
                data_json_context['name'] = self.context_data[0]
                data_json_context['image'] = self.context_data[1]
                data_json_context['time'] = self.context_data[2]
                data_json_context['message'] = self.context_data[3]

                data_json = {}
                full_data_json = []
                for i in range (len(data)):
                    data_json['message'] = data['message'].iloc[i]
                    data_json['name'] = data['name'].iloc[i]
                    data_json['time'] = data['time'].iloc[i]
                    data_json['room_name'] = data['room_name'].iloc[i]
                    data_json['role'] = data['role'].iloc[i]
                    data_json['names_data'] = data['names_data'].iloc[i]
                    data_json['links_data'] = data['links_data'].iloc[i]
                    data_json['profile_image'] = data['profile_image'].iloc[i]
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

                    full_data_json.append(data_json)
                    data_json = {}

                data_json_context['context'] = full_data_json
                return data_json_context
            
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