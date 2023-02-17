import requests
import json
from speech import audio

a = "tether"

def call_api(a):
    url = f"https://api.coingecko.com/api/v3/coins/{a}?localization=false"
    headers = {'X-Auth-Token': 'YOUR_API_KEY'}
    response = requests.get(url, headers=headers)
    if (response.status_code == 200):
        data = response.json()
        currency = data['id']
        price_thb = data['market_data']['current_price']['thb']
        last_date = data['last_updated']
        img_currency = data['image']['large']
        return price_thb, currency
        
    else :return ("Coin not found.")


price, currency = call_api(a)
print(currency, price)