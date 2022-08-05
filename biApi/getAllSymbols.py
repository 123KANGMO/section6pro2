import requests

def get_response(url):
    response = requests.get(url)
    response.raise_for_status()  # raises exception when not a 2xx response
    if response.status_code != 204:
        return response.json()

def get_exchange_info():
    base_url = 'https://api2.binance.com'
    endpoint = '/api/v3/exchangeInfo'
    return get_response(base_url + endpoint)

def create_symbols_list(filter='USDT'):
    rows = []
    info = get_exchange_info()
    pairs_data = info['symbols']
    full_data_dic = {s['symbol']: s for s in pairs_data if filter in s['symbol']}
    return full_data_dic.keys()

print(create_symbols_list('USDT'))