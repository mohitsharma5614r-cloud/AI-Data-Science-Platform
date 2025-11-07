# 🔧 Installation Guide

## Prerequisites

- **Python 3.8 or higher** (recommended: Python 3.9+)
- **pip** (Python package installer)
- **Git** (optional, for cloning)

---

## Installation Methods

### Method 1: Quick Install (Recommended)

```bash
# Navigate to the project directory
cd autonomous_ds_agent

# Install all dependencies
pip install -r requirements.txt

# Verify installation
python -c "import pandas, sklearn, matplotlib, seaborn, reportlab; print('✅ All dependencies installed!')"
```

### Method 2: Virtual Environment (Best Practice)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify
python -c "import pandas, sklearn, matplotlib; print('✅ Ready to go!')"
```

### Method 3: Conda Environment

```bash
# Create conda environment
conda create -n ds_agent python=3.9

# Activate environment
conda activate ds_agent

# Install dependencies
pip install -r requirements.txt
```

---

## Dependency Details

The project requires these packages:

```
pandas>=1.5.0          # Data manipulation
numpy>=1.23.0          # Numerical computing
scipy>=1.9.0           # Scientific computing
scikit-learn>=1.2.0    # Machine learning
matplotlib>=3.6.0      # Plotting
seaborn>=0.12.0        # Statistical visualization
reportlab>=3.6.0       # PDF generation
openpyxl>=3.0.0        # Excel support
```

**Total size:** ~150-200 MB

---

## Verification

### Test Installation

```bash
# Run the quick demo
python quick_demo.py
```

This will:
1. Create sample datasets
2. Run the full pipeline
3. Generate reports

If successful, you'll see:
```
✨ DEMO COMPLETED!
📁 Check the following directories for results:
   • Classification: ...
   • Regression: ...
```

### Manual Test

```python
# Test individual components
python -c "
from data_loader import DataLoader
from data_cleaner import DataCleaner
from feature_engineer import FeatureEngineer
from automl_engine import AutoMLEngine
from visualizer import Visualizer
from report_generator import ReportGenerator
print('✅ All modules imported successfully!')
"
```

---

## Troubleshooting

### Issue: pip not found
```bash
# Install pip
python -m ensurepip --upgrade
```

### Issue: Permission denied
```bash
# Use --user flag
pip install --user -r requirements.txt
```

### Issue: Specific package fails
```bash
# Install packages one by one
pip install pandas
pip install numpy
pip install scikit-learn
pip install matplotlib
pip install seaborn
pip install reportlab
pip install scipy
pip install openpyxl
```

### Issue: Old Python version
```bash
# Check Python version
python --version

# If < 3.8, upgrade Python
# Download from: https://www.python.org/downloads/
```

### Issue: SSL Certificate error
```bash
# Use trusted host
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Issue: Slow installation
```bash
# Use a mirror (example: Aliyun mirror for China)
pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
```

---

## Platform-Specific Notes

### Windows

```bash
# Recommended: Use Anaconda
# Download from: https://www.anaconda.com/download

# Or use Windows Terminal with PowerShell
# Install dependencies
pip install -r requirements.txt
```

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.9

# Install dependencies
pip3 install -r requirements.txt
```

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip

# Install dependencies
pip3 install -r requirements.txt
```

---

## Optional Dependencies

### For Better Performance

```bash
# Install additional packages for speed
pip install numba  # JIT compilation
pip install joblib  # Parallel processing
```

### For Jupyter Notebook Support

```bash
pip install jupyter
pip install ipykernel

# Create kernel
python -m ipykernel install --user --name=ds_agent
```

---

## Upgrading

### Upgrade All Packages

```bash
pip install --upgrade -r requirements.txt
```

### Upgrade Specific Package

```bash
pip install --upgrade scikit-learn
```

---

## Uninstallation

### Remove Dependencies

```bash
pip uninstall -r requirements.txt -y
```

### Remove Virtual Environment

```bash
# Deactivate first
deactivate

# Remove directory
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows
```

---

## System Requirements

### Minimum Requirements
- **RAM:** 4 GB
- **Storage:** 500 MB free space
- **CPU:** Any modern processor

### Recommended Requirements
- **RAM:** 8 GB or more
- **Storage:** 2 GB free space
- **CPU:** Multi-core processor

### For Large Datasets (>100K rows)
- **RAM:** 16 GB or more
- **Storage:** 5 GB free space
- **CPU:** 4+ cores

---

## Quick Start After Installation

```bash
# 1. Create sample data
python create_sample_data.py

# 2. Run on sample data
python main.py sample_churn_data.csv --target churn

# 3. Check results
# Open: output/data_science_report_*.pdf
```

---

## Getting Help

If you encounter issues:

1. **Check Python version:** `python --version` (should be 3.8+)
2. **Update pip:** `pip install --upgrade pip`
3. **Clear cache:** `pip cache purge`
4. **Reinstall:** `pip install --force-reinstall -r requirements.txt`

---

## Success Checklist

- [ ] Python 3.8+ installed
- [ ] pip working
- [ ] All dependencies installed
- [ ] No import errors
- [ ] Demo runs successfully
- [ ] PDF report generated

---

**Installation complete! Ready to analyze data! 🚀**
