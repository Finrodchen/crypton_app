import json
from requests import Request, Session
from datetime import datetime

ticker_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

start = '1'
limit = '5'
sort = 'market_cap'
convert = 'USD'

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '5d21df5e-b463-4783-af58-3af6a2062afd',
}


choice = input("請問你要自訂加密貨幣查詢條件嗎？ (y/n)")

if choice == 'y' :
    limit = input("請輸入要查詢的加密貨幣資料筆數(1~5000)：")
    start = input("請輸入要查詢的加密貨幣起始排名(起始為1)：")
    convert = input("請輸入要計價的真實貨幣代碼(預設為USD)：")

parameters = {
  'start':start,
  'limit':limit,
  'convert':convert,
  'sort':sort,
}

session = Session()
session.headers.update(headers)

response = session.get(ticker_url, params=parameters)
results = json.loads(response.text)

# print(json.dumps(results, sort_keys=True, indent=4))

data = results['data']

for currency in data:
    rank = currency['cmc_rank']
    name = currency['name']
    symbol = currency['symbol']

    circulating_supply = int(currency['circulating_supply'])
    total_supply = int(currency['total_supply'])

    quotes = currency['quote'][convert]
    market_cap = quotes['market_cap']
    percent_change_1h = quotes['percent_change_1h']
    percent_change_24h = quotes['percent_change_24h']
    percent_change_7d = quotes['percent_change_7d']
    price = quotes['price']
    volume =quotes['volume_24h']

    volume_string = '{:,}'.format(volume)
    market_cap_string = '{:,}'.format(market_cap)
    circulating_supply_string = '{:,}'.format(circulating_supply)
    total_supply_string = '{:,}'.format(total_supply)

    print()

    print(str(rank) + ':' + name + '(' + symbol + ')')
    print("Convert :\t\t" + convert)
    print("Market cap: \t\t" + market_cap_string)
    print("Price: $\t\t" + str(price))
    print("24h Volume: \t\t" + volume_string)
    print("Hour change: \t\t" + str(percent_change_1h) + "%")
    print("Day change: \t\t" + str(percent_change_24h) + "%")
    print("Week change: \t\t" + str(percent_change_7d) + "%")
    print("Total supply: \t\t" + total_supply_string)
    print("Circulating supply: \t" + circulating_supply_string)
    print("Percentage of coin in circulating: " + str((int(circulating_supply)/total_supply)*100) + "%")

    print()




