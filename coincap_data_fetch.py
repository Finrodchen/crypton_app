import json
import pandas as pd
from requests import Request, Session
from datetime import datetime

global_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters = {
  'start':'1',
  'limit':'100',
  'convert':'USD',
  'sort':'market_cap'
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '5d21df5e-b463-4783-af58-3af6a2062afd',
}

session = Session()
session.headers.update(headers)

response = session.get(global_url, params=parameters)
results = json.loads(response.text)
data = results['data']

df = pd.json_normalize(data)
final_df = df.drop(columns = ['tags', 'max_supply', 'num_market_pairs', 'slug', 'platform', 'quote.USD.last_updated', 'platform.id', 'platform.name', 'platform.symbol', 'platform.slug', 'platform.token_address'])

final_df.to_csv(f'./data/crypton.csv')