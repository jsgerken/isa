from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import time


def main():
    print('Starting Kafka Listing consumer loop')
    es = Elasticsearch(['es'])
    while True:
        try:
            consumer = KafkaConsumer(
                'new-listings-topic',
                group_id='listing-indexer',
                bootstrap_servers=['kafka:9092'],
                consumer_timeout_ms=5500)
            for message in consumer:
                item = json.loads((message.value).decode('utf-8'))
                index = es.index(
                    index='listing_index', doc_type='listing', id=item['product_id'], body=item)
                es.indices.refresh(index="listing_index")
                print(item)
                print(index)
                # sleep to wait for new messages (temp fix)
                # time.sleep(3)
            print("closing consumer in Listing")
            consumer.close()
        except Exception as e:
            print('Kafka server not online - ' + str(e))
            time.sleep(10)


if __name__ == "__main__":
    main()
