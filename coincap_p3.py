import os
import json
from requests import Request, Session
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore, Back, Style

convert_choice='USD'

global_url ='https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'
listing_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'


headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '5d21df5e-b463-4783-af58-3af6a2062afd',
}

session_global = Session()
session_global.headers.update(headers)

response_global = session_global.get(global_url)
results_global = json.loads(response_global.text)

# print(json.dumps(results_listing, sort_keys=True, indent=4))
# print(json.dumps(results_global, sort_keys=True, indent=4))

data_global = results_global['data']
global_cap = int(data_global['quote'][convert_choice]['total_market_cap'])
global_cap_string = '{:,}'.format(global_cap)
global_cap_update = data_global['last_updated']

while True:

    print()
    print("Welcome to Coinmarketcap exploer")
    print()
    print("The cryptoncurrency global market cap is $" + global_cap_string + " in " + convert_choice + ", last updated at " + global_cap_update + ".")
    print()
    print("1. Top 10 sorted by rank.")
    print("2. Top 10 sorted by 24H change.")
    print("3. Top 10 sorted by 24H volume.")
    print("0. Exit")
    print()

    menu_choice = input("Choose one to explore (1~3 or 0):")

    if menu_choice == '1':
        sort_choice = 'market_cap'
    if menu_choice == '2':
        sort_choice = 'percent_change_24h'
    if menu_choice == '3':
        sort_choice = 'volume_24h'
    if menu_choice == '0':
        break
    
    parameters = {
        'start':'1',
        'limit':'10',
        'convert':convert_choice,
        'sort':sort_choice
        }

    session_listing = Session()
    session_listing.headers.update(headers)

    response_listing = session_listing.get(listing_url, params=parameters)
    results_listing = json.loads(response_listing.text)
    data_listing = results_listing['data']

    table = PrettyTable(['Rank', 'Asset', 'Price', 'Market Cap', 'Volume', '1H', '24H', '7D'])
    table.align['Price'] = 'r'
    table.align['Market Cap'] = 'r'
    table.align['Volume'] = 'r'
    table.align['1H'] = 'r'
    table.align['24H'] = 'r'
    table.align['7D'] = 'r'
    
    for currency in data_listing:
        rank = currency['cmc_rank']
        name = currency['name']
        symbol = currency['symbol']
        quotes = currency['quote'][convert_choice]
        price = quotes['price']
        market_cap = quotes['market_cap']
        volume_24h = quotes['volume_24h']
        percent_change_1h = quotes['percent_change_1h']
        percent_change_24h = quotes['percent_change_24h']
        percent_change_7d = quotes['percent_change_7d']
        
        if market_cap is not None:
            market_cap_string = format(int(market_cap), ',')
        
        if volume_24h is not None:
             value_string = format(int(volume_24h), ',')
        

        if percent_change_1h is not None:
            percent_change_1h = round(quotes['percent_change_1h'], 3)

            if percent_change_1h > 0:
                percent_change_1h = Back.RED + str(percent_change_1h) + '%' + Style.RESET_ALL
            else:
                percent_change_1h = Back.GREEN + str(percent_change_1h) + '%' + Style.RESET_ALL

        if percent_change_24h is not None:
            percent_change_24h = round(quotes['percent_change_24h'], 3)

            if percent_change_24h > 0:
                percent_change_24h = Back.RED + str(percent_change_24h) + '%' + Style.RESET_ALL
            else:
                percent_change_24h = Back.GREEN + str(percent_change_24h) + '%' + Style.RESET_ALL

        if percent_change_7d is not None:
            percent_change_7d = round(quotes['percent_change_7d'], 3)

            if percent_change_7d > 0:
                percent_change_7d = Back.RED + str(percent_change_7d) + '%' + Style.RESET_ALL
            else:
                percent_change_7d = Back.GREEN + str(percent_change_7d) + '%' + Style.RESET_ALL

        

        table.add_row([rank,
                    name + '(' + symbol + ')',
                    '$' + str(round(price, 3)),
                    '$' + str(market_cap_string),
                    '$' + str(value_string),     
                    str(percent_change_1h),
                    str(percent_change_24h),
                    str(percent_change_7d)])
        
    print()
    print(table)
    print("The cryptoncurrency caculated in " + convert_choice + ", last updated at " + global_cap_update + ".")
    print()

    choice = input("Again? (y/n)")

    if choice == 'n':
        break





