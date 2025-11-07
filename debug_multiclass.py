"""
Debug multi-class issue causing 0.0 accuracy
"""
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

# Simulate what might be happening
print("="*60)
print("DEBUGGING MULTI-CLASS ACCURACY ISSUE")
print("="*60)

# Load the data
df = pd.read_csv('sample_churn_data.csv')
print(f"\nDataset shape: {df.shape}")
print(f"Target column 'churn' unique values: {df['churn'].nunique()}")
print(f"Target value counts:\n{df['churn'].value_counts()}")
print(f"Target dtype: {df['churn'].dtype}")

# Check if there's an issue with the target
print("\n" + "="*60)
print("CHECKING FOR ISSUES:")
print("="*60)

# Simulate prediction with wrong number of classes
y_true = np.array([0, 1, 0, 1, 0])
y_pred_correct = np.array([0, 1, 0, 1, 0])
y_pred_wrong_classes = np.array([5, 10, 15, 20, 25])  # Wrong class labels

print(f"\nCorrect prediction accuracy: {accuracy_score(y_true, y_pred_correct)}")
print(f"Wrong classes accuracy: {accuracy_score(y_true, y_pred_wrong_classes)}")

# Check if there's a feature selection issue
print("\n" + "="*60)
print("CHECKING FEATURE ENGINEERING:")
print("="*60)

from feature_engineer import FeatureEngineer
from data_cleaner import DataCleaner

cleaner = DataCleaner()
cleaned = cleaner.clean(df)

engineer = FeatureEngineer()
engineered = engineer.engineer_features(cleaned, target_column='churn')

print(f"\nEngineered data shape: {engineered.shape}")
print(f"Target in engineered data: {'churn' in engineered.columns}")
print(f"Target unique values after engineering: {engineered['churn'].nunique()}")
print(f"Target value counts after engineering:\n{engineered['churn'].value_counts()}")

# Check if target got encoded incorrectly
if engineered['churn'].dtype != df['churn'].dtype:
    print(f"\n⚠️ WARNING: Target dtype changed!")
    print(f"  Original: {df['churn'].dtype}")
    print(f"  After engineering: {engineered['churn'].dtype}")
