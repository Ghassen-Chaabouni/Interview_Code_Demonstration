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

class CreateTables:
    def __init__(self, job_name, host="localhost", port=9200):
        self.job_name = str(job_name)
        self.host = host
        self.port = port

    def profile_settings(self):
        index_name = self.job_name + "-profile"
        print('index: ' + index_name)
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                    "dynamic": "strict",
                    "properties": {
                        "job_name": {
                            "type": "keyword"
                        },
                        "profileid": {
                            "type": "keyword"
                        },
                        "author": {
                            "type": "keyword"
                        },
                        "role": {
                            "type": "keyword"
                        },
                        "names_data": {
                            "type": "keyword"
                        },
                        "links_data": {
                            "type": "keyword"
                        },
                        "steam_link": {
                            "type": "keyword"
                        },
                        "twitch_link": {
                            "type": "keyword"
                        },
                        "spotify_link": {
                            "type": "keyword"
                        },
                        "reddit_link": {
                            "type": "keyword"
                        },
                        "youtube_link": {
                            "type": "keyword"
                        },
                        "steam_name": {
                            "type": "keyword"
                        },
                        "twitch_name": {
                            "type": "keyword"
                        },
                        "spotify_name": {
                            "type": "keyword"
                        },
                        "reddit_name": {
                            "type": "keyword"
                        },
                        "youtube_name": {
                            "type": "keyword"
                        },
                        "battle_net_name": {
                            "type": "keyword"
                        },
                        "facebook_name": {
                            "type": "keyword"
                        },
                        "twitter_name": {
                            "type": "keyword"
                        },
                        "xbox_live_name": {
                            "type": "keyword"
                        }                        
                    }
               }
            }

        return settings, index_name
    
    def comment_settings(self):
        index_name = self.job_name + "-comment"
        print('index: ' + index_name)
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                    "dynamic": "strict",
                    "properties": {
                        "commentid": {
                            "type": "keyword"
                        },
                        "postid": {
                            "type": "keyword"
                        },
                        "author": {
                            "type": "keyword"
                        },
                        "comment": {
                            "type": "keyword"
                        },
                        "comment_published_time": {
                            "type": "keyword"
                        },
                        "update_time": {
                            "type": "keyword"
                        },
                        "number_of_replies": {
                            "type": "keyword"
                        },
                        "can_reply": {
                            "type": "keyword"
                        }
                    }
               }
            }

        return settings, index_name
    
    def post_settings(self):
        index_name = self.job_name + "-post"
        print('index: ' + index_name)
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                    "dynamic": "strict",
                    "properties": {
                        "postid": {
                            "type": "keyword"
                        },
                        "author": {
                            "type": "keyword"
                        },
                        "channelid": {
                            "type": "keyword"
                        },
                        "is_public": {
                            "type": "keyword"
                        },
                        "viewer_rating": {
                            "type": "keyword"
                        },
                        "post_publishedAt": {
                            "type": "keyword"
                        },
                        "video_title": {
                            "type": "keyword"
                        },
                        "video_description": {
                            "type": "keyword"
                        },
                        "thumbnail": {
                            "type": "keyword"
                        },
                        "channelTitle": {
                            "type": "keyword"
                        },
                        "tags": {
                            "type": "keyword"
                        },
                        "video_duration": {
                            "type": "keyword"
                        },
                        "location": {
                            "type": "keyword"
                        },
                        "room_name": {
                            "type": "keyword"
                        }
                    }
               }
            }

        return settings, index_name
    
    def post_reacts_settings(self):
        index_name = self.job_name + "-post_reacts"
        print('index: ' + index_name)
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                    "dynamic": "strict",
                    "properties": {
                        "postid": {
                            "type": "keyword"
                        },
                        "post_likes": {
                            "type": "keyword"
                        }
                    }
               }
            }

        return settings, index_name
    
    def comment_reacts_settings(self):
        index_name = self.job_name + "-comment_reacts"
        print('index: ' + index_name)
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                    "dynamic": "strict",
                    "properties": {
                        "commentid": {
                            "type": "keyword"
                        },
                        "comment_likes": {
                            "type": "keyword"
                        }
                    }
               }
            }

        return settings, index_name
    

    def create_tables(self):
        connectElasticsearch = ConnectElasticsearch.ConnectElasticsearch(self.host, self.port)    # Connect to Elasticsearch.
        es_object = connectElasticsearch.connect_elasticsearch()

        profile_settings, profile_index_name = self.profile_settings()   
        comment_settings, comment_index_name = self.comment_settings()   
        post_settings, post_index_name = self.post_settings()   
        post_reacts_settings, post_reacts_index_name = self.post_reacts_settings()   
        comment_reacts_settings, comment_reacts_index_name = self.comment_reacts_settings()    
        
        createIndex_profile = CreateIndex.CreateIndex(es_object, profile_index_name, profile_settings)     # Create an index.
        created_profile = createIndex_profile.create_index()
        
        createIndex_comment = CreateIndex.CreateIndex(es_object, str(comment_index_name), comment_settings)     
        created_comment = createIndex_comment.create_index()
        
        createIndex_post = CreateIndex.CreateIndex(es_object, post_index_name, post_settings)     
        created_post = createIndex_post.create_index()
        
        createIndex_post_reacts = CreateIndex.CreateIndex(es_object, post_reacts_index_name, post_reacts_settings)     
        created_post_reacts = createIndex_post_reacts.create_index()
        
        createIndex_comment_reacts = CreateIndex.CreateIndex(es_object, comment_reacts_index_name, comment_reacts_settings)     
        created_comment_reacts = createIndex_comment_reacts.create_index()

if __name__ == '__main__':
    createTables = CreateTables("job_name")
    createTables.create_tables()
   