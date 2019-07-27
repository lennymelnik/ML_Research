import requests
from coinbase.wallet.client import Client
import tulipy as ti

client = Client(LImC68pA956IgcIV,nWCgEOc9X3WA6bYjTdIOEJE1v6jSwsuU)


apiData = requests # Get data from api

price = apiData.json()[][]

df = #Price data from api


superTrend = ti.s
#Boling
bband = ti.bbands(df, period=5, stddev=2)

rsi  = ti.rsi(df, period = 5)

simpleMovingAvg = ti.sma(df, period = 5)
#Turn 2D into 3D array
def format_to_lstm(df):
	X = np.array(df)
	return np.reshape(X, (X.shape[0], 1, X.shape[1]))

X = np.array([bband,rsi,simpleMovingAvg])
X = format_to_lstm(X)

y = df["Prices"]



#ANN

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

API Key: LImC68pA956IgcIV

API Secret: nWCgEOc9X3WA6bYjTdIOEJE1v6jSwsuU