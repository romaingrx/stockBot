#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Friday, 20 March 2020
"""


import sys
for path in ['.', '..']:
    sys.path.append(path)
import pandas as pd
import tensorflow as tf
import sklearn
from stockBot.agents.models.model import Neural_Network
from sklearn.model_selection import train_test_split

class LSTM_Network(Neural_Network):

    def __init__(self, input_shape):
        super().__init__(input_shape)

    def _build_model(self):
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.LSTM(64, input_shape=self.input_shape, return_sequences=True),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.LSTM(32, dropout=0.1),
            tf.keras.layers.Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mse')

    def get_train_test_data(self, df, look_back, test_size, predict_col=['Close'], features_col=None):
        self.scaler = sklearn.preprocessing.MinMaxScaler(feature_range=(0,1))
        self.output_scaler = sklearn.preprocessing.MinMaxScaler(feature_range=(0,1))
        n_features = 0
        input_cols = predict_col.copy()
        if features_col:
            n_features = len(features_col)
            input_cols += features_col
        scaled_cols = list(map(lambda x: 'Scaled'+x, input_cols))
        df[scaled_cols] = pd.DataFrame(self.scaler.fit_transform(df[input_cols].values.reshape((-1,1+n_features))), index=df.index)
        self.output_scaler.min_, self.output_scaler.scale_ = self.scaler.min_[0], self.scaler.scale_[0]
        df_train, df_test = sklearn.model_selection.train_test_split(df, test_size=test_size, shuffle=False) # Split data between train and test batch
        X_train = df_train[scaled_cols].values.reshape((-1,1+n_features))
        Y_train = df_train['Scaled'+predict_col[0]].values.reshape((-1,1))
        X_test  = df_test[scaled_cols].values.reshape((-1,1+n_features))
        Y_test  = df_test['Scaled'+predict_col[0]].values.reshape((-1,1))
        train_timeseries = tf.keras.preprocessing.sequence.TimeseriesGenerator(X_train, Y_train, length=look_back, batch_size=32) # Roll the data to look_back shape
        test_timeseries  = tf.keras.preprocessing.sequence.TimeseriesGenerator(X_test, Y_test, length=look_back, batch_size=1)
        return train_timeseries, test_timeseries, df_train, df_test

    def predict(self, *args, **kwargs):
        return self.transform_inverse_prediction(super().predict(*args, **kwargs))

    def transform_inverse_prediction(self, predictions):
        return self.output_scaler.inverse_transform(predictions.reshape((-1,1))).reshape((-1)) # Convert data from 0 to 1 to true value


if __name__=='__main__':
    from stockBot.utils.visualizer import visualizer
    from stockBot.utils.evaluate import evaluate
    from stockBot.data.preprocess import preprocess
    import yfinance as yf, numpy as np, matplotlib.pyplot as plt

    TICKER = yf.Ticker('AIR.PA') # Get info about the stock
    df = TICKER.history('max') # Get the pandas dataframe
    df = preprocess.df_preprocess_yfinance(df) # Preprocess data from preprocess file

    look_back, epochs = 15, 25 # look_back is the price history length LSTM is looking at to train and predict, epochs is the number of tries for training
    features_col = ['MA15']
    input_shape = (look_back, 1+len(features_col))
    LSTM = LSTM_Network(input_shape)
    train_timeseries, test_timeseries, df_train, df_test = LSTM.get_train_test_data(df, look_back, 0.2, features_col=features_col)
    model = LSTM.model # Get the LSTM model
    LSTM.fit(train_timeseries, epochs=epochs) # Fit train data
    predictions = LSTM.predict(test_timeseries) # Predict test data
    df_test['PredictedClose'] = df_test['Close'].values
    df_test['PredictedClose'].values[-len(predictions):] = predictions # The first {look_back} days do not have values

    plt.figure()
    plt.subplot(221)
    evaluate.prediction_correlation(df['Close'], df_test['PredictedClose']) # Plot correlation
    plt.subplot(222)
    evaluate.prediction_cross_correlation(df['Close'], df_test['PredictedClose'])
    plt.subplot(212)
    visualizer.plot_test_prediction(df['Close'], df_test['PredictedClose'], mse=True) # Plot forecast
    plt.legend()
    plt.show()
