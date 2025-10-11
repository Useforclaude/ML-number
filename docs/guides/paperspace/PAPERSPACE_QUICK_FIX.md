# 🚨 Paperspace Quick Fix Guide

## Error 1: No module named 'torch' (MOST COMMON!)

**Problem:**
```
ERROR - Import error: No module named 'torch'
2025-10-11 11:57:01,056 - ERROR - Make sure virtual environment is activated: source .venv/bin/activate
```

**Cause:** PyTorch not installed in virtual environment

**Solution (REQUIRED - ต้องทำครั้งแรก!):**
```bash
cd /notebooks/ML-number
source .venv/bin/activate

# Install PyTorch (CPU version for Paperspace)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Verify installation
python -c "import torch; print(f'✅ PyTorch {torch.__version__} installed')"

# Expected output:
# ✅ PyTorch 2.x.x installed
```

**Why needed:** Training scripts use PyTorch to detect GPU availability

**Note:** ต้องทำครั้งเดียวตอนแรก! Session ถัดไปไม่ต้องติดตั้งอีก

---

## Error 2: IndentationError in Python -c

**Problem:**
```bash
python -c "
  from src.data_handler import load_and_clean_data  # ← Extra spaces!
IndentationError: unexpected indent
```

**Solution - Single Line (Recommended):**
```bash
python -c "from src.data_handler import load_and_clean_data; df_raw, df_cleaned = load_and_clean_data(filter_outliers_param=True, max_price=100000); print(f'✅ Data loaded: raw={len(df_raw)} rows, cleaned={len(df_cleaned)} rows')"
```

**Solution - Multi-line (No Indent!):**
```bash
python -c "
from src.data_handler import load_and_clean_data
df_raw, df_cleaned = load_and_clean_data(filter_outliers_param=True, max_price=100000)
print(f'✅ Data loaded: raw={len(df_raw)} rows, cleaned={len(df_cleaned)} rows')
"
```

**Key:** NO spaces/tabs before each line!

---

## Error 2: No module named 'torch'

**Problem:**
```
ModuleNotFoundError: No module named 'torch'
```

**Check if PyTorch is needed:**
```bash
cd /notebooks/ML-number
source .venv/bin/activate
grep -r "import torch" src/
grep -r "import torch" training/
```

**If PyTorch IS needed:**
```bash
# Install PyTorch (CPU version - for Paperspace M4000)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Or check requirements.txt
pip install -r requirements.txt --upgrade
```

**If PyTorch NOT needed:**
- Comment out torch imports in code
- Or fix the import error

---

## ✅ Correct Workflow (Copy-Paste)

### **Step 1: Activate Virtual Environment**
```bash
cd /notebooks/ML-number
source .venv/bin/activate
```

### **Step 2: Verify Data File**
```bash
ls -lh data/raw/numberdata.csv
# Expected: ~93 KB
```

### **Step 3: Test Data Loading (Single Line)**
```bash
python -c "from src.data_handler import load_and_clean_data; df_raw, df_cleaned = load_and_clean_data(filter_outliers_param=True, max_price=100000); print(f'✅ Data loaded: raw={len(df_raw)} rows, cleaned={len(df_cleaned)} rows')"
```

**Expected Output:**
```
✅ Data loaded: raw=6112 rows, cleaned=6100 rows
```

### **Step 4: Start Training (SEQUENTIAL - Not Parallel!)**
```bash
# SESSION 1: Fast Models (~5h)
echo "=== Starting XGBoost ==="
python training/modular/train_xgboost_only.py 2>&1 | tee logs/xgb.log

echo "=== Starting CatBoost ==="
python training/modular/train_catboost_only.py 2>&1 | tee logs/cat.log

echo "=== Starting RandomForest ==="
python training/modular/train_rf_only.py 2>&1 | tee logs/rf.log

echo "✅ SESSION 1 COMPLETE!"
ls -lh models/checkpoints/
```

---

## 🔍 Debugging Commands

### **Check Virtual Environment:**
```bash
which python
# Expected: /notebooks/ML-number/.venv/bin/python

pip list | grep -E "xgboost|lightgbm|catboost|scikit-learn"
# Should show all ML packages
```

### **Check Data File:**
```bash
ls -lh data/raw/numberdata.csv
wc -l data/raw/numberdata.csv
# Expected: ~6112 lines + header
```

### **Check Imports:**
```bash
python -c "import xgboost; print('XGBoost OK')"
python -c "import lightgbm; print('LightGBM OK')"
python -c "import catboost; print('CatBoost OK')"
python -c "import sklearn; print('Sklearn OK')"
python -c "from src.config import CONFIG; print('Config OK')"
```

### **Monitor Training:**
```bash
# Watch log file
tail -f logs/xgb.log

# Check data loading
grep "Data loaded" logs/*.log

# Check for errors
grep -i "error" logs/*.log
```

---

## 🎯 Common Mistakes

| ❌ Mistake | ✅ Solution |
|-----------|------------|
| Forgot to activate venv | `source .venv/bin/activate` |
| Python -c with indent | No spaces before each line! |
| Run in parallel (6h limit!) | Run sequentially (one by one) |
| Data file not uploaded | Upload `numberdata.csv` first |
| Wrong working directory | `cd /notebooks/ML-number` |

---

**Created**: 2025-10-11
**Purpose**: Fix common Paperspace errors
**Status**: Ready to use
