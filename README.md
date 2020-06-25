# restberry-api
api for my raspberry pi as a rest api host
simple small change
another change to make sure access token persists.
another change, from hercules.

## Endpoints

URL | HTTP Method | Returns
------------ | ------------- | -------------
/ | GET | Simply returns a "Hello World!", to greet user for correct usage
/econ/outcomes/month | GET | Returns this month's result, balance and budget
/econ/outcomes/month/<string:category> | GET | Returns this month's result, balance, budget and average for specific category
/econ/outcomes/categories/findall | GET | Returns all available categories for outcomes
/econ/outcomes/categories/guess/<string:amount> | GET | Returns a list of categories that the specified amount might be registered as
/econ/outcomes/categories/register/<string:category> | GET | Registers a new category to be used for outcomes
