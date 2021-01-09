#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import json
import os, sys


# Login 

class Login:
    def __init__(self, email="", password=""):

        '''
        Reads "email" and "password" values from config.json file or from the function inputs.
        '''
        
        if(len(email)>0 and len(password)>0):     # If email and password are entered.
            self.email = email
            self.password = password
            f = open(self.determine_path () + '/config/config.json',)    # Open config.json
            data = json.load(f)
            data['email'] = self.email            # Store the email.
            data['password'] = self.password      # Store the password.
            f.close()		
            
            with open(self.determine_path () + '/config/config.json', 'w', encoding='utf-8') as f:    # Save the new configurations to config.json
                json.dump(data, f, ensure_ascii=False, indent=4)
	
        else:		  # If email and password aren't entered, config.json is used.
            f = open(self.determine_path () + '/config/config.json',)    # Open config.json
            data = json.load(f)     

            self.email = data['email']            # Load the email.
            self.password = data['password']      # Load the password.

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
			
    def login_to_discord(self):
        '''
        Login to discord account.
        '''
#         chrome_options = webdriver.ChromeOptions()
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--window-size=1366,768')
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--disable-gpu')
#         driver = webdriver.Chrome(chrome_options=chrome_options)

        options = webdriver.firefox.options.Options()
        options.headless = True
 
        driver = webdriver.Firefox(options=options, executable_path=self.determine_path () + '/config/geckodriver')    # Open Firefox webdriver.
        driver.set_window_position(0, 0)
        driver.set_window_size(1229, 1200)
		
        driver.get("https://discord.com/login")    # Open discord login.

        b = 0
        while(not b):    # Wait until the login page is loaded.
            try:
                user_html = driver.find_element_by_name("email")
                pass_html = driver.find_element_by_name("password")
                b = 1
            except:
                time.sleep(1)

        user_html.send_keys(self.email)       # Type the email.
        pass_html.send_keys(self.password)    # Type the password.

        webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()    # Press ENTER.
        time.sleep(15)
        
        return driver

if __name__ == "__main__":
    #   email = "ghassen1302@live.com"
    #   password = "Ghassen123"

    discord_login = Login()
    driver = discord_login.login_to_discord()

