#!/usr/bin/env python
# coding: utf-8

from .get_authenticated import GetAuthenticated
from .get_comments import GetComments
#from .get_images import GetImages

from abc import ABC
import googleapiclient.discovery   # pip install google-api-python-client | pip install protobuf==3.12.2 | pip install --upgrade protobuf --force-reinstall
import googleapiclient.errors
from google.auth.transport.requests import Request    # pip install google
import time
import sys
import json

__version__ = '1.0.0'

class Driver(ABC):
    def get_event(self, user_id, verbose=False):
        pass

    def get_page(self, user_id, verbose=False):
        pass
		
    def get_group(self, user_id, verbose=False):
        pass
		
    def get_images(self, user_id, verbose=False):
        pass

    def get_user_info(self, user_id, json_parser=False, verbose=False):
        pass
		
    def get_user_info_by_pseudo(self, pseudo, json_parser=False, verbose=False):
        pass

    def get_publications(self, user_id, comments, json_parser=False, verbose=False):
        pass
    
    def get_comments_by_publication(self, publication_id, json_parser=False, verbose=False):
        pass

    def get_friends(self, user_id, verbose=False):
        pass
		
    def get_react(self, publication_id, verbose=False):
        pass
    
    def get_comment_by_key(self, key, json_parser=False, verbose=False):
        pass
    
    def get_comment_by_keys(self, keys, json_parser=False, verbose=False):
        pass

class YoutubeDriver(Driver):

    def get_friends(self, user_id):
        pass

    def get_event(self, user_id):
        pass

    def get_page(self, user_id):
        pass
		
    def get_group(self, user_id):
        pass

    def get_comment_by_key(self, key, json_parser=False, verbose=False):

        '''
        Uses a keyword (video name that we are searching for) and returns the messages in the videos.	
        '''
        file_pos = 0
        getAuthenticated = GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
        youtube, file_num = getAuthenticated.get_authenticated()
        

        while(file_pos < file_num):
                    try:
                        request = youtube.search().list(
                            q=key,
                            part="snippet",
                            type="video"
                        )

                        response = request.execute()
                        
                        videoId = response['items'][0]['id']['videoId']   # Get the video id.
                        
                        # Get the video messages.
                        request2 = youtube.commentThreads().list(
                            part="snippet,replies",
                            videoId=str(videoId)
                        )
                        try:
                            response2 = request2.execute()
                        except:  # The video is private.
                            continue

                        getComments = GetComments(response=response2, youtube=youtube, json_parser=json_parser, verbose=verbose)  # Scrape the video messages.
                        if(json_parser):
                            getComments.get_comments()
                        else:
                            return getComments.get_comments()
                        break
                    except:
                        file_pos += 1
                        getAuthenticated = GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
                        youtube, file_num = getAuthenticated.get_authenticated()
                        pass
    
    def get_comment_by_keys(self, keys, json_parser=False, verbose=False):

        '''
        Uses a keyword (video name that we are searching for) and returns the messages in the videos.	
        '''
        file_pos = 0
        getAuthenticated = GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
        youtube, file_num = getAuthenticated.get_authenticated()
        
        l = []
        while(file_pos < file_num):
            for key in keys:
                    try:
                        request = youtube.search().list(
                            q=key,
                            part="snippet",
                            type="video"
                        )

                        response = request.execute()
                        
                        videoId = response['items'][0]['id']['videoId']   # Get the video id.
                        
                        # Get the video messages.
                        request2 = youtube.commentThreads().list(
                            part="snippet,replies",
                            videoId=str(videoId)
                        )
                        try:
                            response2 = request2.execute()
                        except:  # The video is private.
                            continue

                        getComments = GetComments(response=response2, youtube=youtube, json_parser=json_parser, verbose=verbose)  # Scrape the video messages.
                        if(json_parser):
                            getComments.get_comments()
                        else:
                            l.append(getComments.get_comments())
                        
                    except:
                        file_pos += 1
                        getAuthenticated = GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
                        youtube, file_num = getAuthenticated.get_authenticated()
                        pass

            if(not json_parser):
                return l
            break

    def get_images(self, user_id):
        pass   

    def get_react(self, publication_id, verbose=False):
        file_pos = 0
        getAuthenticated = GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
        youtube, file_num = getAuthenticated.get_authenticated()
        while(file_pos < file_num):
            try:
                # Search for the channel id using the youtube username.
                request = youtube.videos().list(
                    part="statistics",
                    id=publication_id
                )

                response = request.execute()
                return response['items'][0]['statistics']['likeCount']
                
            except:
                file_pos += 1
                getAuthenticated = GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
                youtube, file_num = getAuthenticated.get_authenticated()
                pass

    def get_user_info(self, user_id, json_parser=False, verbose=False):
        file_pos = 0
        getAuthenticated = GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
        youtube, file_num = getAuthenticated.get_authenticated()
        while(file_pos < file_num):
            try:
                # Search for the channel id using the youtube username.
                request = youtube.channels().list(
                    part="statistics",
                    id=user_id
                )

                response = request.execute()

                try:
                    channel_id = str(response['items'][0]['id'])
                except:
                    channel_id = ""

                try:
                    view_count = str(response['items'][0]['statistics']['viewCount'])
                except:
                    view_count = ""

                try:
                    subscriber_count = str(response['items'][0]['statistics']['subscriberCount'])
                except:
                    subscriber_count = ""

                try:
                    video_count = str(response['items'][0]['statistics']['videoCount'])
                except:
                    video_count = ""

                request = youtube.channels().list(
                    part="snippet",
                    id=user_id
                )

                response = request.execute()

                try:
                    channel_name = response['items'][0]['snippet']['title']
                except:
                    channel_name = ""

                try:
                    description = response['items'][0]['snippet']['description']
                except:
                    description = ""

                try:
                    channel_creation_date = response['items'][0]['snippet']['publishedAt']
                except:
                    channel_creation_date = ""

                try:
                    profile_image = response['items'][0]['snippet']['thumbnails']['default']['url']
                except:
                    profile_image = ""

                try:
                    country = response['items'][0]['snippet']['country']
                except:
                    country = ""


                request = youtube.channels().list(
                    part="topicDetails",
                    id=user_id
                )

                response = request.execute()

                try:
                    channel_topic_categories = list(response['items'][0]['topicDetails']['topicCategories'])
                except:
                    channel_topic_categories = []

                request = youtube.channels().list(
                    part="brandingSettings",
                    id=user_id
                )

                response = request.execute()

                try:
                    keywords = str(response['items'][0]['brandingSettings']['channel']['keywords'])
                except:
                    keywords = ""

                try:
                    featured_channels = list(response['items'][0]['brandingSettings']['channel']['featuredChannelsUrls'])
                except:
                    featured_channels = [] 

                try:
                    unsubscribed_trailer = str(response['items'][0]['brandingSettings']['channel']['unsubscribedTrailer'])
                except:
                    unsubscribed_trailer = ""

                try:
                    channel_banner_image = str(response['items'][0]['brandingSettings']['image']['bannerImageUrl'])
                except:
                    channel_banner_image = "" 

                if (verbose):
                    print("channel_id: "+ channel_id)
                    print("view_count: "+ view_count)
                    print("subscriber_count: "+ subscriber_count)
                    print("video_count: "+ video_count)

                    print("channel_name: "+ channel_name)
                    print("description: "+ description)
                    print("channel_creation_date: "+ channel_creation_date)
                    print("profile_image: "+ profile_image)
                    print("country: "+ country)

                    print('channel_topic_categories: ' + str(channel_topic_categories))

                    print('keywords: ' + keywords)
                    print('featured_channels: ' + str(featured_channels))
                    print('unsubscribed_trailer: ' + unsubscribed_trailer)
                    print('channel_banner_image: ' + channel_banner_image)

                break

            except:
                file_pos += 1
                getAuthenticated = GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
                youtube, file_num = getAuthenticated.get_authenticated()
                pass

        data = {}
        data['channel_id'] = channel_id
        data['view_count'] = view_count
        data['subscriber_count'] = subscriber_count
        data['video_count'] = video_count
        data['channel_name'] = channel_name
        data['description'] = description
        data['channel_creation_date'] = channel_creation_date
        data['profile_image'] = profile_image
        data['country'] = country
        data['channel_topic_categories'] = channel_topic_categories
        data['keywords'] = keywords
        data['featured_channels'] = featured_channels
        data['unsubscribed_trailer'] = unsubscribed_trailer
        data['channel_banner_image'] = channel_banner_image

        if(not json_parser):
            return data
        else:
            with open(channel_name + '_profile_data.json', 'w') as f:
                json.dump(data, f)		
					  
    def get_user_info_by_pseudo(self, pseudo, json_parser=False, verbose=False):
        file_pos = 0
        getAuthenticated = GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
        youtube, file_num = getAuthenticated.get_authenticated()
        while(file_pos < file_num):
            try:
                # Search for the channel id using the youtube username.
                request = youtube.search().list(
                    q=pseudo,
                    part="snippet",
                    type="channel"
                )

                response = request.execute()
                channel_id = response['items'][0]['id']['channelId']
                
                request2 = youtube.channels().list(
                    part="statistics",
                    id=channel_id
                )

                response = request2.execute()
                if (verbose):
                    print(response['items'][0])
                try:
                    channel_id = str(response['items'][0]['id'])
                except:
                    channel_id = ""

                try:
                    view_count = str(response['items'][0]['statistics']['viewCount'])
                except:
                    view_count = ""

                try:
                    subscriber_count = str(response['items'][0]['statistics']['subscriberCount'])
                except:
                    subscriber_count = ""

                try:
                    video_count = str(response['items'][0]['statistics']['videoCount'])
                except:
                    video_count = ""

                request3 = youtube.channels().list(
                    part="snippet",
                    id=channel_id
                )

                response = request3.execute()

                try:
                    channel_name = response['items'][0]['snippet']['title']
                except:
                    channel_name = ""

                try:
                    description = response['items'][0]['snippet']['description']
                except:
                    description = ""

                try:
                    channel_creation_date = response['items'][0]['snippet']['publishedAt']
                except:
                    channel_creation_date = ""

                try:
                    profile_image = response['items'][0]['snippet']['thumbnails']['default']['url']
                except:
                    profile_image = ""

                try:
                    country = response['items'][0]['snippet']['country']
                except:
                    country = ""


                request4 = youtube.channels().list(
                    part="topicDetails",
                    id=channel_id
                )

                response = request4.execute()

                try:
                    channel_topic_categories = list(response['items'][0]['topicDetails']['topicCategories'])
                except:
                    channel_topic_categories = []

                request5 = youtube.channels().list(
                    part="brandingSettings",
                    id=channel_id
                )

                response = request5.execute()

                try:
                    keywords = str(response['items'][0]['brandingSettings']['channel']['keywords'])
                except:
                    keywords = ""

                try:
                    featured_channels = list(response['items'][0]['brandingSettings']['channel']['featuredChannelsUrls'])
                except:
                    featured_channels = [] 

                try:
                    unsubscribed_trailer = str(response['items'][0]['brandingSettings']['channel']['unsubscribedTrailer'])
                except:
                    unsubscribed_trailer = ""

                try:
                    channel_banner_image = str(response['items'][0]['brandingSettings']['image']['bannerImageUrl'])
                except:
                    channel_banner_image = "" 

                if (verbose):
                    print("channel_id: "+ channel_id)
                    print("view_count: "+ view_count)
                    print("subscriber_count: "+ subscriber_count)
                    print("video_count: "+ video_count)

                    print("channel_name: "+ channel_name)
                    print("description: "+ description)
                    print("channel_creation_date: "+ channel_creation_date)
                    print("profile_image: "+ profile_image)
                    print("country: "+ country)

                    print('channel_topic_categories: ' + str(channel_topic_categories))

                    print('keywords: ' + keywords)
                    print('featured_channels: ' + str(featured_channels))
                    print('unsubscribed_trailer: ' + unsubscribed_trailer)
                    print('channel_banner_image: ' + channel_banner_image)

                break

            except:
                file_pos += 1
                getAuthenticated = GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
                youtube, file_num = getAuthenticated.get_authenticated()
                pass

        data = {}
        data['channel_id'] = channel_id
        data['view_count'] = view_count
        data['subscriber_count'] = subscriber_count
        data['video_count'] = video_count
        data['channel_name'] = channel_name
        data['description'] = description
        data['channel_creation_date'] = channel_creation_date
        data['profile_image'] = profile_image
        data['country'] = country
        data['channel_topic_categories'] = channel_topic_categories
        data['keywords'] = keywords
        data['featured_channels'] = featured_channels
        data['unsubscribed_trailer'] = unsubscribed_trailer
        data['channel_banner_image'] = channel_banner_image

        if(not json_parser):
            return data
        else:
            with open(channel_name + '_profile_data.json', 'w') as f:
                json.dump(data, f)

    def get_publications(self, user_id, comments, json_parser=False, verbose=False):

        '''
        Uses the Youtube username and returns the messages in the videos of the user.
        '''

        file_pos = 0	
        getAuthenticated = GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
        youtube, file_num = getAuthenticated.get_authenticated()
        while(file_pos < file_num):
                try:
                    request = youtube.search().list(
                        q=user_id,
                        part="snippet",
                        type="channel"
                    )

                    response = request.execute()
                    channel_id = response['items'][0]['id']['channelId']   # Get the channel id.

                    # Get the videos in the channel.
                    request = youtube.commentThreads().list(
                        part="snippet,replies",
                        allThreadsRelatedToChannelId=channel_id,
                        maxResults=100
                    )
                    response = request.execute()

                    getComments = GetComments(response=response, youtube=youtube, json_parser=json_parser, take_comments=comments, verbose=verbose)   # Scrape the comments in the video.
                    if(json_parser):
                        getComments.get_comments()
                    else:
                        return getComments.get_comments()
                    break
                except:
                    file_pos += 1
                    getAuthenticated = GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
                    youtube, file_num = getAuthenticated.get_authenticated()
                    pass
        
    def get_comments_by_publication(self, publication_id, json_parser=False, verbose=False):

        '''
        Uses a keyword (video name that we are searching for) and returns the messages in the videos.	
        '''
        file_pos = 0
        getAuthenticated = GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
        youtube, file_num = getAuthenticated.get_authenticated()
        

        while(file_pos < file_num):
                    try:
                        videoId = str(publication_id)   # Get the video id.
                        
                        # Get the video messages.
                        request2 = youtube.commentThreads().list(
                            part="snippet,replies",
                            videoId=str(videoId)
                        )
                        try:
                            response2 = request2.execute()
                        except:  # The video is private.
                            continue

                        getComments = GetComments(response=response2, youtube=youtube, json_parser=json_parser, verbose=verbose)  # Scrape the video messages.
                        if(json_parser):
                            getComments.get_comments()
                        else:
                            return getComments.get_comments()
                        break
                    except:
                        file_pos += 1
                        getAuthenticated = GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
                        youtube, file_num = getAuthenticated.get_authenticated()
                        pass
