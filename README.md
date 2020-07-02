# restberry-api
api for my raspberry pi as a rest api host
simple small change
another change to make sure access token persists.
another change, from hercules.

## Endpoints

There is a base endpoint of **/** which simply greets the user with a `Hello World!`.
If no valid authorization is provided, then the user will be given a `401 UNAUTHORIZED ACCESS` error.
Valid authorizations are provided by me.

### Endpoints

URL | HTTP Method | Returns
------------ | ------------- | -------------
/endps/all | GET | Returns all available endpoints
/endps/search/*string* | GET | Returns all endpoints which contains the search term

### Economy
Further on, *cursive* words in endpoints mean parameters. These are usually strings or ints.

URL | HTTP Method | Returns
------------ | ------------- | -------------
/econ/outcomes/month | GET | Returns this month's outcome result, balance and budget
/econ/outcomes/month/*category* | GET | Returns this month's result, balance, budget and average for specific category
/econ/outcomes/categories/findall | GET | Returns all available categories for outcomes
/econ/outcomes/categories/guess/*amount* | GET | Returns a list of categories that the specified amount might be registered as
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