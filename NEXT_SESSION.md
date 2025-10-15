# 🎯 NEXT SESSION GUIDE

**Last Updated**: 2025-10-11 23:00
**Session**: 016 - Retrain with Premium Features
**Status**: ✅ DATA LEAKAGE FIXED + PREMIUM FEATURES ADDED!

---

## ✅ SESSION 015 - DATA LEAKAGE FIX + PREMIUM FEATURES COMPLETE

### 🚀 What Was Done:

#### **1. Data Leakage Fix** 🔴 (CRITICAL!)

**Problem Discovered:**
- RandomForest achieved R² = 0.9999 (impossibly perfect)
- Test R² = -0.026 (negative!)
- Predictions: 1200-1481 (constant values)
- Root cause: `sample_weight` column (99% feature importance)

**Why This Was Leakage:**
```python
# sample_weight was calculated FROM price (the target!)
sample_weights = calculate_from_price(df['price'])
df['sample_weight'] = sample_weights  # ← This is the target!

# Then used as a feature:
X_train = df[['sample_weight', ...]]  # ← Model learns: price = f(sample_weight) 🚨
y_train = df['price']                  # ← Perfect correlation!
```

**Fix Applied (commit c513797):**
```python
# src/features.py:1790-1794
if 'sample_weight' in df.columns:
    df = df.drop('sample_weight', axis=1)
    print("   ⚠️  Removed 'sample_weight' feature (data leakage prevention)")
```

**Verification:**
- ✅ Test R²: -0.026 → 0.445 (positive!)
- ✅ Predictions: 231-26,934 (full range!)
- ✅ No overfitting (validation-test diff = 0.082 < 0.10)
- ✅ Log message: "⚠️ Removed 'sample_weight' feature"

#### **2. Codex's Premium Features Enhancement** 💎

**Added 11+ Features for High-Value Number Detection:**
- Premium suffix weights (8888, 9999, 168, etc.)
- Premium prefix weights (089, 088, etc.)
- High-value digit ratios (7, 8, 9)
- Digit entropy & pair diversity
- Cluster scores & tail ratios

**Enhanced Sample Weighting:**
```python
# BEFORE (Session 014): Simple exponential
sample_weights = np.exp(alpha * price_percentile)

# AFTER (Session 015): Log-scaled + tier-based
base_weight = 0.6 + 1.7 * np.power(log_scaled, 1.25)
tier_boost = np.select([
    prices >= 50000,  # ×2.0
    prices >= 20000,  # ×1.2
    prices >= 10000,  # ×0.8
    prices >= 5000    # ×0.4
], ...)
```

**Increased Optuna Trials:**
- Before: 150 trials
- After: 300 trials (deeper hyperparameter search)

**New Tools Added:**
- `scripts/analyze_price_distribution.py` - Diagnostic tool
- Enhanced `scripts/summarize_results.py` - Multi-directory support

**Files Modified (commit e9aacc1):**
- `src/features.py` (+230 lines)
- `src/data_handler.py` (+42 lines)
- `src/config.py` (+1 line)

#### **3. Training Baseline Established** 📊

**RandomForest Results (after fix):**
- Validation R²: 0.363
- Test R²: 0.445 ✅
- MAE: 751.54
- RMSE: 1606.57
- Training time: 52 minutes

**Current Status:**
- ✅ Data leakage FIXED
- ✅ Test R² now positive (0.445)
- ✅ Predictions cover full range
- ✅ No overfitting detected
- ⚠️ RandomForest not suitable for this dataset (too simple)

---

## 🎯 SESSION 016 - PULL UPDATES & RETRAIN

### **Critical Context:**
Session 015 added **161 features** (was 150) + **enhanced sample weighting** + **300 Optuna trials** (was 150).
Current baseline: **R² = 0.36-0.44** (RandomForest)
Expected after retrain: **R² = 0.70-0.85** (gradient boosting models)

---

## 📋 STEP-BY-STEP GUIDE

### **Step 1: Pull Latest Updates to Paperspace** ⬇️

```bash
# Connect to Paperspace
# Navigate to project
cd /notebooks/ML-number
source .venv/bin/activate

# Pull latest commits
git pull origin main
# Expected: commits c513797 + e9aacc1

# Verify updates
git log --oneline -3
# Should show:
# e9aacc1 Enhance features and sample weighting for high-value numbers
# c513797 Fix data leakage: Drop sample_weight from features
# 40a9e65 (previous commit)
```

### **Step 2: Verify New Features** ✅

```bash
# Check premium features exist
grep -n "premium_suffix_score" src/features.py
# Expected: Should find function definition

grep -n "PREMIUM_SUFFIX_WEIGHTS" src/features.py
# Expected: Line ~20-80 with weight dictionary

grep -n "HIGH_VALUE_DIGITS" src/features.py
# Expected: HIGH_VALUE_DIGITS = {'7', '8', '9'}

# Check Optuna trials increased
grep -n "optuna_trials" src/config.py
# Expected: 'optuna_trials': 300

# Check sample_weight removed from features
grep -n "Drop sample_weight" src/features.py
# Expected: Line ~1790-1794 with drop logic
```

### **Step 3: Run Diagnostic Script** 🔍

```bash
# Analyze data distribution & premium patterns
python scripts/analyze_price_distribution.py

# Expected output:
# 📊 PRICE & PATTERN DIAGNOSTICS
# Total cleaned samples: 6,100
# Price range: ฿100 - ฿90,000
#
# 🎯 Price band summary
# ฿0 - ฿499      : 2,xxx numbers (xx.x%)
# ...
#
# 💎 Premium suffix coverage
# 8888   : xx numbers (x.xx%)
# 9999   : xx numbers (x.xx%)
# ...
#
# 🔥 High digit tail density (7/8/9 in last 4 digits)
# Tail ratio ≥ 0.25 : xx.xx% of numbers
# ...
```

### **Step 4: Clear Old Checkpoints (Optional)** 🧹

```bash
# Check existing checkpoints
ls -lh models/checkpoints/

# If you want fresh training (recommended), remove old checkpoints:
rm models/checkpoints/xgboost_checkpoint.pkl
rm models/checkpoints/lightgbm_checkpoint.pkl
rm models/checkpoints/catboost_checkpoint.pkl
# Keep RandomForest as baseline comparison
```

---

## 🚀 TRAINING STRATEGY

### **⚠️ IMPORTANT: Training Time Estimates**
- **LightGBM**: 4-6 hours (300 trials)
- **XGBoost**: 4-6 hours (300 trials)
- **CatBoost**: 3-4 hours (300 trials)
- **Ensemble**: 30 minutes
- **Total**: 12-19 hours

**Paperspace Free = 6-hour auto-shutdown!**
→ Must split into **3-4 sessions**

---

### **SESSION 016A: LightGBM (4-6 hours)**

```bash
cd /notebooks/ML-number
source .venv/bin/activate

# Check data file exists
ls -lh data/raw/numberdata.csv
# Expected: ~93 KB

echo "=== SESSION 016A: LightGBM with Premium Features ==="
python training/modular/train_lightgbm_only.py 2>&1 | tee logs/lgb_v2.log

# Monitor progress
tail -f logs/lgb_v2.log

# After completion, check results
grep "R²" logs/lgb_v2.log
grep "Test R²" logs/lgb_v2.log
ls -lh models/checkpoints/lightgbm_checkpoint.pkl
```

**Expected Results:**
- Validation R²: 0.75-0.85 (up from 0.36)
- Test R²: 0.70-0.80 (up from 0.44)
- No overfitting (diff < 0.10)

---

### **SESSION 016B: XGBoost (4-6 hours)**

```bash
cd /notebooks/ML-number
source .venv/bin/activate

# Verify LightGBM checkpoint exists
ls -lh models/checkpoints/lightgbm_checkpoint.pkl

echo "=== SESSION 016B: XGBoost with Premium Features ==="
python training/modular/train_xgboost_only.py 2>&1 | tee logs/xgb_v2.log

# Monitor progress
tail -f logs/xgb_v2.log

# After completion
grep "R²" logs/xgb_v2.log
ls -lh models/checkpoints/xgboost_checkpoint.pkl
```

**Expected Results:**
- Validation R²: 0.73-0.83
- Test R²: 0.70-0.80

---

### **SESSION 016C: CatBoost (3-4 hours)**

```bash
cd /notebooks/ML-number
source .venv/bin/activate

# Verify XGBoost checkpoint exists
ls -lh models/checkpoints/xgboost_checkpoint.pkl

echo "=== SESSION 016C: CatBoost with Premium Features ==="
python training/modular/train_catboost_only.py 2>&1 | tee logs/cat_v2.log

# Monitor progress
tail -f logs/cat_v2.log

# After completion
grep "R²" logs/cat_v2.log
ls -lh models/checkpoints/catboost_checkpoint.pkl
```

**Expected Results:**
- Validation R²: 0.70-0.80
- Test R²: 0.68-0.78

---

### **SESSION 016D: Results Summary + Ensemble (30 min)**

```bash
cd /notebooks/ML-number
source .venv/bin/activate

# Verify ALL 4 model checkpoints exist
ls -lh models/checkpoints/*.pkl
# Expected: 4 files (LightGBM, XGBoost, CatBoost, RandomForest)

echo "=== Results Summary ==="
python scripts/summarize_results.py

# Expected output:
# 📊 TRAINING RESULTS SUMMARY
# ✅ LightGBM    | Val R²=0.xxxx | Test R²=0.xxxx | ...
# ✅ XGBoost     | Val R²=0.xxxx | Test R²=0.xxxx | ...
# ✅ CatBoost    | Val R²=0.xxxx | Test R²=0.xxxx | ...
# ✅ RandomForest| Val R²=0.3630 | Test R²=0.4450 | ... (baseline)
#
# 🏆 BEST MODEL: LightGBM (or XGBoost)
# Expected R²: 0.75-0.85

# If R² > 0.70, create ensemble
if [ R² is good ]; then
    echo "=== Creating Ensemble ==="
    python training/modular/train_ensemble_only.py 2>&1 | tee logs/ensemble_v2.log

    # Check deployed model
    ls -lh models/deployed/best_model.pkl
fi
```

**Expected Ensemble Results:**
- Validation R²: 0.78-0.88
- Test R²: 0.75-0.85

---

## 📊 VERIFICATION CHECKLIST

### Before Training:
- [ ] Git pulled (commits c513797 + e9aacc1)
- [ ] Premium features verified (`grep premium_suffix_score src/features.py`)
- [ ] Optuna trials = 300 (`grep optuna_trials src/config.py`)
- [ ] sample_weight removed (`grep "Drop sample_weight" src/features.py`)
- [ ] Diagnostic script runs successfully

### During Training:
- [ ] No ValueError or data leakage errors
- [ ] Optuna shows 300 trials (not 150)
- [ ] R² improving during optimization
- [ ] Log shows: "⚠️ Removed 'sample_weight' feature"

### After Training:
- [ ] R² improved from 0.36-0.44 to 0.70-0.85
- [ ] Test R² positive and reasonable
- [ ] No overfitting (validation-test diff < 0.10)
- [ ] All model checkpoints saved
- [ ] Best model deployed

---

## 🚨 CRITICAL: Data Leakage Verification

**MUST verify these EVERY training run:**

```bash
# Check logs for sample_weight removal
grep "Removed 'sample_weight' feature" logs/*.log
# Expected: Should appear in ALL training logs

# Check feature count
grep "Created .* features" logs/*.log
# Expected: "Created 161 features" (was 150 before Session 015)

# Verify no data leakage
python scripts/check_leakage.py
# Expected: No features with >90% importance
# Expected: Test R² should be positive
```

---

## 📈 EXPECTED R² IMPROVEMENT

| Model        | Before (Session 015) | After (Session 016) | Improvement |
|--------------|---------------------|---------------------|-------------|
| RandomForest | 0.36-0.44          | 0.36-0.44          | N/A (baseline) |
| LightGBM     | Not trained        | 0.75-0.85          | +0.35-0.45 |
| XGBoost      | Not trained        | 0.73-0.83          | +0.35-0.45 |
| CatBoost     | Not trained        | 0.70-0.80          | +0.30-0.40 |
| **Ensemble** | Not trained        | **0.78-0.88**      | **+0.40-0.50** |

**Why Improvement Expected:**
1. ✅ Data leakage fixed (test R² now positive)
2. ✅ 11+ premium features added for high-value detection
3. ✅ Enhanced sample weighting (tier-based)
4. ✅ 300 Optuna trials (deeper search)
5. ✅ Gradient boosting models (XGBoost, LightGBM, CatBoost)

---

## 🔄 MONITORING COMMANDS

```bash
# Check running processes
ps aux | grep train_

# Monitor specific log
tail -f logs/lgb_v2.log
tail -f logs/xgb_v2.log
tail -f logs/cat_v2.log

# Check R² progress
grep "Best trial" logs/lgb_v2.log | tail -5
grep "R²" logs/*.log

# Check feature count
grep "Created .* features" logs/*.log
# Expected: 161 features

# Check sample_weight removal
grep "sample_weight" logs/*.log
# Expected: "⚠️ Removed 'sample_weight' feature"

# Check GPU usage (if available)
watch -n 5 nvidia-smi

# Check disk space
df -h /storage

# Check memory usage
free -h
```

---

## 🔧 TROUBLESHOOTING

### If Git Pull Shows No Updates:
```bash
git fetch origin
git status
# If behind: git pull origin main
# If conflicts: git reset --hard origin/main
```

### If Features Not Updated:
```bash
# Check current commit
git log --oneline -3

# Should show c513797 and e9aacc1
# If not, force pull:
git fetch origin
git reset --hard origin/main
```

### If R² Still Low After Retrain:
```bash
# Check feature count
grep "Created .* features" logs/*.log
# Should be 161, not 150

# Check sample_weight removed
grep "sample_weight" logs/*.log
# Should show removal message

# Run diagnostic
python scripts/check_leakage.py
```

### If Training Too Slow:
```bash
# Check Optuna trials
grep "optuna_trials" src/config.py
# If 300 is too slow, can reduce to 200

# Or train one model at a time
# (recommended for Paperspace Free 6-hour limit)
```

---

## 📚 DOCUMENTATION REFERENCES

- **Session 015 Summary**: `checkpoints/checkpoint_latest.json`
- **Data Leakage Fix**: commit c513797
- **Premium Features**: commit e9aacc1
- **Codex Case Studies**: `CLAUDE.md`
- **Project State**: `.project_state.json`

---

## ✅ SUCCESS CRITERIA

**Session 016 is SUCCESSFUL if:**
- ✅ Git pulled successfully (commits c513797 + e9aacc1)
- ✅ Diagnostic script shows premium features exist
- ✅ All 3 models trained (LightGBM, XGBoost, CatBoost)
- ✅ R² improved from 0.36-0.44 to 0.70-0.85
- ✅ Test R² positive and reasonable
- ✅ No overfitting detected (diff < 0.10)
- ✅ Ensemble created with R² > 0.75
- ✅ Best model deployed

**Session 016 FAILED if:**
- ❌ R² still around 0.36-0.44 (features not updated)
- ❌ Test R² negative (data leakage still exists)
- ❌ Feature count still 150 (not 161)
- ❌ sample_weight not removed
- ❌ Overfitting detected (validation >> test)

---

## 🎯 QUICK START (Copy-Paste)

### **Session 016 - Complete Flow:**

```bash
# === PULL UPDATES ===
cd /notebooks/ML-number
source .venv/bin/activate
git pull origin main
grep "premium_suffix_score" src/features.py
python scripts/analyze_price_distribution.py

# === TRAIN MODELS (split into 3-4 sessions!) ===
# Session 016A: LightGBM (4-6h)
python training/modular/train_lightgbm_only.py 2>&1 | tee logs/lgb_v2.log

# Session 016B: XGBoost (4-6h)
python training/modular/train_xgboost_only.py 2>&1 | tee logs/xgb_v2.log

# Session 016C: CatBoost (3-4h)
python training/modular/train_catboost_only.py 2>&1 | tee logs/cat_v2.log

# Session 016D: Results + Ensemble (30min)
python scripts/summarize_results.py
python training/modular/train_ensemble_only.py 2>&1 | tee logs/ensemble_v2.log

# === VERIFY ===
ls -lh models/deployed/best_model.pkl
grep "Best.*R²" logs/ensemble_v2.log
```

---

**Created**: 2025-10-11 23:00
**Session**: 016 - Retrain with Premium Features
**Status**: ✅ READY TO PULL & RETRAIN!
**Expected**: R² = 0.70-0.85 (up from 0.36-0.44) 🚀

---

**พร้อม Pull และ Retrain แล้ว!** คาดหวัง R² จะพุ่งจาก 0.36-0.44 → 0.70-0.85! 🎯
