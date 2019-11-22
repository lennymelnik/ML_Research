import __init__
import numpy as np

play = __init__.df["Close"].values.tolist()



def findDrawdown(inputArray):
    #If the given array is of strings, convert to floats
    if(type(inputArray[0]) is not type(float)):
        for i in range(len(inputArray)):
            inputArray[i] = float(inputArray[i])

    newArray = inputArray
    maxValue = max(newArray)
    maxValuePosition = newArray.index(maxValue)
    temp = len(inputArray) - inputArray.index(max(inputArray))
    minValue = min(inputArray[:-temp])
    drawdownFound = (maxValue - minValue)/maxValue
    return minValue, maxValue, drawdownFound


print(findDrawdown(play))