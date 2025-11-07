"""
Verification script to check model accuracy is not 0.0000
"""
import pandas as pd
import numpy as np
from main import AutonomousDataScienceAgent

print("="*60)
print("ACCURACY VERIFICATION TEST")
print("="*60)

# Test with sample churn data
print("\n1. Testing with sample_churn_data.csv...")
agent = AutonomousDataScienceAgent(
    csv_path='sample_churn_data.csv',
    target_column='churn',
    output_dir='verify_output'
)

# Run full pipeline
results = agent.run()

# Check accuracy
model_results = results['model_results']
best_score = model_results['best_score']
best_model = model_results['best_model_name']

print("\n" + "="*60)
print("VERIFICATION RESULTS")
print("="*60)
print(f"Best Model: {best_model}")
print(f"Best Score: {best_score:.4f}")
print(f"Score Type: {type(best_score)}")
print(f"Score > 0: {best_score > 0}")

# Check all model scores
print("\nAll Model Scores:")
for result in model_results['all_results']:
    print(f"  {result['model_name']}: {result['score']:.4f}")

# Check metrics
print("\nDetailed Metrics:")
metrics = model_results['metrics']
for key, value in metrics.items():
    if isinstance(value, (int, float)):
        print(f"  {key}: {value:.4f}")

# Final verdict
print("\n" + "="*60)
if best_score > 0:
    print("✅ SUCCESS: Model accuracy is NOT 0.0000")
    print(f"   Actual accuracy: {best_score:.4f}")
else:
    print("❌ FAILURE: Model accuracy IS 0.0000")
    print("   This needs investigation!")
print("="*60)
