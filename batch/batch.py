from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import time


def main():
    print('Starting Kafka listing consumer loop')
    es = Elasticsearch(['es'])
    while True:
        try:
            # print('hello from listing')
            consumer = KafkaConsumer(
                'new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
            print('consumer: ' + consumer)
            for message in consumer:
                print('in messages')
                item = json.loads((message.value).decode('utf-8'))
                index = es.index(
                    index='listing_index', doc_type='listing', id=item['product_id'], body=item)
                es.indices.refresh(index="listing_index")
                print(item)
                print(index)
            print('at end')
        except:
            print('Kafka server not online')
            time.sleep(5)


if __name__ == "__main__":
    main()
