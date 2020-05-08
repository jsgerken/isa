from pyspark import SparkContext
import urllib.request
import urllib.parse
import json
import time
import csv

# ####################
# Helper functions for HTTP request


def fetch(url):
    try:
        req = urllib.request.Request(url)
        return json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    except Exception as e:
        return {
            'error': 'Failed to fetch from ' + url,
            'errReason':  'Message: ' + str(e)
        }


def post(data, url):
    try:
        data = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request(url, data=data)
        return json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    except Exception as e:
        return {
            'error': 'Failed to post to ' + url,
            'errReason':  'DEV_MODE_MESSAGE: ' + str(e)
        }

# Helper functions for HTTP request
# ####################


# Helper function for transforming spark RDD
def list_to_pair_list(user_id, products_list):
    result = []
    for left in products_list:
        for right in products_list:
            if left != right:
                result.append(((left, right), user_id))
    return result


# Run the spark programming


def run_spark(sc):
    # each worker loads a piece of the data file
    data = sc.textFile("/tmp/data/viewLogs.csv", 2)
    # Read data in as pairs of (user_id, item_id clicked on by the user)
    pairs = data.map(lambda line: line.split(","))
    # Group data into (user_id, list of item ids they clicked on)
    #   When called on a dataset of (K, V) pairs, returns a dataset of (K, Iterable<V>) pairs.
    grouped_by_key = pairs.groupByKey()
    # Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
    user_pairs = grouped_by_key.flatMap(
        lambda pair: list_to_pair_list(pair[0], pair[1]))
    # Remove duplicate pairings using distinct
    user_pairs_distinct = user_pairs.distinct()
    # Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
    group_items_users = user_pairs_distinct.groupByKey()
    # Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
    group_items_distinct = group_items_users.map(
        lambda pair: (pair[0], len(pair[1])))
    # Filter out any results where less than 3 users co-clicked the same pair of items
    filter_greater_3 = group_items_distinct.filter(
        lambda pair: pair[1] >= 3)
    spark_output = filter_greater_3.collect()
    print(spark_output)
    print("Popular items done")
    sc.stop()
    print('FINISHED – rec_spark.py')
    return spark_output


# save spark output to db
def save_to_db(spark_output):
    product_dict = {}

    def get_and_append(get_prd, append_prd):
        get_product_set = product_dict.get(get_prd, set())
        get_product_set.add(append_prd)
        product_dict[get_prd] = get_product_set

    for pairs in spark_output:
        product_pair = pairs[0]
        get_and_append(product_pair[0], product_pair[1])
        # I dont think i need to do the reverse since it prob exist in the data but i'll do it just in case
        get_and_append(product_pair[1], product_pair[0])

    for product_id, new_list in product_dict.items():
        try:
            # do a models get for the list for this product id
            fetch_old_list = fetch(
                'http://models:8000/api/v1/recommendations/get-or-create/' + str(product_id))
            if 'error' in fetch_old_list:
                raise Exception(fetch_old_list)
            old_list = fetch_old_list['recommended_items']
            new_list_as_csv = ','.join(new_list)
            final_list = ""
            # if string is empty i.e. first time being made
            if not old_list:
                final_list = new_list_as_csv
            else:
                final_list = old_list + ',' + new_list_as_csv
            # do a update to models here
            post_data = {
                'recommended_items': final_list
            }
            req_dict = post(
                post_data, 'http://models:8000/api/v1/recommendations/update/' + str(product_id))
            if 'error' in req_dict:
                raise Exception(req_dict)
            print(req_dict)
            product_dict[product_id] = req_dict
        except Exception as e:
            print({
                'error': "failed to update db for this tuple: " + str((product_id, new_list)),
                'error_reason': str(e)
            })
            product_dict[product_id] = str(e)

    print("All product's and their request output")
    print(product_dict)


def main():
    while True:
        try:
            sc = SparkContext("spark://spark-master:7077", "PopularItems")
            spark_output = run_spark(sc)
            sc.stop()
            print('Saving output to output.log!')
            with open('/tmp/data/output.log', 'w') as logfile:
                csvwriter = csv.writer(logfile)
                for pairs in spark_output:
                    csvwriter.writerow([pairs])
            print('Finished saving output')
            save_to_db(spark_output)
            # Run on interval
            print('sleeping @ 90 sec - 1.5 min')
            print('===========================')
            time.sleep(90)
        except Exception as e:
            print({
                'error': "rec_spark FAILED",
                'error_reason': str(e)
            })
            sc.stop()
            # Run on interval
            print('sleeping after exception @ 90 sec - 1.5 min')
            print('===========================')
            time.sleep(90)


if __name__ == "__main__":
    main()
