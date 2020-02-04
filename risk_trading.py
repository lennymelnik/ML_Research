import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import random
import sys
import data
BTCUSDTPrice = requests.get("https://api.binance.com/api/v1/ticker/price?symbol=BTCUSDT")
BTCUSDTPrice = BTCUSDTPrice.json()['price']



seeResults = 'n'
def convertToBTC(usdAmount, day):

    return(usdAmount/int(float(data.df["Close"][timeRange - day])))

def convertToUSD(btcAmount, day):

    return(btcAmount *int(float(data.df["Close"][timeRange - day])))

def SimpleMovingAvg(number, starting, sma = 0):
    for i in range(number):
        sma = sma + int(float(data.df["Close"][starting + 1 + i]))
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

    inUSD = 15000
    startingFund = 15000
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

                dayCompare = int(float(data.df["Close"][timeRange - i]))
                dayPrevious = int(float(data.df["Close"][timeRange - i - 1]))
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

for i in range(50):
    print(max(endValue))
    finalValue = endValue.index(max(endValue))
    print("Sell at:", randIntTop[finalValue], " Buy at: ", randIntBottom[finalValue], "price :", buySell[finalValue])
    endValue.remove(max(endValue))
