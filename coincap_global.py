import json
from requests import Request, Session
from datetime import datetime

global_url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '5d21df5e-b463-4783-af58-3af6a2062afd',
}

session = Session()
session.headers.update(headers)

response = session.get(global_url)
results = json.loads(response.text)

# print(json.dumps(results, sort_keys=True, indent=4))

active_currencies = results['data']['active_cryptocurrencies']
active_markets = results['data']['active_market_pairs']
bitcoin_percentage = results['data']['btc_dominance']
last_updated = results['data']['last_updated']
global_cap = int(results['data']['quote']['USD']['total_market_cap'])
global_volume = int(results['data']['quote']['USD']['total_volume_24h'])

active_currencies_string = '{:,}'.format(active_currencies)
active_markets_string = '{:,}'.format(active_markets)
global_cap_string = '{:,}'.format(global_cap)
global_volume_string = '{:,}'.format(global_volume)

# last_updated_string = datetime.fromtimestamp(last_updated).strftime('%B %d, %Y at %I:%M%p')

print()
print('There are currently ' + active_currencies_string + ' active cryptocurrecies and ' + active_markets_string + ' active markets.')
print('The global cap of all cryptos is ' + global_cap_string + ' and the 24h global volume is ' + global_volume_string + '.')
print('Bitcoin\'s total percentage of the global cap is ' + str(bitcoin_percentage) + '%.')
print()
print('This information was last updated on ' + str(last_updated) + '.')