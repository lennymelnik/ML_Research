import requests
from datetime import datetime
from datetime import timedelta
import time
from binance.client import Client
import array

client = Client('1XGCXOq8RCHuKA0O322OHahi0Kg0KsSHsG4ai4Gbp7MmaLFwVEOxGoZ2G1KSjEAS','207ia9nrYf8OF3LDXjMPUShYxEDAQWUwJBxv1wzHUDmswHWlU1udgCHc7xxwyTiK')


cryptoCount = 1




print (depth)


arr = array.array('i',[])

def find(total, smallavgPrice = 0, mediumavgPrice = 0, largeavgPrice = 0):
    BTCUSDTPrice = requests.get("https://api.binance.com/api/v1/ticker/price?symbol=BTCUSDT")
    arr.insert(total, int(float(BTCUSDTPrice.json()['price'])))
    count = len(arr)
    if (count > 60):
        for i in range(60):
            smallavgPrice = smallavgPrice + arr[count - 1 - i]

        #print("small: ",smallavgPrice/15)
        if (count > 240):
            for i in range(240):
                mediumavgPrice = mediumavgPrice + arr[count - 1 - i]

            #print("medium :",mediumavgPrice / 30)
            if (count > 960):
                for i in range(960):
                    largeavgPrice = largeavgPrice + arr[count - 1 - i]

                #print("large: ",largeavgPrice / 60)

    if (smallavgPrice > largeavgPrice and smallavgPrice > mediumavgPrice and count >= 60):

        print("buy")
    elif (cryptoCount > 0 and smallavgPrice <= mediumavgPrice and count >= 60):

        print("sell")
    time.sleep(60)
    find(total + 1)


find(0)



