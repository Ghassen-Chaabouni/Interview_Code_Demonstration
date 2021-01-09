#!/usr/bin/env python
# coding: utf-8

import youtube_driver.get_authenticated as GetAuthenticated
import youtube_driver.get_comments as GetComments
import youtube_driver.get_images as GetImages
import time
		
import sys
import click

@click.command()
@click.option('--keys', '-k', multiple=True, default=[], help='A list of video names that we are searching.')

def main(keys):

    ''' 
    Scraping conversations in youtube based on the video names.
    '''

    keys = list(keys)
    file_pos = 0
    if (len(keys) > 0):   # If code_secret_file_name and keys are specified.
        click.echo('reading from arguments')
        getAuthenticated = GetAuthenticated.GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
        youtube, file_num = getAuthenticated.get_authenticated()
        for key in keys:   
            # Start searching for the video.
            while(file_pos < file_num):
                    try:
                        request = youtube.search().list(
                                part="snippet",
                                maxResults=25,
                                q=str(key)
                            )
                        response = request.execute()
                        break
                    except:
                        file_pos += 1
                        getAuthenticated = GetAuthenticated.GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
                        youtube, file_num = getAuthenticated.get_authenticated()
                        pass
            while(response):
                time.sleep(1)
                for (index,item) in enumerate(response['items']):
                        while(file_pos < file_num):
                            try:
                                try:
                                    videoId = str(item['id']['videoId'])   # Get the video id.
                                except:
                                    continue
                                # Start scraping the video comments.
                                request2 = youtube.commentThreads().list(
                                    part="snippet,replies",
                                    videoId=str(videoId)
                                )
                                try:
                                    response2 = request2.execute()
                                except:  # The video is private.
                                    continue

                                getComments = GetComments.GetComments(response2, youtube)
                                getComments.get_comments()
                                break
                            except:
                                file_pos += 1
                                getAuthenticated = GetAuthenticated.GetAuthenticated(file_pos)    # Read authentification informations from code_secret_file
                                youtube, file_num = getAuthenticated.get_authenticated()
                                pass

    if(len(keys) == 0):
        click.echo('Missing key')	

		