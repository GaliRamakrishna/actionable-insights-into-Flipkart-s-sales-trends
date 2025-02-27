from flask import Flask, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load and preprocess the dataset
df = pd.read_csv("flipkart_sales.csv")  # Ensure this CSV file exists

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Month'] = df['Order Date'].dt.to_period('M').astype(str)  # Convert Period to string

# Aggregate data
category_sales = df.groupby('Category')['Total Sales (INR)'].sum().reset_index()
monthly_sales = df.groupby('Month')['Total Sales (INR)'].sum().reset_index()

# Route for rendering the visualization
@app.route('/')
def index():
    return render_template('index.html')

# API route to provide sales data by category
@app.route('/api/category_sales')
def category_sales_data():
    return jsonify(category_sales.to_dict(orient='records'))

# API route to provide monthly sales data
@app.route('/api/monthly_sales')
def monthly_sales_data():
    return jsonify(monthly_sales.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
