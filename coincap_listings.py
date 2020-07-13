import json
from requests import Request, Session
from datetime import datetime

global_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters = {
  'start':'1',
  'limit':'100',
  'convert':'USD',
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '5d21df5e-b463-4783-af58-3af6a2062afd',
}

session = Session()
session.headers.update(headers)

response = session.get(global_url, params=parameters)
results = json.loads(response.text)

# print(json.dumps(results, sort_keys=True, indent=4))

data = results['data']

for currency in data:
    rank = currency['cmc_rank']
    name = currency['name']
    symbol = currency['symbol']
    print(str(rank) + ':' + name + '(' + symbol + ')' )