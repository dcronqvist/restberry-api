from datetime import datetime
import pickle
import pandas as pd

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

def predict_accounts(date_trans, amount, is_outcome, is_swish, desc):
    df = pd.DataFrame()

    df["Transaktionsdag"] = [date_trans]
    df["Belopp"] = [amount]
    df["IsOutcome"] = [is_outcome]
    df["IsSwish"] = [is_swish]
    df["DayOfWeek"] = [datetime.fromtimestamp(date_trans).weekday()]
    df["IsWeekend"] = [datetime.fromtimestamp(date_trans) in [5,6]]
    df["Known"] = [get_known(desc)]

    predicted_from = from_account_model.predict(df)
    predicted_to = to_account_model.predict(df)

    from_account = [int(x) for x in list(predicted_from)][0]
    to_account = [int(x) for x in list(predicted_to)][0]

    return {
        "date_trans": date_trans,
        "amount": amount,
        "desc": desc,
        "from_account": from_account,
        "to_account": to_account
    }