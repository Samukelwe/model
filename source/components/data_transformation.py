from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import pandas as pd 
import numpy as np
from source.logger import logging

def Scaler(X):
    try:
        logging.info('Scaling using Minimax scaler')
        scaler = MinMaxScaler()
        X_scaled=scaler.fit_transform(X)
        return X_scaled
    except Exception as e:
            raise exception.CustomException(e,sys)

def train_test(X,y):
    try:
        logging.info("train_test split has begun")
        X_train, X_test, y_train, y_test=train_test_split(X,y, test_size=0.3, random_state=42)
        return  X_train, X_test, y_train, y_test
    except Exception as e:
        raise exception.CustomException(e,sys)
