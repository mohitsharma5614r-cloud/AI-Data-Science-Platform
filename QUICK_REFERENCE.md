# ⚡ Quick Reference Card

## 🚀 Installation (One Command)
```bash
pip install -r requirements.txt
```

## 🎯 Usage (Three Ways)

### 1. Auto-detect Everything
```bash
python main.py your_data.csv
```

### 2. Specify Target Column
```bash
python main.py your_data.csv --target column_name
```

### 3. Full Custom
```bash
python main.py your_data.csv --target price --output my_results
```

## 🎲 Quick Demo
```bash
python quick_demo.py
```

## 📁 File Structure
```
autonomous_ds_agent/
├── main.py                 # Run this
├── requirements.txt        # Install this
├── quick_demo.py          # Demo this
└── README.md              # Read this
```

## 📊 What You Get
```
output/
├── data_science_report_*.pdf    # 📄 Main report
└── visualizations/              # 📊 9 charts
    ├── 01_missing_values.png
    ├── 02_data_types.png
    ├── 03_target_distribution.png
    ├── 04_correlation_heatmap.png
    ├── 05_feature_distributions.png
    ├── 06_model_comparison.png
    ├── 07_feature_importance.png
    ├── 08_confusion_matrix.png
    └── 09_predictions.png
```

## 🔧 Pipeline Steps
1. **Load** → Auto-detect encoding
2. **Clean** → Remove duplicates, handle missing, cap outliers
3. **Engineer** → Create features, encode, scale, select
4. **Train** → Test 7+ models, pick best
5. **Visualize** → Generate 9 charts
6. **Report** → Create PDF with everything

## 📈 Models Tested

**Classification:**
- Random Forest
- Gradient Boosting
- Logistic Regression
- Decision Tree
- K-Nearest Neighbors
- Naive Bayes
- AdaBoost

**Regression:**
- Random Forest
- Gradient Boosting
- Linear Regression
- Ridge
- Lasso
- Decision Tree
- K-Nearest Neighbors
- AdaBoost

## 📊 Metrics

**Classification:**
- Accuracy, Precision, Recall, F1-Score
- Confusion Matrix

**Regression:**
- R² Score, MSE, RMSE, MAE

## ⚙️ Key Features

✅ 100% Automatic
✅ Handles missing values
✅ Removes outliers
✅ Creates features
✅ Selects best model
✅ Generates visualizations
✅ Creates PDF report

## 🎓 Documentation

- **README.md** - Overview & features
- **INSTALLATION.md** - Setup guide
- **USAGE_GUIDE.md** - Detailed usage
- **WORKFLOW.md** - Pipeline details
- **PROJECT_SUMMARY.md** - Complete info

## 💡 Common Commands

```bash
# Install
pip install -r requirements.txt

# Create sample data
python create_sample_data.py

# Run demo
python quick_demo.py

# Run on your data
python main.py data.csv --target target_col

# Check Python version
python --version

# Verify installation
python -c "import pandas, sklearn; print('OK')"
```

## 🐛 Troubleshooting

**Issue:** Module not found
```bash
pip install -r requirements.txt
```

**Issue:** Permission denied
```bash
pip install --user -r requirements.txt
```

**Issue:** Slow installation
```bash
pip install --upgrade pip
```

## 📞 Quick Help

1. Read **README.md** first
2. Run **quick_demo.py** to see it work
3. Check **USAGE_GUIDE.md** for details
4. Review **INSTALLATION.md** if issues

## ⏱️ Expected Time

- **Small dataset (<1K):** 20-30 seconds
- **Medium (1K-10K):** 1-2 minutes
- **Large (10K-100K):** 2-5 minutes

## 🎯 Best For

✓ Quick data analysis
✓ Baseline models
✓ Data quality check
✓ Automated reporting
✓ Learning ML
✓ Prototyping

## 🔒 Data Requirements

- **Format:** CSV with headers
- **Size:** 100 - 100K rows (optimal)
- **Target:** Clearly identifiable column
- **Quality:** Better data = better results

## 📊 Success Indicators

✅ PDF report generated
✅ 9 visualizations created
✅ Best model identified
✅ Metrics calculated
✅ No errors in console

## 🌟 Pro Tips

1. **Specify target explicitly** for best results
2. **Check PDF report first** - has everything
3. **Review feature importance** - understand drivers
4. **Use sample data** to learn the system
5. **Customize** by editing Python files

## 🔄 Typical Workflow

```
1. Prepare CSV file
2. Install dependencies
3. Run: python main.py data.csv --target target
4. Wait for completion
5. Open PDF report
6. Review insights
7. Take action!
```

## 📦 Dependencies (8 packages)

```
pandas          # Data manipulation
numpy           # Numerical computing
scipy           # Scientific computing
scikit-learn    # Machine learning
matplotlib      # Plotting
seaborn         # Visualization
reportlab       # PDF generation
openpyxl        # Excel support
```

## 🎨 Customization Points

- **Models:** `automl_engine.py`
- **Features:** `feature_engineer.py`
- **Plots:** `visualizer.py`
- **Report:** `report_generator.py`
- **Cleaning:** `data_cleaner.py`

## 📱 Quick Commands Cheat Sheet

```bash
# Setup
pip install -r requirements.txt

# Demo
python quick_demo.py

# Basic usage
python main.py data.csv

# With target
python main.py data.csv --target price

# Custom output
python main.py data.csv --target price --output results

# Create samples
python create_sample_data.py

# Help
python main.py --help
```

## 🎯 Output Checklist

After running, verify:
- [ ] PDF report exists
- [ ] 9 PNG visualizations created
- [ ] No errors in console
- [ ] Report opens correctly
- [ ] Metrics look reasonable

## 🚨 Common Mistakes

❌ Forgetting to install dependencies
❌ Wrong target column name
❌ CSV file not found
❌ No headers in CSV
❌ Target column not in data

## ✅ Best Practices

✓ Install in virtual environment
✓ Specify target explicitly
✓ Check data quality first
✓ Review cleaning report
✓ Understand feature importance
✓ Validate model performance

---

**Keep this card handy for quick reference!** 🚀

*Bilkul AI Data Scientist jaisa!*
