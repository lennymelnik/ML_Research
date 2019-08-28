import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import requests
import time
from lossGain import lossGain

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


#def standardDeviation
daySMA = 200
timeRange = 365

differenceList = []
finalFund = 0

def backtest():
    startingFund = 10000
    Funds = startingFund
    toBuy = startingFund
    minimum = Funds/2
    inBitcoin = 0
    valueBought = 0
    valueSold = 0

    print("First Day:   ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", int(float(df["Close"][timeRange])), "     SMA:   ", SimpleMovingAvg(daySMA,(timeRange )), "     Standard Deviation: ")

    for i in range(timeRange):
        hello = i
        currentAssets = 1
        smaForDay = SimpleMovingAvg(daySMA,(timeRange - i))
        dayCompare = int(float(df["Close"][timeRange - i]))
        if (i>0):
            dayPrevious = int(float(df["Close"][timeRange - i - 1]))
            difference = (dayCompare / dayPrevious) * 100 - 100
            print("Difference ", difference, "%")
            print()
            differenceList.append(difference)


        dayStart = int(float(df["Close"][timeRange - i + 1]))


        #BUYING
        if (dayCompare > (smaForDay * 1.05)):
            if (Funds >= toBuy and inBitcoin < toBuy):
                Funds = Funds - toBuy
                inBitcoin = inBitcoin + toBuy
                valueBought = dayCompare
                print("Buying:    ","Funds : ",Funds,"   In Bitcoin: ", inBitcoin,"  Bitcoin Price: ", dayCompare, "     SMA:   ", smaForDay, "     Standard Deviation: ")
                print(i)
            elif (Funds < toBuy and inBitcoin > 0):

                print("Staying in:   ","Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare, "    SMA:   ", smaForDay, "     Standard Deviation: ")
                print(i)
            elif (Funds < toBuy and inBitcoin == 0):

                print("Lost Money:   ","Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare, "    SMA:   ", smaForDay, "     Standard Deviation: ")
                print(i)
            elif (inBitcoin > 0 and inBitcoin < toBuy):
                valuePartialSold = dayCompare
                Funds = Funds + inBitcoin * valuePartialSold/valuePartialBought
                inBitcoin = 0
                print("Partial Sell:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ",
                      dayCompare,
                      "    SMA:   ", smaForDay, "     Standard Deviation: ")
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
                  "    SMA:   ", smaForDay, "     Standard Deviation: ")
                print(i)

        elif (dayCompare < (smaForDay * .95)):
            if (inBitcoin == toBuy):
                valueSold = dayCompare

                overallSell = toBuy
                overallPercent = valueSold/valueBought
                Funds = Funds + overallSell * overallPercent
                inBitcoin = 0

                print("Selling:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare, "    SMA:   ", smaForDay, "     Standard Deviation: ")
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
                      "    SMA:   ", smaForDay, "     Standard Deviation: ")
                print(i)

            elif (inBitcoin == 0 and Funds <= startingFund):

                print("Staying out:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ",
                      dayCompare,
                      "    SMA:   ", smaForDay, "     Standard Deviation: ")
                print(i)
            else:
                print("Do nothing:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ",
                      dayCompare,
                      "    SMA:   ", smaForDay, "     Standard Deviation: ")
                print(i)

        if (i == timeRange - 1):
            finalFund = Funds + inBitcoin * (dayCompare/valueBought) - startingFund
            print("Final:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare,
                  "    SMA:   ", smaForDay, "   USD Afer:", Funds + inBitcoin * (dayCompare/valueBought), "    Profit:  ", Funds + inBitcoin * (dayCompare/valueBought) - startingFund)

print(backtest())


#Plot Close Data
y = df.head(100)["Close"]
y = pd.to_numeric(y)
plt.plot(np.linspace(0,100,100),y,'k')
plt.xlabel("The Past 100 Days")
plt.ylabel("Bitcoin Closing Price")
plt.show()
timeHa = str(timeRange)
y = differenceList
plt.plot(np.linspace(0,len(y),len(y)),y,'k')
print(len(y))
plt.xlabel("The Past " + timeHa +" Days")
plt.ylabel("Bitcoin Gain/Loss")
plt.show()

print("Difference List: ", differenceList)

fivePercent = sorted(differenceList)
fivePercent = fivePercent[:round(timeRange *.05)]
print("Five Percent", fivePercent)
timeHa2 =  str(round(timeRange * .05))
print("We have 95% conference that our loss will not exceed ", fivePercent[round(timeRange * .05 -1)],"%")
print("Funds", finalFund)
y = fivePercent
plt.plot(np.linspace(0,len(y),len(y)),y,'o')
print(len(y))
print("Timerange ",timeRange)

plt.xlabel("The Past " + timeHa2 +" Days")
plt.ylabel("Lowest 5 Percent")
plt.show()
