#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Wednesday, 19 March 2020
"""

from keras.models import Sequential
from keras.layers import LSTM, Dense

def get_LSTM_model(look_back):
    """
        Construct a simple LSTM model
    """
    model = Sequential()
    model.add(LSTM(10, activation='relu', input_shape=(look_back,1), return_sequences=False))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

if __name__=='__main__':
    import visualizer, evaluate, preprocess
    import yfinance as yf, numpy as np, matplotlib.pyplot as plt
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import MinMaxScaler
    from keras.preprocessing.sequence import TimeseriesGenerator

    TICKER = yf.Ticker('AIR.PA') # Get info about the stock
    df = TICKER.history('max') # Get the pandas dataframe
    df = preprocess.df_preprocess_yfinance(df) # Preprocess data from preprocess file

    look_back, epochs = 15, 25 # look_back is the price history length LSTM is looking at to train and predict, epochs is the number of tries for training
    scaler = MinMaxScaler(feature_range=(0, 1)) # Get the scaler to map the data from 0 to 1
    df['ScaledClose'] = scaler.fit_transform(df['Close'].values.reshape((-1,1))) # Scale the data from 0 to 1
    model = get_LSTM_model(look_back) # Get the LSTM model
    df_train, df_test = train_test_split(df, test_size=0.2, shuffle=False) # Split data between train and test batch
    train_values = df_train['ScaledClose'].values.reshape((-1,1))
    test_values = df_test['ScaledClose'].values.reshape((-1,1))
    train_rolling = TimeseriesGenerator(train_values, train_values, length=look_back, batch_size=20) # Roll the data to look_back shape
    test_rolling = TimeseriesGenerator(test_values, test_values, length=look_back, batch_size=1)
    model.fit_generator(train_rolling, epochs=epochs, verbose=1) # Fit train data
    predictions = model.predict_generator(test_rolling) # Predict test data
    predictions = scaler.inverse_transform(predictions.reshape((-1,1))).reshape((-1)) # Convert data from 0 to 1 to true value
    df_test['Close'].values[len(df_test.index)-len(predictions):] = predictions # The first {look_back} days do not have values

    evaluate.prediction_correlation(df['Close'].values[-len(predictions):], predictions) # Plot correlation
    visualizer.plot_test_prediction(df['Close'], df_test['Close'], mse=True) # Plot forecast
