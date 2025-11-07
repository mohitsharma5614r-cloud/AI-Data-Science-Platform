"""
Create sample datasets for testing the Autonomous DS Agent
"""

import pandas as pd
import numpy as np

def create_classification_dataset():
    """Create a sample classification dataset (Customer Churn)"""
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'customer_id': range(1, n_samples + 1),
        'age': np.random.randint(18, 70, n_samples),
        'tenure_months': np.random.randint(1, 72, n_samples),
        'monthly_charges': np.random.uniform(20, 120, n_samples),
        'total_charges': np.random.uniform(100, 8000, n_samples),
        'contract_type': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples),
        'payment_method': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'], n_samples),
        'internet_service': np.random.choice(['DSL', 'Fiber optic', 'No'], n_samples),
        'online_security': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'tech_support': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'num_services': np.random.randint(0, 8, n_samples),
        'customer_service_calls': np.random.randint(0, 10, n_samples),
    }
    
    # Create target based on features (with some logic)
    churn_prob = (
        (data['customer_service_calls'] > 5).astype(int) * 0.3 +
        (data['tenure_months'] < 12).astype(int) * 0.3 +
        (data['contract_type'] == 'Month-to-month').astype(int) * 0.2 +
        np.random.uniform(0, 0.2, n_samples)
    )
    
    churn_binary = (churn_prob > 0.5).astype(int)
    data['churn'] = np.where(churn_binary == 1, 'Yes', 'No')
    
    # Add some missing values
    missing_indices = np.random.choice(n_samples, size=50, replace=False)
    data['total_charges'] = pd.Series(data['total_charges'])
    data['total_charges'].iloc[missing_indices] = np.nan
    
    df = pd.DataFrame(data)
    df.to_csv('sample_churn_data.csv', index=False)
    print("Created sample_churn_data.csv (Classification)")
    return df

def create_regression_dataset():
    """Create a sample regression dataset (House Prices)"""
    np.random.seed(42)
    n_samples = 800
    
    data = {
        'house_id': range(1, n_samples + 1),
        'square_feet': np.random.randint(800, 4000, n_samples),
        'bedrooms': np.random.randint(1, 6, n_samples),
        'bathrooms': np.random.uniform(1, 4, n_samples),
        'year_built': np.random.randint(1950, 2024, n_samples),
        'lot_size': np.random.uniform(2000, 15000, n_samples),
        'garage_spaces': np.random.randint(0, 4, n_samples),
        'neighborhood': np.random.choice(['Downtown', 'Suburb', 'Rural', 'Coastal'], n_samples),
        'condition': np.random.choice(['Excellent', 'Good', 'Fair', 'Poor'], n_samples),
        'has_pool': np.random.choice(['Yes', 'No'], n_samples),
        'has_fireplace': np.random.choice(['Yes', 'No'], n_samples),
        'distance_to_city': np.random.uniform(0, 50, n_samples),
    }
    
    # Create target based on features
    base_price = 100000
    price = (
        base_price +
        data['square_feet'] * 150 +
        data['bedrooms'] * 20000 +
        data['bathrooms'] * 15000 +
        (2024 - data['year_built']) * -500 +
        data['lot_size'] * 5 +
        data['garage_spaces'] * 10000 +
        (data['neighborhood'] == 'Coastal').astype(int) * 100000 +
        (data['neighborhood'] == 'Downtown').astype(int) * 50000 +
        (data['condition'] == 'Excellent').astype(int) * 50000 +
        (data['has_pool'] == 'Yes').astype(int) * 30000 +
        np.random.normal(0, 50000, n_samples)
    )
    
    data['price'] = np.maximum(price, 50000)  # Minimum price
    
    # Add some missing values
    missing_indices = np.random.choice(n_samples, size=30, replace=False)
    data['lot_size'] = pd.Series(data['lot_size'])
    data['lot_size'].iloc[missing_indices] = np.nan
    
    df = pd.DataFrame(data)
    df.to_csv('sample_house_prices.csv', index=False)
    print("Created sample_house_prices.csv (Regression)")
    return df

if __name__ == "__main__":
    print("Creating sample datasets...\n")
    create_classification_dataset()
    create_regression_dataset()
    print("\nSample datasets created successfully!")
    print("\nYou can now run:")
    print("  python main.py sample_churn_data.csv --target churn")
    print("  python main.py sample_house_prices.csv --target price")
