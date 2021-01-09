#!/usr/bin/env python
# coding: utf-8

from .connect_elasticsearch import  ConnectElasticsearch
from .create_index import  CreateIndex
from .store_row import  StoreRow 
from .store_youtube_driver import  StoreYoutubeDriver 
from .store_discord_driver import  StoreDiscordDriver 
from .store_instagram_driver import  StoreInstagramDriver 
import re

from abc import ABC

__version__ = '1.0.0'

class Store(ABC):

    def get_user_info(self, user, **kwargs):
        pass
    
    def get_posts_from_key(self, user, **kwargs):
        pass
    
    def get_posts_from_keys(self, user, **kwargs):
        pass
    

class StoreElasticsearch(Store):
    def get_user_info(self, user, **kwargs):

        '''
        Uses the username and:
            * In the case of discord-driver, It returns the informations about the user(message, name...)
            * In the case of youtube-driver, It returns informations about the user's videos and informations about the comments posted on the videos.	
        '''

        if len(kwargs) != 0:   # If there are parameters specified.
            for dict in kwargs.values(): 
                for key in dict.keys(): 
                    if (key == 'company_name'):
                        company_name = str(dict[key])       # Store the company name.
                    elif (key == 'driver'):
                        driver = str(dict[key])             # Store the driver name(youtube, disocord...).
                    elif (key == 'host'):
                        host = (dict[key])             # Store the host.
                    elif (key == 'port'):
                        port = int(dict[key])             # Store the port.
                    elif (key == 'post_type'):
                        post_type = (dict[key])             # Store the post type.
            connectElasticsearch = ConnectElasticsearch(host, port)    # Connect to Elasticsearch.
            es_object = connectElasticsearch.connect_elasticsearch()

            if(driver == "youtube"):   # Search in the youtube data.
                print("Searching in youtube-driver data corresponding to the company name: " + str(company_name))
                if(post_type == "video"):
                    query_body = {
                        "query": {
                            "match": {
                                "channelTitle" : str(user)
                            }
                        }
                    }
                    result = es_object.search(index=company_name+"-youtube-driver", body=query_body)

                elif(post_type == "comment"):
                    query_body = {
                        "query": {
                            "match": {
                                "author" : str(user)
                            }
                        }
                    }
                    result = es_object.search(index=company_name+"-youtube-driver", body=query_body)

            elif(driver == "discord"):   # Search in the discord data.
                print("Searching in discord-driver data corresponding to the company name: " + str(company_name))
                query_body = {
                    "query": {
                        "match": {
                            "name" : str(user)
                        }
                    }
                }
                result = es_object.search(index=company_name+"-discord-driver", body=query_body)
				
            elif(driver == "instagram"):   # Search in the instagram data.
                print("Searching in instagram-driver data corresponding to the company name: " + str(company_name))
                query_body = {
                    "query": {
                        "match": {
                            "owner" : str(user)
                        }
                    }
                }
                result = es_object.search(index=company_name+"-instagram-driver", body=query_body)

            elif(driver == "*"):   # Search in all the data.
                print("Searching in all the documents corresponding to the company name: " + str(company_name))
                if(post_type == "video"):
                    query_body1 = {
                        "query": {
                            "match": {
                                "channelTitle" : str(user)
                            }
                        }
                    }

                elif(post_type == "comment"):
                    query_body1 = {
                        "query": {
                            "match": {
                                "author" : str(user)
                            }
                        }
                    }

                query_body2 = {
                    "query": {
                        "match": {
                            "name" : str(user)
                        }
                    }
                }
                query_body3 = {
                    "query": {
                        "match": {
                            "owner" : str(user)
                        }
                    }
                }
                result1 = es_object.search(index=company_name+"-youtube-driver", body=query_body1)
                result2 = es_object.search(index=company_name+"-discord-driver", body=query_body2)
                result3 = es_object.search(index=company_name+"-instagram-driver", body=query_body3)
                result = [result1, result2, result3]

        else:   # If there are no parameters specified.
            print("Enter the parameters")
            result = ""

        return result
    
    def get_posts_from_key(self, key, **kwargs):

        '''
        Returns the informations of the messages containing the key.
        '''

        if len(kwargs) != 0:   # If there are parameters specified.
            for dict in kwargs.values(): 
                for dict_key in dict.keys(): 
                    if (dict_key == 'company_name'):
                        company_name = dict[dict_key]       # Store the company_name.
                    elif (dict_key == 'driver'):
                        driver = dict[dict_key]             # Store the driver name.
                    elif (dict_key == 'host'):
                        host = (dict[dict_key])             # Store the host.
                    elif (dict_key == 'port'):
                        port = int(dict[dict_key])             # Store the port.
            connectElasticsearch = ConnectElasticsearch(host, port)    # Connect to Elasticsearch.
            es_object = connectElasticsearch.connect_elasticsearch()

            if(driver == "youtube"):   # Search in the youtube data.
                print("Searching in youtube-driver data corresponding to the company name: " + str(company_name))
                query_body = {
                    "query": {
                        "match": {
                            "display_text" : str(key)
                        }
                    }
                }
                result = es_object.search(index=company_name+"-youtube-driver", body=query_body)

            elif(driver == "discord"):   # Search in the discord data.
                print("Searching in discord-driver data corresponding to the company name: " + str(company_name))
                query_body = {
                    "query": {
                        "match": {
                            "message" : str(key)
                        }
                    }
                }
                result = es_object.search(index=company_name+"-discord-driver", body=query_body)

            elif(driver == "instagram"):   # Search in the instagram data.
                print("Searching in instagram-driver data corresponding to the company name: " + str(company_name))
                query_body = {
                    "query": {
                        "match": {
                            "comment" : str(key)
                        }
                    }
                }
                result = es_object.search(index=company_name+"-instagram-driver", body=query_body)
				
            elif(driver == "*"):   # Search in all the data.
                print("Searching in all the documents corresponding to the company name: " + str(company_name))
                query_body1 = {
                    "query": {
                        "match": {
                            "display_text" : str(key)
                        }
                    }
                }
                query_body2 = {
                    "query": {
                        "match": {
                            "message" : str(key)
                        }
                    }
                }
                query_body3 = {
                    "query": {
                        "match": {
                            "comment" : str(key)
                        }
                    }
                }
                result1 = es_object.search(index=company_name+"-youtube-driver", body=query_body1)
                result2 = es_object.search(index=company_name+"-discord-driver", body=query_body2) 
                result3 = es_object.search(index=company_name+"-instagram-driver", body=query_body3) 
                result = [result1, result2, result3]

        else:   # If there are no parameters specified.
            print("Enter the parameters")
            result = ""

        return result

	
    def get_posts_from_keys(self, keys, **kwargs):
        if len(kwargs) != 0:   # If there are parameters specified.
            for dict in kwargs.values(): 
                for dict_key in dict.keys(): 
                    if (dict_key == 'company_name'):
                        company_name = dict[dict_key]       # Store the company_name.
                    elif (dict_key == 'driver'):
                        driver = dict[dict_key]             # Store the driver name.
                    elif (dict_key == 'host'):
                        host = (dict[dict_key])             # Store the host.
                    elif (dict_key == 'port'):
                        port = int(dict[dict_key])             # Store the port.
            connectElasticsearch = ConnectElasticsearch(host, port)    # Connect to Elasticsearch.
            es_object = connectElasticsearch.connect_elasticsearch()

            if(driver == "youtube"):   # Search in the youtube data.
                print("Searching in youtube-driver data corresponding to the company name: " + str(company_name))
                result=[]
                for word in keys:
                    query_body = {
                        "query": {
                            "match": {
                                "display_text" : str(word)
                            }
                        }
                    }
                    result.append(es_object.search(index=company_name+"-youtube-driver", body=query_body))

            elif(driver == "discord"):   # Search in the discord data.
                print("Searching in discord-driver data corresponding to the company name: " + str(company_name))
                result=[]
                for word in keys:
                    query_body = {
                        "query": {
                            "match": {
                                "message" : str(word)
                            }
                        }
                    }
                    result.append(es_object.search(index=company_name+"-discord-driver", body=query_body))

            elif(driver == "instagram"):   # Search in the instagram data.
                print("Searching in instagram-driver data corresponding to the company name: " + str(company_name))
                result=[]
                for word in keys:
                    query_body = {
                        "query": {
                            "match": {
                                "comment" : str(word)
                            }
                        }
                    }
                    result.append(es_object.search(index=company_name+"-instagram-driver", body=query_body))
					
            elif(driver == "*"):   # Search in all the data.
                print("Searching in all the documents corresponding to the company name: " + str(company_name))
                result1 = []
                result2 = []
                result3 = []
                result = []
                for word in keys:
                    query_body1 = {
                        "query": {
                            "match": {
                                "display_text" : str(word)
                            }
                        }
                    }
                    query_body2 = {
                        "query": {
                            "match": {
                                "message" : str(word)
                            }
                        }
                    }
                    query_body3 = {
                        "query": {
                            "match": {
                                "comment" : str(word)
                            }
                        }
                    }
                    result1.append(es_object.search(index=company_name+"-youtube-driver", body=query_body1))
                    result2.append(es_object.search(index=company_name+"-discord-driver", body=query_body2))
                    result3.append(es_object.search(index=company_name+"-instagram-driver", body=query_body3))
                    result.append([result1, result2, result3])
 
        else:   # If there are no parameters specified.
            print("Enter the parameters")
            result = []

        return result

    def get_posts_from_date(self, key, **kwargs):

        '''
        Returns the informations of the messages containing the key.
        '''

        if len(kwargs) != 0:   # If there are parameters specified.
            for dict in kwargs.values(): 
                for dict_key in dict.keys(): 
                    if (dict_key == 'company_name'):
                        company_name = dict[dict_key]       # Store the company_name.
                    elif (dict_key == 'driver'):
                        driver = dict[dict_key]             # Store the driver name.
                    elif (dict_key == 'host'):
                        host = (dict[dict_key])             # Store the host.
                    elif (dict_key == 'port'):
                        port = int(dict[dict_key])             # Store the port.
                    elif (dict_key == 'post_type'):
                        post_type = (dict[dict_key])             # Store the post type.
                    
            connectElasticsearch = ConnectElasticsearch(host, port)    # Connect to Elasticsearch.
            es_object = connectElasticsearch.connect_elasticsearch()

            if(driver == "youtube"):   # Search in the youtube data.
                print("Searching in youtube-driver data corresponding to the company name: " + str(company_name))
                date = re.sub('[/.:]', '-', str(key))                
                if(post_type == "comment"):
                    query_body = {
                        "query": {
                            "wildcard": {
                                "published_time.keyword" : "*"+date+"*"
                            }
                        }
                    }

                    result = es_object.search(index=company_name+"-youtube-driver", body=query_body)
                elif(post_type == "video"):
                    query_body = {
                        "query": {
                            "wildcard": {
                                "video_publishedAt.keyword" : "*"+date+"*"
                            }
                        }
                    }

                    result = es_object.search(index=company_name+"-youtube-driver", body=query_body)

            elif(driver == "discord"):   # Search in the discord data.
                print("Searching in discord-driver data corresponding to the company name: " + str(company_name))
                date = str(key)
                date = date[8:10] + '/' + date[5:7] + '/' + date[:4]
                query_body = {
                    "query": {
                        "wildcard": {
                            "time.keyword" : "*"+date+"*"
                        }
                    }
                }
                result = es_object.search(index=company_name+"-discord-driver", body=query_body)

            elif(driver == "instagram"):   # Search in the instagram data.
                print("Searching in instagram-driver data corresponding to the company name: " + str(company_name))
                date = re.sub('[/.:]', '-', str(key))
                query_body = {
                    "query": {
                        "wildcard": {
                            "taken_at_timestamp.keyword" : "*"+date+"*"
                        }
                    }
                }
                result = es_object.search(index=company_name+"-instagram-driver", body=query_body)
				
            elif(driver == "*"):   # Search in all the data.
                print("Searching in all the documents corresponding to the company name: " + str(company_name))
                date = re.sub('[/.:]', '-', str(key)) 
                if(post_type == "comment"):
                    query_body1 = {
                        "query": {
                            "wildcard": {
                                "published_time.keyword" : "*"+date+"*"
                            }
                        }
                    }

                elif(post_type == "video"):
                    query_body1 = {
                        "query": {
                            "wildcard": {
                                "video_publishedAt.keyword" : "*"+date+"*"
                            }
                        }
                    }
                date = str(key)
                date = date[8:10] + '/' + date[5:7] + '/' + date[:4]
                query_body2 = {
                    "query": {
                        "wildcard": {
                            "time.keyword" : "*"+date+"*"
                        }
                    }
                }
                date = re.sub('[/.:]', '-', str(key))
                query_body3 = {
                    "query": {
                        "wildcard": {
                            "taken_at_timestamp.keyword" : "*"+date+"*"
                        }
                    }
                }
                result1 = es_object.search(index=company_name+"-youtube-driver", body=query_body1)
                result2 = es_object.search(index=company_name+"-discord-driver", body=query_body2) 
                result3 = es_object.search(index=company_name+"-instagram-driver", body=query_body3) 
                result = [result1, result2, result3]

        else:   # If there are no parameters specified.
            print("Enter the parameters")
            result = ""

        return result

    def get_posts_from_dates(self, keys, **kwargs):
        if len(kwargs) != 0:   # If there are parameters specified.
            for dict in kwargs.values(): 
                for dict_key in dict.keys(): 
                    if (dict_key == 'company_name'):
                        company_name = dict[dict_key]       # Store the company_name.
                    elif (dict_key == 'driver'):
                        driver = dict[dict_key]             # Store the driver name.
                    elif (dict_key == 'host'):
                        host = (dict[dict_key])             # Store the host.
                    elif (dict_key == 'port'):
                        port = int(dict[dict_key])             # Store the port.
                    elif (dict_key == 'post_type'):
                        post_type = (dict[dict_key])             # Store the post type.

            connectElasticsearch = ConnectElasticsearch(host, port)    # Connect to Elasticsearch.
            es_object = connectElasticsearch.connect_elasticsearch()

            if(driver == "youtube"):   # Search in the youtube data.
                print("Searching in youtube-driver data corresponding to the company name: " + str(company_name))
                result=[]
                for input_date in keys:
                    date = re.sub('[/.:]', '-', str(input_date))                
                    if(post_type == "comment"):
                        query_body = {
                            "query": {
                                "wildcard": {
                                    "published_time.keyword" : "*"+date+"*"
                                }
                            }
                        }
                        result.append(es_object.search(index=company_name+"-youtube-driver", body=query_body))

                    elif(post_type == "video"):
                        query_body = {
                            "query": {
                                "wildcard": {
                                    "video_publishedAt.keyword" : "*"+date+"*"
                                }
                            }
                        }
                        result.append(es_object.search(index=company_name+"-youtube-driver", body=query_body))

            elif(driver == "discord"):   # Search in the discord data.
                print("Searching in discord-driver data corresponding to the company name: " + str(company_name))
                result=[]
                for input_date in keys:
                    date = str(input_date)
                    date = date[8:10] + '/' + date[5:7] + '/' + date[:4]
                    query_body = {
                        "query": {
                            "wildcard": {
                                "time.keyword" : "*"+date+"*"
                            }
                        }
                    }
                    result.append(es_object.search(index=company_name+"-discord-driver", body=query_body))

            elif(driver == "instagram"):   # Search in the instagram data.
                print("Searching in instagram-driver data corresponding to the company name: " + str(company_name))
                result=[]
                for input_date in keys:
                    date = re.sub('[/.:]', '-', str(input_date))
                    query_body = {
                        "query": {
                            "wildcard": {
                                "taken_at_timestamp.keyword" : "*"+date+"*"
                            }
                        }
                    }
                    result.append(es_object.search(index=company_name+"-instagram-driver", body=query_body))
					
            elif(driver == "*"):   # Search in all the data.
                print("Searching in all the documents corresponding to the company name: " + str(company_name))
                result1 = []
                result2 = []
                result3 = []
                result = []
                for input_date in keys:
                    date = re.sub('[/.:]', '-', str(input_date)) 
                    if(post_type == "comment"):
                        query_body1 = {
                            "query": {
                                "wildcard": {
                                    "published_time.keyword" : "*"+date+"*"
                                }
                            }
                        }

                    elif(post_type == "video"):
                        query_body1 = {
                            "query": {
                                "wildcard": {
                                    "video_publishedAt.keyword" : "*"+date+"*"
                                }
                            }
                        }
                    date = str(input_date)
                    date = date[8:10] + '/' + date[5:7] + '/' + date[:4]
                    query_body2 = {
                        "query": {
                            "wildcard": {
                                "time.keyword" : "*"+date+"*"
                            }
                        }
                    }
                    date = re.sub('[/.:]', '-', str(input_date))
                    query_body3 = {
                        "query": {
                            "wildcard": {
                                "taken_at_timestamp.keyword" : "*"+date+"*"
                            }
                        }
                    }

                    result1.append(es_object.search(index=company_name+"-youtube-driver", body=query_body1))
                    result2.append(es_object.search(index=company_name+"-discord-driver", body=query_body2))
                    result3.append(es_object.search(index=company_name+"-instagram-driver", body=query_body3))
                    result.append([result1, result2, result3])
 
        else:   # If there are no parameters specified.
            print("Enter the parameters")
            result = []

        return result

