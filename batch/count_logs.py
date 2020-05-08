import csv
import time
from elasticsearch import Elasticsearch


# might need refactor to index the es first to see what the views is and then update based on the larger one
# seems like a most advanced thing tho
def main():
    print('Starting Count Logs ES Updating Loop')
    es = Elasticsearch(['es'])
    while True:
        try:
            product_to_views = {}
            print('Updating Count Logs ES')
            with open('./data/viewLogs.csv', 'r') as logfile:
                csv_reader = csv.reader(logfile)
                for row in csv_reader:
                    # row[0] is user_id #row[1] is product_id
                    # reading file for the first time so skip the name line
                    if row[0] == 'user_id':
                        continue
                    get_cur_views = product_to_views.get(row[1], 0)
                    product_to_views[row[1]] = get_cur_views + 1
            for product, views in product_to_views.items():
                # print("updating ES logs for product_id: " +
                #       str(product) + " to views: " + str(views))
                # print("<------------------->")
                index = es.update(
                    index='listing_index', id=product, body={
                        "script": {
                            "source": "ctx._source.views = params.views",
                            "params": {
                                "views": views
                            }
                        }
                    })
                es.indices.refresh(index="listing_index")
            # periodically count logs and update docs
            time.sleep(5)
        except Exception as e:
            print('Count_logs Error: ' + str(e))
            time.sleep(12)


if __name__ == "__main__":
    main()
