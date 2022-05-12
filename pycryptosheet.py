import json
import os
import datetime as dt

from binance.client import Client
import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac
from twisted.internet import task, reactor


# Font Colors
RED_DICT = {"foregroundColor": {
                "red": 0.99,
                "green": 0.0,
                "blue": 0.0}}

GREEN_DICT = {"foregroundColor": {
                "red": 0.0,
                "green": 0.66,
                "blue": 0.0}}


def get_price_by_symbol(symbol="BTCBUSD"):

    try:

        for sym_dic in ALL_CRYPTO_PRICES:

            if sym_dic["symbol"] == symbol:
                return float(sym_dic["price"])

        return 0.0

    except Exception as e:
        print("[ERROR] Unable get price:", symbol, e)


def update_cells(symbol, col, row, update_colors=True):

    try:
        cell = "{}{}".format(col, row)
        # Get current binance price
        curr_price = get_price_by_symbol(symbol)

        # Get price on the sheet
        last_price = float(GD_WORKSHEET.acell(cell).value.replace(",", "."))

        # Update the new price value
        GD_WORKSHEET.update(cell, curr_price)

        # Update colors
        if update_colors:
            if last_price <= curr_price:
                GD_WORKSHEET.format(cell, {"textFormat": GREEN_DICT})
            else:
                GD_WORKSHEET.format(cell, {"textFormat": RED_DICT})

    except Exception as e:
        print("[ERROR] Unable to Update cells:", symbol,  e)


def loop():
    global ALL_CRYPTO_PRICES
    ALL_CRYPTO_PRICES = BIN_CLIENT.get_all_tickers()

    # Get time
    now = dt.datetime.now()
    timestamp = int(dt.datetime.timestamp(now))

    # Update sheet with crypto
    for symbol, cell_info in CRYPTO_MAP.items():
        update_cells(symbol, cell_info["col"], cell_info["row"])

    # Update timestamp on google sheet
    if TMS_CELL:
        GD_WORKSHEET.update(TMS_CELL, timestamp)


def parse_config_json():
    """Parse the configuration file"""

    global GOOGLE_CREDS_PATH
    global BIN_API_KEY
    global BIN_API_SECRET
    global SHEET_NAME
    global LOOP_TIMEOUT
    global TMS_CELL

    try:
        with open("config/config.json") as f:
            config = json.load(f)

        GOOGLE_CREDS_PATH = config["google_creds_path"]
        BIN_API_KEY = os.environ[config["binance_api_key"]]
        BIN_API_SECRET = os.environ[config["binance_api_secret"]]
        SHEET_NAME = config["sheet_name"]
        LOOP_TIMEOUT = config["loop_timeout"]
        TMS_CELL = config["timestamp_cell"]

    except KeyError:
        print("[INFO] Read raw binance creds")
        BIN_API_KEY = config["binance_api_key"]
        BIN_API_SECRET = config["binance_api_secret"]

    except Exception as e:
        print("[ERROR] Unable to parse config file:", e)


def parse_cryptos_json():
    """Parse the crypto mapper file"""

    global CRYPTO_MAP

    try:
        with open("config/cryptos.json") as f:
            CRYPTO_MAP = json.load(f)

    except Exception as e:
        print("[ERROR] Unable to parse crypto file:", e)


def main():
    """ Main method """

    global BIN_CLIENT
    global GD_WORKSHEET

    # Config file
    parse_config_json()

    # Crypto map file
    parse_cryptos_json()

    # Binance
    BIN_CLIENT = Client(BIN_API_KEY, BIN_API_SECRET)

    # Google Sheets
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]

    creds = sac.from_json_keyfile_name(GOOGLE_CREDS_PATH, scope)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME)
    GD_WORKSHEET = sheet.get_worksheet(0)

    # When Timeout is set a loop in seconds should start
    if LOOP_TIMEOUT > 0:
        loop_call = task.LoopingCall(loop)
        loop_call.start(LOOP_TIMEOUT)
        reactor.run()

    # else the loop would execute once
    else:
        loop()


if __name__ == "__main__":
    """ Continue on Main"""
    main()
