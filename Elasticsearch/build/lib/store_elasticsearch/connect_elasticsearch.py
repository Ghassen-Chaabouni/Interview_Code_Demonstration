import logging
from elasticsearch import Elasticsearch

class ConnectElasticsearch:
    def __init__(self, host='localhost', port=9200):

        ''' 
        Reads the value of the host and the port.
        '''	

        self.host = host
        self.port = port 
    def connect_elasticsearch(self):
        es_object = None
        es_object = Elasticsearch([{'host': self.host, 'port': self.port}])   # Connect to Elasticsearch.
        if es_object.ping():     # If we can ping then we are connected.
            print('Connect')
        else:
            print('Could not connect!')
        return es_object
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    connectElasticsearch = ConnectElasticsearch('localhost', 9200)
    es_object = connectElasticsearch.connect_elasticsearch()
