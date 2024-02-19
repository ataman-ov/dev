import requests

def get_opt_usd_buy():
    url = 'ввести URL для получения обекта JSON'
    r = requests.get(url).json()
    price = r['acf']['opt_usd_buy']

    url = 'ввести URL для получения обекта JSON'
    r = requests.get(url).json()
    price = r['acf']['opt_usd_sell']

    url = 'ввести URL для получения обекта JSON'
    r = requests.get(url).json()
    price = r['acf']['opt_eur_buy']

    url = 'ввести URL для получения обекта JSON'
    r = requests.get(url).json()
    price = r['acf']['opt_eur_sell']

    url = 'ввести URL для получения обекта JSON'
    r = requests.get(url).json()
    price = r['acf']['opt_uah_buy']

    url = 'ввести URL для получения обекта JSON'
    r = requests.get(url).json()
    price = r['acf']['opt_uah_sell']
    #print(str(price) + ' rub')

    #return str(price) + ' rub'

print(get_opt_usd_buy())
