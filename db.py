from pymongo import MongoClient
import config as config

db_conn = MongoClient(config.get_setting("mongo-db-conn", "null"))
db = db_conn.restberry

coll_trans = db.transactions
coll_accounts = db.accounts

def stringify_ids(docs):
    """
    Expects docs to be a list of documents, not a cursor.
    """
    for doc in docs:
        doc["_id"] = str(doc["_id"])
    return docs