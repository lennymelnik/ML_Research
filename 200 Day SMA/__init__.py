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

def SimpleMovingAvg(number, starting, sma = 0):
    for i in range(number):
        sma = sma + int(float(df["Close"][starting + 1 + i]))
    return sma/number
totalFunds = []

timeRange = 365*4
def backtest():
    Funds = 15000
    startingFund = 15000

    inBitcoin = 0
    valueBought = 0


    print("First Day:   ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", int(float(df["Close"][timeRange])), "     SMA:   ", SimpleMovingAvg(200,(timeRange )))

    for i in range(timeRange):

        smaForDay = SimpleMovingAvg(200,(timeRange - i))
        dayCompare = int(float(df["Close"][timeRange - i]))

        if (dayCompare > (smaForDay * 1.05)):
            if (Funds >= 10000):
                Funds = Funds - 10000
                inBitcoin = inBitcoin + 10000
                valueBought = dayCompare
                print("Buying:    ","Funds : ",Funds,"   In Bitcoin: ", inBitcoin,"  Bitcoin Price: ", dayCompare, "     SMA:   ", smaForDay)
                
            elif (inBitcoin > 0 and inBitcoin < 10000):

                Funds = Funds + inBitcoin * dayCompare/valuePartialBought
                inBitcoin = 0
                print("Partial Sell:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ",
                      dayCompare,
                      "    SMA:   ", smaForDay)
            if ((Funds < 10000) and inBitcoin > 0 and inBitcoin < 10000):
                print("Staying in:   ","Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare, "    SMA:   ", smaForDay)



        elif (dayCompare < (smaForDay * .95)):
            if (inBitcoin >= 10000):
                valueSold = dayCompare
                overallSell = 10000
                overallPercent = valueSold/valueBought
                Funds = Funds + overallSell * overallPercent
                inBitcoin = 0
                print("Selling:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare, "    SMA:   ", smaForDay)
            elif (inBitcoin > 10000):
                valueSold = dayCompare
                partialSell = inBitcoin - 10000
                overallPercent = valueSold / valueBought
                partialPercent = valueSold / valuePartialBought
                Funds = Funds + 10000 * overallPercent + partialSell * partialPercent
                inBitcoin = 0
            elif (inBitcoin == 0 and Funds > 15000):
                valuePartialBought = dayCompare
                tempFund = Funds - 15000
                Funds = 15000
                inBitcoin = tempFund
                print("Partial Buy:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare,
                      "    SMA:   ", smaForDay)

        if (i == timeRange - 1):
            print("Final:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare,
                  "    SMA:   ", smaForDay, "   USD Afer:", Funds + inBitcoin * (dayCompare/valueBought), "    Profit:  ", Funds + inBitcoin * (dayCompare/valueBought) - startingFund)
        if (inBitcoin > 0):
            totalFund = Funds + inBitcoin * dayCompare / valueBought
        else:
            totalFund = Funds
        totalFunds.append(totalFund)
        print(i)

print(backtest())
plt.plot(np.linspace(0,len(totalFunds),len(totalFunds)), totalFunds )
plt.show()
