#!/usr/bin/env python
# coding: utf-8

import store_elasticsearch.connect_elasticsearch as  ConnectElasticsearch
import store_elasticsearch.create_index as  CreateIndex 
import store_elasticsearch.store_row as  StoreRow
import json
import sys
import os
from tqdm import tqdm
import pandas as pd
import csv

class StoreYoutubeDriver:
    def __init__(self, company_name, host="localhost", port=9200):

        ''' 
        Reads the value of the company name.
        '''

        self.company_name = str(company_name)
        self.host = host
        self.port = port
		
    def process_data(self):
        data = pd.read_csv(self.determine_path () + '/config/youtube_data.csv')
        data = data.replace(',',';')
        data = data.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r", ","], value=["","", ";"], regex=True)
        data.to_csv(self.determine_path () + '/config/youtube_data.csv', index=False)
		
        csvfile = open(self.determine_path () + '/config/youtube_data.csv', 'r', encoding="utf8")
        jsonfile = open(self.determine_path () + '/config/youtube_data.json', 'w', encoding="utf8")

        fieldnames = ("videoId", "number_of_replies", "author", "display_text", "original_text", "likes",
                      "published_time", "update_time", "can_reply", "is_public", "viewer_rating", "video_publishedAt",
                      "channelId", "video_title", "video_description", "thumbnail", "channelTitle", "tags", "video_duration")


        reader = csv.DictReader(csvfile, fieldnames)
        out = json.dumps([row for row in reader])
        jsonfile.write(out)

    def youtube_driver_settings(self):

        ''' 
        The settings required to store the youtube data in Elasticsearch.
        '''	

        index_name = self.company_name + "-youtube-driver"
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
                        "videoId": {
                            "type": "text"
                        },
                        "number_of_replies": {
                            "type": "text"
                        },
                        "author": {
                            "type": "text"
                        },
                        "display_text": {
                            "type": "text"
                        },
                        "original_text": {
                            "type": "text"
                        },
                        "likes": {
                            "type": "text"
                        },
                        "published_time": {
                            "type": "text"
                        },
                        "update_time": {
                            "type": "text"
                        },
                        "can_reply": {
                            "type": "text"
                        },
                        "is_public": {
                            "type": "text"
                        },
                        "viewer_rating": {
                            "type": "text"
                        },
                        "video_publishedAt": {
                            "type": "text"
                        },
                        "channelId": {
                            "type": "text"
                        },
                        "video_title": {
                            "type": "text"
                        },
                        "video_description": {
                            "type": "text"
                        },
                        "thumbnail": {
                            "type": "text"
                        },
                        "channelTitle": {
                            "type": "text"
                        },
                        "tags": {
                            "type": "text"
                        },
                        "video_duration": {
                            "type": "text"
                        }
                    }
               }
            }
        }

        return settings, index_name

    def store_youtube_driver(self):
	
        ''' 
        Store discord data in Elasticsearch.
        '''	

        self.process_data()

        connectElasticsearch = ConnectElasticsearch.ConnectElasticsearch(self.host, self.port)    # Connect to Elasticsearch.
        es_object = connectElasticsearch.connect_elasticsearch()

        settings, index_name = self.youtube_driver_settings()    # Get the settings.
        
        createIndex = CreateIndex.CreateIndex(es_object, index_name, settings)     # Create an index.
        created = createIndex.create_index()
        
        with open(self.determine_path () + "/config/youtube_data.json", 'r') as handle:     # Load the data youtube_data.json
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
    storeYoutubeDriver = StoreYoutubeDriver()
    storeYoutubeDriver.store_youtube_driver()
   