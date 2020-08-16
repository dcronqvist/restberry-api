# restberry-api
A REST API that is hosted on my raspberry pi 4. Has different categories of endpoints which all serve different purposes. Most of them are GET endpoints, to make it as easy as possible to interact with. It's always hosted over a connection with SSL, to make sure all traffic is secured.

## Endpoints

There is a base endpoint of **/** which simply greets the user with a `Hello World!`.
If no valid authorization is provided, then the user will be given a `401 UNAUTHORIZED ACCESS` error.
*Cursive* words in endpoints mean parameters. These are usually strings or ints.

### Endpoints

These are endpoints which serve as a way to find all available endpoints of the API in a list. I use these as a way to quickly
test new endpoints from my Siri Shortcuts.

URL | HTTP Method | Returns
------------ | ------------- | -------------
/endps/all | GET | Returns all available endpoints
/endps/search/*string* | GET | Returns all endpoints which contains the search term

### Economy

All of these endpoints are tied to my personal finance management spreadsheet. If you need help with Excel, hmu.

URL | HTTP Method | Returns
------------ | ------------- | -------------
/econ/outcomes/month | GET | Returns this month's outcome result, balance and budget
/econ/outcomes/month/*category* | GET | Returns this month's result, balance, budget and average for specific category
/econ/outcomes/categories/findall | GET | Returns all available categories for outcomes
/econ/outcomes/categories/guess/*amount* | GET | Returns a list of categories that the specified amount might be registered as
/econ/outcomes/categories/search/*category* | GET | Returns a list of categories that match the specified search string
/econ/outcomes/categories/register/*category* | GET | Registers a new category to be used for outcomes
/econ/outcomes/register/*date*/*category*/*description*/*amount* | GET | Registers the specified outcome to the spreadsheet
/econ/incomes/month | GET | Returns this month's income result, balance and budget
/econ/incomes/categories/findall | GET | Returns all available categories for incomes
/econ/incomes/register/*date*/*category*/*description*/*amount* | GET | Registers the specified income to the spreadsheets

### Food

For all available food endpoints, you can specify which language you want the response in, either **swe** or **eng**.

URL | HTTP Method | Returns
------------ | ------------- | -------------
/food/jh/express/today/*lang* | GET | Returns today's Express lunch
/food/jh/express/week/*lang* | GET | Returns the current week's Express lunches
/food/jh/karr/week/*lang* | GET | Returns the current week's Kårrestaurangen lunches
