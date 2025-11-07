# 📘 Usage Guide - Autonomous Data Science Agent

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Demo
```bash
python quick_demo.py
```

This will:
- Create 2 sample datasets (classification & regression)
- Run the full pipeline on both
- Generate PDF reports and visualizations

### Step 3: Check Results
Open the generated PDF reports in:
- `output_churn/data_science_report_*.pdf`
- `output_house_prices/data_science_report_*.pdf`

---

## 📊 Using Your Own Data

### Basic Usage
```bash
python main.py your_data.csv
```

The agent will:
- Auto-detect the target column (last column or columns with keywords)
- Run the full pipeline
- Save results to `output/` directory

### Specify Target Column
```bash
python main.py your_data.csv --target column_name
```

### Custom Output Directory
```bash
python main.py your_data.csv --target price --output my_analysis
```

---

## 🎯 Use Cases & Examples

### 1. Customer Churn Prediction
```bash
python main.py customer_data.csv --target churn
```

**What it does:**
- Cleans customer data
- Engineers features from customer behavior
- Trains classification models
- Predicts which customers will churn
- Generates insights report

### 2. House Price Prediction
```bash
python main.py housing_data.csv --target price
```

**What it does:**
- Analyzes house features
- Creates interaction features
- Trains regression models
- Predicts house prices
- Shows feature importance

### 3. Sales Forecasting
```bash
python main.py sales_data.csv --target sales_amount
```

### 4. Credit Risk Assessment
```bash
python main.py loan_data.csv --target default
```

### 5. Product Quality Prediction
```bash
python main.py manufacturing_data.csv --target quality_score
```

---

## 📁 Project Structure

```
autonomous_ds_agent/
│
├── main.py                      # 🎯 Main orchestrator
├── data_loader.py              # 📂 CSV loading
├── data_cleaner.py             # 🧹 Data cleaning
├── feature_engineer.py         # ⚙️ Feature engineering
├── automl_engine.py            # 🤖 AutoML
├── visualizer.py               # 📊 Visualizations
├── report_generator.py         # 📄 PDF reports
│
├── requirements.txt            # 📦 Dependencies
├── README.md                   # 📖 Documentation
├── USAGE_GUIDE.md             # 📘 This file
│
├── create_sample_data.py      # 🎲 Sample data generator
├── quick_demo.py              # 🚀 Quick demo script
└── __init__.py                # 📦 Package init
```

---

## 🔧 What Happens Under the Hood

### Pipeline Flow:

```
CSV File
   ↓
📂 Data Loading (auto encoding detection)
   ↓
🧹 Data Cleaning
   ├─ Remove duplicates
   ├─ Handle missing values
   ├─ Cap outliers
   └─ Drop useless columns
   ↓
⚙️ Feature Engineering
   ├─ Interaction features (multiply, divide)
   ├─ Polynomial features (squared, sqrt)
   ├─ Aggregation features (sum, mean, std)
   ├─ Encode categorical variables
   ├─ Scale numeric features
   └─ Select best features
   ↓
🤖 AutoML
   ├─ Detect task type (classification/regression)
   ├─ Train 7+ models
   ├─ Evaluate each model
   └─ Select best model
   ↓
📊 Visualizations
   ├─ 9+ charts and graphs
   └─ Export as PNG (300 DPI)
   ↓
📄 PDF Report
   ├─ Executive summary
   ├─ Data overview
   ├─ Cleaning report
   ├─ Feature engineering
   ├─ Model performance
   ├─ Visualizations
   └─ Recommendations
   ↓
✅ Done!
```

---

## 📊 Output Files

After running the agent, you'll get:

### 1. PDF Report
**Location:** `output/data_science_report_TIMESTAMP.pdf`

**Contains:**
- Executive summary
- Data statistics
- Cleaning details
- Feature engineering report
- Model comparison
- Performance metrics
- All visualizations
- Recommendations

### 2. Visualizations Folder
**Location:** `output/visualizations/`

**Files:**
1. `01_missing_values.png` - Missing data analysis
2. `02_data_types.png` - Data type distribution
3. `03_target_distribution.png` - Target variable analysis
4. `04_correlation_heatmap.png` - Feature correlations
5. `05_feature_distributions.png` - Feature distributions
6. `06_model_comparison.png` - All models compared
7. `07_feature_importance.png` - Most important features
8. `08_confusion_matrix.png` - Classification results (or regression metrics)
9. `09_predictions.png` - Predictions vs actual

---

## 🎓 Understanding the Results

### Classification Metrics

**Accuracy:** Percentage of correct predictions
- > 0.9: Excellent
- 0.8-0.9: Good
- 0.7-0.8: Fair
- < 0.7: Needs improvement

**Precision:** Of predicted positives, how many are correct
**Recall:** Of actual positives, how many were found
**F1-Score:** Balance between precision and recall

### Regression Metrics

**R² Score:** How well the model fits the data
- > 0.9: Excellent fit
- 0.7-0.9: Good fit
- 0.5-0.7: Moderate fit
- < 0.5: Poor fit

**RMSE:** Average prediction error (lower is better)
**MAE:** Average absolute error (lower is better)

---

## 💡 Tips & Best Practices

### Data Preparation

1. **CSV Format:** Ensure your data is in CSV format
2. **Headers:** First row should contain column names
3. **Target Column:** Should be clearly identifiable
4. **Size:** Works best with 100-100K rows
5. **Quality:** Better data = better results

### Target Column Selection

The agent auto-detects target if:
- Column name contains: 'target', 'label', 'y', 'class', 'output'
- Or uses the last column

**Best practice:** Explicitly specify with `--target` flag

### Interpreting Results

1. **Check the PDF report first** - It has everything
2. **Look at model comparison** - See which models performed best
3. **Review feature importance** - Understand what drives predictions
4. **Check visualizations** - Spot patterns and issues
5. **Read recommendations** - Get actionable insights

### Common Issues

**Issue:** Low model performance
**Solution:** 
- Check data quality
- Ensure target column is correct
- May need more data or better features

**Issue:** Missing values warning
**Solution:** 
- Agent handles automatically
- Check cleaning report for details

**Issue:** Memory error
**Solution:** 
- Reduce dataset size
- Sample your data before running

---

## 🔬 Advanced Usage

### Programmatic Usage

```python
from main import AutonomousDataScienceAgent

# Create agent
agent = AutonomousDataScienceAgent(
    csv_path='data.csv',
    target_column='target',
    output_dir='results'
)

# Run pipeline
results = agent.run()

# Access results
print(f"Best Model: {results['best_model_name']}")
print(f"Score: {results['best_score']:.4f}")
print(f"Report: {results['report_path']}")
```

### Batch Processing

```python
import glob

csv_files = glob.glob('data/*.csv')

for csv_file in csv_files:
    agent = AutonomousDataScienceAgent(
        csv_path=csv_file,
        output_dir=f'output_{Path(csv_file).stem}'
    )
    agent.run()
```

---

## 🛠️ Customization

### Add Custom Models

Edit `automl_engine.py`:

```python
def _get_models(self):
    if self.is_classification:
        return {
            'Random Forest': RandomForestClassifier(...),
            'Your Model': YourCustomModel(...),
            # Add more models
        }
```

### Add Custom Features

Edit `feature_engineer.py`:

```python
def _create_custom_features(self, df):
    # Add your custom feature engineering
    df['custom_feature'] = df['col1'] * df['col2']
    return df
```

### Customize Visualizations

Edit `visualizer.py`:

```python
def _plot_custom_viz(self, df):
    # Add your custom visualization
    plt.figure(figsize=(10, 6))
    # Your plotting code
    plt.savefig(self.output_dir / 'custom_plot.png')
```

---

## 📞 Support & Troubleshooting

### Common Errors

**Error:** `FileNotFoundError`
- Check CSV file path is correct
- Use absolute path if needed

**Error:** `KeyError: 'target_column'`
- Verify target column name
- Check for typos in column name

**Error:** `MemoryError`
- Dataset too large
- Try sampling: `df.sample(n=10000)`

**Error:** `No models were successfully trained`
- Check data has enough samples
- Verify target column has valid values

### Getting Help

1. Check README.md for general info
2. Review this guide for usage details
3. Examine sample datasets for reference
4. Run `quick_demo.py` to see it working

---

## 🎯 Next Steps

1. ✅ Run the quick demo
2. ✅ Try with sample data
3. ✅ Use your own dataset
4. ✅ Review the PDF report
5. ✅ Understand the insights
6. ✅ Take action on recommendations

---

## 🌟 Features Summary

✅ **Automatic** - No manual intervention needed
✅ **Fast** - Complete analysis in minutes
✅ **Comprehensive** - Full data science workflow
✅ **Professional** - Publication-ready reports
✅ **Flexible** - Works with any CSV dataset
✅ **Intelligent** - Smart decisions at each step
✅ **Visual** - Beautiful charts and graphs
✅ **Actionable** - Clear recommendations

---

**Happy Analyzing! 🚀**

*Bilkul AI Data Scientist jaisa!*
