#!/usr/bin/env python
# coding: utf-8

import os
import pickle
import pandas as pd

import google_auth_oauthlib.flow
import googleapiclient.discovery   # pip install google-api-python-client | pip install protobuf==3.12.2 | pip install --upgrade protobuf --force-reinstall
import googleapiclient.errors
from google.auth.transport.requests import Request    # pip install google
import youtube_driver.get_authenticated as  GetAuthenticated
import time
import json
import csv

class GetComments:
    def __init__(self, response, youtube, json_parser=True, take_comments=True, verbose=False):

        ''' 
        Reads the value of response returned by request.execute()
        '''

        self.response = response
        self.youtube = youtube
        self.json_parser = json_parser
        self.take_comments = take_comments
        self.verbose = verbose
    
    def save_data_json(self, file_name, fieldnames):
        data_csv = open('./youtube_data.csv', 'r', encoding="utf8")
        data_json = open('./youtube_data.json', 'w', encoding="utf8")

        reader = csv.DictReader(data_csv, fieldnames)
        out = json.dumps([row for row in reader], indent=2)
        data_json.write(out)
	
    def get_comments(self):

        ''' 
        Scrape comments in videos specified by a response.
        '''

        comments = []
        while(self.response):
            time.sleep(1)
            video_id_list = []
            for (index,item) in enumerate(self.response['items']):
                try:
                    videoId = str(item['snippet']['videoId'])     # Get the video id.
                except:
                    continue
                if(self.take_comments):
                    number_of_replies = str(item['snippet']['totalReplyCount'])    # Get the number of replies.

                    is_public = str(item['snippet']['isPublic'])   # Get whether the thread, including all of its comments and comment replies, is visible to all YouTube users.
                    can_reply = str(item['snippet']['canReply'])   # Get whether the current viewer can reply to the thread.
                    author = str(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])   # Get the name of the person who wrote the message.
                    display_text = str(item['snippet']['topLevelComment']['snippet']['textDisplay'])   # Get the message in the html format.
                    try:
                        author_profile_image = str(item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'])                 
                    except:
                        author_profile_image = ""
                    original_text = str(item['snippet']['topLevelComment']['snippet']['textOriginal']) # Get The original, raw text of the comment as it was initially posted or last updated.
                    likes = str(item['snippet']['topLevelComment']['snippet']['likeCount'])   # Get the total number of likes (positive ratings) the comment has received.
                    published_time = str(item['snippet']['topLevelComment']['snippet']['publishedAt'])   # Get the date and time when the comment was orignally published. The value is specified in ISO 8601 format.
                    update_time = str(item['snippet']['topLevelComment']['snippet']['updatedAt'])        # Get the date and time when the comment was last updated. The value is specified in ISO 8601 format.
                    viewer_rating = str(item['snippet']['topLevelComment']['snippet']['viewerRating'])   # Get the rating value: "like" if the viewer has rated the comment positively, "none" in all other cases.
                    try:
                        replies = str(item['replies'])
                    except:
                        replies = ""

                    if (self.verbose):
                        try:
                            print("videoId: " + str(videoId))
                            print("can_reply: " + str(can_reply))
                            print("author: " + str(author))
                            print("message: " + str(display_text))
                            print("likes: " + str(likes))
                            print("published_time: " + str(published_time))
                            print("update_time: " + str(update_time))
                            print("viewer_rating: " + str(viewer_rating))
                            print("replies: " + str(replies))
                            print('author_profile_image: ' + str(author_profile_image))
                        except:
                            pass

                # Scrape the video details.
                request = self.youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=str(videoId)
                )
                response2 = request.execute()
                if(self.take_comments):
                    while(response2):
                        time.sleep(1)
                        k = 0
                        for (index2,item2) in enumerate(response2['items']):

                            publishedAt = str(item2['snippet']['publishedAt'])  # Get the date and time that the video was published.
                            channelId = str(item2['snippet']['channelId'])  # Get the ID that YouTube uses to uniquely identify the channel that the video was uploaded to.
                            title = str(item2['snippet']['title'])  # Get the video's title.
                            video_like = str(item2['statistics']['likeCount'])

                            try:
                                description = str(item2['snippet']['description'])  # Get the video's description.
                            except:
                                description = "No description"

                            thumbnails = str(item2['snippet']['thumbnails']["default"]["url"])   # Get the video's thumbnail.
                            channelTitle = str(item2['snippet']['channelTitle'])   # Get the channel name which the video belongs to.

                            try:
                                tags = str(item2['snippet']['tags'])    # Get the video's tags.
                            except:
                                tags = "No tags"

                            contentDetails = str(item2['contentDetails']['duration'])   # Get the length of the video. The property value is an ISO 8601 duration.

                        if (self.verbose):
                            try:
                                print("publishedAt: " + str(publishedAt))
                                print("channelId: " + str(channelId))
                                print("title: " + str(title))
                                print("video like: " + str(video_like)) 
                                print("description: " + str(description))
                                print("thumbnails: " + str(thumbnails))
                                print("channelTitle: " + str(channelTitle))
                                print("tags: " + str(tags))
                                print("contentDetails: " + str(contentDetails))
                            except:
                                pass

                            print("--------------------------------------------------")

                        break

                elif(not self.take_comments and videoId not in video_id_list):
                    while(response2):
                        time.sleep(1)
                        k = 0
                        for (index2,item2) in enumerate(response2['items']):

                            publishedAt = str(item2['snippet']['publishedAt'])  # Get the date and time that the video was published.
                            channelId = str(item2['snippet']['channelId'])  # Get the ID that YouTube uses to uniquely identify the channel that the video was uploaded to.
                            title = str(item2['snippet']['title'])  # Get the video's title.
                            video_like = str(item2['statistics']['likeCount'])

                            try:
                                description = str(item2['snippet']['description'])  # Get the video's description.
                            except:
                                description = "No description"

                            thumbnails = str(item2['snippet']['thumbnails']["default"]["url"])   # Get the video's thumbnail.
                            channelTitle = str(item2['snippet']['channelTitle'])   # Get the channel name which the video belongs to.

                            try:
                                tags = str(item2['snippet']['tags'])    # Get the video's tags.
                            except:
                                tags = "No tags"

                            contentDetails = str(item2['contentDetails']['duration'])   # Get the length of the video. The property value is an ISO 8601 duration.

                        if (self.verbose):
                            try:
                                print("publishedAt: " + str(publishedAt))
                                print("channelId: " + str(channelId))
                                print("title: " + str(title))
                                print("video like: " + str(video_like)) 
                                print("description: " + str(description))
                                print("thumbnails: " + str(thumbnails))
                                print("channelTitle: " + str(channelTitle))
                                print("tags: " + str(tags))
                                print("contentDetails: " + str(contentDetails))
                            except:
                                pass

                            print("--------------------------------------------------")

                        break

                if(self.take_comments):
                    comments.append([videoId, number_of_replies, author, display_text, original_text, likes, 
                                     published_time, update_time, can_reply, is_public, viewer_rating, 
                                     publishedAt, channelId, title, description, thumbnails, channelTitle, 
                                     tags, contentDetails, author_profile_image, replies, video_like])

                elif(not self.take_comments and videoId not in video_id_list):
                    comments.append([videoId, publishedAt, channelId, title, description, thumbnails, channelTitle, 
                                     tags, contentDetails, video_like])
                    
                video_id_list.append(videoId)
            if(self.json_parser):
                if(self.take_comments):
                    data = pd.DataFrame(comments,columns=['videoId','number_of_replies','author','display_text','original_text',
                                                           'likes','published_time','update_time','can_reply','is_public',
                                                           'viewer_rating', 'video_publishedAt', 'channelId', 'video_title',
                                                           'video_description', 'thumbnail', 'channelTitle', 'tags', 
                                                           'video_duration', 'author_profile_image', 'replies', 'video_like'])
                else:
                    data = pd.DataFrame(comments,columns=['videoId', 'video_publishedAt', 'channelId', 'video_title',
                                                           'video_description', 'thumbnail', 'channelTitle', 'tags', 
                                                           'video_duration', 'video_like'])
                comments = []
                # Save the data.
                if(os.path.exists("./youtube_data.csv")):         # If an old dataset exists, we concatenate it with the new data.
                    data2 = pd.read_csv("./youtube_data.csv")
                    full_data = pd.concat([data2, data], axis=0)
                    full_data.to_csv("./youtube_data.csv", index=False)
                    full_data = pd.read_csv("./youtube_data.csv")				
                    full_data.drop_duplicates(inplace=True)		
                    full_data.reset_index(drop=True, inplace=True)
                    full_data.to_csv("./youtube_data.csv", index=False)

                else:   # Else, we create a new dataset.
                    data.to_csv("./youtube_data.csv", index=False)

                if(self.take_comments):
                    self.save_data_json('youtube_data', ('videoId','number_of_replies','author','display_text','original_text',
                                                         'likes','published_time','update_time','can_reply','is_public',
                                                         'viewer_rating', 'video_publishedAt', 'channelId', 'video_title',
                                                         'video_description', 'thumbnail', 'channelTitle', 'tags', 
                                                         'video_duration', 'author_profile_image', 'replies', 'video_like'))
                else:
                    self.save_data_json('youtube_data', ('videoId', 'video_publishedAt', 'channelId', 'video_title',
                                                         'video_description', 'thumbnail', 'channelTitle', 'tags', 
                                                         'video_duration', 'video_like'))
            else:
                if(self.take_comments):
                    dict = {}
                    comments_json = []
                    data_return = []
                    videoId_list = []
                    for i in range(len(comments)):
                        if(comments[i][0] not in videoId_list):
                            dict['channelId'] = comments[i][12]
                            dict['channelTitle'] = comments[i][16]
                            dict['videoId'] = comments[i][0]
                            dict['video_title'] = comments[i][13]
                            dict['video_description'] = comments[i][14]  
                            dict['video_publishedAt'] = comments[i][11]
                            dict['thumbnail'] = comments[i][15]            
                            dict['tags'] = comments[i][17]
                            dict['video_duration'] = comments[i][18]
                            dict['video_like'] = comments[i][21]

                            for j in range(len(comments)):
                                if(comments[i][0] == comments[j][0] and comments[j][0] not in videoId_list):
                                    dict2 = {}

                                    dict2['number_of_replies'] = comments[j][1]
                                    dict2['author'] = comments[j][2]
                                    dict2['display_text'] = comments[j][3]
                                    dict2['original_text'] = comments[j][4]
                                    dict2['likes'] = comments[j][5]
                                    dict2['published_time'] = comments[j][6]
                                    dict2['update_time'] = comments[j][7]
                                    dict2['can_reply'] = comments[j][8]
                                    dict2['is_public'] = comments[j][9]
                                    dict2['viewer_rating'] = comments[j][10]
                                    dict2['author_profile_image'] = comments[j][19]
                                    dict2['replies'] = comments[j][20]
                                    comments_json.append(dict2)
                            dict['comments'] = comments_json
                            comments_json = []

                            data_return.append(dict)
                            dict = {}
                        videoId_list.append(comments[i][0])

                    return data_return
                else:
                    dict = {}
                    comments_json = []
                    for i in range(len(comments)):
                        dict['channelId'] = comments[i][2]
                        dict['channelTitle'] = comments[i][6]
                        dict['videoId'] = comments[i][0]
                        dict['video_title'] = comments[i][3]
                        dict['video_description'] = comments[i][4]  
                        dict['video_publishedAt'] = comments[i][1]
                        dict['thumbnail'] = comments[i][5]            
                        dict['tags'] = comments[i][7]
                        dict['video_duration'] = comments[i][8]
                        dict['video_like'] = comments[i][9]
                        comments_json.append(dict)
                        dict = {}
                    return comments_json
				
            if('nextPageToken' in self.response):   # Go to the next page.
                try:
                    self.response = self.youtube.commentThreads().list(part="snippet,replies",
                                                                       allThreadsRelatedToChannelId=channelId,
                                                                       pageToken = self.response['nextPageToken'],
                                                                       maxResults=100).execute()
                except:
                    break
            else:
                break
       

                
if __name__ == "__main__":
    getAuthenticated = GetAuthenticated()
    youtube = getAuthenticated.get_authenticated()
    
    request = youtube.channels().list(
        part="id",
        forUsername="pewdiepie"
    )
    response = request.execute()
    
    getComments = GetComments(response, youtube)
    getComments.get_comments()