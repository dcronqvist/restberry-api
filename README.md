# restberry-api
A REST API that is hosted on my raspberry pi 4. Has different categories of endpoints which all serve different purposes. Most of them are GET endpoints, to make it as easy as possible to interact with. It's always hosted over a connection with SSL, to make sure all traffic is secured.

## Endpoints

There is a base endpoint of **/** which simply greets the user with a `Hello World!`.
If no valid authorization is provided, then the user will be given a `401 UNAUTHORIZED ACCESS` error.
*Cursive* words in endpoints mean parameters. These are usually strings or ints. Most endpoints have some required privileges which are given to a user by an administrator.

### All available privileges

Privilege | Description
------------ | -------------
ECON_OUT | Allows for viewing information from the economy outcome endpoints
ECON_IN | Allows for viewing information from the economy income endpoints
ECON_REG | Allows for registering incomes, outcomes and categories on the economy endpoints
FOOD | Gives the user access to all food endpoints

### Endpoints

These are endpoints which serve as a way to find all available endpoints of the API in a list. I use these as a way to quickly
test new endpoints from my Siri Shortcuts.

URL | HTTP Method | Privileges | Returns
------------ | ------------- | ------------- |-------------
/endps/all | GET | None | Returns all available endpoints
/endps/search/*string* | GET | None | Returns all endpoints which contains the search term

### Economy

All of these endpoints are tied to my personal finance management spreadsheet. If you need help with Excel, hmu.

URL | HTTP Method | Privileges | Returns
------------ | ------------- | ------------- |-------------
/econ/outcomes/month | GET | ECON_OUT | Returns this month's outcome result, balance and budget
/econ/outcomes/month/*category* | GET | ECON_OUT | Returns this month's result, balance, budget and average for specific category
/econ/outcomes/categories/findall | GET | ECON_OUT | Returns all available categories for outcomes
/econ/outcomes/categories/guess/*amount* | GET | ECON_OUT | Returns a list of categories that the specified amount might be registered as
/econ/outcomes/categories/search/*category* | GET | ECON_OUT | Returns a list of categories that match the specified search string
/econ/outcomes/categories/register/*category* | GET | ECON_REG | Registers a new category to be used for outcomes
/econ/outcomes/register | POST | ECON_REG | Registers the specified outcome to the spreadsheet. Expects payload of format: `{"date:" "short-iso", "category": "yup", "description": "yadda", "amount": 1337}`.
/econ/incomes/month | GET | ECON_IN | Returns this month's income result, balance and budget
/econ/incomes/categories/findall | GET | ECON_IN | Returns all available categories for incomes
/econ/incomes/register/*date*/*category*/*description*/*amount* | GET | ECON_REG | Registers the specified income to the spreadsheets

### Food

For all available food endpoints, you can specify which language you want the response in, either **swe** or **eng**.

URL | HTTP Method | Privileges | Returns
------------ | ------------- | ------------- |-------------
/food/jh/express/today/*lang* | GET | FOOD | Returns today's Express lunch
/food/jh/express/week/*lang* | GET | FOOD | Returns the current week's Express lunches
/food/jh/karr/week/*lang* | GET | FOOD | Returns the current week's Kårrestaurangen lunches
