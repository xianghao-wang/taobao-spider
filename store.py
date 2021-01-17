import os
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGO_URL'))
db = client[os.getenv('MONGO_DB')]
collection = db[os.getenv('MONGO_COLLECTION')]

def save_to_mongo(item):
    try:
        collection.insert_one(item)
    except Exception:
        print('存储到MongoDB失败: ' + str(item))