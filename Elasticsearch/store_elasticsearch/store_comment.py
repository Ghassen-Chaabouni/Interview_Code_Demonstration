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

class StoreComment:
    def __init__(self, job_name, driver_name, folder_path=".", host="localhost", port=9200):
        self.job_name = str(job_name)
        self.driver_name = driver_name
        self.folder_path = folder_path
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
        if(self.driver_name=='instagram'):
            data = pd.read_json(self.folder_path + '/instagram_data.json')
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

            data = pd.DataFrame()
            data["shortcode"] = shortcode
            data["owner"] = owner
            data["comment"] = comment
            data["likes"] = likes
            data["text"] = text
            data["location"] = location
            data["post_likes"] = post_likes
            data["taken_at_timestamp"] = taken_at_timestamp
            data = data.replace(',',';')
            data = data.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r", ","], value=["","", ";"], regex=True)
            data.rename(columns={'owner': 'author', 'likes': 'comment_likes', 'taken_at_timestamp': 'post_publishedAt', 'shortcode': 'postid'}, inplace=True)

        elif(self.driver_name=='discord'):
            data = pd.read_csv(self.folder_path + '/discord_data.csv')
            data = data.replace(',',';')
            data = data.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r", ","], value=["","", ";"], regex=True)
            data.rename(columns={'message': 'comment', 'name': 'author', 'time': 'comment_published_time'}, inplace=True)
			
        elif(self.driver_name=='youtube'):
            data = pd.read_csv(self.folder_path + '/youtube_data.csv')
            data = data.replace(',',';')
            data = data.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r", ","], value=["","", ";"], regex=True)
            data.rename(columns={'videoId': 'postid', 'display_text': 'comment', 'likes': 'comment_likes', 'published_time': 'comment_published_time'}, inplace=True)
           
        id_count = es_object.count(index=self.job_name+'-comment')
        
        commentid = []
        for i in range (1, len(data)+1):
            commentid.append(str(i+id_count['count']))

        data['commentid'] = commentid
        data['job_name'] = self.job_name
        
        columns = ["job_name", "commentid", "postid", "author", "role", "names_data", "links_data", "steam_link", "twitch_link", "spotify_link", "reddit_link", "youtube_link", "steam_name", "twitch_name", "spotify_name", "reddit_name", "youtube_name", "battle_net_name", "facebook_name", "twitter_name", "xbox_live_name", "channelid", "is_public", "viewer_rating", "post_publishedAt", "video_title", "video_description", "thumbnail", "channelTitle", "tags", "video_duration", "location", "room_name", "comment", "comment_published_time", "update_time", "number_of_replies", "can_reply", "post_likes", "comment_likes"]
        for col in columns:
            if(col not in data.columns):
                data[col] = "No data"
            
        post_data = data[["postid", "author", "channelid", "is_public", "viewer_rating", "post_publishedAt", "video_title", "video_description", "thumbnail", "channelTitle", "tags", "video_duration", "location", "room_name"]]
        comment_data = data[["commentid", "postid", "author", "comment", "comment_published_time", "update_time", "number_of_replies", "can_reply"]]
        post_reacts_data = data[["postid", "post_likes"]]
        comment_reacts_data = data[["commentid", "comment_likes"]]
        
        self.save_data_csv("post_data.csv", post_data)
        self.save_data_csv("comment_data.csv", comment_data)
        self.save_data_csv("post_reacts_data.csv", post_reacts_data)
        self.save_data_csv("comment_reacts_data.csv", comment_reacts_data)
        
        self.save_data_json('post_data', ("postid", "author", "channelid", "is_public", "viewer_rating", "post_publishedAt", "video_title", "video_description", "thumbnail", "channelTitle", "tags", "video_duration", "location", "room_name"))
        self.save_data_json('comment_data', ("commentid", "postid", "author", "comment", "comment_published_time", "update_time", "number_of_replies", "can_reply"))
        self.save_data_json('post_reacts_data', ("postid", "post_likes"))
        self.save_data_json('comment_reacts_data', ("commentid", "comment_likes"))

    def store_comment(self):
	
        ''' 
        Store data in Elasticsearch.
        '''
        connectElasticsearch = ConnectElasticsearch.ConnectElasticsearch(self.host, self.port)    # Connect to Elasticsearch.
        es_object = connectElasticsearch.connect_elasticsearch()

        createTables = CreateTables.CreateTables(self.job_name)
        createTables.create_tables()

        self.process_data(es_object)
    
        with open(self.folder_path + "/post_data.json", 'r') as handle:     # Load post_data.json
            post_data = json.load(handle)
        
        with open(self.folder_path + "/comment_data.json", 'r') as handle:     # Load comment_data.json
            comment_data = json.load(handle)
        
        with open(self.folder_path + "/post_reacts_data.json", 'r') as handle:     # Load post_reacts_data.json
            post_reacts_data = json.load(handle)
            
        with open(self.folder_path + "/comment_reacts_data.json", 'r') as handle:     # Load comment_reacts_data.json
            comment_reacts_data = json.load(handle)
        
        comment_index = self.job_name + "-comment"
        post_index = self.job_name + "-post"
        post_reacts_index = self.job_name + "-post_reacts"
        comment_reacts_index = self.job_name + "-comment_reacts"

        storeRow_comment = StoreRow.StoreRow(es_object, comment_index)     
        storeRow_post = StoreRow.StoreRow(es_object, post_index)     
        storeRow_post_reacts = StoreRow.StoreRow(es_object, post_reacts_index)    
        storeRow_comment_reacts = StoreRow.StoreRow(es_object, comment_reacts_index)     
        
        print('Storing ' + self.driver_name + ' data')
        for i in tqdm(range(len(comment_data))):  # Store each row.
            storeRow_comment.store_row(comment_data[i])
            storeRow_post.store_row(post_data[i])
            storeRow_post_reacts.store_row(post_reacts_data[i])
            storeRow_comment_reacts.store_row(comment_reacts_data[i])
            
    
if __name__ == '__main__':
    storeComment = StoreComment("job_name")
    storeComment.store_comment()
   