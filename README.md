# restberry-api
api for my raspberry pi as a rest api host
simple small change
another change to make sure access token persists.
another change, from hercules.

## Endpoints

There is a base endpoint of **/** which simply greets the user with a `Hello World!`.

### Economy

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
