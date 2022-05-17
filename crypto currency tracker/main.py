import keys
import requests
import pandas as pd
from time import sleep

def get_crypto_rates(base_currency = "INR",assets = "BTC,ETH,XRP"):
    url = "https://api.nomics.com/v1/currencies/ticker"
    payload = {'key': keys.NOMICS_API_KEY,'convert': base_currency,'ids': assets,'interval':'1d'}
    response = requests.get(url,params=payload)
    data = response.json()

    crypto_currency,crypto_price,crypto_timestamp = [] ,[] ,[]

    for assets in data:
        crypto_currency.append(assets['currency'])
        crypto_price.append(assets['price'])
        crypto_timestamp.append(assets['price_timestamp'])

    raw_data = {
        'assets': crypto_currency,
        'rates' : crypto_price,
        'timestamp' : crypto_timestamp
    }
    df = pd.DataFrame(raw_data)
    return df

def set_alert(dataframe,asset,alert_high_price):
    crypto_value = float(dataframe[dataframe['assets']== asset]['rates'].item())
    details = f'{asset}: {crypto_value}, Target: {alert_high_price}'

    if crypto_value >= alert_high_price:
        print(details,'Target value reached!')
    else:
        print(details)


loop = 0
while True:
    print(f'----------------------------------({loop})-------------------------------------')

    try:
        df = get_crypto_rates()
        set_alert(df,'BTC',3000000)
        set_alert(df,'ETH',300000)
        set_alert(df,'XRP',100)
    except Exception as e:
        print("Could not retrieve data... Trying again.")
    
    loop +=1
    sleep(30)
    