import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import random
import sys
import csv
import math
import yfinance as yf
import time
import multiprocessing 

fullList = 0
def getTickerInfo():
    with open("stocks.csv") as f:
        reader = csv.reader(f)
        liste = list(reader)

    csv_list = []
    number2 = 0
    for i in liste:
        #Format to get ticker
        ticker = str(i)[2:-2]
        #Get closing price
        closingPrice = yf.Ticker(str(i)[2:-2]).history(period="max")['Close'][1:]
        number2 = number2 + 1
        csv_list.append(closingPrice)
        
    fullList = np.array(csv_list)
    
    for i in range(len(fullList)):
        fullList[i] = np.flip(fullList[i],0)


    return(fullList)
        
    






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
def convertToBTC(usdAmount, day, timerange):

    return(usdAmount/int(float(df["Close"][timerange - day])))

def convertToUSD(btcAmount, day, timerange):

    return(btcAmount *int(float(df["Close"][timerange - day])))

def SimpleMovingAvg(number, starting, sma = 0):
    for i in range(number):
        sma = sma + int(float(df["Close"][starting + 1 + i]))
    return sma/number

def returnRisk(timerange, differenceList, finalFund):
    fivePercent = sorted(differenceList)
    fivePercent = fivePercent[:round(timerange *.05)]
    if(seeResults == 'y'):
        print("We have 95% confidence that our loss will not exceed ", fivePercent[round(timerange * .05 -1)]* .01 * finalFund, "which is ", fivePercent[round(timerange * .05 -1)], "% of our funds" )
        print("Funds", finalFund)
    return(fivePercent[round(timerange * .05) - 1])



def plot(sell, buy, price):
    totalFunds = []
    differenceList = []
    inUSD = 1000
    inBitcoin = 0
    timeRange = 365*3

       
    print("First Day:   ", "Funds : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", int(float(df["Close"][timeRange])), "     SMA:   ", SimpleMovingAvg(200,(timeRange )))

    for i in range(timeRange - 1):
            
        dayCompare = int(float(df["Close"][timeRange - i]))
        dayPrevious = int(float(df["Close"][timeRange - i - 1]))
        difference = (dayCompare / dayPrevious) * 100 - 100
        differenceList.append(difference)
                
        if(i > round(timeRange *.1)):
            finalFund = inUSD +convertToUSD(inBitcoin, i, timeRange)
            percentLoss = returnRisk(timeRange, differenceList, finalFund)
                    
            #if the percent loss is less than the tolerated amount then sell
            if(percentLoss < sell):
                    
                print("sell")
                inUSD = inUSD + convertToUSD(inBitcoin * price, i, timeRange)
                inBitcoin = inBitcoin * (1 - price)
            elif(percentLoss > buy):
                    
                print("buy/stay")
                inBitcoin = inBitcoin + convertToBTC(inUSD * price, i, timeRange)
                inUSD = inUSD * (1 - price)
                
        totalFunds.append(inUSD + convertToUSD(inBitcoin, i, timeRange))
        print(inUSD + convertToUSD(inBitcoin, i, timeRange))
         
               
    plt.plot(np.linspace(0, len(totalFunds), len(totalFunds)), totalFunds)
    plt.show()



totalFunds = []
differenceList = []
randIntTop = []
randIntBottom = []
endValue = []
buySell = []
finalFund = 0
timeRange = 365*1
testingAmount = getTickerInfo() 


def findUsingRiskBTC(i, data):        
    
    inUSD = 1000

    inBitcoin = 0

    if((i % math.ceil(testingAmount/40)) == 0):
        sys.stdout.write("-")
        sys.stdout.flush()
            
    topTemp = random.randint(-800,400)
    top = topTemp * .01
    bottom = random.randint(topTemp, 400) * .01
  

    differenceList = []
    payPrice = .5
    for i in range(timeRange):
                #for every day until the current
        if (i < timeRange):

            dayCompare = int(float(df["Close"][timeRange - i]))
            dayPrevious = int(float(df["Close"][timeRange - i - 1]))
            difference = (dayCompare / dayPrevious) * 100 - 100
            differenceList.append(difference)
            
            if(i > round(timeRange *.1)):
                finalFund = inUSD +convertToUSD(inBitcoin, i, timeRange)
                percentLoss = returnRisk(timeRange, differenceList, finalFund)
                
                #if the percent loss is less than the tolerated amount then sell
                if(percentLoss < top):
                  
                    inUSD = inUSD + convertToUSD(inBitcoin * payPrice, i, timeRange)
                    inBitcoin = inBitcoin * (1 - payPrice)
                elif(percentLoss > bottom):
                    
                    inBitcoin = inBitcoin + convertToBTC(inUSD * payPrice, i, timeRange)
                    inUSD = inUSD * (1 - payPrice)
            totalFunds = (inUSD + convertToUSD(inBitcoin, i, timeRange))
            
        else:
            print("Done")
        
        #plt.plot(np.linspace(0, len(totalFunds), len(totalFunds)), totalFunds)
        #plt.show()

        endValue.append(totalFunds)
    randIntTop.append(top)
    randIntBottom.append(bottom)
    buySell.append(payPrice)
    totalFunds = 0
    finalValue = endValue.index(max(endValue))
    if(max(endValue) > 1000):
        print("Sell at:", top, " Buy at: ", bottom, "price :", payPrice, "Maximum Value : ", max(endValue), "End Value : ", endValue[-1] )



def findUsingRisk(x, data):        
    
    inUSD = 1000

    invested = 0

    if((x % math.ceil(testingAmount/40)) == 0):
        sys.stdout.write("-")
        sys.stdout.flush()
            
    topTemp = random.randint(-800,400)
    top = topTemp * .01
    bottom = random.randint(topTemp, 400) * .01
  

    differenceList = []
    payPrice = 1
    for i in range(timeRange):
                #for every day until the current
        if (i < timeRange):

            dayCompare = int(float(data[x][timeRange - i]))
            dayPrevious = int(float(data[x][timeRange - i - 1]))
            difference = (dayCompare / dayPrevious) * 100 - 100
            differenceList.append(difference)
            
            if(i > round(timeRange *.1)):
                finalFund = inUSD + invested
                percentLoss = returnRisk(timeRange, differenceList, finalFund)
                
                #if the percent loss is less than the tolerated amount then sell
                if(percentLoss < top):
                  
                    inUSD = inUSD + invested
                    invested = 0
                elif(percentLoss > bottom):
                    
                    invested = invested + inUSD
                    inUSD = 0
            totalFunds = (inUSD + invested)
            
        else:
            print("Done")
        
        #plt.plot(np.linspace(0, len(totalFunds), len(totalFunds)), totalFunds)
        #plt.show()

        endValue.append(totalFunds)
    randIntTop.append(top)
    randIntBottom.append(bottom)
    buySell.append(payPrice)
    totalFunds = 0
    finalValue = endValue.index(max(endValue))
    if(max(endValue) > 1000):
        print("Sell at:", top, " Buy at: ", bottom, "price :", payPrice, "Maximum Value : ", max(endValue), "End Value : ", endValue[-1] )


def findUsingSMA():
    print("Do you want to see every step? ( Y/N)")
    seeResults = input()
    differenceList = []
    finalFund = 0
    totalFunds = []
    timeRange = 365*1
    inUSD = 15000
    startingFund = 15000
    inBitcoin = 0
    valueBought = 0
    smaOfDays = 200


    if(seeResults == 'y'):
        print("First Day:   ", "Funds : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", int(float(df["Close"][timeRange])), "     SMA:   ", SimpleMovingAvg(200,(timeRange )))
    
    for i in range(timeRange):
        smaForDay = SimpleMovingAvg(smaOfDays,(timeRange - i))
        dayCompare = int(float(df["Close"][timeRange - i]))
        if (i>0):
            dayPrevious = int(float(df["Close"][timeRange - i - 1]))
            difference = (dayCompare / dayPrevious) * 100 - 100
            differenceList.append(difference)

        if (dayCompare > (smaForDay * 1.05)):

            if (inUSD > startingFund*2/3):
                inBitcoin = inBitcoin + convertToBTC(startingFund*2/3,i, timeRange)
                inUSD = inUSD - startingFund*2/3
                valueBought = dayCompare
                if(seeResults == 'y'):
                    print("Buying:    ","Funds : ",inUSD,"   In Bitcoin: ", inBitcoin,"  Bitcoin Price: ", dayCompare, "     SMA:   ", smaForDay)

            elif (inBitcoin > 0 and inBitcoin < convertToUSD(startingFund*2/3, i, timeRange)):

                inUSD = inUSD + convertToUSD(inBitcoin, i, timeRange)

                inBitcoin = 0
                if(seeResults == 'y'):
                    print("Partial Sell:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ",
                    dayCompare,
                    "    SMA:   ", smaForDay)

            if ((inUSD < startingFund*2/3) and inBitcoin > 0 and inBitcoin < convertToBTC(startingFund*2/3, i, timeRange)):
                if(seeResults == 'y'):
                    print("Staying in:   ","USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare, "    SMA:   ", smaForDay)

            else:
                if(seeResults == 'y'):
                    print("Don't do anything")

        elif (dayCompare <= smaForDay * .95):

            if (inBitcoin >= convertToBTC(startingFund*2/3, i, timeRange)):
                valueSold = dayCompare
                overallPercent = valueSold/valueBought
                inUSD = inUSD + convertToUSD(inBitcoin, i, timeRange) * overallPercent
                inBitcoin = 0
                if(seeResults == 'y'):
                    print("Selling:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare, "    SMA:   ", smaForDay)

            elif (inBitcoin > convertToBTC(startingFund*2/3, i, timeRange)):

                inUSD = inUSD + convertToUSD(inBitcoin - convertToBTC(startingFund*2/3), i, timeRange)
                inBitcoin = convertToBTC(startingFund*2/3,i, timeRange)

                if(seeResults == 'y'):
                    print("Partial Sell:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare,
                    "    SMA:   ", smaForDay)

            elif (inBitcoin == 0 and inUSD > startingFund):

                tempFund = inUSD - startingFund
                inUSD = startingFund
                inBitcoin = convertToBTC(tempFund, i, timeRange)
                if(seeResults == 'y'):
                    print("Partial Buy:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare,
                    "    SMA:   ", smaForDay)

            elif(seeResults == 'y'):
                print("Do nothing:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ",
                    dayCompare,
                    "    SMA:   ", smaForDay)

        elif(seeResults == 'y'):
            print("Price is between")
        
            
        if (inBitcoin > 0):

            totalFund = inUSD + convertToUSD(inBitcoin, i, timeRange)


        else:

            totalFund = inUSD
        totalFunds.append(totalFund)
        if (i == timeRange - 1):
            if(seeResults == 'y'):
                print("Final:    ", "USD : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare,
                "    SMA:   ", smaForDay, "   USD Afer:", inUSD + convertToUSD(inBitcoin, i, timeRange), "    Profit:  ", inUSD + convertToUSD(inBitcoin, i, timeRange) - startingFund)
                plt.plot(np.linspace(0,len(totalFunds),len(totalFunds)), totalFunds )

                plt.show()
            return(totalFund)

#plot(-4.19,-1.6500000000000001,0.09)

#indUsingSMA()
#Two years
#plot(-4.51,-3.93, .5)

def startRisk():
    starttime = time.time()
    processes = []
    for i in range(0,fullList):
        p = multiprocessing.Process(target=findUsingRisk, args=(i,fullList,))
        processes.append(p)
        p.start()
         
    for process in processes:
        process.join()
        
    print('That took {} seconds'.format(time.time() - starttime))

startRisk()