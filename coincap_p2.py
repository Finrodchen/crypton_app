import os
import json
import time
from requests import Request, Session
from datetime import datetime
from gtts import gTTS

print()
print('Alert tracking...')
print()

already_hit_symbol = []

convert_choice = 'USD'

while True:
    with open('alert.txt') as inp:
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

            name = currency['name']
            symbol = currency['symbol']
            last_updated = currency['last_updated']
            quotes = currency['quote'][convert_choice]
            price = quotes['price']

            if float(price) >= float(amount) and symbol not in already_hit_symbol:
                print(symbol + '\thit\t' + amount + '\ton\t' + last_updated)
                already_hit_symbol.append(symbol)

    tts = gTTS(text = "There's some cryptoncurrency hit taget price.", lang='en')
    tts.save('alert_words.mp3')
    os.system('start alert_words.mp3')
    
    print()
    print('...')
    time.sleep(300)

