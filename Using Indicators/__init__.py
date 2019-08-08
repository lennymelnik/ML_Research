import requests
from coinbase.wallet.client import Client
import matplotlib
import matplotlib.pyplot as plt
import tulipy as ti
#from binance.client import Client
import numpy as np
import pandas as pd
#from keras.models import Sequential
#from keras.layers import LSTM, Dense, Activation, Dropout
import time
from sklearn.model_selection import train_test_split
#COINBASE API
client = Client('LImC68pA956IgcIV','nWCgEOc9X3WA6bYjTdIOEJE1v6jSwsuU')
#client = Client('1XGCXOq8RCHuKA0O322OHahi0Kg0KsSHsG4ai4Gbp7MmaLFwVEOxGoZ2G1KSjEAS','207ia9nrYf8OF3LDXjMPUShYxEDAQWUwJBxv1wzHUDmswHWlU1udgCHc7xxwyTiK')

currency_code = 'USD'

price = client.get_spot_price(currency=currency_code)
priceHist = client.get_historic_prices()
print(priceHist)

print('Current bitcoin price in %s: %s' % (currency_code, price.amount))
print(client.get_accounts())

print(client.get_transactions('fd3b21d8-21b7-5f18-881c-4359d8850a1e'))
'''
apiData = pd.read_csv('btc.csv', skiprows= (0,1))

apiData = apiData.iloc[:,3]

#price = apiData.json()[][]

#df = #Price data from api

#superTrend = ti.s
#Boling
apiData = np.array(apiData)
bband = np.array(ti.bbands(apiData, period=5, stddev=2))
#print(bband)
print(bband.shape[1])
bband = bband.reshape(bband.shape[1],len(bband))
print(bband)
print("bband has been created")
rsi  = np.array(ti.rsi(apiData, period = 5))
length = len(rsi)
rsi = rsi.reshape(len(rsi),1)
print("RSI has been calculated")
simpleMovingAvg = np.array(ti.sma(apiData, period = 6))
simpleMovingAvg = simpleMovingAvg.reshape(len(simpleMovingAvg), 1)
print("RSI: ",rsi)
plt.plot(np.linspace(0,length, length), rsi*100)
plt.ylabel("RSI")
plt.xlabel("Every single data point")
plt.show()
plt.plot(np.linspace(0,length,length), simpleMovingAvg)
plt.ylabel("Simple Moving AVG")
plt.xlabel("Every single data point")
plt.show()
plt.ylabel("Historical Price")
plt.xlabel("Every single data point")
plt.plot(np.linspace(0,length, length), apiData[:length])
plt.show()
print("RSI:",len(rsi))
print("SMA: ", len(simpleMovingAvg))
print("Simple Moving Avg has been calculated")

#Turn 2D into 3D array

def format_to_lstm(df):

	return np.reshape(X, (X.shape[0], 1, X.shape[1]))

X = np.concatenate([rsi,simpleMovingAvg], axis= 1)
print(X.shape)
#X = np.concatenate([X, bband]),, np.zeros(length).reshape(length,1)
print(X)
X = format_to_lstm(X)

y = apiData[:length]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)


#ANN

batch_size = 2            # Batch size (you may try different values)
epochs = 15               # Epoch (you may try different values)
loss='mse' # Since the metric is MSE/RMSE
optimizer = 'sgd'     # Recommended optimizer for RNN
activation = 'linear'     # Linear activation
input_shape=(1, 2)     # Input dimension
output_dim = 30



model = Sequential()
model.add(LSTM(units = output_dim,return_sequences=True, input_shape=input_shape))
model.add(Dense(units=512,activation=activation))
model.add(LSTM(units = output_dim, return_sequences=False))
model.add(Dense(units=1,activation=activation))
model.compile(optimizer=optimizer,loss=loss)
model.summary()

start_time = time.time()
model.fit(x=X_train,
          y=y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_split=.02
          )
end_time = time.time()
processing_time = end_time - start_time

#API Key: LImC68pA956IgcIV

#API Secret: nWCgEOc9X3WA6bYjTdIOEJE1v6jSwsuU
'''
