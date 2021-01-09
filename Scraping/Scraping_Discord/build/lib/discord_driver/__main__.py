#!/usr/bin/env python
# coding: utf-8

import discord_driver.scrape_rooms as ScrapeRooms
import discord_driver.login as Login
import discord_driver.clean_data as CleanData
		
import sys
import click

@click.command()
@click.option('--email', default="", help='Your account email.')
@click.option('--password', default="", help='Your password')
@click.option('--game_name', default="", help='The game name')
@click.option('--start_date', default="", help='The starting date of the messages to scrape.')
@click.option('--end_date', default="", help='The last date of the messages to scrape.')
@click.option('--keys', '-k', multiple=True, default=[], help='A list of words that we are searching in the conversations.')
def main(email, password, game_name, start_date, end_date, keys):

    ''' 
    Scraping conversations in discord based on two dates and the words that we are searching for.
    In case of no email or no password or no game_name or no dates are entered, config.json file is used.
    In case of no keys are entered, words_data.txt is used.
    '''
	
    keys = list(keys)    
    if ((len(email) > 0) and (len(password) > 0) and (len(game_name) > 0) and (len(start_date) > 0) and (len(end_date) > 0)):   # If email, password, game_name, start_date and end_date are specified.
        click.echo('reading from arguments')
        click.echo('Login...')
        login = Login.Login(email, password)    # Login to Discord.
        driver = login.login_to_discord()
        
        click.echo('Scraping...')
        if(len(keys) == 1):     # If there is one word specified.
            scraper = ScrapeRooms.ScrapeRooms(driver, game_name, start_date, end_date, keys[0])   
        elif(len(keys) > 1):    # If there is more than one word specified.
            scraper = ScrapeRooms.ScrapeRooms(driver, game_name, start_date, end_date, keys)       
        else:                   # If there are no words specified, words_date.txt is used.
            scraper = ScrapeRooms.ScrapeRooms(driver, game_name, start_date, end_date)       
        scraper.scrape()        # Start scraping.
		
        click.echo('Cleaning...')
        clean_data = CleanData.CleanData()     # Clean data.
        clean_data.clean_data_function()
    else:        # If email or password or game_name or start_date or end_date aren't specified, config.json is used.
        click.echo('reading from config.json')
        click.echo('Login...')
        login = Login.Login()      # Login to Discord.
        driver = login.login_to_discord()   
		
        click.echo('Scraping...')
        if(len(keys) == 1):     # If there is one word specifed.        
            scraper = ScrapeRooms.ScrapeRooms(driver, game_name, start_date, end_date, keys[0])
        elif(len(keys) > 1):    # If there is more than one word specified.
            scraper = ScrapeRooms.ScrapeRooms(driver, game_name, start_date, end_date, keys)
        else:                   # If there are no words specified, words_date.txt is used
            scraper = ScrapeRooms.ScrapeRooms(driver, game_name, start_date, end_date)
        scraper.scrape()        # Start scraping.
		
        click.echo('Cleaning...')
        clean_data = CleanData.CleanData()     # Clean data.
        clean_data.clean_data_function()

	
	
	






