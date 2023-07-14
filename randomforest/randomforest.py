#this file performs random forest on the processed dataframe containing all features
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import r2_score

#load df, assign X and y, then split with sklearn:
df = pd.read_csv('df_processed.csv', encoding='ISO-8859-1')
y = df["rating"]
X = df.drop(["rating"], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.10, random_state=24)

#fit rf and predict rating:
rf = RandomForestRegressor(n_estimators=200, random_state=12)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

err = mse(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(r2)

#shows feature importance for each feature. The sum of all sums to 1.
print(rf.feature_importances_)
