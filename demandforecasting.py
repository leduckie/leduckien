import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load the data
file_path = r'D:/SCM/Supply Chain/Competition/SCMission 2024/Round 3/CEL SCMission 2024 _ Round 3 _ Data (cleaned).xlsx'
sales_data = pd.read_excel(file_path, sheet_name='Sales Order')

# Data Cleaning
if 'Quantity in units' not in sales_data.columns or 'Date' not in sales_data.columns:
    print("Critical columns are missing from the data.")
else:
    sales_data.dropna(subset=['Quantity in units', 'Date'], inplace=True)
    sales_data['Date'] = pd.to_datetime(sales_data['Date'])
    sales_data['Year'] = sales_data['Date'].dt.year
    sales_data['Month'] = sales_data['Date'].dt.month

    if sales_data['Quantity in units'].isnull().any():
        sales_data['Quantity in units'].fillna(sales_data['Quantity in units'].median(), inplace=True)

    print("After cleaning and modifying:", sales_data.shape)
    print("Data types:", sales_data.dtypes)

    # Plotting Monthly Sales Volume
    monthly_sales = sales_data.groupby('Month')['Quantity in units'].sum()
    if not monthly_sales.empty:
        monthly_sales.plot(kind='bar')
        plt.title('Monthly Sales Volume')
        plt.xlabel('Month')
        plt.ylabel('Quantity in Units')
        plt.show()
    else:
        print("No data to plot after grouping.")

    # Machine Learning Application
    if not sales_data.empty:
        features = sales_data[['Month', 'Year']]
        target = sales_data['Quantity in units']

        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        print(f'MSE: {mse}, R2: {r2}')

        # Visualize Predictions vs Actual
        plt.figure(figsize=(10, 5))
        plt.scatter(y_test.index, y_test, color='blue', label='Actual', alpha=0.6)
        plt.scatter(y_test.index, predictions, color='red', label='Predicted', alpha=0.6)
        plt.legend()
        plt.title('Actual vs Predicted Sales')
        plt.xlabel('Index')
        plt.ylabel('Sales Volume')
        plt.show()

        # Residual Plot
        residuals = y_test - predictions
        plt.figure(figsize=(10, 5))
        plt.scatter(y_test.index, residuals)
        plt.hlines(y=0, xmin=residuals.index.min(), xmax=residuals.index.max(), colors='red', linestyles='--')
        plt.title('Residual Plot')
        plt.xlabel('Index')
        plt.ylabel('Residuals (Errors)')
        plt.show()

    else:
        print("Insufficient data for machine learning.")
