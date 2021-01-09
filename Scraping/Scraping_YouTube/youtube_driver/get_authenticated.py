#!/usr/bin/env python
# coding: utf-8

import os
import pickle
import pandas as pd

import google_auth_oauthlib.flow
import googleapiclient.discovery   # pip install google-api-python-client | pip install protobuf==3.12.2 | pip install --upgrade protobuf --force-reinstall
import googleapiclient.errors
from google.auth.transport.requests import Request    # pip install google
from os import listdir
from os.path import isfile, join
import os
import sys

class GetAuthenticated:
    def __init__(self, file_pos):

        ''' 
        Reads the value of file_pos.
        '''

        self.file_pos = file_pos
	
    def get_authenticated(self):

        ''' 
        Authentication process.
        '''
        path = self.determine_path () + "/config/"
        try:
            os.remove(path + "token.pickle")
        except:
            pass

        file_list = [f for f in listdir(path) if isfile(join(path, f))]
        i = 0
        b = 0
        for code_secret_file_name in file_list:
            if("secret" in code_secret_file_name):
                if(i == self.file_pos):
				
                    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

                    # Get credentials and create an API client
                    api_service_name = "youtube"
                    api_version = "v3"
                    client_secrets_file = self.determine_path () + "/config/" + code_secret_file_name

                    credentials = None
                    if os.path.exists(self.determine_path () + "/config/token.pickle"+str(self.file_pos)):
                        with open(self.determine_path () + "/config/token.pickle"+str(self.file_pos), 'rb') as token:
                            credentials = pickle.load(token)
                    #  Check if the credentials are invalid or do not exist
                    if not credentials or not credentials.valid:
                        # Check if the credentials have expired
                        if credentials and credentials.expired and credentials.refresh_token:
                            credentials.refresh(Request())
                        else:
                            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                                client_secrets_file, scopes)
                            credentials = flow.run_console()
                        with open(self.determine_path () + "/config/token.pickle"+str(self.file_pos), 'wb') as token:
                            pickle.dump(credentials, token)
                    youtube = googleapiclient.discovery.build(
                    api_service_name, api_version, credentials=credentials)
                    b = 1
                    break
                i += 1
        if(not b):
            print('Error')
        return youtube, len(file_list)
		
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
			

if __name__ == "__main__":
    getAuthenticated = GetAuthenticated()
    youtube = getAuthenticated.get_authenticated()