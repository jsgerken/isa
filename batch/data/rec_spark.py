from pyspark import SparkContext


def list_to_pair_list(user_id, products_list):
    result = []
    for left in products_list:
        for right in products_list:
            if left != right:
                result.append(((left, right), user_id))
    return result


sc = SparkContext("spark://spark-master:7077", "PopularItems")

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
filter_greater_3 = group_items_distinct.filter(lambda pair: pair[1] >= 3)
output = filter_greater_3.collect()
print(output)
print("Popular items done")
sc.stop()
print('FINISHED – rec_spark.py')

# ----------------------- saving output to db
# product_dict = {}
# for
