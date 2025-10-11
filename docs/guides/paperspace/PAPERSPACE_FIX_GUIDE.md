# 🔧 Paperspace Training Fix Guide

**Date**: 2025-10-06
**Issue**: GPU Conflict + Poor Model Performance
**Status**: Ready to Fix

---

## 🎯 ปัญหาที่เจอใน Paperspace:

1. ❌ `CatBoostError: device already requested 0`
2. ❌ XGBoost R² = -0.06 (แย่มาก)
3. ❌ LightGBM R² = -0.86 (แย่มาก)
4. ❌ Training เสร็จเร็วเกินไป (1.5 ชม. แทน 9-12 ชม.)

**สาเหตุ**: Code ใน Paperspace outdated - ไม่มี Session 011C และ 011D fixes

---

## ✅ Solution: Pull Latest Code from GitHub

### Step 1: Open Paperspace Terminal

ใน Paperspace Jupyter Notebook:
1. คลิก **"+"** (New Launcher)
2. เลือก **"Terminal"**

---

### Step 2: Pull Latest Fixes

รันคำสั่งนี้ใน Terminal:

```bash
# Navigate to project directory
cd /storage/ML-number

# Pull latest fixes from GitHub
git pull origin main

# Should see:
# Updating ef12477..28fe4c0
# Fast-forward
#  src/model_utils.py | 8 ++++----
#  src/evaluate.py    | 2 +-
#  ...
```

**Expected Output:**
```
From https://github.com/Useforclaude/ML-number
 * branch            main       -> FETCH_HEAD
Updating XXXXXXX..28fe4c0
Fast-forward
 src/model_utils.py              | 8 ++++----
 src/evaluate.py                 | 2 +-
 SESSION_011C_GPU_FIX.md         | 238 +++++++++++++++++++++++
 SESSION_011D_SKLEARN17_FIX.md   | 312 ++++++++++++++++++++++++++++
 NEXT_SESSION.md                 | 35 +++-
 ...
```

---

### Step 3: Verify Fixes Applied

รันคำสั่งเหล่านี้เพื่อยืนยัน:

```bash
# Check Session 011C fix (n_jobs=1)
echo "=== Checking GPU Conflict Fix (Session 011C) ==="
grep -n "n_jobs=1.*Prevent GPU" src/model_utils.py

# Expected output:
# 825:            n_jobs=1,  # Prevent GPU device conflict with CatBoost/XGBoost

# Check Session 011D fix (params)
echo ""
echo "=== Checking sklearn 1.7 Fix (Session 011D) ==="
grep -n "params={'sample_weight'" src/model_utils.py | head -3

# Expected output:
# 443:                params={'sample_weight': sample_weight},  # sklearn 1.7+
# 595:                params={'sample_weight': sample_weight},  # sklearn 1.7+
# 701:                params={'sample_weight': sample_weight},  # sklearn 1.7+

# Check git commits
echo ""
echo "=== Latest Git Commits ==="
git log --oneline -5

# Expected output:
# 28fe4c0 Add Session 011D documentation
# b626090 Session 011D: Fix scikit-learn 1.7 API
# 70189de Add SESSION_011C_GPU_FIX.md
# 07edf24 Update NEXT_SESSION.md
# ef12477 Session 011C: Fix CatBoost GPU conflict
```

---

### Step 4: Restart Jupyter Kernel

1. กลับไปที่ Jupyter Notebook tab
2. คลิก menu **"Kernel"**
3. เลือก **"Restart & Clear Output"**
4. คลิก **"Restart"** ยืนยัน

---

### Step 5: Re-run All Cells

**Cell 1: Install Libraries** (ถ้ามี)
```python
!pip install -q xgboost lightgbm catboost optuna
```

**Cell 2: Setup Environment**
```python
import sys
sys.path.insert(0, '/storage/ML-number')

from src.config import BASE_PATH
print(f"✅ BASE_PATH: {BASE_PATH}")
```

**Cell 3: Load Data & Features**
```python
# Your data loading code here
```

**Cell 4: Training**
```python
from src.train_production import train_production_pipeline

# IMPORTANT: Verify these parameters
print(f"🎯 optimize = True")
print(f"🎯 n_trials = 100")
print(f"🎯 use_gpu = True")

result = train_production_pipeline(
    X_train, y_train,
    X_test, y_test,
    optimize=True,        # ✅ Must be True
    n_trials=100,         # ✅ Must be 100 (not 0!)
    use_gpu=True,         # ✅ Use Paperspace GPU
    verbose=True
)
```

---

## 📊 Expected Results (After Fixes)

### Training Timeline:
```
⏱️  XGBoost optimization:    ~2.5 hours (100 trials)
⏱️  LightGBM optimization:   ~3.5 hours (100 trials)
⏱️  CatBoost optimization:   ~1.5 hours (100 trials)
⏱️  RandomForest optimization: ~1.0 hour (100 trials)
⏱️  Ensemble creation:       ~0.5 hours
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️  Total:                   ~9-12 hours
```

**⚠️ ถ้ารันเสร็จภายใน < 2 ชม. = optimization ไม่ทำงาน!**

---

### Model Performance:
```
Individual Models (with optimization):
✅ GradientBoosting:  R² > 0.90
✅ CatBoost:          R² > 0.88
✅ RandomForest:      R² > 0.85
✅ XGBoost:           R² > 0.87  (not -0.06!)
✅ LightGBM:          R² > 0.86  (not -0.86!)
✅ ExtraTrees:        R² > 0.82

Ensemble Models:
✅ Stacking Ensemble:  R² > 0.93  (best model)
✅ Voting Ensemble:    R² > 0.91
✅ Weighted Average:   R² > 0.90
```

---

### Optuna Progress (Must See This!):
```
================================================================================
⚪ Training XGBoost (GPU)
================================================================================
🎯 Target: Find best hyperparameters
🔢 Trials: 100
📊 Method: Optuna TPE Sampler + 10-Fold CV
⏱️  Started: 2025-10-06 21:30:00
================================================================================

[I 2025-10-06 21:30:01] Trial 0 complete. Value: 0.8523
[I 2025-10-06 21:30:15] Trial 1 complete. Value: 0.8612
[I 2025-10-06 21:30:29] Trial 2 complete. Value: 0.8701
...
[I 2025-10-06 23:15:42] Trial 99 complete. Value: 0.9234

✅ Best R²: 0.9234
⏱️  Time: 1.75 hours
```

**ถ้าไม่เห็น log นี้ = optimization ไม่รัน!**

---

## 🚨 Troubleshooting

### Issue 1: "Already up to date" แต่ code ยังเก่า

```bash
# Force pull
cd /storage/ML-number
git fetch origin
git reset --hard origin/main

# Verify again
git log --oneline -5
```

---

### Issue 2: Training ยังเร็วเกินไป (< 2 ชม.)

**Check 1: Verify n_trials in Cell 4**
```python
# MUST be 100, NOT 0
n_trials = 100
```

**Check 2: Check if optimize=True actually works**
```python
# Add debug print
print(f"DEBUG: optimize={optimize}, n_trials={n_trials}")

# Before calling train_production_pipeline
```

**Check 3: Check train_production.py**
```bash
# Verify optimize parameter is used
grep -n "if optimize:" src/train_production.py
```

---

### Issue 3: GPU Conflict ยังเกิด

```bash
# Verify n_jobs=1 fix exists
grep -n "n_jobs=1" src/model_utils.py src/train.py

# Should see:
# src/model_utils.py:825:            n_jobs=1,  # Prevent GPU device conflict
# src/train.py:338:voting_ensemble = VotingRegressor(voting_models, n_jobs=1)
```

---

### Issue 4: fit_params error ยังเกิด

```bash
# Verify params (not fit_params) is used
grep -n "fit_params" src/model_utils.py src/evaluate.py

# Should return: (no results)

# Check params is used instead
grep -n "params={'sample_weight'" src/model_utils.py

# Should see 4 results (XGBoost, LightGBM, CatBoost, RF)
```

---

## ✅ Success Checklist

- [ ] `git pull` เสร็จไม่มี error
- [ ] `grep n_jobs=1` เจอใน model_utils.py
- [ ] `grep params=` เจอใน model_utils.py และ evaluate.py
- [ ] `git log` แสดง commit 28fe4c0, b626090, ef12477
- [ ] Kernel restart สำเร็จ
- [ ] Optuna trials แสดงใน output (Trial 0, 1, 2, ...)
- [ ] Training ใช้เวลา 9-12 ชั่วโมง (ไม่ใช่ 1.5 ชม.)
- [ ] Individual model R² > 0.85
- [ ] Ensemble model R² > 0.90
- [ ] ไม่มี GPU conflict error
- [ ] ไม่มี fit_params error

---

## 📞 ถ้ายังมีปัญหา

1. แสดง output ของ `git pull`
2. แสดง output ของ `git log --oneline -5`
3. แสดง output ของ `grep n_jobs=1 src/model_utils.py`
4. แสดง training time และ R² results
5. Copy error traceback (ถ้ามี)

---

**Created**: 2025-10-06
**Fixes Required**: Session 011C (GPU) + Session 011D (sklearn 1.7)
**Expected Training Time**: 9-12 hours
**Expected Best R²**: > 0.93
