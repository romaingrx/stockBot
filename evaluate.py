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
import pandas as pd

def auto_correlation(df):
    """
        Plot the correlation between all columns.

            Parameters:
                df (pandas.DataFrame) : dataframe with all columns.
    """
    plt.title("Correlation between all features.")
    corrmat = df.corr() # Correlation matrix
    g = sns.heatmap(corrmat, annot=True, cmap='RdYlGn')

def prediction_correlation(real_data, test_data):
    """
        Plot the correlation between true data and predicted data.

            Parameters:
                real_data (pandas.Series) : True data
                test_data (pandas.Series) : Predicted data
    """
    assert isinstance(real_data, pd.Series) and isinstance(test_data, pd.Series)

    intersect = test_data.index.intersection(real_data.index)
    df_intersect = real_data.loc[intersect]

    plt.title("The correlation between predicted data and true data.")
    plt.xlabel("True values")
    plt.ylabel("Prediction values")
    plt.scatter(df_intersect.values, test_data.values, color='purple', label='Data')
    min_value = min(min(df_intersect.values), min(test_data.values))
    max_value = max(max(df_intersect.values), max(test_data.values))
    arange = np.linspace(min_value, max_value, 200)
    plt.plot(arange, arange, ls='--', color='blue', label='Desired correlation')

def prediction_cross_correlation(real_data, test_data):
    assert isinstance(real_data, pd.Series) and isinstance(test_data, pd.Series)

    plt.title('Cross correlation')
    intersect = test_data.index.intersection(real_data.index)
    df_intersect = real_data.loc[intersect]
    plt.xcorr(df_intersect.values, test_data.values, usevlines=True, normed=True)


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
