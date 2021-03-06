import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import data

print("Do you want to see every step? (Y/N)")
seeResults = input()

print("Do you want to trade using SMA(1) or Historical Risk(2)")
whatMethod = input()

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
finalFund = 0
timeRange = 365*4

def backtest(percentBuy,percentSell):
    if(whatMethod == '1'):
        inUSD = 15000
        startingFund = 15000
        inBitcoin = 0
        valueBought = 0
        if(seeResults == 'y'):
            print("First Day:   ", "Funds : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", int(float(df["Close"][timeRange])), "     SMA:   ", SimpleMovingAvg(200,(timeRange )))
        
        for i in range(timeRange):

            smaForDay = SimpleMovingAvg(200,(timeRange - i))
            dayCompare = int(float(data.df["Close"][timeRange - i]))
            if (i>0):
                dayPrevious = int(float(data.df["Close"][timeRange - i - 1]))
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
        inUSD = 1000
        startingFund = 1000
        inBitcoin = 0
        valueBought = 0
        
        if(seeResults == 'y'):
            print("First Day:   ", "Funds : ", inUSD, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", int(float(df["Close"][timeRange])), "     SMA:   ", SimpleMovingAvg(200,(timeRange )))
        
        for i in range(timeRange):
    
            
            if (i < timeRange):
                dayCompare = int(float(data.df["Close"][timeRange - i]))
                dayPrevious = int(float(data.df["Close"][timeRange - i - 1]))
                difference = (dayCompare / dayPrevious) * 100 - 100
                differenceList.append(difference)
                if(i > round(timeRange *.1)):
                    finalFund = inUSD +convertToUSD(inBitcoin, i)
                    percentLoss = returnRisk(timeRange, differenceList, finalFund)

                    if(percentLoss < percentSell):
                        if(seeResults == 'y'):
                            print("sell")
                        inUSD = inUSD + convertToUSD(inBitcoin * .25, i)
                        inBitcoin = inBitcoin * .75
                    elif(percentLoss > percentBuy):
                        if(seeResults == 'y'):
                            print("buy/stay")
                        inBitcoin = inBitcoin + convertToBTC(inUSD *.25, i)
                        inUSD = inUSD * .75

            

                
            else:
                print("Done")
        return finalFund
       
finalFund = backtest(-3, -5)
print(finalFund)
hello = True
i = 0
print(backtest(-1.05,-4.72))


plt.plot(np.linspace(0,len(totalFunds),len(totalFunds)), totalFunds )

plt.show()
