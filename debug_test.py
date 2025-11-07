"""
Debug script to test the pipeline with sample data
"""
import pandas as pd
import numpy as np
from main import AutonomousDataScienceAgent

# Test with sample churn data
print("Testing with sample_churn_data.csv...")
print("=" * 60)

try:
    agent = AutonomousDataScienceAgent(
        csv_path='sample_churn_data.csv',
        target_column='churn',
        output_dir='output_debug'
    )
    
    # Load data
    print("\n1. Loading data...")
    agent.raw_data = agent.loader.load_csv(agent.csv_path)
    print(f"   Loaded: {len(agent.raw_data)} rows, {len(agent.raw_data.columns)} columns")
    print(f"   Columns: {agent.raw_data.columns.tolist()}")
    
    # Clean data
    print("\n2. Cleaning data...")
    agent.cleaned_data = agent.cleaner.clean(agent.raw_data)
    print(f"   Cleaned: {len(agent.cleaned_data)} rows, {len(agent.cleaned_data.columns)} columns")
    print(f"   Columns: {agent.cleaned_data.columns.tolist()}")
    
    # Feature engineering
    print("\n3. Feature engineering...")
    agent.engineered_data = agent.feature_engineer.engineer_features(
        agent.cleaned_data,
        target_column=agent.target_column
    )
    print(f"   Engineered: {len(agent.engineered_data)} rows, {len(agent.engineered_data.columns)} columns")
    print(f"   Columns: {agent.engineered_data.columns.tolist()}")
    
    # Check for issues
    print("\n4. Checking for data issues...")
    X = agent.engineered_data.drop(columns=[agent.target_column])
    y = agent.engineered_data[agent.target_column]
    
    print(f"   Features shape: {X.shape}")
    print(f"   Target shape: {y.shape}")
    print(f"   NaN in features: {X.isnull().sum().sum()}")
    print(f"   Inf in features: {np.isinf(X.values).sum()}")
    print(f"   NaN in target: {y.isnull().sum()}")
    print(f"   Target unique values: {y.nunique()}")
    print(f"   Target value counts:\n{y.value_counts()}")
    
    # Try AutoML
    print("\n5. Running AutoML...")
    model_results = agent.automl.find_best_model(
        agent.engineered_data,
        target_column=agent.target_column
    )
    
    print(f"\n✅ SUCCESS!")
    print(f"   Best model: {model_results['best_model_name']}")
    print(f"   Score: {model_results['best_score']:.4f}")
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"   Message: {str(e)}")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()
