import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import time
import datetime
from dateutil.parser import parse
from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation
import time
from sklearn.model_selection import train_test_split
import tensorflow as tf

#Prices
names = ['Date','Symbol', 'Open', 'Close', 'Volume BTC', 'Volume USD']
url = 'http://www.cryptodatadownload.com/cdd/Coinbase_BTCUSD_d.csv'
df = pd.read_csv(url, skiprows=[0,1], header = None, delim_whitespace = True, na_values='?')

new = df[0].str.split(",", n=7, expand=True)
length =len(df)
print(length)

df["Date"] = new[0]
df["Symbol"] = new[1]
df["Open"] = new[2]
df["High"] = new[3]
df["Low"] = new[4]
df["Close"] = new[5]
df["Volume BTC"] = new[6]
df["Volume USD"] = new[7]

def format_to_lstm(df):
	X = np.array(df)
	return np.reshape(X, (X.shape[0], 1, X.shape[1]))

x = np.linspace(0,len(df["Open"]),len(df["Open"]))
y = df["Open"]
X = format_to_lstm(x)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
print(X_train.shape)


batch_size = 2            # Batch size (you may try different values)
epochs = 15               # Epoch (you may try different values)
loss='mean_squared_error' # Since the metric is MSE/RMSE
optimizer = 'rmsprop'     # Recommended optimizer for RNN
activation = 'linear'     # Linear activation
input_shape=(1, 2)     # Input dimension
output_dim = 30

model = Sequential()
model.add(LSTM(units = output_dim,return_sequences=True, input_shape=input_shape))
model.add(Dense(units=32,activation=activation))
model.add(LSTM(units = output_dim, return_sequences=False))
model.add(Dense(units=1,activation=activation))
model.compile(optimizer=optimizer,loss=loss)

start_time = time.time()
model.fit(x=X_train,
          y=y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_split=0.05,
          )
end_time = time.time()
processing_time = end_time - start_time