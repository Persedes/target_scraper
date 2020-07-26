import requests
import json
import os
import gmail
import dotenv
import datetime

PRICE_HISTORY_FILE = "stroller_price.json"

def get_stroller_price():

    s = requests.session()
    s.get('https://www.target.com')

    key = s.cookies['visitorId']
    location = s.cookies['GuestLocation'].split('|')[0]

    store_id = requests.get('https://redsky.target.com/v3/stores/nearby/%s?key=%s&limit=1&within=100&unit=mile' %(location, key)).json()
    store_id = store_id[0]['locations'][0]['location_id']

    product_id = '76429219'
    url = 'https://redsky.target.com/web/pdp_location/v1/tcin/%s' %product_id
    payload = {
    'pricing_store_id': store_id,
    'key': key}

    jsonData = requests.get(url, params=payload).json()
    return jsonData['price'],

def get_price_history():
    jj = []
    if os.path.isfile(PRICE_HISTORY_FILE):
        with open(PRICE_HISTORY_FILE) as f:
            jj = json.load(f)

    return jj


def price_has_changed(current_price: list, last_price: list):
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


if __name__ == "__main__":
    dotenv.load_dotenv()
    current_price = get_stroller_price()
    last_price = get_price_history()
    # if price fields differ send email
    if price_has_changed(current_price, last_price):
        json_string = json.dumps(current_price, indent=2, sort_keys=True)
        print(json_string)
        msg = gmail.create_message(
                sender=os.environ["SENDER"],
                to=os.environ["TO"],
                subject="Stroller price change found!",
                message_text=f"New price for stroller found: {json_string}"
        )
        gmail.send_via_smtp(sender=os.environ["SENDER"], to=list(map(str.strip, os.environ["TO"].split(","))), message=msg)

        # lastly dump the new price to file
        last_price.append(current_price[0])
        with open(PRICE_HISTORY_FILE, "w") as f:
            json.dump(last_price, f)
    elif datetime.datetime.now().hour == 19: 
        msg = gmail.create_message(
                sender=os.environ["SENDER"],
                to=os.environ["SENDER"],
                subject="Stroller scraper still running",
                message_text=f"Hello :), current price:\n {json_string}"
        )
        gmail.send_via_smtp(sender=os.environ["SENDER"], to=os.environ["SENDER"], message=msg)
    else:
         print("No price change detected")


