import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor



price_df = pd.read_csv("data/crop_price_dataset.csv")
price_df.columns = price_df.columns.str.strip()
prod_df = pd.read_csv("data/crop_production.csv")



price_df['month'] = pd.to_datetime(price_df['month'])

price_df['Year'] = price_df['month'].dt.year
price_df['Month'] = price_df['month'].dt.month

price_df.dropna(inplace=True)
price_df.drop_duplicates(inplace=True)



# Rename Crop column
# Remove extra spaces from column names
prod_df.columns = prod_df.columns.str.strip()

# Rename columns
prod_df.rename(columns={
    'Crop': 'commodity_name',
    'Crop_Year': 'Year'
}, inplace=True)

print(prod_df.columns)

prod_df.dropna(inplace=True)
prod_df.drop_duplicates(inplace=True)


df = pd.merge(
    price_df,
    prod_df,
    on=['commodity_name', 'Year'],
    how='inner'
)



def get_season(month):
    if month in [6, 7, 8, 9]:
        return 1   # Kharif
    elif month in [10, 11, 12, 1]:
        return 2   # Rabi
    else:
        return 3   # Summer

df['Season'] = df['Month'].apply(get_season)



df['Rainfall'] = np.random.randint(10, 100, size=len(df))
df['Temperature'] = np.random.randint(20, 40, size=len(df))



X = df[[
    'Year',
    'Month',
    'avg_min_price',
    'avg_max_price',
    'Production',
    'Area',
    'Season',
    'Rainfall',
    'Temperature'
]]


y = df['avg_modal_price']



X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)



model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)


pickle.dump(model, open("models/model_v2.pkl", "wb"))

print("✅ Model Trained Successfully")
print("✅ Model Saved Successfully")