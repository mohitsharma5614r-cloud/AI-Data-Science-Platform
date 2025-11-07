# 🤖 Autonomous Data Science Agent

**Full Automated Data Pipeline AI** - Your personal AI Data Scientist!

## ✨ Features

This autonomous agent performs a **complete end-to-end data science workflow** automatically:

- 📂 **CSV Load** - Intelligent file loading with automatic encoding detection
- 🧹 **Auto Clean** - Handles missing values, outliers, duplicates automatically
- ⚙️ **Feature Engineering** - Creates interaction, polynomial, and aggregation features
- 🤖 **AutoML** - Tests multiple ML models and selects the best one
- 📊 **Visualizations** - Generates comprehensive charts and graphs
- 📄 **PDF Report** - Creates professional analysis report

**100% Automatic** - Just provide a CSV file and target column!

## 🚀 Quick Start

### Installation

```bash
# Clone or download this project
cd autonomous_ds_agent

# Install dependencies
pip install -r requirements.txt
```

### Usage

**Basic Usage:**
```bash
python main.py your_data.csv
```

**Specify Target Column:**
```bash
python main.py your_data.csv --target target_column_name
```

**Custom Output Directory:**
```bash
python main.py your_data.csv --target price --output my_results
```

### Example

```bash
# Auto-detect target column
python main.py sales_data.csv

# Specify target column
python main.py house_prices.csv --target price

# Full custom
python main.py customer_churn.csv --target churn --output churn_analysis
```

## 📊 What You Get

After running the agent, you'll get:

### 1. **Comprehensive PDF Report** 📄
- Executive summary
- Data overview and statistics
- Cleaning report
- Feature engineering details
- Model performance metrics
- Visualizations
- Recommendations

### 2. **Visualizations** 📈
- Missing values analysis
- Data type distribution
- Target variable distribution
- Correlation heatmap
- Feature distributions
- Model comparison chart
- Feature importance plot
- Confusion matrix / Regression metrics
- Predictions vs Actual

### 3. **Best ML Model** 🎯
Automatically trained and evaluated models:
- **Classification**: Random Forest, Gradient Boosting, Logistic Regression, Decision Tree, KNN, Naive Bayes, AdaBoost
- **Regression**: Random Forest, Gradient Boosting, Linear Regression, Ridge, Lasso, Decision Tree, KNN, AdaBoost

## 🏗️ Architecture

```
autonomous_ds_agent/
├── main.py                  # Main orchestrator
├── data_loader.py          # CSV loading with encoding detection
├── data_cleaner.py         # Automatic data cleaning
├── feature_engineer.py     # Feature engineering
├── automl_engine.py        # AutoML model selection
├── visualizer.py           # Visualization generation
├── report_generator.py     # PDF report creation
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🔧 Pipeline Steps

### 1. **Data Loading**
- Automatic encoding detection (UTF-8, Latin-1, etc.)
- Error handling and recovery
- Data type inference

### 2. **Data Cleaning**
- Remove duplicate rows
- Handle missing values (median/mode/KNN imputation)
- Detect and cap outliers (IQR method)
- Drop useless columns (high missing %, single value, IDs)
- Fix data types
- Clean text columns

### 3. **Feature Engineering**
- **Interaction features**: Multiplication and division between numeric features
- **Polynomial features**: Squared, square root
- **Aggregation features**: Sum, mean, standard deviation
- **Encoding**: One-hot for low cardinality, label encoding for high cardinality
- **Scaling**: StandardScaler for numeric features
- **Feature selection**: SelectKBest to keep most important features

### 4. **AutoML**
- Automatic task detection (classification vs regression)
- Train multiple models in parallel
- Cross-validation
- Select best model based on performance
- Generate detailed metrics

### 5. **Visualization**
- 9+ automatic visualizations
- High-quality PNG exports (300 DPI)
- Professional styling with Seaborn

### 6. **Report Generation**
- Professional PDF with ReportLab
- Embedded visualizations
- Detailed metrics and insights
- Actionable recommendations

## 📋 Requirements

- Python 3.8+
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- reportlab
- scipy

## 🎯 Use Cases

- **Quick Data Analysis**: Get instant insights from any CSV
- **Baseline Models**: Quickly establish baseline ML performance
- **Data Quality Assessment**: Understand data issues automatically
- **Automated Reporting**: Generate reports for stakeholders
- **Learning Tool**: Understand data science workflow
- **Prototyping**: Rapid experimentation with datasets

## 💡 Tips

1. **Target Column**: If not specified, the agent will auto-detect (last column or columns with keywords like 'target', 'label', 'y')

2. **Data Size**: Works best with datasets up to 100K rows. For larger datasets, consider sampling.

3. **Feature Limit**: Automatically limits to top 50 features to prevent overfitting and improve performance.

4. **Missing Values**: Handles up to 50% missing values per column. Columns with more are dropped.

5. **Categorical Variables**: Automatically detects and encodes. One-hot for <10 unique values, label encoding otherwise.

## 🔍 Output Structure

```
output/
├── data_science_report_YYYYMMDD_HHMMSS.pdf
└── visualizations/
    ├── 01_missing_values.png
    ├── 02_data_types.png
    ├── 03_target_distribution.png
    ├── 04_correlation_heatmap.png
    ├── 05_feature_distributions.png
    ├── 06_model_comparison.png
    ├── 07_feature_importance.png
    ├── 08_confusion_matrix.png (or regression_metrics.png)
    └── 09_predictions.png
```

## 🛠️ Customization

You can easily customize the agent by modifying:

- **Models**: Add/remove models in `automl_engine.py`
- **Feature Engineering**: Add custom features in `feature_engineer.py`
- **Visualizations**: Add new plots in `visualizer.py`
- **Report Sections**: Customize PDF in `report_generator.py`
- **Cleaning Rules**: Adjust thresholds in `data_cleaner.py`

## 📝 Example Output

```
🤖 Autonomous Data Science Agent Starting...
============================================================

📂 Step 1: Loading Data...
   Loaded with encoding: utf-8
✅ Loaded 1000 rows, 15 columns

🎯 Auto-detecting target column...
✅ Target column detected: price

🧹 Step 2: Cleaning Data...
   Removed 5 duplicate rows
   Dropped 2 useless columns: ['id', 'timestamp']
✅ Data cleaned successfully

⚙️ Step 3: Engineering Features...
   Selected 35 best features out of 87
✅ Features engineered: 35 total features

🤖 Step 4: Running AutoML (Finding Best Model)...
   Task type: Regression
   Training samples: 800, Test samples: 200
   Training Random Forest... R² Score: 0.8523
   Training Gradient Boosting... R² Score: 0.8712
   Training Linear Regression... R² Score: 0.7845
   ...
✅ Best Model: Gradient Boosting
   Score: 0.8712

📊 Step 5: Generating Visualizations...
   Generated 9 visualizations
✅ Visualizations saved to output/visualizations

📄 Step 6: Generating PDF Report...
✅ Report saved to output/data_science_report_20241106_174530.pdf

============================================================
🎉 Autonomous Data Science Pipeline Completed!
📁 All outputs saved to: output
============================================================
```

## 🤝 Contributing

Feel free to enhance this agent! Some ideas:
- Add deep learning models
- Support for time series data
- Automated hyperparameter tuning
- Interactive HTML reports
- API endpoint deployment

## 📄 License

MIT License - Feel free to use and modify!

## 🎓 Learn More

This agent demonstrates:
- End-to-end ML pipeline automation
- Best practices in data cleaning
- Feature engineering techniques
- Model selection strategies
- Professional reporting

Perfect for learning or as a starting point for your own data science projects!

---

**Made with ❤️ for the Data Science Community**

*Bilkul AI Data Scientist jaisa!* 🚀
