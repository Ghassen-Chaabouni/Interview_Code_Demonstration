#!/usr/bin/env python
# coding: utf-8

import store_elasticsearch.connect_elasticsearch as  ConnectElasticsearch 

class CreateIndex:
    def __init__(self, es_object, index_name, settings):

        ''' 
        Reads the value of elasticsearch object, index_name and the settings.
        '''

        self.es_object = es_object
        self.index_name = index_name
        self.settings = settings

    def create_index(self):

        ''' 
        Create an index if it doesn't exist.
        '''

        created = False
        try:
            if not self.es_object.indices.exists(self.index_name):   # if the index doesn't exist.
                # Ignore 400 means to ignore "Index Already Exist" error.
                self.es_object.indices.create(index=self.index_name, ignore=400, body=self.settings)
                print('Created Index')
            created = True
        except Exception as ex:
            print(str(ex))
        finally:
            return created    # True or False.

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    connectElasticsearch = ConnectElasticsearch('localhost', 9200)
    es_object = connectElasticsearch.connect_elasticsearch()
    
    index_name = "testtt"
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "discord-driver": {
                "dynamic": "strict",
                "properties": {
                    "property1": {
                        "type": "text"
                    },
                    "property2": {
                        "type": "text"
                    },
                    "property3": {
                        "type": "text"
                    }
                }
           }
        }
    }
        
    createIndex = CreateIndex(es_object, index_name, settings)
    created = createIndex.create_index()