import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import requests
import time

BTCUSDTPrice = requests.get("https://api.binance.com/api/v1/ticker/price?symbol=BTCUSDT")
BTCUSDTPrice = BTCUSDTPrice.json()['price']
#Prices
names = ['Date','Symbol', 'Open', 'Close', 'Volume BTC', 'Volume USD']
url = 'http://www.cryptodatadownload.com/cdd/Coinbase_BTCUSD_d.csv'
df = pd.read_csv(url, skiprows=[0,1], header = None, delim_whitespace = True, na_values='?')

print(df)


new = df[0].str.split(",", n=7, expand=True)
length =len(df)

df["Date"] = new[0]
df["Symbol"] = new[1]
df["Open"] = new[2]
df["High"] = new[3]
df["Low"] = new[4]
df["Close"] = new[5]
df["Volume BTC"] = new[6]
df["Volume USD"] = new[7]

print(df)
length = len(df['Close'])
print(df['Close'][1])
def SimpleMovingAvg(number, starting, sma = 0):
    for i in range(number):
        sma = sma + int(float(df["Close"][starting + 1 + i]))
    return sma/number
daySMA = 200
timeRange = 365*2
def backtest():
    startingFund = 10000
    Funds = startingFund
    toBuy = startingFund
    minimum = Funds/2
    inBitcoin = 0
    valueBought = 0
    valueSold = 0

    print("First Day:   ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", int(float(df["Close"][timeRange])), "     SMA:   ", SimpleMovingAvg(daySMA,(timeRange )))

    for i in range(timeRange):
        hello = i
        currentAssets = 1
        smaForDay = SimpleMovingAvg(daySMA,(timeRange - i))
        dayCompare = int(float(df["Close"][timeRange - i]))
        dayStart = int(float(df["Close"][timeRange - i + 1]))

        #BUYING
        if (dayCompare > (smaForDay * 1.05)):
            if (Funds >= toBuy and inBitcoin < toBuy):
                Funds = Funds - toBuy
                inBitcoin = inBitcoin + toBuy
                valueBought = dayCompare
                print("Buying:    ","Funds : ",Funds,"   In Bitcoin: ", inBitcoin,"  Bitcoin Price: ", dayCompare, "     SMA:   ", smaForDay)
                print(i)
            elif (Funds < toBuy and inBitcoin > 0):

                print("Staying in:   ","Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare, "    SMA:   ", smaForDay)
                print(i)
            elif (Funds < toBuy and inBitcoin == 0):

                print("Lost Money:   ","Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare, "    SMA:   ", smaForDay)
                print(i)
            elif (inBitcoin > 0 and inBitcoin < toBuy):
                valuePartialSold = dayCompare
                Funds = Funds + inBitcoin * valuePartialSold/valuePartialBought
                inBitcoin = 0
                print("Partial Sell:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ",
                      dayCompare,
                      "    SMA:   ", smaForDay)
                print(i)

        #SELLING
        elif (dayCompare < (smaForDay * .80)):
            # BUYING IF BELOW ORIGINAL AND NO BITCOIN IS OWNED
            if (inBitcoin < 1 and Funds > startingFund):
                valuePartialBought = dayCompare
                tempFund = Funds - startingFund
                Funds = startingFund
                inBitcoin = tempFund
                print("Partial Buy:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare,
                  "    SMA:   ", smaForDay)
                print(i)

        elif (dayCompare < (smaForDay * .95)):
            if (inBitcoin == toBuy):
                valueSold = dayCompare

                overallSell = toBuy
                overallPercent = valueSold/valueBought
                Funds = Funds + overallSell * overallPercent
                inBitcoin = 0

                print("Selling:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare, "    SMA:   ", smaForDay)
                print(i)
            #SELL EVERYTHING
            elif (inBitcoin > toBuy):
                valueSold = dayCompare
                partialSell = inBitcoin - toBuy
                overallPercent = valueSold / valueBought
                partialPercent = valueSold / valuePartialBought
                Funds = Funds + toBuy * overallPercent + partialSell * partialPercent
                inBitcoin = 0
                print("Selling w/profit:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ",
                      dayCompare,
                      "    SMA:   ", smaForDay)
                print(i)

            elif (inBitcoin == 0 and Funds <= startingFund):

                print("Staying out:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ",
                      dayCompare,
                      "    SMA:   ", smaForDay)
                print(i)
            else:
                print("Do nothing:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ",
                      dayCompare,
                      "    SMA:   ", smaForDay)
                print(i)

        if (i == timeRange - 1):
            print("Final:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare,
                  "    SMA:   ", smaForDay, "   USD Afer:", Funds + inBitcoin * (dayCompare/valueBought), "    Profit:  ", Funds + inBitcoin * (dayCompare/valueBought) - startingFund)

print(backtest())