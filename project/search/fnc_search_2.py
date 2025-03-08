from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import json
from pprint import PrettyPrinter
load_dotenv(find_dotenv())

password = os.getenv("MONGO_PASSWORD")
connect_string=f'mongodb://{password}:27017'
client = MongoClient(connect_string)

mealmatch_db = client.mealmatch_db
restaurants=mealmatch_db.restaurants

printer = PrettyPrinter()
def fuzzy_matching():
    result=restaurants.aggregate([
        {
            "$search": {
                "index": "language_search",
                "text": {
                    "query": "computer",
                    "path": "category",
                    # "fuzzy" : {} #Hiểu rằng ko nhất thiết phải là chữ computer oàn toàn mà có thể sai chính tả nó ẫn truy xuất được
                    "synonyms":"mapping"
                }
            }
        }
    ])
    printer.pprint(list(result))

fuzzy_matching()