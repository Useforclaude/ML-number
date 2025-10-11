# 🎯 Paperspace 6-Hour Training Strategy

**Problem**: Paperspace Free tier auto-shutdown after 6 hours
**Solution**: Split training into 3 sessions (5h + 5h + 0.5h)

---

## 📊 Training Time Breakdown

| Model | Time | Trials | Priority |
|-------|------|--------|----------|
| RandomForest | 1 hour | 50 | Fast |
| CatBoost | 1-2 hours | 50 | Fast |
| XGBoost | 2-3 hours | 100 | Medium |
| LightGBM | 3-4 hours | 100 | Slow |
| Ensemble | 15-30 min | - | Final |

---

## ✅ Optimal Strategy (3 Sessions)

### **Session 1: Fast Models (5 hours total)**
```bash
cd /notebooks/ML-number
source .venv/bin/activate

# Run sequentially (not parallel!)
echo "=== SESSION 1: Fast Models ==="

# Step 1: XGBoost (2-3 hours)
echo "▶️ Starting XGBoost..."
python training/modular/train_xgboost_only.py 2>&1 | tee logs/xgb.log

# Step 2: CatBoost (1-2 hours)
echo "▶️ Starting CatBoost..."
python training/modular/train_catboost_only.py 2>&1 | tee logs/cat.log

# Step 3: RandomForest (1 hour) - if time permits
echo "▶️ Starting RandomForest..."
python training/modular/train_rf_only.py 2>&1 | tee logs/rf.log

echo "✅ SESSION 1 COMPLETE!"
ls -lh models/checkpoints/
```

**Expected Duration**: ~5 hours
**Checkpoints Saved**:
- `models/checkpoints/xgboost_checkpoint.pkl` ✅
- `models/checkpoints/catboost_checkpoint.pkl` ✅
- `models/checkpoints/random_forest_checkpoint.pkl` ✅

---

### **Session 2: Slow Model (4 hours total)**
```bash
cd /notebooks/ML-number
source .venv/bin/activate

# Verify previous checkpoints exist
echo "=== Verifying Session 1 checkpoints ==="
ls -lh models/checkpoints/xgboost_checkpoint.pkl
ls -lh models/checkpoints/catboost_checkpoint.pkl
ls -lh models/checkpoints/random_forest_checkpoint.pkl

echo "=== SESSION 2: Slow Model ==="

# LightGBM (3-4 hours)
echo "▶️ Starting LightGBM (longest model)..."
python training/modular/train_lightgbm_only.py 2>&1 | tee logs/lgb.log

echo "✅ SESSION 2 COMPLETE!"
ls -lh models/checkpoints/
```

**Expected Duration**: ~4 hours
**Checkpoints Saved**:
- `models/checkpoints/lightgbm_checkpoint.pkl` ✅

---

### **Session 3: Ensemble (30 minutes)**
```bash
cd /notebooks/ML-number
source .venv/bin/activate

# Verify all 4 checkpoints exist
echo "=== Verifying ALL checkpoints ==="
ls -lh models/checkpoints/xgboost_checkpoint.pkl
ls -lh models/checkpoints/lightgbm_checkpoint.pkl
ls -lh models/checkpoints/catboost_checkpoint.pkl
ls -lh models/checkpoints/random_forest_checkpoint.pkl

echo "=== SESSION 3: Ensemble ==="

# Create ensemble (15-30 min)
echo "▶️ Creating ensemble from all 4 models..."
python training/modular/train_ensemble_only.py 2>&1 | tee logs/ensemble.log

echo "✅ SESSION 3 COMPLETE - TRAINING DONE!"
ls -lh models/deployed/best_model.pkl
```

**Expected Duration**: ~30 minutes
**Final Output**:
- `models/deployed/best_model.pkl` ✅ (Best model from ensemble)

---

## 📋 Session Checklist

### **Before Session 1:**
- [ ] Data file uploaded (`data/raw/numberdata.csv`)
- [ ] Virtual environment active
- [ ] Data loading tested (raw=6112, cleaned=6100)
- [ ] `logs/` directory exists

### **Between Sessions:**
- [ ] Verify checkpoints saved
- [ ] Check R² scores in logs
- [ ] Note any errors

### **After Session 3:**
- [ ] All 4 checkpoints exist
- [ ] R² scores all ≥ 0.85
- [ ] Best model deployed
- [ ] Download models to local

---

## 🔍 Verification Commands

### **Check Progress During Training:**
```bash
# Monitor current training
tail -f logs/xgb.log      # XGBoost
tail -f logs/cat.log      # CatBoost
tail -f logs/rf.log       # RandomForest
tail -f logs/lgb.log      # LightGBM
tail -f logs/ensemble.log # Ensemble

# Check data loading (verify Codex fix)
grep "Data loaded" logs/*.log
# Expected: raw=6112, cleaned=6100

# Check R² progress
grep "R²" logs/*.log
grep "Test R²" logs/*.log
```

### **Verify Checkpoints Between Sessions:**
```bash
# List all checkpoints
ls -lh models/checkpoints/

# After Session 1 (should have 3 files):
ls -lh models/checkpoints/xgboost_checkpoint.pkl
ls -lh models/checkpoints/catboost_checkpoint.pkl
ls -lh models/checkpoints/random_forest_checkpoint.pkl

# After Session 2 (should have 4 files):
ls -lh models/checkpoints/lightgbm_checkpoint.pkl

# After Session 3 (should have deployed model):
ls -lh models/deployed/best_model.pkl
```

---

## 🚨 Important Notes

### **Why Sequential (Not Parallel)?**
```bash
# ❌ DON'T run in parallel:
nohup python train_xgboost_only.py > logs/xgb.log 2>&1 &
nohup python train_lightgbm_only.py > logs/lgb.log 2>&1 &
# Result: 3h + 4h = 7 hours total (exceeds 6h limit!) ❌

# ✅ DO run sequentially:
python train_xgboost_only.py    # 3h
python train_catboost_only.py   # 2h
# Result: 3h → then → 2h = 5 hours total ✅
```

### **Checkpoint Safety:**
- All checkpoints saved to `/notebooks/` → **Persistent!** ✅
- Files survive Paperspace session restart
- Can resume from any checkpoint

### **Alternative: If RandomForest Too Late in Session 1:**
```bash
# Session 1 (safer): XGBoost + CatBoost only (4-5h)
python training/modular/train_xgboost_only.py 2>&1 | tee logs/xgb.log
python training/modular/train_catboost_only.py 2>&1 | tee logs/cat.log

# Session 2: LightGBM + RandomForest (4-5h)
python training/modular/train_lightgbm_only.py 2>&1 | tee logs/lgb.log
python training/modular/train_rf_only.py 2>&1 | tee logs/rf.log

# Session 3: Ensemble (30 min)
python training/modular/train_ensemble_only.py 2>&1 | tee logs/ensemble.log
```

---

## 📊 Expected R² Results

### **After Each Session:**
```
Session 1:
✅ XGBoost:     R² ~0.88-0.92
✅ CatBoost:    R² ~0.85-0.89
✅ RandomForest: R² ~0.82-0.86

Session 2:
✅ LightGBM:    R² ~0.86-0.90

Session 3:
✅ Ensemble:    R² ~0.90-0.93 (BEST!)
```

### **Verify R² in Logs:**
```bash
grep "Test R²" logs/xgb.log
grep "Test R²" logs/lgb.log
grep "Test R²" logs/cat.log
grep "Test R²" logs/rf.log
grep "Best.*R²" logs/ensemble.log
```

---

## 🎯 Copy-Paste Commands

### **SESSION 1 (Copy-Paste Ready):**
```bash
#!/bin/bash
cd /notebooks/ML-number
source .venv/bin/activate

echo "=== SESSION 1: Fast Models (5h) ==="
echo "Start time: $(date)"

# XGBoost (2-3h)
echo "▶️ XGBoost starting..."
python training/modular/train_xgboost_only.py 2>&1 | tee logs/xgb.log
echo "✅ XGBoost done: $(date)"

# CatBoost (1-2h)
echo "▶️ CatBoost starting..."
python training/modular/train_catboost_only.py 2>&1 | tee logs/cat.log
echo "✅ CatBoost done: $(date)"

# RandomForest (1h)
echo "▶️ RandomForest starting..."
python training/modular/train_rf_only.py 2>&1 | tee logs/rf.log
echo "✅ RandomForest done: $(date)"

echo "=== SESSION 1 COMPLETE ==="
echo "End time: $(date)"
ls -lh models/checkpoints/
```

### **SESSION 2 (Copy-Paste Ready):**
```bash
#!/bin/bash
cd /notebooks/ML-number
source .venv/bin/activate

echo "=== Verify Session 1 checkpoints ==="
ls -lh models/checkpoints/*.pkl

echo "=== SESSION 2: Slow Model (4h) ==="
echo "Start time: $(date)"

# LightGBM (3-4h)
echo "▶️ LightGBM starting (longest model)..."
python training/modular/train_lightgbm_only.py 2>&1 | tee logs/lgb.log
echo "✅ LightGBM done: $(date)"

echo "=== SESSION 2 COMPLETE ==="
ls -lh models/checkpoints/
```

### **SESSION 3 (Copy-Paste Ready):**
```bash
#!/bin/bash
cd /notebooks/ML-number
source .venv/bin/activate

echo "=== Verify ALL 4 checkpoints ==="
ls -lh models/checkpoints/*.pkl | wc -l
# Should show: 4

echo "=== SESSION 3: Ensemble (30min) ==="
echo "Start time: $(date)"

# Ensemble (15-30min)
echo "▶️ Creating ensemble..."
python training/modular/train_ensemble_only.py 2>&1 | tee logs/ensemble.log
echo "✅ Ensemble done: $(date)"

echo "=== ALL TRAINING COMPLETE! ==="
ls -lh models/deployed/best_model.pkl
grep "Best.*R²" logs/ensemble.log
```

---

## 📝 Quick Reference

| Session | Models | Time | Checkpoints |
|---------|--------|------|-------------|
| 1 | XGBoost + CatBoost + RF | ~5h | 3 files |
| 2 | LightGBM | ~4h | 1 file |
| 3 | Ensemble | ~30min | Best model |
| **Total** | **All models** | **~10h** | **Complete!** |

---

**Created**: 2025-10-11
**Purpose**: Avoid Paperspace 6-hour auto-shutdown by splitting training
**Status**: Ready to use ✅
