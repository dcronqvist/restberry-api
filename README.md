# restberry-api

![Uptime Robot ratio (7 days)](https://img.shields.io/uptimerobot/ratio/7/m788440920-edcdd5975b38ec31da628d55) ![Website](https://img.shields.io/website?down_message=down&label=status&up_message=up&url=https%3A%2F%2Fapi.dcronqvist.se)

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/dcronqvist/restberry-api/CI%20to%20Docker%20Hub?label=build%20%26%20docker%20hub%20push) ![Docker Pulls](https://img.shields.io/docker/pulls/dcronqvist/restberry-api) ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/dcronqvist/restberry-api/latest)

A REST API that is hosted on my raspberry pi 4. Has different categories of endpoints which all serve different purposes. Most of them are GET endpoints, to make it as easy as possible to interact with. It's always hosted over a connection with SSL, to make sure all traffic is secured.

Check it out here [https://api.dcronqvist.se](https://api.dcronqvist.se)

## Endpoints

There is a multitude of RESTful endpoints, which all required certain ***privileges***.

### All available privileges

Privilege | Description
------------ | -------------
minecraft_command | Allows for performing any RCON command on the connected minecraft server
minecraft_whitelist | Allows the user to manage the whitelist of the connected minecraft server
economy_accounts | Allows access to all endpoints regarding economy accounts
economy_periods | Allows access to all economy periods endpoints
economy_transactions | Allows access to register and view economy transactions

### Endpoints

These are endpoints which serve as a way to find all available endpoints of the API in a list. I use these as a way to quickly test new endpoints from my Siri Shortcuts.

URL | HTTP Method | Privileges | Returns
------------ | ------------- | ------------- |-------------
/endpoints/all | GET | None | Returns all available endpoints
/endpoints/search/*string* | GET | None | Returns all endpoints which contains the search term

### Economy

All endpoints which allow access to the personal finance part of this API. In the following endpoints, all URL parameters which are followed by `[]` can be specified multiple times in order to specify multiple of whatever the specific endpoint retrieves. All URL parameters which are followed by a `?` is considered optional and will usually make the specific endpoint return all possible values instead of any specific value. To see what payloads are expected by `POST` & `PUT` endpoints, click the `POST` & `PUT` links on the respective table row.

URL | URL Parameters | HTTP Method | Privileges | Returns/Performs
------------ | ------------- |------------- | ---------- | --
/v1/economy/accounts | number[]? | GET | `economy_accounts` | List of all accounts whose numbers were specified, or all of them if not specified at all
/v1/economy/accounts | | [POST](#post-&-put-/v1/economy/accounts) | `economy_accounts` | Creates a new account with the specified details
/v1/economy/accounts | | [PUT](#post-&-put-/v1/economy/accounts) | `economy_accounts` | Updates an existing account with new details
/v1/economy/accounts | number[] | DELETE | `economy_accounts` | Deletes/removes the specified account(s)
/v1/economy/periods/months | year[]?, month[] | GET | `economy_periods` | Retrieves the specified period(s)
/v1/economy/periods/months/current | | GET | `economy_periods` | Retrieves the current period
/v1/economy/periods/years | year[]? | GET | `economy_periods` | Retrieves all month peiods in the specified year(s)
/v1/economy/periods/years/current | | GET | `economy_periods` | Retrieves all month periods in the current year
/v1/economy/transactions | id[]? or startDate, endDate, toAccount?, fromAccount? | GET | `economy_transactions` | Retrieves the specified transaction(s)
/v1/economy/transactions | | [POST](#post-/v1/economy/transactions) | `economy_transactions` | Registers a new transactions with the specified details
/v1/economy/transactions | id | [PUT](#put-/v1/economy/transactions) | `economy_transactions` | Updates the specified transactions with the specified details
/v1/economy/transactions | id | DELETE | `economy_transactions` | Deletes/removes the specified transaction

### Food

For all available food endpoints, you can specify which language you want the response in, either **swe** or **eng**.

URL | HTTP Method | Privileges | Returns
------------ | ------------- | ------------- |-------------
/food/jh/express/today/*lang* | GET | FOOD | Returns today's Express lunch
/food/jh/express/week/*lang* | GET | FOOD | Returns the current week's Express lunches
/food/jh/karr/week/*lang* | GET | FOOD | Returns the current week's Kårrestaurangen lunches

## Payloads

All payloads specified in the list of endpoints above.

### POST & PUT /v1/economy/accounts
```python
{
    "number": {
        "required": True,
        "allowed_types": [int]
    },
    "name": {
        "required": True,
        "allowed_types": [str]
    },
    "desc": {
        "required": True,
        "allowed_types": [str]
    }
}
```

### POST /v1/economy/transactions
```python
{
    "amount": {
        "required": True,
        "allowed_types": [float, int]
    },
    "date_trans": {
        "required": False,
        "allowed_types": [int]
    },
    "desc": {
        "required": True,
        "allowed_types": [str]
    },
    "from_account": {
        "required": True,
        "allowed_types": [int]
    },
    "to_account": {
        "required": True,
        "allowed_types": [int]
    }
}
```

### PUT /v1/economy/transactions
```python
{
    "amount": {
        "required": False,
        "allowed_types": [float, int]
    },
    "date_trans": {
        "required": False,
        "allowed_types": [int]
    },
    "desc": {
        "required": False,
        "allowed_types": [str]
    },
    "from_account": {
        "required": False,
        "allowed_types": [int]
    },
    "to_account": {
        "required": False,
        "allowed_types": [int]
    }
}
```