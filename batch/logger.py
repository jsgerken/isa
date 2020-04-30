from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import time


def main():
    print('Starting Kafka logger consumer loop')
    es = Elasticsearch(['es'])
    while True:
        try:
            print('hello from logger')
            time.sleep(10)
            # consumer = KafkaConsumer(
            #     'new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
            # for message in consumer:
            #     item = json.loads((message.value).decode('utf-8'))
            #     index = es.index(
            #         index='listing_index', doc_type='listing', id=item['product_id'], body=item)
            #     es.indices.refresh(index="listing_index")
            #     print(item)
            #     print(index)
        except:
            print('Kafka server not online')
            time.sleep(5)


if __name__ == "__main__":
    main()
