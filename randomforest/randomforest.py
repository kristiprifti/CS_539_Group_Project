#this file performs random forest on the processed dataframe containing all features and outputs a summary df for the website
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import r2_score

#load df, assign X and y, then split with sklearn:
df = pd.read_csv('df_processed.csv', encoding='ISO-8859-1')
y = df["rating"]
coords = df["coord"]
X = df.drop(["rating", "coord"], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.10, random_state=24)

#fit rf and predict rating:
rf = RandomForestRegressor(n_estimators=100, random_state=12)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

r2 = r2_score(y_test, y_pred)
print(f"The R^2 value of the Random Forest model is: {r2}")

#get feature importance
important_features = rf.feature_importances_ #importance metrics of all features
top5feature_idx = np.argsort(important_features)[-5:] #index of top 5 features
top5feature_names = X.columns[top5feature_idx] #names of top 5 features
top5feature_names = [name for name in top5feature_names]
top5feature_importances = important_features[top5feature_idx]
print(f"The 5 most important features include: {top5feature_names}")
print(f"The importance values of the top 5 features: {[val for val in top5feature_importances]}")

## create result DF for website
resultDF = df.groupby('coord').mean().reset_index() #groups by coordinate and averages feature values for each unique coordinate
#create list of column names to keep for the final result DF:
keep_columns = top5feature_names
keep_columns.append("coord")
keep_columns.append("rating")
resultDF = resultDF[keep_columns]

resultDF.to_csv("websiteDF.csv",index=False)