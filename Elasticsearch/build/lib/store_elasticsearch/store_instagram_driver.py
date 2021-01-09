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
import pandas as pd

class StoreInstagramDriver:
    def __init__(self, company_name, host="localhost", port=9200):

        ''' 
        Reads the value of the company_name.
        '''	

        self.company_name = str(company_name)
        self.host = host
        self.port = port

    def process_data(self):
        data = pd.read_json(self.determine_path () + '/config/instagram_data.json')
        owner = []
        comment = []
        likes = []
        shortcode = []
        text = []
        location = []
        post_likes = []
        taken_at_timestamp = []
        for i in range(len(data)):
            for j in range (len(list(data['comments'])[i])):
                shortcode.append(str(list(data['shortcode'])[i]))
                owner.append(str(dict(list(data['comments'])[i][j])['owner']))
                comment.append(str(dict(list(data['comments'])[i][j])['comment']))
                likes.append(str(dict(list(data['comments'])[i][j])['likes']))
                text.append(str(list(data['text'])[i]))
                location.append(str(list(data['location'])[i]))
                post_likes.append(str(list(data['likes'])[i]))
                taken_at_timestamp.append(str(list(data['taken_at_timestamp'])[i]))
    
        data2 = pd.DataFrame()
        data2["shortcode"] = shortcode
        data2["owner"] = owner
        data2["comment"] = comment
        data2["likes"] = likes
        data2["text"] = text
        data2["location"] = location
        data2["post_likes"] = post_likes
        data2["taken_at_timestamp"] = taken_at_timestamp
        
        data2.to_csv(self.determine_path () + '/config/instagram_data_cleaned.csv', index=False)

        csvfile = open(self.determine_path () + '/config/instagram_data_cleaned.csv', 'r', encoding="utf8")
        jsonfile = open(self.determine_path () + '/config/instagram_data_cleaned.json', 'w', encoding="utf8")

        fieldnames = ("shortcode", "owner", "comment", "likes", "text", "location", "post_likes", "taken_at_timestamp")

        reader = csv.DictReader(csvfile, fieldnames)
        out = json.dumps([row for row in reader])
        jsonfile.write(out)

    def instagram_driver_settings(self):

        ''' 
        The settings required to store the discord data in Elasticsearch.
        '''

        index_name = self.company_name + "-instagram-driver"
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
                        "owner": {
                            "type": "text"
                        },
                        "comment": {
                            "type": "text"
                        },
                        "likes": {
                            "type": "text"
                        },
                        "shortcode": {
                            "type": "text"
                        },
                        "text": {
                            "type": "text"
                        },
                        "location": {
                            "type": "text"
                        },
                        "post_likes": {
                            "type": "text"
                        },
                        "taken_at_timestamp": {
                            "type": "text"
                        }
                    }
               }
            }
        }

        return settings, index_name

    def store_instagram_driver(self):

        ''' 
        Store discord data in Elasticsearch.
        '''
        
        self.process_data()
        
        connectElasticsearch = ConnectElasticsearch.ConnectElasticsearch(self.host, self.port)    # Connect to Elasticsearch.
        es_object = connectElasticsearch.connect_elasticsearch()

        settings, index_name = self.instagram_driver_settings()   # Get the settings.
        
        createIndex = CreateIndex.CreateIndex(es_object, index_name, settings)   # Create an index.
        created = createIndex.create_index()
        
        with open(self.determine_path () + "/config/instagram_data_cleaned.json", 'r') as handle:   # Load the data discord_data.json
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
    storeInstagramDriver = StoreInstagramDriver('testing')
    storeInstagramDriver.store_instagram_driver()
   