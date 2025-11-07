"""
Create a demo ML-ready dataset for testing the web app
"""
import pandas as pd
import numpy as np

np.random.seed(42)

print("Creating demo ML dataset...")

# Create a realistic employee attrition dataset
n_samples = 500

data = {
    'employee_id': range(1, n_samples + 1),
    'age': np.random.randint(22, 65, n_samples),
    'years_at_company': np.random.randint(0, 20, n_samples),
    'salary': np.random.randint(30000, 150000, n_samples),
    'satisfaction_score': np.random.randint(1, 11, n_samples),
    'performance_rating': np.random.choice(['Low', 'Medium', 'High'], n_samples, p=[0.2, 0.5, 0.3]),
    'department': np.random.choice(['Sales', 'Engineering', 'HR', 'Marketing', 'Finance'], n_samples),
    'remote_work': np.random.choice(['Yes', 'No'], n_samples, p=[0.4, 0.6]),
    'overtime_hours': np.random.randint(0, 30, n_samples),
    'projects_completed': np.random.randint(1, 15, n_samples),
}

df = pd.DataFrame(data)

# Create target variable (attrition) based on some logic
# More likely to leave if: low satisfaction, low salary, high overtime
attrition_prob = (
    (10 - df['satisfaction_score']) * 0.1 +  # Low satisfaction increases probability
    (df['overtime_hours'] / 30) * 0.3 +       # High overtime increases probability
    (1 - df['salary'] / 150000) * 0.2 +       # Low salary increases probability
    np.random.random(n_samples) * 0.4          # Random factor
)

df['attrition'] = (attrition_prob > 0.5).astype(int)
df['attrition'] = df['attrition'].map({0: 'No', 1: 'Yes'})

# Save to CSV
output_file = 'demo_employee_attrition.csv'
df.to_csv(output_file, index=False)

print(f"\n✅ Created: {output_file}")
print(f"   Rows: {len(df)}")
print(f"   Columns: {len(df.columns)}")
print(f"\nTarget column: 'attrition'")
print(f"   Values: {df['attrition'].value_counts().to_dict()}")
print(f"\nThis dataset is ready for ML!")
print(f"\nUpload this file to the web interface at http://localhost:5000")
