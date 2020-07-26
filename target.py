"""Logic to query the target api"""
import os
import requests
import json

def get_price_history(price_history_file_path) -> list:
    jj = []
    if os.path.isfile(price_history_file_path):
        with open(price_history_file_path) as f:
            jj = json.load(f)

    return jj


def price_has_changed(current_price: list, last_price: list) -> bool:
    if not last_price:
        return True 
    else:
        # not sure which one of these changes, so compare all of them
        price_fields = ['reg_retail', 'current_retail', 'formatted_current_price']
        for field in price_fields:
            if current_price[0][field] != last_price[-1][field]:
                return True
        else:
            return False


def get_price_for_item(product_id) -> tuple:
    s = requests.session()
    s.get('https://www.target.com')

    key = s.cookies['visitorId']
    location = s.cookies['GuestLocation'].split('|')[0]

    store_id = requests.get('https://redsky.target.com/v3/stores/nearby/%s?key=%s&limit=1&within=100&unit=mile' %(location, key)).json()
    store_id = store_id[0]['locations'][0]['location_id']

    url = 'https://redsky.target.com/web/pdp_location/v1/tcin/%s' %product_id
    payload = {
    'pricing_store_id': store_id,
    'key': key}

    jsonData = requests.get(url, params=payload).json()
    return jsonData['price'],


