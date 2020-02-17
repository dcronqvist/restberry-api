from mymongo import client
import config as config

db = client.restberry

def find_user(username):
    user = {
        "username" : username
    }
    res = db.users.find_one(user)
    if res:
        u = {
            "username" : res["username"],
            "password" : res["password"]
        }
        return True, u
    return False, None

def add_user(username, password):
    user = {
        "username" : username,
        "password" : password
    }
    db.users.insert_one(user)
    return True