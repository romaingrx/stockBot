#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Wednesday, 19 March 2020
"""

from settings import *
import seaborn as sns, numpy as np
import matplotlib.pyplot as plt
import numpy as np

def auto_correlation(df):
    """
        Plot the correlation between all columns.

            Parameters:
                df (pandas.DataFrame) : dataframe with all columns.
    """
    corrmat = df.corr() # Correlation matrix
    plt.figure()
    g = sns.heatmap(corrmat, annot=True, cmap='RdYlGn')
    plt.show()

def prediction_correlation(true_array, prediction_array):
    """
        Plot the correlation between true data and predicted data.

            Parameters:
                true_array       (array)
                prediction_array (array)
    """
    plt.Figure()
    plt.xlabel("True values")
    plt.ylabel("Prediction values")
    plt.scatter(true_array, prediction_array, color='purple', label='Data')
    min_value = min(min(true_array), min(prediction_array))
    max_value = max(max(true_array), max(prediction_array))
    arange = np.linspace(min_value, max_value, 200)
    plt.plot(arange, arange, ls='--', color='blue', label='Desired correlation')
    plt.legend()
    plt.show()

def prediction_cross_correlation(true_array, prediction_array):
    plt.Figure()
    plt.title('Cross correlation')
    plt.xcorr(real[-prediction_size:], prediction, usevlines=True, normed=True)
    plt.show()


if __name__=='__main__':
    from preprocess import df_preprocess_alpha_vantage
    SPCE = TS.get_intraday(symbol='SPCE', outputsize='full', interval='30min')[0]
    print(SPCE.head)
    df = df_preprocess_alpha_vantage(SPCE)
    PLOT = df.drop('Volume', axis=1)
    print(PLOT.head)
    auto_correlation(df)
    PLOT.plot()
    plt.show()
