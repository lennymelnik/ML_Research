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
        dayStart = int(float(df["Close"][timeRange - i + 1]))

        #BUYING
        if (dayCompare > (smaForDay * 1.05)):
            if (Funds >= toBuy and inBitcoin < toBuy):
                Funds = Funds - toBuy
                inBitcoin = inBitcoin + toBuy
                valueBought = dayCompare
                print("Buying:    ","Funds : ",Funds,"   In Bitcoin: ", inBitcoin,"  Bitcoin Price: ", m, "     SMA:   ", smaForDay, "     Standard Deviation: ")
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
            print("Final:    ", "Funds : ", Funds, "   In Bitcoin: ", inBitcoin, "  Bitcoin Price: ", dayCompare,
                  "    SMA:   ", smaForDay, "   USD Afer:", Funds + inBitcoin * (dayCompare/valueBought), "    Profit:  ", Funds + inBitcoin * (dayCompare/valueBought) - startingFund)
