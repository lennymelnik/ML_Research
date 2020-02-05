import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import random
import sys
import csv



with open("stocks.csv") as f:
    reader = csv.reader(f)
    liste = list(reader)
print(liste[0])

csv_list = []
number2 = 0
""" for i in liste:
    print(i[1:])
    print(yf.Ticker(i[2:-2]).history(period="max")["Close"])
    number2 = number2 + 1
print(csv_list) """

#BTCUSDTPrice = requests.get("https://api.binance.com/api/v1/ticker/price?symbol=BTCUSDT")
#BTCUSDTPrice = BTCUSDTPrice.json()['price']
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


seeResults = 'n'
def convertToBTC(usdAmount, day):

    return(usdAmount/int(float(df["Close"][timeRange - day])))

def convertToUSD(btcAmount, day):

    return(btcAmount *int(float(df["Close"][timeRange - day])))

def SimpleMovingAvg(number, starting, sma = 0):
    for i in range(number):
        sma = sma + int(float(df["Close"][starting + 1 + i]))
    return sma/number

def returnRisk(timerange, differentList, finalFund):
    fivePercent = sorted(differenceList)
    fivePercent = fivePercent[:round(timeRange *.05)]
    if(seeResults == 'y'):
        print("We have 95% confidence that our loss will not exceed ", fivePercent[round(timeRange * .05 -1)]* .01 * finalFund, "which is ", fivePercent[round(timeRange * .05 -1)], "% of our funds" )
        print("Funds", finalFund)
    return(fivePercent[round(timeRange * .05 -1)])


totalFunds = []
differenceList = []

randIntTop = []
randIntBottom = []
endValue = []
buySell = []
finalFund = 0
timeRange = 365*4

testingAmount = 100
sys.stdout.write("[%s]" % (" " * 40))
sys.stdout.flush()
sys.stdout.write("\b" * (40+1))
for i in range(testingAmount):

    inUSD = 1000
    startingFund = 1000
    inBitcoin = 0
    valueBought = 0

    if((i % round(testingAmount/40)) == 0):
        sys.stdout.write("-")
        sys.stdout.flush()
            
    if(seeResults == 'y'):
        print("First Day:   ", "Funds : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", int(float(df["Close"][timeRange])), "     SMA:   ", SimpleMovingAvg(200,(timeRange )))
    topTemp = random.randint(-1500,700)
    top = topTemp * .01
    bottom = random.randint(topTemp, 700) * .01
    for i in range(100):
        payPrice = .01 * i
        for i in range(timeRange):
            
                    
            if (i < timeRange):

                dayCompare = int(float(df["Close"][timeRange - i]))
                dayPrevious = int(float(df["Close"][timeRange - i - 1]))
                difference = (dayCompare / dayPrevious) * 100 - 100
                differenceList.append(difference)
                
                if(i > round(timeRange *.1)):
                    finalFund = inUSD +convertToUSD(inBitcoin, i)
                    percentLoss = returnRisk(timeRange, differenceList, finalFund)
                    

                    if(percentLoss < top):
                        if(seeResults == 'y'):
                            print("sell")
                        inUSD = inUSD + convertToUSD(inBitcoin * payPrice, i)
                        inBitcoin = inBitcoin * (1 - payPrice)
                    elif(percentLoss > bottom):
                        if(seeResults == 'y'):
                            print("buy/stay")
                        inBitcoin = inBitcoin + convertToBTC(inUSD * payPrice, i)
                        inUSD = inUSD * (1 - payPrice)
                
                totalFunds.append(inUSD + convertToUSD(inBitcoin, i))
                
                

            else:
                print("Done")
        
        #plt.plot(np.linspace(0, len(totalFunds), len(totalFunds)), totalFunds)
        #plt.show()
        endValue.append(inUSD + convertToUSD(inBitcoin, i))
        randIntTop.append(top)
        randIntBottom.append(bottom)
        buySell.append(payPrice)
        totalFunds = []
        differenceList = []
        ##print(inUSD + convertToUSD(inBitcoin, i))
    
sys.stdout.write("]\n")
print(max(endValue))

finalValue = endValue.index(max(endValue))
print("Sell at:", randIntTop[finalValue], " Buy at: ", randIntBottom[finalValue], "price :", buySell[finalValue])
