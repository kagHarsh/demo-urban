# -*- coding: utf-8 -*-
"""Urban_with _pandas.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fwbyYui4i6hfe5zQzJrvwenrd3AH9G_L
"""

import locale
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.offline as pyo
import plotly.io as pio
import gdown

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, r2_score


import warnings
warnings.filterwarnings('ignore')

#Read data from a csv file
# Google Drive file ID
file_id = "1LMnNSW3w2L1A9IooTK8ZRo3UkbRsosgt"
output = "Urban_Air_Quality_Dataset.csv"

# Download CSV file from Google Drive
gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)

# Load the CSV into DataFrame
csv_file_path = "Urban_Air_Quality_Dataset.csv"
df = pd.read.csv(csv_file_path, header=True)

df.head()

def summary(df):
    print(f'data shape: {df.shape}')
    summ = pd.DataFrame(df.dtypes, columns=['Data Type'])
    summ['Missing#'] = df.isna().sum()
    summ['Missing%'] = (df.isna().sum())/len(df)
    summ['Dups'] = df.duplicated().sum()
    summ['Uniques'] = df.nunique().values
    summ['Count'] = df.count().values
    desc = pd.DataFrame(df.describe(include='all').transpose())
    summ['Min'] = desc['min'].values
    summ['Max'] = desc['max'].values
    summ['Average'] = desc['mean'].values
    summ['Standard Deviation'] = desc['std'].values
    summ['First Value'] = df.loc[0].values
    summ['Second Value'] = df.loc[1].values
    summ['Third Value'] = df.loc[2].values

    display(summ)

summary(df)

#We will exclude columns that have only 1 data type and/or a very large percentage of null data.

df.drop(["preciptype", "snow", "snowdepth", "Condition_Code", "Month", "Season", "stations"], axis=1, inplace=True)

# Check if there is still null data
df.isna().sum().sum()

# Histogram - 'Health_Risk_Score'
ax = sns.distplot(df['Health_Risk_Score'])
ax.figure.set_size_inches(12, 6)
ax.set_title('Frequency Distribution - Health_Risk_Score', fontsize=20, color = "blue")
ax.set_ylabel('Health_Risk_Score', fontsize=11)
plt.show()

# Distribution of Average Temperature
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 7))
sns.histplot(df['temp'], bins=30, kde=True, color='royalblue', edgecolor='black', alpha=0.7) # Changed df to data
plt.title('Distribution of Average Temperature', fontsize=16)
plt.xlabel('Temperature (°F)', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.grid(True)
plt.show()

# # Convert datetime column to datetime type
# df['datetime'] = pd.to_datetime(df['datetime']) # Changed df to data

# # Temperature Trends Over Time
# plt.figure(figsize=(14, 8))
# df_grouped = df.groupby(df['datetime'].dt.date).agg({'temp': 'mean'}).reset_index() # Changed df to data
# sns.lineplot(x='datetime', y='temp', data=df_grouped, color='firebrick', linewidth=2.5, marker='o')
# plt.title('Temperature Trends Over Time', fontsize=16)
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('Average Temperature (°F)', fontsize=14)
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.show()

# Correlation Heatmap
plt.figure(figsize=(14, 12))
corr = df[['temp', 'humidity', 'severerisk', 'pressure', 'uvindex', 'visibility', 'Health_Risk_Score']].corr() # Assuming your DataFrame is named 'data' based on previous code
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5, vmin=-1, vmax=1, cbar_kws={"shrink": .8})
plt.title('Correlation Heatmap', fontsize=16)
plt.show()

# Scatter plot for Health Risk Score vs Temperature
plt.figure(figsize=(8, 6))
plt.scatter(df['Health_Risk_Score'], df['temp'], alpha=0.5, color='brown')
plt.title('Health Risk Score vs Temperature')
plt.xlabel('Health Risk Score')
plt.ylabel('Temperature (°F)')
plt.show()

# Average of Health_Risk_Score X Top 10 City
df_cat = df.groupby('City')["Health_Risk_Score"].mean().reset_index()
df_cat = df_cat.sort_values(by='Health_Risk_Score', ascending=False).head(10)

# create bar plot
fig, ax = plt.subplots(figsize=(8, 5))
ax = sns.barplot(x = 'City', y = "Health_Risk_Score", data = df_cat, palette = 'cool')
plt.title("Average of Health_Risk_Score X Top 10 City", fontsize = 16)
plt.xticks(rotation=45, fontsize = 10)


# Adding labels to each bar
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.1f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center',
                xytext = (0, 5), textcoords = 'offset points', rotation=0, fontsize=10)

plt.show()

# Average of Health_Risk_Score X Top 10 City
df_cat = df.groupby('City')[["tempmin", "temp", "tempmax"]].mean().reset_index()
#df_cat = df_cat.sort_values(by='temp', ascending=False).head(10)

# create bar plot
fig, ax = plt.subplots(figsize=(8, 5))
ax = sns.barplot(x = 'City', y = "temp", data = df_cat, palette = 'cool', label = "temp")
ax = sns.lineplot(x = 'City', y = "tempmax", data = df_cat, label = "tempmax")
ax = sns.lineplot(x = 'City', y = "tempmin", data = df_cat, label = "tempmin")

plt.title("Average of temp vs Top 10 City", fontsize = 16)
plt.xticks(rotation=45, fontsize = 10)


# Adding labels to each bar
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.1f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center',
                xytext = (0, 5), textcoords = 'offset points', rotation=0, fontsize=10)

plt.show()

# Convert non-numeric columns to numeric ones.

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

le= LabelEncoder()

for col in df:
    if df[col].dtype == 'O':
        df[col] = le.fit_transform(df[col])

# Correlation with Health_Risk_Score

limite = -1

data = df.corr()["Health_Risk_Score"].sort_values(ascending=False)
indices = data.index
labels = []
corr = []
for i in range(1, len(indices)):
    if data[indices[i]]>limite:
        labels.append(indices[i])
        corr.append(data[i])
sns.barplot(x=corr, y=labels, palette = 'cool')
plt.title('Correlation between Features and Health_Risk_Score')
plt.show()

df.head()

print(df.iloc[0])

# Assuming your DataFrame is `df` and you want to exclude the target column
feature_columns = df.columns[:-1]  # This will give you all feature columns except the last column (target)
print(feature_columns)

print(df.dtypes)

# Prepare data for modeling
X = df.drop(['Health_Risk_Score'], axis=1)
y = df['Health_Risk_Score']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

import pickle
pickle.dump(scaler,open('scaling.pkl','wb'))

#Random Forest

# Define model
rf = RandomForestRegressor()

# Define parameter grid
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Perform grid search
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# Make predictions
best_rf = grid_search.best_estimator_
y_pred_rf = best_rf.predict(X_test)

# Evaluate the model
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"Best Parameters for random forest: {grid_search.best_params_}")
print(f"Mean Squared Error for random forest: {mse_rf}")
print(f"R-squared for random forest: {r2_rf}")

#Linear Regression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# Scaling the data
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# Define model
lr = LinearRegression()

# Define parameter grid (without 'normalize' parameter)
param_grid = {
    'fit_intercept': [True, False],  # We can still tune whether to fit the intercept
    'positive': [True, False]        # This ensures coefficients are non-negative if set to True
}

# Perform grid search
grid_search_lr = GridSearchCV(estimator=lr, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
grid_search_lr.fit(X_train, y_train)

# Make predictions
best_lr = grid_search_lr.best_estimator_
y_pred_lr = best_lr.predict(X_test)

# Evaluate the model
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

print(f"Best Parameters for Linear Regression: {grid_search_lr.best_params_}")
print(f"Mean Squared Error for Linear Regression: {mse_lr}")
print(f"R-squared for Linear Regression: {r2_lr}")

#SVM
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

# Initialize the SVM model
svm = SVR()

# Define the parameter grid for hyperparameter tuning
param_grid = {
    'C': [0.1, 1, 10, 100],
    'kernel': ['linear', 'rbf', 'poly'],  # Testing different kernel functions
    'degree': [2, 3, 4],  # Only used if kernel is 'poly'
    'gamma': ['scale', 'auto'],  # Kernel coefficient for 'rbf', 'poly'
}

# Perform grid search with cross-validation
grid_search = GridSearchCV(estimator=svm, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# Get the best estimator (SVM model with the best hyperparameters)
best_svm = grid_search.best_estimator_

# Make predictions on the test set
y_pred_svm = best_svm.predict(X_test)

# Evaluate the model performance
mse_svm = mean_squared_error(y_test, y_pred_svm)
r2_svm = r2_score(y_test, y_pred_svm)

# Print the best hyperparameters and evaluation metrics
print(f"Best Parameters for SVM: {grid_search.best_params_}")
print(f"Mean Squared Error (MSE) for SVM: {mse_svm}")
print(f"R-squared (R²) for SVM: {r2_svm}")

from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

# Define the Decision Tree model
dt = DecisionTreeRegressor()

# Define parameter grid for tuning
param_grid = {
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': [None, 'auto', 'sqrt', 'log2']
}

# Perform grid search
grid_search_dt = GridSearchCV(estimator=dt, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
grid_search_dt.fit(X_train, y_train)

# Make predictions using the best estimator from grid search
best_dt = grid_search_dt.best_estimator_
y_pred_dt = best_dt.predict(X_test)

# Evaluate the model
mse_dt = mean_squared_error(y_test, y_pred_dt)
r2_dt = r2_score(y_test, y_pred_dt)

print(f"Best Parameters for Decision Tree: {grid_search_dt.best_params_}")
print(f"Mean Squared Error for Decision Tree: {mse_dt}")
print(f"R-squared for Decision Tree: {r2_dt}")

# Calculate residuals
residuals = y_test - y_pred_rf

# Plot residuals
plt.figure(figsize=(12, 6))
sns.histplot(residuals, kde=True, bins=30)
plt.title('Distribution of Residuals using Random Forest')
plt.xlabel('Residual')
plt.ylabel('Frequency')
plt.show()

# Plot actual vs predicted values
plt.figure(figsize=(12, 6))
plt.scatter(y_test, y_pred_rf, alpha=0.3)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r', linewidth=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted Values using Random Forest')
plt.show()

# Calculate residuals for linear regression
residuals = y_test - y_pred_lr

# Plot residuals
plt.figure(figsize=(12, 6))
sns.histplot(residuals, kde=True, bins=30)
plt.title('Distribution of Residuals using Linear Regression')
plt.xlabel('Residual')
plt.ylabel('Frequency')
plt.show()

# Plot actual vs predicted values
plt.figure(figsize=(12, 6))
plt.scatter(y_test, y_pred_lr, alpha=0.3)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r', linewidth=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted Values using Linear Regression')
plt.show()

# Calculate residuals for SVM
residuals = y_test - y_pred_svm

# Plot residuals
plt.figure(figsize=(12, 6))
sns.histplot(residuals, kde=True, bins=30)
plt.title('Distribution of Residuals using SVM')
plt.xlabel('Residual')
plt.ylabel('Frequency')
plt.show()

# Plot actual vs predicted values
plt.figure(figsize=(12, 6))
plt.scatter(y_test, y_pred_svm, alpha=0.3)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r', linewidth=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted Values using SVM')
plt.show()

# Calculate residuals for DT
residuals = y_test - y_pred_dt

# Plot residuals
plt.figure(figsize=(12, 6))
sns.histplot(residuals, kde=True, bins=30)
plt.title('Distribution of Residuals using Decision Tree')
plt.xlabel('Residual')
plt.ylabel('Frequency')
plt.show()

# Plot actual vs predicted values
plt.figure(figsize=(12, 6))
plt.scatter(y_test, y_pred_dt, alpha=0.3)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r', linewidth=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted Values using Decision Tret')
plt.show()

# Perform cross-validation linear regression
cv_scores = cross_val_score(best_lr, X, y, cv=5, scoring='r2')

print(f"Cross-validation R-squared scores for Linear Regression: {cv_scores}")
print(f"Mean R-squared score for Linear Regression: {cv_scores.mean()}")
print(f"Standard deviation of R-squared scores for Linear Regression: {cv_scores.std()}")

# Perform cross-validation random forest
cv_scores = cross_val_score(best_rf, X, y, cv=5, scoring='r2')

print(f"Cross-validation R-squared scores for Random Forest: {cv_scores}")
print(f"Mean R-squared score for Random Forest: {cv_scores.mean()}")
print(f"Standard deviation of R-squared scores for Random Forest: {cv_scores.std()}")

# Perform cross-validation SVM
cv_scores = cross_val_score(best_svm, X, y, cv=5, scoring='r2')

print(f"Cross-validation R-squared scores for SVM: {cv_scores}")
print(f"Mean R-squared score for SVM: {cv_scores.mean()}")
print(f"Standard deviation of R-squared scores for SVM: {cv_scores.std()}")

# Perform cross-validation linear regression
cv_scores = cross_val_score(best_dt, X, y, cv=5, scoring='r2')

print(f"Cross-validation R-squared scores for Decision Tree: {cv_scores}")
print(f"Mean R-squared score for Decision Tree: {cv_scores.mean()}")
print(f"Standard deviation of R-squared scores for Decision Tree: {cv_scores.std()}")

# Assuming y_test contains the actual values and y_pred contains the predicted values
# Get the first 5 predictions along with their actual values
comparison_df = pd.DataFrame({
    'Actual Value': y_test,
    'Predicted Value': y_pred_lr  # Change this to y_pred_rf for Random Forest predictions
})

# Display the first 5 rows of the comparison table
print(comparison_df.head(5))

import pickle

pickle.dump(best_lr,open('regmodel.pkl','wb'))

pickled_model=pickle.load(open('regmodel.pkl','rb'))

feature_columns = df.columns[:-1]

## Prediction
pickled_model.predict(scaler.transform(df[feature_columns].iloc[0].values.reshape(1, -1)))
