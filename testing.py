import yfinance as yf
from rtstock.stock import Stock


#print(yf.Ticker("AAPL").history(period="max")["Close"])
print(yf.Ticker("AAPL").recommendations)
