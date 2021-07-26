import datetime
import graphene
import requests as req
import config as conf
from models.users.users import user_client
from models.economy.periods import get_dates_month_period
from db import coll_accounts, coll_trans

dev_user = conf.get_setting("dev-user", None)

def get_token_from_info(info, require_token=False) -> str:
    if "Authorization" in info.context.headers:
        print(info.context.headers["Authorization"])
        return info.context.headers["Authorization"]
    else:
        if require_token:
            raise Exception("Must specify 'Authorization' header in request.")
        return None

class Cache(object):
    def __init__(self):
        self.cache = {}
    
    def __getitem__(self, key):
        return self.cache.get(key, None)

    def __setitem__(self, key, value):
        self.cache[key] = value

account_cache = Cache()

def get_account(number : int, token : str):
    succ, username = user_client.get_username_from_token(token)
    if not succ:
        raise Exception(f"User {username} does not exist.")

    if number in account_cache.cache:
        return account_cache[number]

    account = coll_accounts.find_one({"user": username, "number": number})
    account_cache[number] = Account(**account)
    return Account(**account) if account else None

class TransactionInput(graphene.InputObjectType):
    date_trans = graphene.Int()
    amount = graphene.Float()
    desc = graphene.String()
    from_account = graphene.Int()
    to_account = graphene.Int()

class Account(graphene.ObjectType):
    _id = graphene.String()
    user = graphene.String()
    name = graphene.String()
    desc = graphene.String()
    number = graphene.Int()

class Transaction(graphene.ObjectType):
    _id = graphene.String()
    date_reg = graphene.Int()
    date_trans = graphene.Int()
    amount = graphene.Float()
    desc = graphene.String()
    from_account = graphene.Field(Account)
    to_account = graphene.Field(Account)
    user = graphene.String()

    def resolve_from_account(self, info):
        token = get_token_from_info(info, require_token=not dev_user) or user_client.get_valid_token(dev_user)
        return get_account(self.from_account, token)

    def resolve_to_account(self, info):
        token = get_token_from_info(info, require_token=not dev_user) or user_client.get_valid_token(dev_user)
        return get_account(self.to_account, token)

class Period(graphene.ObjectType):
    year = graphene.Int()
    month = graphene.Int()
    start = graphene.String()
    end = graphene.String()
    start_timestamp = graphene.Int()
    end_timestamp = graphene.Int()

class Mutations(graphene.ObjectType):
    pass

class AccountInput(graphene.InputObjectType):
    number = graphene.Int(required=True, description="Account number")

class Query(graphene.ObjectType):
    transactions = graphene.List(Transaction, start_date=graphene.Int(default_value=0), end_date=graphene.Int(default_value=(2 ** 53 - 1)), amount=graphene.Int(), desc=graphene.String(), from_account=graphene.Argument(AccountInput), to_account=graphene.Argument(AccountInput))

    accounts = graphene.List(Account, numbers=graphene.List(graphene.Int, required=False))

    periods = graphene.List(Period, year=graphene.List(graphene.Int), month=graphene.List(graphene.Int), description="Gets economic periods based on what is specified. If neither year or month is specified, then the current period will be returned.")

    def resolve_periods(self, info, year = None, month = None):
        token = get_token_from_info(info, require_token=not dev_user) or user_client.get_valid_token(dev_user)

        succ, username = user_client.get_username_from_token(token)
        if not succ:
            raise Exception(f"User {username} does not exist")

        if user_client.token_has_privileges(token, ["periods", "economy"]):
            if not year and not month:
                s, e = get_dates_month_period(datetime.date.today())
                return [Period(year=e.year, month=e.month, start=s.isoformat(), end=e.isoformat(), start_timestamp=s.timestamp(), end_timestamp=e.timestamp())]

            start_ends = [(y, m, *get_dates_month_period(datetime.date(y, m, 1))) for y in year for m in month ]
            return sorted([Period(year=y, month=m, start=s.isoformat(), end=e.isoformat(), start_timestamp=s.timestamp(), end_timestamp=e.timestamp()) for y, m, s, e in start_ends], key=lambda p: p.start_timestamp)
        else:
            raise Exception("User must have privileges 'periods' and 'economy'")

    def resolve_accounts(self, info, numbers = []):
        token = get_token_from_info(info, require_token=not dev_user) or user_client.get_valid_token(dev_user)

        succ, username = user_client.get_username_from_token(token)
        if not succ:
            raise Exception(f"User {username} does not exist")
        
        if user_client.token_has_privileges(token, ["accounts", "economy"]):
            query = { "user": username }
            if numbers != []:
                query["number"] = {"$in": numbers}

            accounts = [Account(**a) for a in list(coll_accounts.find(query, sort=[("number", 1)]))]

            for acc in accounts:
                account_cache[acc.number] = acc

            return accounts
        
        raise Exception("User must have privileges 'accounts' and 'economy'")

    def resolve_transactions(self, info, start_date = 0, end_date = (2 ** 53 - 1), amount = None, desc = None, from_account = None, to_account = None):
        token = get_token_from_info(info, require_token=not dev_user) or user_client.get_valid_token(dev_user)
        
        succ, username = user_client.get_username_from_token(token)
        if not succ:
            raise Exception(f"User {username} does not exist")

        if user_client.token_has_privileges(token, ["transactions", "economy"]):
            query = { 
                "user": username,
                "date_trans": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
            if amount:
                query["amount"] = amount
            if desc:
                query["desc"] = { 
                    "$regex": ".*" + desc + ".*"
                }
            if from_account:
                query["from_account"] = from_account.number
            if to_account:
                query["to_account"] = to_account.number
            return [Transaction(**t) for t in list(coll_trans.find(query, {"_id": 0}, sort=[("date_trans", 1)]))]
        
        raise Exception("User must have privileges 'transactions', 'accounts' and 'economy'")
            
graphql_schema = graphene.Schema(query=Query)