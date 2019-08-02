import requests
from datetime import datetime
from datetime import timedelta
import easygui
import time
import array
from coinbase.wallet.client import Client
import tulipy as ti

client = Client('1XGCXOq8RCHuKA0O322OHahi0Kg0KsSHsG4ai4Gbp7MmaLFwVEOxGoZ2G1KSjEAS','207ia9nrYf8OF3LDXjMPUShYxEDAQWUwJBxv1wzHUDmswHWlU1udgCHc7xxwyTiK')
cryptoCount = 1

arr = array.array('i',[])

BTCUSDTPrice = requests.get("https://api.binance.com/api/v1/ticker/price?symbol=BTCUSDT")
print(BTCUSDTPrice.json())
arr.insert(1, int(float(BTCUSDTPrice.json()['price'])))
print(arr)