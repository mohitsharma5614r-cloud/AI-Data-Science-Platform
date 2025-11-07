"""
Test to check what the web app actually returns
"""
import json
from main import AutonomousDataScienceAgent

print("Testing web app flow...")
print("="*60)

# Simulate what web app does
agent = AutonomousDataScienceAgent(
    csv_path='sample_churn_data.csv',
    target_column='churn',
    output_dir='web_test_output'
)

results = agent.run()

print("\n" + "="*60)
print("RESULTS STRUCTURE:")
print("="*60)

# Check what's in results
print(f"\nKeys in results: {results.keys()}")
print(f"\nmodel_results keys: {results['model_results'].keys()}")

# Check the actual values
model_results = results['model_results']
print(f"\nBest Model: {model_results['best_model_name']}")
print(f"Best Score: {model_results['best_score']}")
print(f"Best Score Type: {type(model_results['best_score'])}")
print(f"Best Score Value: {model_results['best_score']:.10f}")

# Check if it's actually zero
if model_results['best_score'] == 0.0:
    print("\n❌ ERROR: Score is 0.0000!")
    print("This is the bug!")
else:
    print(f"\n✅ Score is NOT zero: {model_results['best_score']}")

# Check all models
print("\n" + "="*60)
print("ALL MODEL SCORES:")
print("="*60)
for result in model_results['all_results']:
    score = result['score']
    print(f"{result['model_name']:25s}: {score:.4f} (raw: {score})")
    if score == 0.0:
        print(f"  ⚠️ WARNING: {result['model_name']} has 0.0 score!")

# Check metrics
print("\n" + "="*60)
print("METRICS:")
print("="*60)
metrics = model_results['metrics']
for key, value in metrics.items():
    if isinstance(value, (int, float)):
        print(f"{key:20s}: {value:.4f}")
        if value == 0.0 and key == 'accuracy':
            print("  ⚠️ WARNING: Accuracy is 0.0!")
