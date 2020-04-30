from kafka import KafkaConsumer
import json
import time
import csv
import os


def main():
    print('Starting Logger Consumer Loop')
    while True:
        try:
            consumer = KafkaConsumer(
                'new-logs-topic', group_id='logs-indexer', bootstrap_servers=['kafka:9092'],
                # if in 5 ms it doesn't receive a message , close the consumer and restart
                consumer_timeout_ms=5000
            )
            for message in consumer:
                file_exist = os.path.isfile('viewLogs.csv')
                item = json.loads((message.value).decode('utf-8'))
                print('Updating in logger for : ' + str(item))
                # a means append to file
                with open('viewLogs.csv', 'a') as logfile:
                    csvwriter = csv.writer(logfile)
                    if not file_exist:
                        csvwriter.writerow(['user_id', 'product_id'])
                    csvwriter.writerow([item['user_id'], item['product_id']])
                # sleep to wait for new logs
                # time.sleep(5)
            print("closing consumer in logger")
            consumer.close()
        except Exception as e:
            print('Kafka server not online - Logger: ' + str(e))
            time.sleep(11)


if __name__ == "__main__":
    main()
