#!/usr/bin/env python
# coding: utf-8

import store_elasticsearch.connect_elasticsearch as  ConnectElasticsearch
import store_elasticsearch.create_index as  CreateIndex 
import store_elasticsearch.store_row as  StoreRow
import json
import sys
import os
from tqdm import tqdm
import csv

class StoreDiscordDriver:
    def __init__(self, company_name, host="localhost", port=9200):
	
        ''' 
        Reads the value of the company_name.
        '''	

        self.company_name = str(company_name)
        self.host = host
        self.port = port

    def process_data(self):
        csvfile = open(self.determine_path () + '/config/discord_data.csv', 'r', encoding="utf8")
        jsonfile = open(self.determine_path () + '/config/discord_data.json', 'w', encoding="utf8")

        fieldnames = ("message", "name", "time", "room_name", "role", "names_data", "links_data", "steam_link",
                      "twitch_link", "spotify_link", "reddit_link", "youtube_link", "steam_name", "twitch_name",
                      "spotify_name", "reddit_name", "youtube_name", "battle_net_name", "facebook_name", "twitter_name",
                      "xbox_live_name")

        reader = csv.DictReader(csvfile, fieldnames)
        out = json.dumps([row for row in reader])
        jsonfile.write(out)
		
    def discord_driver_settings(self):
	
        ''' 
        The settings required to store the discord data in Elasticsearch.
        '''	
	
        index_name = self.company_name + "-discord-driver"
        print('index: ' + index_name)
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                index_name: {
                    "dynamic": "strict",
                    "properties": {
                        "message": {
                            "type": "text"
                        },
                        "name": {
                            "type": "text"
                        },
                        "time": {
                            "type": "text"
                        },
                        "room_name": {
                            "type": "text"
                        },
                        "role": {
                            "type": "text"
                        },
                        "names_data": {
                            "type": "text"
                        },
                        "links_data": {
                            "type": "text"
                        },
                        "steam_link": {
                            "type": "text"
                        },
                        "twitch_link": {
                            "type": "text"
                        },
                        "spotify_link": {
                            "type": "text"
                        },
                        "reddit_link": {
                            "type": "text"
                        },
                        "youtube_link": {
                            "type": "text"
                        },
                        "steam_name": {
                            "type": "text"
                        },
                        "twitch_name": {
                            "type": "text"
                        },
                        "spotify_name": {
                            "type": "text"
                        },
                        "reddit_name": {
                            "type": "text"
                        },
                        "youtube_name": {
                            "type": "text"
                        },
                        "battle_net_name": {
                            "type": "text"
                        },
                        "facebook_name": {
                            "type": "text"
                        },
                        "twitter_name": {
                            "type": "text"
                        },
                        "xbox_live_name": {
                            "type": "text"
                        }
                    }
               }
            }
        }

        return settings, index_name

    def store_discord_driver(self):
	
        ''' 
        Store discord data in Elasticsearch.
        '''	

        self.process_data()

        connectElasticsearch = ConnectElasticsearch.ConnectElasticsearch(self.host, self.port)    # Connect to Elasticsearch.
        es_object = connectElasticsearch.connect_elasticsearch()

        settings, index_name = self.discord_driver_settings()   # Get the settings.
        
        createIndex = CreateIndex.CreateIndex(es_object, index_name, settings)   # Create an index.
        created = createIndex.create_index()
        
        with open(self.determine_path () + "/config/discord_data.json", 'r') as handle:   # Load the data discord_data.json
            parsed = json.load(handle)
        
        _type = "data"
        storeRow = StoreRow.StoreRow(es_object, index_name, _type)     # Store the data in Elasticsearch
        for i in tqdm(range(len(parsed))):  # Store each row.
            storeRow.store_row(parsed[i])
	
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

    
if __name__ == '__main__':
    storeDiscordDriver = StoreDiscordDriver('test')
    storeDiscordDriver.store_discord_driver()
   