"""
Test the fix with customers-100.csv to see if it now detects a valid target
"""
import pandas as pd
from main import AutonomousDataScienceAgent

print("="*60)
print("TESTING TARGET AUTO-DETECTION FIX")
print("="*60)

# Test with customers-100.csv (the problematic file)
csv_path = 'uploads/20251107_182259_customers-100.csv'

df = pd.read_csv(csv_path)
print(f"\nDataset: {csv_path}")
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Show unique counts for each column
print("\nUnique value counts:")
for col in df.columns:
    n_unique = df[col].nunique()
    pct_unique = (n_unique / len(df)) * 100
    print(f"  {col:25s}: {n_unique:3d} unique ({pct_unique:5.1f}%)")

# Test auto-detection
print("\n" + "="*60)
print("TESTING AUTO-DETECTION:")
print("="*60)

try:
    agent = AutonomousDataScienceAgent(
        csv_path=csv_path,
        target_column=None,  # Let it auto-detect
        output_dir='test_customers_output'
    )
    
    # Load data
    agent.raw_data = agent.loader.load_csv(agent.csv_path)
    
    # Auto-detect target
    detected_target = agent._auto_detect_target()
    
    print(f"\n✓ Detected target column: {detected_target}")
    print(f"  Unique values: {agent.raw_data[detected_target].nunique()}")
    print(f"  Data type: {agent.raw_data[detected_target].dtype}")
    
    # Check if it's valid
    is_valid = agent._is_valid_target(detected_target)
    print(f"  Is valid target: {is_valid}")
    
    if agent.raw_data[detected_target].nunique() > len(agent.raw_data) * 0.8:
        print("\n❌ ERROR: Still detecting high-cardinality column!")
        print("   This will result in 0% accuracy.")
    else:
        print("\n✅ SUCCESS: Detected a reasonable target column!")
        
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
