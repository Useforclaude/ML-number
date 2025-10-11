# 🎯 NEXT SESSION GUIDE

**Last Updated**: 2025-10-11 18:15
**Session**: 014 - Paperspace Deployment Complete
**Status**: ✅ READY FOR TRAINING!

---

## ✅ SESSION 014 - PAPERSPACE DEPLOYMENT COMPLETE

### 🚀 What Was Done:

1. **Git Push to GitHub** ✅
   - Commit: `40a9e65`
   - Session 013 documentation + project refactor
   - 76 files changed (+4,573 insertions, -244 deletions)

2. **Paperspace Setup** ✅
   - Path: `/notebooks/ML-number`
   - Git cloned from: https://github.com/Useforclaude/ML-number.git
   - Virtual environment created: `.venv`
   - All requirements installed ✅
   - Imports verified ✅
   - BASE_PATH detected: `/storage/number-ML` ✅

3. **Key Benefits** 🎯
   - **Persistent storage**: Files in `/notebooks/` won't be deleted when session expires (unlike Colab/Kaggle)
   - **All Codex fixes included**: Tuple unpacking bug fixed in all 6 training scripts
   - **Ready to train**: Just need to upload data file

---

## 📋 CRITICAL: Paperspace Environment Info (บันทึกไว้!)

```bash
# Paperspace Paths (MUST REMEMBER!)
PROJECT_PATH="/notebooks/ML-number"
BASE_PATH="/storage/number-ML"  # Auto-detected by config
VENV_PATH="/notebooks/ML-number/.venv"
LOGS_PATH="/notebooks/ML-number/logs"

# Key Feature: Persistent Storage ✅
# ไฟล์ที่ /notebooks/ ไม่โดนลบเมื่อ session หมดเวลา
# (ต่างจาก Colab/Kaggle ที่ลบทุกครั้ง!)

# Git Remote
GIT_REMOTE="https://github.com/Useforclaude/ML-number.git"
```

---

## 🎯 NEXT STEPS (Session 015)

### **Step 1: Upload Data File** ⬆️

**Option A: Web Upload (Easiest)**
```bash
# In Paperspace:
# 1. Click "Upload" button in file browser
# 2. Navigate to local: /home/u-and-an/projects/number-ML/data/raw/numberdata.csv
# 3. Upload to Paperspace: /notebooks/ML-number/data/raw/
# 4. Verify:
(.venv) root@xxx:/notebooks/ML-number# ls -lh data/raw/numberdata.csv
# Expected: ~93 KB file
```

**Option B: SCP Upload (Alternative)**
```bash
# From local machine:
scp /home/u-and-an/projects/number-ML/data/raw/numberdata.csv \
    root@paperspace:/notebooks/ML-number/data/raw/
```

### **Step 2: Install PyTorch (ครั้งแรกเท่านั้น!)** 🔧

```bash
cd /notebooks/ML-number
source .venv/bin/activate

# Install PyTorch (required for GPU detection)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Verify installation
python -c "import torch; print(f'✅ PyTorch {torch.__version__} installed')"
```

**Note**: ต้องทำครั้งเดียวตอนแรก! Session ถัดไปไม่ต้องติดตั้งอีก

### **Step 3: Verify Setup** ✅

```bash
# Activate venv
cd /notebooks/ML-number
source .venv/bin/activate

# Check data file exists
ls -lh data/raw/numberdata.csv
# Expected: ~93 KB, 6,112 rows

# Test data loading (CRITICAL!)
python -c "
from src.data_handler import load_and_clean_data
df_raw, df_cleaned = load_and_clean_data(filter_outliers_param=True, max_price=100000)
print(f'✅ Data loaded: raw={len(df_raw)} rows, cleaned={len(df_cleaned)} rows')
"
# Expected output: "✅ Data loaded: raw=6112 rows, cleaned=6100 rows"
```

### **Step 3: Start Training** 🚀

**⚠️ IMPORTANT: Paperspace Free = 6-hour auto-shutdown!**
- Must run **sequentially** (one by one), NOT parallel
- Split into 3 sessions to avoid timeout
- See: `docs/guides/paperspace/PAPERSPACE_6HR_TRAINING_STRATEGY.md`

#### **SESSION 1: Fast Models (~5 hours)**
```bash
cd /notebooks/ML-number
source .venv/bin/activate

# Run ONE by ONE (sequential, not parallel!)
echo "=== SESSION 1: Fast Models ==="

# Step 1: XGBoost (2-3h)
python training/modular/train_xgboost_only.py 2>&1 | tee logs/xgb.log

# Step 2: CatBoost (1-2h)
python training/modular/train_catboost_only.py 2>&1 | tee logs/cat.log

# Step 3: RandomForest (1h)
python training/modular/train_rf_only.py 2>&1 | tee logs/rf.log

echo "✅ SESSION 1 COMPLETE!"
ls -lh models/checkpoints/
```

**Verify Data Loading (CRITICAL!):**
```bash
grep "Data loaded" logs/*.log
# Expected: "✅ Data loaded: raw=6112 rows, cleaned=6100 rows"
```

#### **SESSION 2: Slow Model (~4 hours)**
```bash
cd /notebooks/ML-number
source .venv/bin/activate

# Verify Session 1 checkpoints
ls -lh models/checkpoints/xgboost_checkpoint.pkl
ls -lh models/checkpoints/catboost_checkpoint.pkl
ls -lh models/checkpoints/random_forest_checkpoint.pkl

echo "=== SESSION 2: Slow Model ==="

# LightGBM (3-4h - longest model)
python training/modular/train_lightgbm_only.py 2>&1 | tee logs/lgb.log

echo "✅ SESSION 2 COMPLETE!"
ls -lh models/checkpoints/
```

#### **SESSION 3: Ensemble (~30 minutes)**
```bash
cd /notebooks/ML-number
source .venv/bin/activate

# Verify ALL 4 checkpoints exist
ls -lh models/checkpoints/*.pkl
# Should show 4 files

echo "=== SESSION 3: Ensemble ==="

# Create ensemble (15-30 min)
python training/modular/train_ensemble_only.py 2>&1 | tee logs/ensemble.log

echo "✅ ALL TRAINING COMPLETE!"
ls -lh models/deployed/best_model.pkl
```

### **Step 4: Monitor Training** 👀

```bash
# Check running processes
ps aux | grep train_

# Monitor logs
tail -f logs/xgb.log       # XGBoost progress
tail -f logs/lgb.log       # LightGBM progress
tail -f logs/cat.log       # CatBoost progress
tail -f logs/rf.log        # RandomForest progress

# Check GPU usage (if available)
watch -n 5 nvidia-smi

# Check data loading confirmation (VERIFY CODEX FIX!)
grep "Data loaded" logs/*.log
# MUST show: raw=6112, cleaned=6100
```

### **Step 5: After Training Complete** ✅

```bash
# Check R² scores
grep "R²" logs/*.log
grep "Test R²" logs/*.log

# Expected Results (after Codex fix):
# XGBoost:     R² ~0.88-0.92 ✅
# LightGBM:    R² ~0.86-0.90 ✅
# CatBoost:    R² ~0.85-0.89 ✅
# RandomForest: R² ~0.82-0.86 ✅

# Check checkpoints saved
ls -lh models/checkpoints/
# Expected: xgboost_checkpoint.pkl, lightgbm_checkpoint.pkl, etc.

# Run ensemble (final step)
python training/modular/train_ensemble_only.py

# Check deployed model
ls -lh models/deployed/best_model.pkl
# Expected: Best model from ensemble
```

---

## 📊 Expected Timeline

```
XGBoost:     2-3 hours  → checkpoint saved
LightGBM:    3-4 hours  → checkpoint saved
CatBoost:    1-2 hours  → checkpoint saved
RandomForest: 1 hour    → checkpoint saved
Ensemble:    15-30 min  → best model deployed
────────────────────────────────────────────
Total:       8-11 hours (can run in parallel!)
```

---

## 🔍 Verification Checklist

### Before Training:
- [x] Code pushed to GitHub (commit 40a9e65) ✅
- [x] Code cloned to Paperspace ✅
- [x] Virtual environment created ✅
- [x] Requirements installed ✅
- [x] Imports verified ✅
- [x] BASE_PATH detected (/storage/number-ML) ✅
- [x] Logs directory created ✅
- [ ] Data file uploaded to Paperspace
- [ ] Data loading tested (verify raw=6112, cleaned=6100)

### During Training:
- [ ] Logs show: "✅ Data loaded: raw=6112 rows, cleaned=6100 rows" (confirms Codex fix!)
- [ ] No ValueError or TypeError
- [ ] GPU active (if available)
- [ ] Checkpoints saving to models/checkpoints/
- [ ] R² improving during optimization

### After Training:
- [ ] All 4 model checkpoints saved
- [ ] R² scores logged and ≥ 0.85
- [ ] Ensemble created successfully
- [ ] Best model deployed to models/deployed/
- [ ] Can download trained models

---

## 🚨 CRITICAL: Data Loading Verification

**WHY THIS IS CRITICAL:**

Session 013 fixed a bug where training scripts would crash or use wrong data format:

```python
# ❌ BEFORE (Bug - Session 012):
df_cleaned = load_and_clean_data(filter_outliers_param=True, max_price=100000)
# Result: df_cleaned = tuple (df_raw, df_cleaned) ← WRONG!
# Impact: Training fails OR uses unfiltered data (R² = 0.4)

# ✅ AFTER (Fixed - Session 013 by Codex):
df_raw, df_cleaned = load_and_clean_data(filter_outliers_param=True, max_price=100000)
logger.info(f"✅ Data loaded: raw={len(df_raw)} rows, cleaned={len(df_cleaned)} rows")
# Result: df_cleaned = DataFrame with filtered data ← CORRECT!
# Impact: Training succeeds with R² = 0.85-0.92 ✅
```

**VERIFICATION COMMAND (Run this FIRST!):**
```bash
grep "Data loaded" logs/*.log
# MUST see: "✅ Data loaded: raw=6112 rows, cleaned=6100 rows"
# If you see this, Codex fix is working! ✅
# If you DON'T see this, STOP and debug!
```

---

## 🎯 Success Criteria

**Training is SUCCESSFUL if:**
- ✅ Logs show: `raw=6112 rows, cleaned=6100 rows` (confirms Codex fix works!)
- ✅ No ValueError or TypeError during execution
- ✅ All 4 model checkpoints saved to models/checkpoints/
- ✅ R² score ≥ 0.85 (target: 0.90+)
- ✅ Best model deployed to models/deployed/best_model.pkl

**Training FAILED if:**
- ❌ ValueError: "too many values to unpack" (Codex fix not applied)
- ❌ R² still around 0.4 (using unfiltered data - bug not fixed)
- ❌ Missing checkpoints or process crashes
- ❌ Import errors or dependency issues

---

## 🔄 Recovery Commands (If Needed)

### If Git Pull Needed:
```bash
cd /notebooks/ML-number
git fetch origin
git reset --hard origin/main
```

### If Imports Fail:
```bash
cd /notebooks/ML-number
source .venv/bin/activate
pip install -r requirements.txt --upgrade
```

### If Training Crashes:
```bash
# Check which checkpoint exists
ls -lh models/checkpoints/

# Resume from next model
# Example: If XGBoost done, continue with LightGBM
nohup python training/modular/train_lightgbm_only.py > logs/lgb.log 2>&1 &
```

### If Data File Missing:
```bash
# Re-upload from local
scp /home/u-and-an/projects/number-ML/data/raw/numberdata.csv \
    root@paperspace:/notebooks/ML-number/data/raw/
```

---

## 📚 Monitoring Commands Reference

```bash
# Check running processes
ps aux | grep train_

# Monitor specific log
tail -f logs/xgb.log

# Check all logs for errors
grep -i "error" logs/*.log

# Check data loading (CRITICAL!)
grep "Data loaded" logs/*.log

# Check R² progress
grep "R²" logs/*.log

# Check GPU usage
watch -n 5 nvidia-smi

# Check disk space
df -h /storage

# Check memory usage
free -h

# Check checkpoints
ls -lh models/checkpoints/

# Check deployed model
ls -lh models/deployed/
```

---

## 📝 Key Files & Paths (Paperspace)

### Project Structure:
```
/notebooks/ML-number/
├── training/modular/          # Training scripts (5 files)
│   ├── train_xgboost_only.py
│   ├── train_lightgbm_only.py
│   ├── train_catboost_only.py
│   ├── train_rf_only.py
│   └── train_ensemble_only.py
├── data/raw/                  # Data files
│   └── numberdata.csv         # Upload this!
├── models/
│   ├── checkpoints/           # Model checkpoints
│   └── deployed/              # Best model
├── logs/                      # Training logs
├── src/                       # Core code
├── .venv/                     # Virtual environment (persistent!)
└── requirements.txt
```

### Important Paths:
- **Project**: `/notebooks/ML-number`
- **Data**: `/notebooks/ML-number/data/raw/numberdata.csv`
- **Venv**: `/notebooks/ML-number/.venv`
- **Logs**: `/notebooks/ML-number/logs/`
- **Checkpoints**: `/notebooks/ML-number/models/checkpoints/`
- **Deployed**: `/notebooks/ML-number/models/deployed/`

---

## 🎯 Session 015 Quick Start (Copy-Paste)

### **⚠️ IMPORTANT: Paperspace = 6-hour limit!**
Run sequentially, split into 3 sessions:

#### **SESSION 1 (Copy-Paste - 5 hours):**
```bash
# === SESSION 015A: FAST MODELS ===
cd /notebooks/ML-number
source .venv/bin/activate

# Verify data file
ls -lh data/raw/numberdata.csv

# Test data loading (CRITICAL!)
python -c "
from src.data_handler import load_and_clean_data
df_raw, df_cleaned = load_and_clean_data(filter_outliers_param=True, max_price=100000)
print(f'✅ Data loaded: raw={len(df_raw)} rows, cleaned={len(df_cleaned)} rows')
"
# Expected: raw=6112, cleaned=6100

# Run SEQUENTIALLY (NOT parallel!)
echo "=== SESSION 1: Fast Models (5h) ==="

python training/modular/train_xgboost_only.py 2>&1 | tee logs/xgb.log
python training/modular/train_catboost_only.py 2>&1 | tee logs/cat.log
python training/modular/train_rf_only.py 2>&1 | tee logs/rf.log

echo "✅ SESSION 1 DONE!"
grep "Data loaded" logs/*.log
ls -lh models/checkpoints/
```

#### **SESSION 2 (Copy-Paste - 4 hours):**
```bash
# === SESSION 015B: SLOW MODEL ===
cd /notebooks/ML-number
source .venv/bin/activate

# Verify Session 1 checkpoints
ls -lh models/checkpoints/*.pkl

echo "=== SESSION 2: Slow Model (4h) ==="
python training/modular/train_lightgbm_only.py 2>&1 | tee logs/lgb.log

echo "✅ SESSION 2 DONE!"
ls -lh models/checkpoints/
```

#### **SESSION 3 (Copy-Paste - 30 min):**
```bash
# === SESSION 015C: ENSEMBLE ===
cd /notebooks/ML-number
source .venv/bin/activate

# Verify ALL 4 checkpoints
ls -lh models/checkpoints/*.pkl

echo "=== SESSION 3: Ensemble (30min) ==="
python training/modular/train_ensemble_only.py 2>&1 | tee logs/ensemble.log

echo "✅ ALL TRAINING COMPLETE!"
ls -lh models/deployed/best_model.pkl
grep "Best.*R²" logs/ensemble.log
```

---

## 📊 Documentation References

- **Session 013 Fix**: `docs/sessions/SESSION_013_FIX.md` (if exists)
- **Codex Methodology**: `CLAUDE.md` (Case Study #5)
- **Paperspace Guide**: `docs/guides/paperspace/PAPERSPACE_START_FROM_ZERO.md`
- **Modular Training**: `docs/guides/paperspace/PAPERSPACE_MODULAR_TRAINING_GUIDE.md`

---

## ✅ Status Summary

**Session 014**: COMPLETE ✅
- Git push to GitHub ✅
- Paperspace setup complete ✅
- All Codex fixes verified ✅
- Ready for training ✅

**Session 015**: NEXT
- Upload data file
- Start training (8-11 hours)
- Monitor progress
- Verify R² ≥ 0.85
- Deploy best model

---

**Created**: 2025-10-11 18:15
**Session**: 014 - Paperspace Deployment Complete
**Status**: ✅ READY FOR TRAINING!
**Next**: Upload data → Start training → Monitor R² 🚀

---

**พร้อมเทรนแล้ว!** อัพโหลดไฟล์ data แล้วเริ่มได้เลย! 🎯
