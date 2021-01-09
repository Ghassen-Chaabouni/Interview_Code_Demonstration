from .clean_data import CleanData
from .login import Login
from .scrape_chosen_messages import ScrapeChosenMessages
from .scrape_messages import ScrapeMessages
from .scrape_rooms import ScrapeRooms
from .scrape_profile import ScrapeProfile

from abc import ABC
import json
import os, sys

__version__ = '1.0.0'
		
from abc import ABC
class Driver(ABC):

    def get_user_info(self, user, **kwargs):
        pass
    
    def get_posts_from_key(self, key, **kwargs):
        pass
    
    def get_posts_from_keys(self, list_key, **kwargs):
        pass
		
class DiscordDriver(Driver):
    def get_user_info(self, user, **kwargs):

        '''
        Uses the username and returns informations about the user.
        Parameters are otional if they aren't specified config.json is used		
        '''

        if len(kwargs) == 0:   # If there are no parameters specified, config.json is used.
            f = open(self.determine_path () + '/config/config.json',)   # Determinate the path of config.json and opens it.
            data = json.load(f)            # Load the data from config.json
            f.close()     
            email = data['email']          # Store the email.
            password = data['password']    # Store the password.

        else:    # If there are parameters specified.
            for dict in kwargs.values(): 
                for key in dict.keys(): 
                    if (key == 'email'):
                        email = dict[key]       # Store the email.
                    elif (key == 'password'):
                        password = dict[key]    # Store the password.

        login = Login(email, password)          # Login to Discord.
        driver = login.login_to_discord()       

        scrape = ScrapeProfile(driver, user)    # Start scraping the user profile.
        scrape.scrape()
        
        
    def get_posts_from_key(self, key, **kwargs):

        '''
        Uses a keyword and returns the posts that contains it.
        Parameters are optional. If they aren't specified config.json is used		
        '''

        if len(kwargs) == 0:     # If there are no parameters specified, config.json is used.
            f = open(self.determine_path () + '/config/config.json',)    # Determinate the path of config.json and opens it.
            data = json.load(f)              # Load the configurations from config.json
            f.close()     
            game_name = data['game_name']    # Store the game name.
            email = data['email']            # Store the email.
            password = data['password']      # Store the password.
            start_date = data['start_date_(dd/mm/yyyy)']    # Store the start scraping date.
            end_date = data['end_date_(dd/mm/yyyy)']        # Store the last scraping date.
            
        else:   # If they are parameters specified.
            for dict in kwargs.values(): 
                for x in dict.keys(): 
                    if (x == 'email'):
                        email = dict[x]           # Store the email.
                    elif (x == 'password'):
                        password = dict[x]        # Store the password.
                    elif (x == 'game_name'):      
                        game_name = dict[x]       # Store the game name.
                    elif (x == 'start_date'):     
                        start_date = dict[x]      # Store the start scraping date.
                    elif (x == 'end_date'):     
                        end_date = dict[x]        # Store the last scraping date.

        login = Login(email, password)         # Login to Discord.
        driver = login.login_to_discord()

        scraper = ScrapeRooms(driver, game_name, start_date, end_date, key)     # Start scraping the posts.
        scraper.scrape()
         
    def get_posts_from_keys(self, list_key, **kwargs):
	
        '''
        Uses a list of keywords and returns posts that contains them.
        Parameters are optional. If they aren't specified config.json is used.		
        '''
		
        if len(kwargs) == 0:       # If there are no parameters specified, config.json is used.
            f = open(self.determine_path () + '/config/config.json',)        # Determinate the path of config.json and opens it.
            data = json.load(f)               # Load the configurations from config.json
            f.close()     
            game_name = data['game_name']     # Store the game name.
            email = data['email']             # Store the email.
            password = data['password']       # Store the password.
            start_date = data['start_date_(dd/mm/yyyy)']     # Store the start scraping date.
            end_date = data['end_date_(dd/mm/yyyy)']         # Store the last scraping date.
            
        else:        # If they are parameters specified.
            for dict in kwargs.values(): 
                for key in dict.keys(): 
                    if (key == 'email'):
                        email = dict[key]            # Store the email.
                    elif (key == 'password'): 
                        password = dict[key]         # Store the password.
                    elif (key == 'game_name'): 
                        game_name = dict[key]        # Store the game name.
                    elif (key == 'start_date'):
                        start_date = dict[key]       # Store the start scraping date.
                    elif (key == 'end_date'):
                        end_date = dict[key]         # Store the last scraping date.
               
        login = Login(email, password)           # Login to Discord.
        driver = login.login_to_discord()

        scraper = ScrapeRooms(driver, game_name, start_date, end_date, list_key)    # Start scraping the posts.
        scraper.scrape()	
	
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
	