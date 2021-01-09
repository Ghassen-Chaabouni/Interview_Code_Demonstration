#!/usr/bin/env python
# coding: utf-8

import store_elasticsearch.connect_elasticsearch as  ConnectElasticsearch 
import store_elasticsearch.create_index as  CreateIndex


class StoreRow:
    def __init__(self, es_object, index_name, _type="data"):

        ''' 
        Reads the value of elasticsearch object, index_name and the data type.
        '''

        self.es_object = es_object
        self.index_name = index_name
        self._type = _type
    
    def store_row(self, data_row):

        ''' 
        Store the data in Elasticsearch.
        '''

        try:
            outcome = self.es_object.index(index=self.index_name, doc_type=self._type, body=data_row)   # Store the data in Elasticsearch.
       
        except Exception as ex:
            print('Error in indexing data')
            print(str(ex))

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    connectElasticsearch = ConnectElasticsearch('localhost', 9200)
    es_object = connectElasticsearch.connect_elasticsearch()
    
    index_name = "ttttestt"
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
    
    _type = "data"
    data_json = [{"property1": "test1", "property2": "test2", "property3": "test3"},
                 {"property1": "test11", "property2": "test22", "property3": "test33"}]
    

    storeRow = StoreRow(es_object, index_name, _type)
    for data_row in data_json:  # Insert each row.
        storeRow.store_row(data_row)
  