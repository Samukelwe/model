import pandas as pd
from source.components.data_preprocessin import preprocess
from source.components.data_transformation import Scaler
from source.components.data_transformation import train_test
from sklearn.svm import SVR
from source.logger import logging
import pickle
Turbofan=pd.read_csv('notebook\data\Turbofan (2).csv')
logging.info("Entered the data ingestion method or component")
df=preprocess(Turbofan)
y = df['RUL'].clip(upper=125)
X = df.drop(['RUL'], axis=1)
X_scaled=Scaler(X)
X_train, X_test, y_train, y_test=train_test(X_scaled,y)

svr = SVR(kernel='rbf',C=10)
svr.fit(X_train, y_train) # fitting
logging.info("Model fitting initiated")
# Make pickle file of our model
pickle.dump(svr, open("model.pkl", "wb"))
logging.info("model pickle file saved")