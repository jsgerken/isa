from kafka import KafkaProducer
from elasticsearch import Elasticsearch
import time
import json
import urllib.request


def fetch(url):
    try:
        req = urllib.request.Request(url)
        return json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    except Exception as e:
        return {
            'error': 'Failed to fetch from ' + url,
            'errReason': 'Message: ' + str(e)
        }


def main():
    print('Starting Index ES Fixtures Script')
    es = Elasticsearch(['es'])
    while True:
        try:
            print('Attempting index Products into ES')
            es = Elasticsearch(['es'])
            es.indices.delete(index='listing_index')
            print("es listing_index data deleted succesfully")
            prods = fetch('http://models:8000/api/v1/products/')
            all_prods = prods['allProducts']
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
            for product in all_prods:
                producer.send('new-listings-topic',
                              json.dumps(product).encode('utf-8'))
            producer.flush()
            producer.close()
            print('Products from db indexed into ES successfully!')
            return
        except Exception as e:
            print('ES Container or Kafka not online - ' + str(e))
            time.sleep(35)


if __name__ == "__main__":
    main()
