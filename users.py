from pymongo import MongoClient
import config as config

client = MongoClient(config.get_setting("mongo-db-conn", "null"))
db = client.restberry

def find_user(username):
    user = {
        "username" : username
    }
    res = db.users.find_one(user)
    if res:
        u = {
            "username" : res["username"],
            "password" : res["password"],
            "privileges": res["privileges"]
        }
        return True, u
    return False, None

def add_user(username, password):
    succ, us = find_user(username)
    if succ:
        return False, None
    
    user = {
        "username" : username,
        "password" : password,
        "privileges" : []
    }
    db.users.insert_one(user)
    return True, user

def validate_user(username, password):
    succ, user = find_user(username)
    if succ:
        if user["password"] == password:
            return True
    return False

def has_privilege(username, priv):
    succ, user = find_user(username)
    if succ:
        if "super" in user["privileges"]:
            return True

        return priv in user["privileges"]
    else:
        return False

def add_privilege(username, priv):
    succ, user = find_user(username)
    if succ:
        query = {"username" : username}
        newVal = {"$set" : { "privileges" : [priv.lower()] + user["privileges"]}}
        db.users.update_one(query, newVal)
        succ, user = find_user(username)
        return True, user
    else:
        return False, None

def remove_privilege(username, priv):
    succ, user = find_user(username)
    if succ:
        query = {"username" : username}
        user["privileges"].remove(priv)
        newVal = {"$set" : { "privileges" : user["privileges"]}}
        db.users.update_one(query, newVal)
        succ, user = find_user(username)
        return True, user
    else:
        return False, None