# Pycryptosheet

  

[![Na|solid](https://img.shields.io/badge/license-GPL-brightgreen)](https://github.com/alturiano/pycryptosheet/blob/main/LICENSE) ![Na|solid](https://img.shields.io/badge/python-3.8-brightgreen) ![example workflow](https://github.com/alturiano/pycryptosheet/actions/workflows/python-app.yml/badge.svg)

 
Get the latest prices of several crypto assets on **Google Sheets**. Download the sheet in excel format if required.
  
Several crypto-third-party tools could be potentially connected to google sheets as addons but you may lose your privacy by giving them your permissions. This project is aimed to the people who want real-time prices of **cryptocurrencies** preserving privacy.


Excel Sheets is an extraordinary tool to make finance calculations, in case you want to know how your portfolio is going or take investing decisions based on prices, volumes, liquidity, etc.

https://user-images.githubusercontent.com/22453747/177639922-a12ca486-471d-4f8d-a412-ed5b606b5149.mp4
  

# Prerequisites

- Binance as the main exchange to get cryptocurrency data. A Binance [API](https://www.binance.com/en/support/faq/360002502072) Key is required.
- Google Sheets API using the gspread python library. You can follow [this](https://docs.gspread.org/en/latest/oauth2.html) tutorial to get access to google sheets via service account.
-  Python3

# Configuration

1. The main configuration is located at `config/config.json`  and should be filled with:

- `google_creds_path`: path of the **JSON** with the google service account credentials.
- `binance_api_key`: string with your binance **API** key. It's prefered and more securely to use the environment variable **BIN_API_KEY**.
- `binance_api_secret`: string with your binance **API** secret. It's prefered and more securely to use the environment variable **BIN_API_SECRET**.
- `sheet_name`: your google drive sheet name must be exactly the same name.
- `loop_timeout` : the program could be executed every **X** seconds in a loop, **0** when no loop is required.
- `timestamp_cell`: sheet coordinate with the last timestamp, **0** or **None** if you don't want this.

2. A new Google Sheet should be created on Google Drive. This sheet must have the same name as the `sheet_name` in `config/config.json`, then you must share it to the google service account email located in your google credentials json (`client_email` field). To share the sheet with this account you have to open the sheet, and hit share button on the upper right then puth the service account email and give **edit permissions**.

3. 
# Usage

  
  
  


