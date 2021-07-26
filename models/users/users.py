from pymongo import MongoClient
import config as config
import datetime
import uuid

class UsersClient(object):
    def __init__(self):
        self.client = MongoClient(config.get_setting("mongo-db-conn", "null"))
        self.db = self.client.restberry_api

    def find_user(self, username):
        user = {
            "username" : username
        }
        res = self.db.users.find_one(user)
        if res:
            del res['_id']
            return True, res
        return False, None

    def add_user(self, username, password):
        succ, us = self.find_user(username)
        if succ:
            return False, None
        
        user = {
            "username" : username,
            "password" : password,
            "privileges" : [],
            "tokens": []
        }
        self.db.users.insert_one(user)
        return True, user

    def validate_user(self, username, password):
        succ, user = self.find_user(username)
        if succ:
            if user["password"] == password:
                return True
        return False

    def has_privilege(self, username, priv : str):
        succ, user = self.find_user(username)
        if succ:
            if "super" in user["privileges"]:
                return True

            return priv.lower() in user["privileges"]
        else:
            return False

    def add_privilege(self, username, priv : str):
        succ, user = self.find_user(username)
        if succ:
            query = {"username" : username}
            newVal = {"$set" : { "privileges" : [priv.lower()] + user["privileges"]}}
            self.db.users.update_one(query, newVal)
            succ, user = self.find_user(username)
            return True, user
        else:
            return False, None

    def remove_privilege(self, username, priv):
        succ, user = self.find_user(username)
        if succ:
            query = {"username" : username}
            user["privileges"].remove(priv.lower())
            newVal = {"$set" : { "privileges" : user["privileges"]}}
            self.db.users.update_one(query, newVal)
            succ, user = self.find_user(username)
            return True, user
        else:
            return False, None

    def get_all_tokens_for_user(self, username):
        succ, user = self.find_user(username)
        if succ:
            return True, user["tokens"]
        else:
            return False, None

    def validate_token_for_user(self, username, token):
        # tokens are valid for 30 minutes
        token_timeout = config.get_setting("token-lifetime-minutes", 30) * 60
        succ, tokens = self.get_all_tokens_for_user(username)
        if succ:
            check = [tokenobj for tokenobj in tokens if ((tokenobj["created"] + token_timeout) > datetime.datetime.now().timestamp()) or (tokenobj["token"] == token)]
            filt = {"username": username }
            query = { "$set": { "tokens": check } }
            self.db.users.update_one(filt, query)
            if len(check) > 0:
                return True, check
            return False, check
        return False, None

    def create_token_for_user(self, username):
        succ, user = self.find_user(username)
        if succ:
            new_token = uuid.uuid4()
            succ, tokens = self.get_all_tokens_for_user(username)
            tok = { "token": str(new_token), "created": round(datetime.datetime.now().timestamp()) }
            tokens.append(tok)
            filt = {"username": username}
            query = { "$set": { "tokens": tokens } }
            self.db.users.update_one(filt, query)
            succ, tokens = self.validate_token_for_user(username, new_token)
            return True, tok
        else:
            return False, None

    def get_username_from_token(self, token):
        user = {
            "tokens" : {
                "$elemMatch": {
                    "token": token
                }
            }
        }
        res = self.db.users.find_one(user)
        if res:
            del res['_id']
            return True, res["username"]
        return False, None

    def token_has_privilege(self, token, privilege):
        succ, username = self.get_username_from_token(token)
        return self.has_privilege(username, privilege)

    def token_has_privileges(self, token, privileges):
        succ, username = self.get_username_from_token(token)
        for p in privileges:
            if not self.has_privilege(username, p):
                return False
        return True

    def get_valid_token(self, username):
        succ, user = self.find_user(username)
        if succ:
            succ, tokens = self.get_all_tokens_for_user(username)
            if succ:
                check = [tokenobj for tokenobj in tokens if ((tokenobj["created"] + config.get_setting("token-lifetime-minutes", 30) * 60) > datetime.datetime.now().timestamp())]
                if len(check) > 0:
                    return check[0]["token"]
                else:
                    return self.create_token_for_user(username)[1]["token"]
        return None
            


user_client = UsersClient()