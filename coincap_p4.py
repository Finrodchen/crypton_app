import os
import math
import locale
import json
from requests import Request, Session
from prettytable import PrettyTable

locale.setlocale(locale.LC_ALL, 'en-US.UTF-8')

global_url ='https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'
listing_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

convert_choice = 'USD'

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '5d21df5e-b463-4783-af58-3af6a2062afd',
}

session_global = Session()
session_global.headers.update(headers)

response_global = session_global.get(global_url)
results_global = json.loads(response_global.text)

data_global = results_global['data']
global_cap = data_global['quote'][convert_choice]['total_market_cap']
global_cap_update = data_global['last_updated']

table=PrettyTable([
    'Name',
    'Symbol',
    '% of Global Cap',
    'Current',
    '7.7T (Gold)',
    '36.8T (Narrow Money)',
    '73T (World Stock Markets)',
    '90.4T (Broad Money)',
    '217T (Real Estate)',
    '544T (Derivatives)'
])

table.align['Symbol'] = 'l'
table.align['% of Global Cap'] = 'r'
table.align['Current'] = 'r'
table.align['7.7T (Gold)'] = 'r'
table.align['36.8T (Narrow Money)'] = 'r'
table.align['73T (World Stock Markets)'] = 'r'
table.align['90.4T (Broad Money)'] = 'r'
table.align['217T (Real Estate)'] = 'r'
table.align['544T (Derivatives)'] = 'r'

parameters = {
        'start':'1',
        'limit':'5',
        'convert':convert_choice,
        }

session_listing = Session()
session_listing.headers.update(headers)

response_listing = session_listing.get(listing_url, params=parameters)
results_listing = json.loads(response_listing.text)
data_listing = results_listing['data']

for currency in data_listing:
    name = currency['name']
    symbol = currency['symbol']
    quotes = currency['quote'][convert_choice]
    current_price = round(quotes['price'], 2)
    pecentage_global_cap = round(float(quotes['market_cap'])/float(global_cap)*100, 2)
    circulating_supply = float(currency['circulating_supply'])

    trillon7price = round(700000000000 * pecentage_global_cap/circulating_supply,2)
    trillon36price = round(3600000000000 * pecentage_global_cap/circulating_supply,2)
    trillon73price = round(7300000000000 * pecentage_global_cap/circulating_supply,2)
    trillon90price = round(9000000000000 * pecentage_global_cap/circulating_supply,2)
    trillon217price = round(21700000000000 * pecentage_global_cap/circulating_supply,2)
    trillon544price = round(54400000000000 * pecentage_global_cap/circulating_supply,2)

    pecentage_global_cap_string = str(pecentage_global_cap) + '%'
    current_price_string = '$' + str(current_price)
    trillon7price_string = '$' + locale.format_string('%.2f', trillon7price,True)
    trillon36price_string = '$' + locale.format_string('%.2f', trillon36price,True)
    trillon73price_string = '$' + locale.format_string('%.2f', trillon73price,True)
    trillon90price_string = '$' + locale.format_string('%.2f', trillon90price,True)
    trillon217price_string = '$' + locale.format_string('%.2f', trillon217price,True)
    trillon544price_string = '$' + locale.format_string('%.2f', trillon544price,True)

    table.add_row([name,
                            symbol,
                            pecentage_global_cap_string,
                            current_price_string,
                            trillon7price_string,
                            trillon36price_string,
                            trillon73price_string,
                            trillon90price_string,
                            trillon217price_string,
                            trillon544price_string])

print()
print(table)
print("The cryptoncurrency caculated in " + convert_choice + ", last updated at " + global_cap_update + ".")
print()