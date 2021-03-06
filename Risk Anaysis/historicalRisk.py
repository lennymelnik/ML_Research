import pandas as pd
import requests



BTCUSDTPrice = requests.get("https://api.binance.com/api/v1/ticker/price?symbol=BTCUSDT")
BTCUSDTPrice = BTCUSDTPrice.json()['price']

#Get and Pre-Proccess Dataset
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

#Get simple moving average for past 200 days
def SimpleMovingAvg(number, starting, sma = 0):
    for i in range(number):
        sma = sma + int(float(df["Close"][starting + 1 + i]))
    return sma/number

#def standardDeviation
daySMA = 200
timeRange = 365
differenceList = []
finalFund = 0
print(df["Close"][0])
def backtest():
    startingFund = 10000
    Funds = startingFund
    toBuy = startingFund
    minimum = Funds/2
    inBitcoin = 0
    valueBought = 0
    valueSold = 0
    #What to do per day
    for i in range(timeRange):


        smaForDay = SimpleMovingAvg(daySMA,(timeRange - i))
        dayCompare = int(float(df["Close"][timeRange - i]))
        if (i>0):
            dayPrevious = int(float(df["Close"][timeRange - i - 1]))
            difference = (dayCompare / dayPrevious) * 100 - 100
            differenceList.append(difference)

        #BUYING
        if (dayCompare > (smaForDay * 1.05)):
            if (Funds >= toBuy and inBitcoin < toBuy):
                Funds = Funds - toBuy
                inBitcoin = inBitcoin + toBuy
                valueBought = dayCompare
            elif (inBitcoin > 0 and inBitcoin < toBuy):
                valuePartialSold = dayCompare
                Funds = Funds + inBitcoin * valuePartialSold/valuePartialBought
                inBitcoin = 0
        #SELLING
        elif (dayCompare < (smaForDay * .80)):
            # BUYING IF BELOW ORIGINAL AND NO BITCOIN IS OWNED
            if (inBitcoin < 1 and Funds > startingFund):
                valuePartialBought = dayCompare
                tempFund = Funds - startingFund
                Funds = startingFund
                inBitcoin = tempFund

        elif (dayCompare < (smaForDay * .95)):
            if (inBitcoin == toBuy):
                valueSold = dayCompare
                overallSell = toBuy
                overallPercent = valueSold/valueBought
                Funds = Funds + overallSell * overallPercent
                inBitcoin = 0
            #SELL EVERYTHING
            elif (inBitcoin > toBuy):
                partialSell = inBitcoin - toBuy
                overallPercent = dayCompare / valueBought
                partialPercent = dayCompare / valuePartialBought
                Funds = Funds + toBuy * overallPercent + partialSell * partialPercent
                inBitcoin  = 0
        if (i == timeRange - 1):

            return(Funds + inBitcoin * (dayCompare/valueBought))
finalFund = backtest()

#Plot Close Data

timeHa = str(timeRange)
fivePercent = sorted(differenceList)
fivePercent = fivePercent[:round(timeRange *.05)]
timeHa2 =  str(round(timeRange * .05))
print("We have 95% confidence that our loss will not exceed ", fivePercent[round(timeRange * .05 -1)]* .01 * finalFund, "which is ", fivePercent[round(timeRange * .05 -1)], "% of our funds" )
print("Funds", finalFund)