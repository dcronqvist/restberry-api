from pymongo import MongoClient
import config as config

s = config.get_setting("mongo-db-conn", "null")
client = MongoClient(s)

