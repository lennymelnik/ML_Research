import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests


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


def convertToBTC(usdAmount, day):

    return(usdAmount/int(float(df["Close"][timeRange - day])))

def convertToUSD(btcAmount, day):

    return(btcAmount *int(float(df["Close"][timeRange - day])))

def SimpleMovingAvg(number, starting, sma = 0):
    for i in range(number):
        sma = sma + int(float(df["Close"][starting + 1 + i]))
    return sma/number


totalFunds = []

timeRange = 365*4
def backtest():

    inUSD = 15000
    startingFund = 15000
    inBitcoin = 0
    valueBought = 0


    print("First Day:   ", "Funds : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", int(float(df["Close"][timeRange])), "     SMA:   ", SimpleMovingAvg(200,(timeRange )))

    for i in range(timeRange):

        smaForDay = SimpleMovingAvg(200,(timeRange - i))
        dayCompare = int(float(df["Close"][timeRange - i]))

        if (dayCompare > (smaForDay * 1.05)):
            if (inUSD > 10000):
                inBitcoin = inBitcoin + convertToBTC(10000,i)
                inUSD = inUSD - 10000

                valueBought = dayCompare
                print("Buying:    ","Funds : ",inUSD,"   In Bitcoin: ", inBitcoin,"  Bitcoin Price: ", dayCompare, "     SMA:   ", smaForDay)

            elif (inBitcoin > 0 and inBitcoin < convertToUSD(10000, i)):

                inUSD = inUSD + convertToUSD(inBitcoin, i)

                inBitcoin = 0

                print("Partial Sell:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ",
                      dayCompare,
                      "    SMA:   ", smaForDay)

            if ((inUSD < 10000) and inBitcoin > 0 and inBitcoin < convertToBTC(10000, i)):
                print("Staying in:   ","USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare, "    SMA:   ", smaForDay)

            else:
                print("Don't do anything")

        elif (dayCompare < (smaForDay * .95)):

            if (inBitcoin >= convertToBTC(10000, i)):
                valueSold = dayCompare
                overallPercent = valueSold/valueBought
                inUSD = inUSD + convertToUSD(inBitcoin, i) * overallPercent
                inBitcoin = 0
                print("Selling:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare, "    SMA:   ", smaForDay)

            elif (inBitcoin > convertToBTC(10000, i)):

                inUSD = inUSD + convertToUSD(inBitcoin - convertToBTC(10000), i)
                inBitcoin = convertToBTC(10000,i)


                print("Partial Sell:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare,
                      "    SMA:   ", smaForDay)

            elif (inBitcoin == 0 and inUSD > 15000):

                tempFund = inUSD - 15000
                inUSD = 15000
                inBitcoin = convertToBTC(tempFund, i)

                print("Partial Buy:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare,
                      "    SMA:   ", smaForDay)

            else:
                print("Do nothing:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ",
                      dayCompare,
                      "    SMA:   ", smaForDay)

        else:
            print("Price difference does not matter")
        if (i == timeRange - 1):
            print("Final:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare,
                  "    SMA:   ", smaForDay, "   USD Afer:", inUSD + convertToUSD(inBitcoin, i), "    Profit:  ", inUSD + convertToUSD(inBitcoin, i) - startingFund)

        if (inBitcoin > 0):

            totalFund = inUSD + convertToUSD(inBitcoin, i)


        else:

            totalFund = inUSD

        totalFunds.append(totalFund)

        print(i)

print(backtest())
plt.plot(np.linspace(0,len(totalFunds),len(totalFunds)), totalFunds )
plt.show()
