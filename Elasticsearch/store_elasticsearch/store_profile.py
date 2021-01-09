#!/usr/bin/env python
# coding: utf-8

import store_elasticsearch.connect_elasticsearch as  ConnectElasticsearch
import store_elasticsearch.create_index as  CreateIndex 
import store_elasticsearch.store_row as  StoreRow
import store_elasticsearch.create_tables as  CreateTables
import json
import sys
import os
from tqdm import tqdm
import pandas as pd
import csv

class StoreProfile:
    def __init__(self, job_name, driver_name, data_var="none", folder_path=".", host="localhost", port=9200):

        ''' 
        Reads the value of the company name.
        '''

        self.job_name = str(job_name)
        self.driver_name = str(driver_name)
        self.folder_path = folder_path
        self.data_var = data_var
        self.host = host
        self.port = port

    def save_data_csv(self, file_name, data):
        data.to_csv(self.folder_path + "/" + file_name, index=False)

    def save_data_json(self, file_name, fieldnames):
            data_csv = open(self.folder_path + '/' + file_name + '.csv', 'r', encoding="utf8")
            data_json = open(self.folder_path + '/' + file_name + '.json', 'w', encoding="utf8")

            reader = csv.DictReader(data_csv, fieldnames)
            out = json.dumps([row for row in reader])
            data_json.write(out)
        

    def process_data(self, es_object):
        data = pd.read_csv(self.folder_path + '/' + self.driver_name + '_data_profile.csv')
        data = data.replace(',',';')
        data = data.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r", ","], value=["","", ";"], regex=True)

        if(self.driver_name=='instagram'):
            data.rename(columns={'owner': 'author'}, inplace=True)
        elif(self.driver_name=='discord'):
            data.rename(columns={'name': 'author'}, inplace=True)

        id_count = es_object.count(index=self.job_name+'-profile')
        
        profileid = []
        for i in range (1, len(data)+1):
            profileid.append(str(i+id_count['count']))

        data['profileid'] = profileid
        data['job_name'] = self.job_name
        
        columns = ["job_name", "profileid", "author", "role", "names_data", "links_data", "steam_link", "twitch_link", "spotify_link", "reddit_link", "youtube_link", "steam_name", "twitch_name", "spotify_name", "reddit_name", "youtube_name", "battle_net_name", "facebook_name", "twitter_name", "xbox_live_name"]
        for col in columns:
            if(col not in data.columns):
                data[col] = "No data"
            
        profile_data = data[["job_name", "profileid", "author", "role", "names_data", "links_data", "steam_link", "twitch_link", "spotify_link", "reddit_link", "youtube_link", "steam_name", "twitch_name", "spotify_name", "reddit_name", "youtube_name", "battle_net_name", "facebook_name", "twitter_name", "xbox_live_name"]]
        
        self.save_data_csv("profile_data.csv", profile_data)
        
        self.save_data_json('profile_data', ("job_name", "profileid", "author", "role", "names_data", "links_data", "steam_link", "twitch_link", "spotify_link", "reddit_link", "youtube_link", "steam_name", "twitch_name", "spotify_name", "reddit_name", "youtube_name", "battle_net_name", "facebook_name", "twitter_name", "xbox_live_name"))

    def store_profile(self):
	
        ''' 
        Store discord data in Elasticsearch.
        '''
        connectElasticsearch = ConnectElasticsearch.ConnectElasticsearch(self.host, self.port)    # Connect to Elasticsearch.
        es_object = connectElasticsearch.connect_elasticsearch()

        createTables = CreateTables.CreateTables(self.job_name)
        createTables.create_tables()

        if(self.data_var == "none"):
            self.process_data(es_object)

            with open(self.folder_path + "/profile_data.json", 'r') as handle:     # Load profile_data.json
                profile_data = json.load(handle)
        
        
            profile_index = self.job_name + "-profile"

            storeRow_profile = StoreRow.StoreRow(es_object, profile_index)     # Store the data in Elasticsearch
        
            print('Storing ' + self.driver_name + ' data')
            for i in tqdm(range(len(profile_data))):  # Store each row.
                storeRow_profile.store_row(profile_data[i])

        else:
            profile_index = self.job_name + "-profile"
            id_count = es_object.count(index=profile_index)
            profileid = []
            for i in range (1, len(self.data_var)+1):
                self.data_var[i-1]['profileid'] = str(i+id_count['count'])
                self.data_var[i-1]['job_name'] = self.job_name

            columns = ["job_name", "profileid", "author", "role", "names_data", "links_data", "steam_link", "twitch_link", "spotify_link", "reddit_link", "youtube_link", "steam_name", "twitch_name", "spotify_name", "reddit_name", "youtube_name", "battle_net_name", "facebook_name", "twitter_name", "xbox_live_name"]
            for col in columns:
                if(col not in self.data_var[0].keys()):
                    for i in range (len(self.data_var)):
                        self.data_var[i][col] = "No data"

            storeRow_profile = StoreRow.StoreRow(es_object, profile_index)     # Store the data in Elasticsearch

            print('Storing ' + self.driver_name + ' data')
            for i in tqdm(range(len(self.data_var))):  # Store each row.
                storeRow_profile.store_row(self.data_var[i])

    
if __name__ == '__main__':
    storeProfile = StoreProfile("job_name")
    storeProfile.store_profile()
   