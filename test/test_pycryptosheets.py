import sys
from pathlib import Path
import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac
from twisted.internet import reactor

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pycryptosheet  # noqa: E402


class MockCell():
    value = "123,456"

    def __init__(self):
        pass


class MockBinClient():
    def __init__(self):
        pass

    def get_all_tickers(self):
        return "SucessMock"


class MockSheet():
    color = None

    def __init__(self, sheet_name):
        pass

    def get_worksheet(self, sheet):
        return "SucessMock"

    def update(self, cell, tms):
        return "SucessMock"

    def acell(self, cell):
        return MockCell()

    def format(self, cell, color):
        self.color = color["textFormat"]


class MockSheetClient():

    def __init__(self, mock):
        pass

    def open(self, sheet_name):
        return MockSheet(sheet_name)


def mock_authorize(mock):
    return MockSheetClient(mock)


def mock_parse_config_timeout_json():

    pycryptosheet.GOOGLE_CREDS_PATH = "sfafgasdgf"
    pycryptosheet.BIN_API_KEY = "asdfdasfas"
    pycryptosheet.BIN_API_SECRET = "sfsdgasdgasdfgas"
    pycryptosheet.SHEET_NAME = None
    pycryptosheet.LOOP_TIMEOUT = 60
    pycryptosheet.TMS_CELL = None


def test_parse_cryptos_json():

    pycryptosheet.parse_cryptos_json()

    with open("config/cryptos.json") as f:
        crypto_map = json.load(f)
    assert list(crypto_map.values()) == list(pycryptosheet.CRYPTO_MAP.values())
    assert isinstance(pycryptosheet.CRYPTO_MAP, dict)


def test_parse_config_json(monkeypatch):

    monkeypatch.setenv("BIN_API_KEY", "key")
    monkeypatch.setenv("BIN_API_SECRET", "secret")
    
    pycryptosheet.parse_config_json()

    assert isinstance(pycryptosheet.SHEET_NAME, str)
    assert isinstance(pycryptosheet.LOOP_TIMEOUT, int)
    assert isinstance(pycryptosheet.TMS_CELL, str)


def test_parse_delenv_config_json(monkeypatch):

    monkeypatch.delenv("BIN_API_KEY", raising=False)
    monkeypatch.delenv("BIN_API_SECRET", raising=False)

    pycryptosheet.parse_config_json()

    assert "BIN_API_KEY" == pycryptosheet.BIN_API_KEY
    assert "BIN_API_SECRET" == pycryptosheet.BIN_API_SECRET


def test_main_one_loop(monkeypatch):

    monkeypatch.setattr(pycryptosheet, "loop", lambda: None)
    monkeypatch.setattr(pycryptosheet, "parse_config_json", lambda: None)
    monkeypatch.setattr(sac, "from_json_keyfile_name", lambda x, y: None)
    monkeypatch.setattr(gspread, "authorize", mock_authorize)

    pycryptosheet.LOOP_TIMEOUT = 0

    pycryptosheet.main()

    assert MockSheet(None).get_worksheet(None) == pycryptosheet.GD_WORKSHEET


def test_main_multiple_loop(monkeypatch):

    monkeypatch.setattr(pycryptosheet, "parse_config_json",
                        mock_parse_config_timeout_json)
    monkeypatch.setattr(reactor, "run", lambda: None)
    monkeypatch.setattr(pycryptosheet, "loop", lambda: None)
    monkeypatch.setattr(sac, "from_json_keyfile_name", lambda x, y: None)
    monkeypatch.setattr(gspread, "authorize", mock_authorize)

    pycryptosheet.LOOP_TIMEOUT = 60

    pycryptosheet.main()

    assert MockSheet(None).get_worksheet(None) == pycryptosheet.GD_WORKSHEET


def test_loop(monkeypatch):

    monkeypatch.setattr(pycryptosheet, "update_cells", lambda x, y, z: None)
    pycryptosheet.CRYPTO_MAP = {"BTCBUSD": {"col": "A", "row": "1"}}
    pycryptosheet.BIN_CLIENT = MockBinClient()
    pycryptosheet.TMS_CELL = 1
    pycryptosheet.GD_WORKSHEET = MockSheet(None)

    pycryptosheet.loop()

    assert pycryptosheet.ALL_CRYPTO_PRICES == MockBinClient().get_all_tickers()


def test_update_smaller_cells(monkeypatch):
    monkeypatch.setattr(pycryptosheet, "get_price_by_symbol", lambda x: 1)
    pycryptosheet.GD_WORKSHEET = MockSheet(None)

    pycryptosheet.update_cells("BTCBUSD", "A", "1")

    assert pycryptosheet.GD_WORKSHEET.color == pycryptosheet.RED_DICT


def test_update_greater_cells(monkeypatch):

    monkeypatch.setattr(pycryptosheet, "get_price_by_symbol",
                        lambda x: 987.654)
    pycryptosheet.GD_WORKSHEET = MockSheet(None)

    pycryptosheet.update_cells("BTCBUSD", "A", "1")

    assert pycryptosheet.GD_WORKSHEET.color == pycryptosheet.GREEN_DICT


def test_get_good_price_by_symbol():
    price = 100.000
    pycryptosheet.ALL_CRYPTO_PRICES = [{"symbol": "BTCBUSD", "price": price}]

    result = pycryptosheet.get_price_by_symbol()

    assert result == price


def test_get_bad_price_by_symbol():

    pycryptosheet.ALL_CRYPTO_PRICES = [{"symbol": "WHATEVER", "price": 123}]

    result = pycryptosheet.get_price_by_symbol()

    assert result == 0.0
