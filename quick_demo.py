"""
Quick Demo Script for Autonomous Data Science Agent
Run this to see the agent in action with sample data
"""

import os
import sys
from pathlib import Path

# Create sample data first
print("=" * 60)
print("🚀 Autonomous Data Science Agent - Quick Demo")
print("=" * 60)
print("\n📊 Step 1: Creating sample datasets...")

from create_sample_data import create_classification_dataset, create_regression_dataset

# Create sample datasets
churn_df = create_classification_dataset()
house_df = create_regression_dataset()

print("\n" + "=" * 60)
print("🤖 Step 2: Running Autonomous DS Agent on Classification Data")
print("=" * 60)

# Run on classification data
from main import AutonomousDataScienceAgent

print("\n🎯 Analyzing Customer Churn Dataset...\n")
agent1 = AutonomousDataScienceAgent(
    csv_path='sample_churn_data.csv',
    target_column='churn',
    output_dir='output_churn'
)

results1 = agent1.run()

print("\n" + "=" * 60)
print("🤖 Step 3: Running Autonomous DS Agent on Regression Data")
print("=" * 60)

print("\n🏠 Analyzing House Prices Dataset...\n")
agent2 = AutonomousDataScienceAgent(
    csv_path='sample_house_prices.csv',
    target_column='price',
    output_dir='output_house_prices'
)

results2 = agent2.run()

print("\n" + "=" * 60)
print("✨ DEMO COMPLETED!")
print("=" * 60)
print("\n📁 Check the following directories for results:")
print(f"   • Classification: {Path('output_churn').absolute()}")
print(f"   • Regression: {Path('output_house_prices').absolute()}")
print("\n📄 PDF Reports generated:")
print(f"   • {results1['report_path']}")
print(f"   • {results2['report_path']}")
print("\n🎉 Bilkul AI Data Scientist jaisa!")
