
import requests
from datetime import datetime
from datetime import timedelta
import easygui
import time
from binance.client import Client
import array
import tulipy as ti

client = Client('1XGCXOq8RCHuKA0O322OHahi0Kg0KsSHsG4ai4Gbp7MmaLFwVEOxGoZ2G1KSjEAS','207ia9nrYf8OF3LDXjMPUShYxEDAQWUwJBxv1wzHUDmswHWlU1udgCHc7xxwyTiK')
cryptoCount = 1

arr = array.array('i',[])
small = 60
medium = 540
large = 960
def find(total, smallavgPrice = 0, mediumavgPrice = 0, largeavgPrice = 0):
    BTCUSDTPrice = requests.get("https://api.binance.com/api/v1/ticker/price?symbol=ALGOBTC")
    arr.insert(total, int(float(BTCUSDTPrice.json()['price'])))
    count = len(arr)
    if (count > small):
        for i in range(small):
            smallavgPrice = smallavgPrice + arr[count - 1 - i]

        #print("small: ",smallavgPrice/15)
        if (count > medium):
            for i in range(medium):
                mediumavgPrice = mediumavgPrice + arr[count - 1 - i]

            #print("medium :",mediumavgPrice / 30)
            if (count > large):
                for i in range(large):
                    largeavgPrice = largeavgPrice + arr[count - 1 - i]

                #print("large: ",largeavgPrice / 60)

    if (smallavgPrice > largeavgPrice and smallavgPrice > mediumavgPrice and count >= medium):

        print("Buy")
    elif (cryptoCount > 0 and smallavgPrice <= mediumavgPrice and count >= medium):

        print("Sell")
    time.sleep(900)
    find(total + 1)


find(0)
