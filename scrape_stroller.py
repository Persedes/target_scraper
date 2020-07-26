"""Script that fetches price history for stroller and sends email if it changes."""
import requests
import json
import os
import mail
import dotenv
import datetime

from target import get_price_history, price_has_changed, get_price_for_item

PRICE_HISTORY_FILE_PATH = "stroller_price.json"


def get_stroller_price() -> tuple:
    product_id = '76429219'
    return get_price_for_item(product_id)


if __name__ == "__main__":
    dotenv.load_dotenv()
    current_price = get_stroller_price()
    last_price = get_price_history(price_history_file_path=PRICE_HISTORY_FILE_PATH)

    # if price fields differ send email
    if price_has_changed(current_price, last_price):
        json_string = json.dumps(current_price, indent=2, sort_keys=True)
        print(json_string)
        msg = mail.create_message(
                sender=os.environ["SENDER"],
                to=os.environ["TO"],
                subject="Stroller price change found!",
                message_text=f"New price for stroller found: {json_string}"
        )
        mail.send_via_smtp(sender=os.environ["SENDER"], to=list(map(str.strip, os.environ["TO"].split(","))), message=msg)

        # lastly dump the new price to file
        last_price.append(current_price[0])
        with open(PRICE_HISTORY_FILE, "w") as f:
            json.dump(last_price, f)

    # once a day send a "still alive memo" 
    elif datetime.datetime.now().hour == 19: 
        msg = mail.create_message(
                sender=os.environ["SENDER"],
                to=os.environ["SENDER"],
                subject="Stroller scraper still running",
                message_text=f"Hello :), current price:\n {json_string}"
        )
        mail.send_via_smtp(sender=os.environ["SENDER"], to=os.environ["SENDER"], message=msg)
    else:
         print("No price change detected")


