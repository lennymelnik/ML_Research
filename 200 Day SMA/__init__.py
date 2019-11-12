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

print("Do you want to see every step? (Y/N)")
seeResults = input()

print("Do you want to trade using SMA(1) or Historical Risk(2)")
whatMethod = input()

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
finalFund = 0
timeRange = 365*4

def backtest():
    if(whatMethod == 1):
        inUSD = 15000
        startingFund = 15000
        inBitcoin = 0
        valueBought = 0
        if(seeResults == 'y'):
            print("First Day:   ", "Funds : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", int(float(df["Close"][timeRange])), "     SMA:   ", SimpleMovingAvg(200,(timeRange )))
        
        for i in range(timeRange):

            smaForDay = SimpleMovingAvg(200,(timeRange - i))
            dayCompare = int(float(df["Close"][timeRange - i]))
            if (i>0):
                dayPrevious = int(float(df["Close"][timeRange - i - 1]))
                difference = (dayCompare / dayPrevious) * 100 - 100
                differenceList.append(difference)

            if (dayCompare > (smaForDay * 1.05)):
                if (inUSD > 10000):
                    inBitcoin = inBitcoin + convertToBTC(10000,i)
                    inUSD = inUSD - 10000
                    valueBought = dayCompare
                    if(seeResults == 'y'):
                        print("Buying:    ","Funds : ",inUSD,"   In Bitcoin: ", inBitcoin,"  Bitcoin Price: ", dayCompare, "     SMA:   ", smaForDay)

                elif (inBitcoin > 0 and inBitcoin < convertToUSD(10000, i)):

                    inUSD = inUSD + convertToUSD(inBitcoin, i)

                    inBitcoin = 0
                    if(seeResults == 'y'):
                        print("Partial Sell:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ",
                        dayCompare,
                        "    SMA:   ", smaForDay)

                if ((inUSD < 10000) and inBitcoin > 0 and inBitcoin < convertToBTC(10000, i)):
                    if(seeResults == 'y'):
                        print("Staying in:   ","USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare, "    SMA:   ", smaForDay)

                else:
                    if(seeResults == 'y'):
                        print("Don't do anything")

            elif (dayCompare < (smaForDay * .95)):

                if (inBitcoin >= convertToBTC(10000, i)):
                    valueSold = dayCompare
                    overallPercent = valueSold/valueBought
                    inUSD = inUSD + convertToUSD(inBitcoin, i) * overallPercent
                    inBitcoin = 0
                    if(seeResults == 'y'):
                        print("Selling:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare, "    SMA:   ", smaForDay)

                elif (inBitcoin > convertToBTC(10000, i)):

                    inUSD = inUSD + convertToUSD(inBitcoin - convertToBTC(10000), i)
                    inBitcoin = convertToBTC(10000,i)

                    if(seeResults == 'y'):
                        print("Partial Sell:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare,
                        "    SMA:   ", smaForDay)

                elif (inBitcoin == 0 and inUSD > 15000):

                    tempFund = inUSD - 15000
                    inUSD = 15000
                    inBitcoin = convertToBTC(tempFund, i)
                    if(seeResults == 'y'):
                        print("Partial Buy:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare,
                        "    SMA:   ", smaForDay)

                elif(seeResults == 'y'):
                    print("Do nothing:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ",
                        dayCompare,
                        "    SMA:   ", smaForDay)

            elif(seeResults == 'y'):
                print("Price difference does not matter")
            
                
            if (inBitcoin > 0):

                totalFund = inUSD + convertToUSD(inBitcoin, i)


            else:

                totalFund = inUSD
            totalFunds.append(totalFund)
            if (i == timeRange - 1):
                if(seeResults == 'y'):
                    print("Final:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare,
                    "    SMA:   ", smaForDay, "   USD Afer:", inUSD + convertToUSD(inBitcoin, i), "    Profit:  ", inUSD + convertToUSD(inBitcoin, i) - startingFund)
        
                return(totalFund)

    else:
        inUSD = 150000
        startingFund = 15000
        inBitcoin = 0
        valueBought = 0
        
        if(seeResults == 'y'):
            print("First Day:   ", "Funds : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", int(float(df["Close"][timeRange])), "     SMA:   ", SimpleMovingAvg(200,(timeRange )))
        
        for i in range(timeRange):
    
            
            if (i < timeRange):
                dayCompare = int(float(df["Close"][timeRange - i]))
                dayPrevious = int(float(df["Close"][timeRange - i - 1]))
                difference = (dayCompare / dayPrevious) * 100 - 100
                differenceList.append(difference)
                if(i > round(timeRange *.1)):
                    
                    percentLoss = returnRisk(timeRange, differenceList, finalFund)

                    if(percentLoss < -6.11):
                        if(seeResults == 'y'):
                            print("sell")
                        inUSD = inUSD + convertToUSD(inBitcoin * .99, i)
                        inBitcoin = inBitcoin * .01
                    elif(percentLoss > -1.04):
                        if(seeResults == 'y'):
                            print("buy/stay")
                        inBitcoin = inBitcoin + convertToBTC(inUSD *.99, i)
                        inUSD = inUSD * .01

            

                
            else:
                print("Done")
            finalFund = inUSD +convertToUSD(inBitcoin, i)
            totalFunds.append(finalFund)
        return finalFund
       
finalFund = backtest()
#print(finalFund)

    

plt.plot(np.linspace(0,len(totalFunds),len(totalFunds)), totalFunds )

plt.show()
