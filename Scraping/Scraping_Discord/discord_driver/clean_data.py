#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from bs4 import BeautifulSoup as soup
import os.path
import re
from datetime import datetime as dt
from datetime import timedelta 

class CleanData:
    
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
    
    def clean_data_function(self):

        ''' 
        Clean the data from "discord_data_uncleaned.csv".
        This function creates a cleaned DataFrame called "discord_data.csv".
        '''

        data = pd.read_csv("./discord_data_uncleaned.csv")

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

        # Save the data.
        if(os.path.exists("./discord_data.csv")):         # If an old dataset exists, we concatenate it with the new data.
            data2 = pd.read_csv("./discord_data.csv")
            full_data = pd.concat([data2, data], axis=0)
            full_data.to_csv("./discord_data.csv", index=False)

        else:   # Else, we create a new dataset.
            data.to_csv("./discord_data.csv", index=False)


if __name__ == "__main__":
    data = CleanData()
    data.clean_data_function()
