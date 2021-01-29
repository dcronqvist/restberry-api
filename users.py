from pymongo import MongoClient
import config as config
import datetime
import uuid

client = MongoClient(config.get_setting("mongo-db-conn", "null"))
db = client.restberry

def find_user(username):
    user = {
        "username" : username
    }
    res = db.users.find_one(user)
    if res:
        del res['_id']
        return True, res
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

def get_all_tokens_for_user(username):
    succ, user = find_user(username)
    if succ:
        return True, user["tokens"]
    else:
        return False, None

def validate_token_for_user(username, token):
    # tokens are valid for 30 minutes
    token_timeout = 30 * 60
    succ, tokens = get_all_tokens_for_user(username)
    if succ:
        check = [tokenobj for tokenobj in tokens if ((tokenobj["created"] + token_timeout) > datetime.datetime.now().timestamp()) and (tokenobj["token"] == token)]
        if len(check) > 0:
            return True, check

        filt = {"username": username }
        query = { "$set": { "tokens": check } }
        db.users.update_one(filt, query)
        return False, check
    return False, None

def create_token_for_user(username):
    succ, user = find_user(username)
    if succ:
        new_token = uuid.uuid4()
        succ, tokens = validate_token_for_user(username, new_token)
        succ, tokens = get_all_tokens_for_user(username)
        tokens.append({ "token": str(new_token), "created": round(datetime.datetime.now().timestamp()) })
        filt = {"username": username}
        query = { "$set": { "tokens": tokens } }
        db.users.update_one(filt, query)
        return True, tokens
    else:
        return False, None