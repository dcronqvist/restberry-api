from datetime import datetime
from flask import request
from flask_restx import Resource, Namespace, fields, reqparse
from api_v1 import privilege_required
import pandas as pd
import pickle
from db import coll_accounts

api = Namespace("ai", path="/ai", description="Endpoints utilizing some of my trained scikit models.")

post_model = api.model("accountant_payload", {
    "amount": fields.Float(example=39.9, required=True, min=0),
    "date_trans": fields.Integer(example=round(datetime.now().timestamp()), required=True),
    "desc": fields.String(example="Transaction for stuff", required=True),
    "is_outcome": fields.Boolean(example=True, required=True),
    "is_swish": fields.Boolean(example=False, required=True),
    "account_names": fields.Boolean(example=True, default=False, help="If true, account names will also be returned.")
})

accountant_post_doc = """
### A model for predicting transaction accounts

By supplying only very little information about a transaction, this model will be able to quite accurately predict both which account the transaction's amount is going FROM, but also TO.
"""

def get_known(desc):
    known_tech_stores = [
        "webhall",
        "elgig",
        "clas ohl",
        "nintendo",
        "steam",
        "adobe",
        "blizzard",
        "komplett",
        "inet",
        "KJELL & CO",
        "Electrokit",
        "Billigtekn",
        "SLOJD ",
        "DISCORD",
        "Proshop",
        "Miss Hosting"
    ]
    known_grocery_stores = [
        "coop",
        "ica",
        "willys",
        "hemköp",
        "wh götebo",
        "SAIGON",
        "matse",
        "HEMK@P",
        "tempo"
    ]
    known_restaurants = [
        "sanneg",
        "miss faj",
        "taco bar",
        "tugg",
        "max",
        "bruncho",
        "lucy",
        "pizza",
        "pizz",
        "hamburg",
        "foodora",
        "UBER *EATS",
        "frasses",
        "brodernas",
        "iZ *DATATEKNOLOG",
        "sush",
        "plankan",
        "dine",
        "O LEARYS",
        "john sco",
        "UBER * EATS",
        "taverna",
        "W.O.K"
    ]
    known_snacks = [
        "selecta",
        "alltgodis",
        "alltigodis",
        "pressbyr",
        "condeco",
        "espresso",
        "pomona",
        "cafe",
        "too good to go",
        "7-ELEVEN",
        "CIRCLE K"
    ]   
    known_stuff = {
        1: known_grocery_stores,
        2: known_snacks,
        3: known_restaurants,
        4: known_tech_stores,
        5: ["västtrafik"],
        6: ["lyko", "salong", "levi", "zalando"]
    }  
    for known in known_stuff:
        if any([k.lower() in desc.lower() for k in known_stuff[known]]):
            return known
    return 0

with open("scikit-models/from_account_v1.ai", "rb") as f:
    from_account_model = pickle.load(f)

with open("scikit-models/to_account_v1.ai", "rb") as f:
    to_account_model = pickle.load(f)

@api.route("/accountant")
class TransactionAccountsPredictor(Resource):
    @api.doc(description=accountant_post_doc)
    @api.expect(post_model, validate=True)
    def post(self):
        trans = api.payload
        df = pd.DataFrame()

        df["Transaktionsdag"] = [trans["date_trans"]]
        df["Belopp"] = [trans["amount"]]
        df["IsOutcome"] = [trans["is_outcome"]]
        df["IsSwish"] = [trans["is_swish"]]
        df["DayOfWeek"] = [datetime.fromtimestamp(trans["date_trans"]).weekday()]
        df["IsWeekend"] = [datetime.fromtimestamp(trans["date_trans"]) in [5,6]]
        df["Known"] = [get_known(trans["desc"])]

        predicted_from = from_account_model.predict(df)
        predicted_to = to_account_model.predict(df)

        trans["from_account"] = [int(x) for x in list(predicted_from)][0]
        trans["to_account"] = [int(x) for x in list(predicted_to)][0]

        if trans["account_names"]:
            trans["from_account_info"] = coll_accounts.find_one({ "number": trans["from_account"], "user": "dani" }, { "_id": 0, "user": 0, "number": 0})
            trans["to_account_info"] = coll_accounts.find_one({ "number": trans["to_account"], "user": "dani" }, { "_id": 0, "user": 0, "number": 0})
        

        del trans["account_names"]
        del trans["is_outcome"]
        del trans["is_swish"] 

        return trans, 200
