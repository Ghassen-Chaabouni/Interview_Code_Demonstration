#!/usr/bin/env python
# coding: utf-8

from .connect_elasticsearch import ConnectElasticsearch
from .create_index import CreateIndex
from .store_row import StoreRow 
from .store_profile import StoreProfile
from .store_comment import StoreComment
from .create_tables import CreateTables
import re

from abc import ABC

__version__ = '1.0.0'

class Store(ABC):
    def search(self, **kwargs):
        pass
    

class StoreElasticsearch(Store):
    def search(self, **kwargs):
        for dict in kwargs.values(): 
            for dict_key in dict.keys(): 
                if (dict_key == 'job_name'):
                    job_name = str(dict[dict_key])       # Store the job name.
                elif (dict_key == 'search_by'):
                    search_by = str(dict[dict_key])  
                elif (dict_key == 'table_name'):
                    table_name = str(dict[dict_key])     
                elif (dict_key == 'key'):
                    key = str(dict[dict_key])         
                elif (dict_key == 'host'):
                    host = (dict[dict_key])             # Store the host.
                elif (dict_key == 'port'):
                    port = int(dict[dict_key])             # Store the port.

        connectElasticsearch = ConnectElasticsearch(host, port)    # Connect to Elasticsearch.
        es_object = connectElasticsearch.connect_elasticsearch()
			
        print('searching for ' + key + " in " + table_name)
        query_body = {
            "query": {
                "match": {
                    search_by : key
                }
            }
        }
        result = es_object.search(index=job_name + "-" + table_name, body=query_body)
        return result
