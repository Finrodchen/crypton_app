import os
import json
from requests import Request, Session
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore, Back, Style

print()
print('MY PORTFOLIO')
print()

convert_choice='USD'

portfolio_value = 0.00
last_updated = 0

table = PrettyTable(['Asset', 'Amount Owned', convert_choice + ' Value', 'Price', '1h', '24h', '7d'])

with open('portfolio.txt') as inp:
    for line in inp:
        ticker, amount = line.split()
        ticker = ticker.upper()

        ticker_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        
        headers = {
                    'Accepts': 'application/json',
                    'X-CMC_PRO_API_KEY': '5d21df5e-b463-4783-af58-3af6a2062afd',
                }

        parameters = {
                    'symbol':ticker,
                    'convert':convert_choice,
                }

        session = Session()
        session.headers.update(headers)

        response = session.get(ticker_url, params=parameters)
        results = json.loads(response.text)

        currency = results['data'][ticker]

        rank = currency['cmc_rank']
        name = currency['name']
        symbol = currency['symbol']
        last_updated = currency['last_updated']
        quotes = currency['quote'][convert_choice]
        market_cap = quotes['market_cap']
        percent_change_1h = quotes['percent_change_1h']
        percent_change_24h = quotes['percent_change_24h']
        percent_change_7d = quotes['percent_change_7d']
        price = quotes['price']
        
        value = float(price) * float(amount)

        if percent_change_1h > 0:
            percent_change_1h = Back.RED + str(percent_change_1h) + '%' + Style.RESET_ALL
        else:
            percent_change_1h = Back.GREEN + str(percent_change_1h) + '%' + Style.RESET_ALL

        if percent_change_24h > 0:
            percent_change_24h = Back.RED + str(percent_change_24h) + '%' + Style.RESET_ALL
        else:
            percent_change_24h = Back.GREEN + str(percent_change_24h) + '%' + Style.RESET_ALL

        if percent_change_7d > 0:
            percent_change_7d = Back.RED + str(percent_change_7d) + '%' + Style.RESET_ALL
        else:
            percent_change_7d = Back.GREEN + str(percent_change_7d) + '%' + Style.RESET_ALL

        portfolio_value += value

        value_string = '{:,}'.format(round(value,2))

        table.add_row([name + ' (' + symbol + ')',
                       amount,
                       '$' + value_string,
                       '$' + str(price),
                       str(percent_change_1h),
                       str(percent_change_24h),
                       str(percent_change_7d)])

print(table)
print()

portfolio_value_string = '{:,}'.format(round(portfolio_value,2))

print('Total Portfolio Value: ' + Back.RED + '$' + portfolio_value_string + Style.RESET_ALL)
print()
print('API Results Last Updated on ' + last_updated)
print()