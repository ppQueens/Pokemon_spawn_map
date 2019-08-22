import boto3
from botocore.exceptions import NoCredentialsError

# ACCESS_KEY = 'AKIAVLDKGU6Y6TAFUQ4B'
# SECRET_KEY = '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'
# backet_name = 'pokemon-map-spawn'
#
# def upload_to_aws(local_file, bucket):
#     s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
#                       aws_secret_access_key=SECRET_KEY)
#
#     try:
#         s3.upload_file(local_file, bucket, local_file, ExtraArgs={'ACL':'public-read'})
#         print("Upload Successful")
#         return True
#     except FileNotFoundError:
#         print("The file was not found")
#         return False
#     except NoCredentialsError:
#         print("Credentials not available")
#         return False
#
#
# uploaded = upload_to_aws('test_aws_2.txt', backet_name)
# import json
# with open('teece.json', 'r+') as jsn:
#     jsdict = json.load(jsn)
#     jsdict['1']['2'] = 'test.xml'
#     z = json.dumps(jsdict)
#     jsn.seek(0)
#     jsn.write(z)

from geopy.distance import distance
import random
import itertools

start_point = 46.851157, 35.378227

left_top_point = 46.857157, 35.375227
left_bottom_point = 46.847157, 35.375227

right_top_point = 46.857157, 35.385227
right_bottom_point = 46.847157, 35.385227

c_range = -.003, .003

points = [left_top_point, left_bottom_point, right_top_point, right_bottom_point]
for i in range(50):
    lat = random.uniform(*c_range)
    # print(lat)
    lon = random.uniform(*c_range)
    points.append(tuple(map(lambda x: round(x, 6), (start_point[0] + lat, start_point[1] + lon))))

only_30_m = set()
# for p1 in points[4:]:
#     b = True
#     for p2 in points[4:]:
#         if p1 != p2 and p1 not in only_30_m:
#             f = distance(p1, p2).km
#             if f < 0.03:
#                 only_30_m.update((p1,p2))


# for i in only_30_m:
#     print(*i)

import networkx as nx
from networkx.algorithms.approximation.clique import max_clique

g = itertools.combinations(points[4:], 2)

graph = nx.Graph()
for i in g:
    f = distance(i[0], i[1]).km
    if f <= 0.03:
        graph.add_edge(*i)
        # print(*i)

# graph = nx.Graph()

# graph.add_edge((3, 4), (5, 5))
# graph.add_edge((3, 4), (7, 4))
# print(graph.number_of_nodes())

# print(graph.number_of_nodes())
print(max_clique(graph))
# print(tuple(g))
