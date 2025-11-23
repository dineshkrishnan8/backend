import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from joblib import dump, load
from datetime import timedelta

MODEL_PATH = "models/"
import os
os.makedirs(MODEL_PATH, exist_ok=True)

def create_features(df):
    df = df.sort_values("sale_date").copy()
    df['dow'] = df['sale_date'].dt.dayofweek
    df['month'] = df['sale_date'].dt.month
    # lag feature
    df['lag_1'] = df['quantity'].shift(1).fillna(method='bfill')
    df['rolling_7'] = df['quantity'].rolling(7, min_periods=1).mean()
    return df

def train_model(df, model_name="rf_model.pkl"):
    if df.empty:
        return None
    df = create_features(df)
    X = df[['dow','month','lag_1','rolling_7','price','promo_flag']].astype(float)
    y = df['quantity']
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,shuffle=False)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    dump(model, MODEL_PATH + model_name)
    return model

def forecast_next_days(df, days=7, model=None):
    if df.empty:
        return []
    df = create_features(df)
    if model is None:
        try:
            model = load(MODEL_PATH + "rf_model.pkl")
        except:
            model = train_model(df)
    last_date = df['sale_date'].max()
    preds = []
    last_row = df.iloc[-1].copy()
    for i in range(1, days+1):
        d = last_date + timedelta(days=i)
        dow = d.dayofweek
        month = d.month
        lag_1 = float(last_row['quantity'])
        rolling_7 = float(df['quantity'].tail(7).mean())
        price = float(last_row['price'])
        promo_flag = float(0)  # default; you can add logic to forecast promo days
        X = np.array([[dow, month, lag_1, rolling_7, price, promo_flag]])
        pred_q = float(model.predict(X)[0])
        preds.append({"date": d.date(), "predicted_quantity": max(0, round(pred_q,3))})
        # update last_row quantity for next step (feeding predicted value)
        last_row['quantity'] = pred_q
    return preds

