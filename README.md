# restberry-api

![Uptime Robot ratio (7 days)](https://img.shields.io/uptimerobot/ratio/7/m788440920-edcdd5975b38ec31da628d55) ![Website](https://img.shields.io/website?down_message=down&label=status&up_message=up&url=https%3A%2F%2Fapi.dcronqvist.se) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/dcronqvist/restberry-api/Run%20Pytest?label=tests) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/dcronqvist/restberry-api/CI%20to%20Docker%20Hub?label=build%20%26%20docker%20hub%20push) ![Docker Pulls](https://img.shields.io/docker/pulls/dcronqvist/restberry-api) ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/dcronqvist/restberry-api/latest)

A REST API that used to be hosted on my Raspberry Pi 4, hence the name. Is now hosted as a docker container on another server. 

Check it out here: [https://api.dcronqvist.se](https://api.dcronqvist.se)

## Table of contents

- [Authentication](#authentication)
- [Available privileges](#available-privileges)
- [List of endpoints](#list-of-endpoints)
    - [Authorization](#authorization)
        - [/v1/auth/login](#authorization)
    - [Economy](#economy)
        - [/v1/economy/periods/months](#economy)
        - [/v1/economy/periods/months/current](#economy)
        - [/v1/economy/periods/years](#economy)
        - [/v1/economy/periods/years/current](#economy)
        - [/v1/economy/accounts](#economy)
        - [/v1/economy/transactions](#economy)
        - [/v1/economy/transactions/id](#economy)
    - [PiHole](#pihole)
        - [/v1/pihole/status](#pihole)

## Authentication

To authenticate against the API, you must have a valid login (username & password), which you POST to [https://api.dcronqvist.se/v1/auth/login](https://api.dcronqvist.se/v1/). Once authorized, you'll be given a token which will be valid for the following 60 minutes, after that you must acquire a new token to remain authorized. 

The acquired token must be supplied in the `Authorization` header for all subsequent API requests. The only endpoint which does not require the `Authorization` header is of course the `/v1/auth/login` endpoint, as that wouldn't make much sense.

## Available privileges

There is a multitude of RESTful endpoints, which all require certain ***privileges***.

Privilege | Description
------------ | -------------
economy | Base privilege for most endpoints regarding economy
accounts | Additional economy privilege for accessing accounts
transactions | Additional economy privilege for accessing transactions
periods | Additional economy privilege for accessing economic periods
pihole | Privilege that gives access to status information from dani's pihole

## List of endpoints

Here is a list of endpoints which you can request, however, to have some more insight to what they expect (regarding query parameters or payloads), or more detailed information in general, please head to [https://api.dcronqvist.se](https://api.dcronqvist.se) and go to the relevant version to see the official documentation.

### Authorization
All endpoints related to authentication in the API.

URL | HTTP Method | Privileges | Returns/Performs
--- | ----------- | ---------- | ---------------
/v1/auth/login | POST | None | A token which is valid for 60 minutes

### Economy

All endpoints related to dani's personal finance, all of  **the following endpoints require the privilege `economy`** in addition to their specific privilege.

URL | HTTP Method | Privileges | Returns/Performs
--- | ----------- | ---------- | ---------------
/v1/economy/periods/months | GET | `periods` | Returns the specified month(s)'s economic period
/v1/economy/periods/months/current | GET | `periods` | Returns the current month's economic period
/v1/economy/periods/years | GET | `periods` | Returns the specified year's economic period
/v1/economy/periods/years/current | GET | `periods` | Returns the current year's economic period
/v1/economy/accounts | GET | `accounts` | Returns all or the specified account(s)'s information
/v1/economy/accounts | POST | `accounts` | Creates a new economy account
/v1/economy/transactions | GET | `transactions` | Returns all or the specified transaction(s)'s information
/v1/economy/transactions | POST | `transactions` | Creates a new transaction
/v1/economy/transactions/id | GET | `transactions` | Returns the specified transaction

### PiHole

All endpoints related to dani's PiHole, all the following endpoints require the privilege `pihole`.

URL | HTTP Method | Returns/Performs
--- | ----------- | ---------------
/v1/pihole/status | GET | Returns PiHole statistics
