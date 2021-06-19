# restberry-api

![Uptime Robot ratio (7 days)](https://img.shields.io/uptimerobot/ratio/7/m788440920-edcdd5975b38ec31da628d55) ![Website](https://img.shields.io/website?down_message=down&label=status&up_message=up&url=https%3A%2F%2Fapi.dcronqvist.se) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/dcronqvist/restberry-api/CI%20to%20Docker%20Hub?label=build%20%26%20docker%20hub%20push) ![Docker Pulls](https://img.shields.io/docker/pulls/dcronqvist/restberry-api) ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/dcronqvist/restberry-api/latest)

A REST API that used to be hosted on my Raspberry Pi 4, hence the name. Is now hosted as a docker container on another server. 

Check it out here: [https://api.dcronqvist.se](https://api.dcronqvist.se)

## Table of contents

- [Authentication](#authentication)
- [Endpoints](#endpoints)
    - [Available privileges](#available-privileges)
    - [List of endpoints](#list-of-endpoints)
        - [Authorization](#authorization)
            - [/v1/auth/login](#authorization)

## Authentication

To authenticate against the API, you must have a valid login (username & password), which you POST to [https://api.dcronqvist.se/v1/auth/login](https://api.dcronqvist.se/v1/). Once authorized, you'll be given a token which will be valid for the following 60 minutes, after that you must acquire a new token to remain authorized. 

The acquired token must be supplied in the `Authorization` header for all subsequent API requests. The only endpoint which does not require the `Authorization` header is of course the `/v1/auth/login` endpoint, as that wouldn't make much sense.

## Endpoints

There is a multitude of RESTful endpoints, which all require certain ***privileges***.

### Available privileges

Privilege | Description
------------ | -------------
economy | Base privilege for most endpoints regarding economy
accounts | Additional economy privilege for accessing accounts
transactions | Additional economy privilege for accessing transactions
periods | Additional economy privilege for accessing economic periods
pihole | Privilege that gives access to status information from dani's pihole

### List of endpoints

Here is a list of endpoints which you can request, however, to have some more insight to what they expect, or more detailed information, please head to [https://api.dcronqvist.se](https://api.dcronqvist.se) and go to the relevant version to see the official documentation.

#### Authorization
All endpoints related to authentication in the API.

URL | HTTP Method | Privileges | Returns/Performs
--- | ----------- | ---------- | ---------------
/v1/auth/login | POST | None | A token which is valid for 60 minutes.

#### Economy

All endpoints related to dani's personal finance.

URL | HTTP Method | Privileges | Returns/Performs
--- | ----------- | ---------- | ---------------
/v1/


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