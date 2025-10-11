# 🚀 Kaggle CatBoost Quick Start Guide

**Created**: 2025-10-08
**Model**: CatBoost Only
**Duration**: 1-2 hours
**Expected R²**: 0.85-0.89

---

## 📋 Step 1: Create Kaggle Notebook

1. Go to https://www.kaggle.com/code
2. Click **"New Notebook"**
3. Turn ON **GPU**: Settings → Accelerator → **GPU P100**
4. Turn ON **Internet**: Settings → Internet → **ON**

---

## 📂 Step 2: Upload Code + Data

### Option A: Via GitHub (แนะนำ!)

```bash
# Cell 1
!git clone https://github.com/YOUR_USERNAME/number-ML.git
%cd number-ML
!ls -lh
```

### Option B: Via Kaggle Dataset

1. Upload `number-ML` folder as Kaggle Dataset
2. Add dataset to notebook
3. Copy to working directory:

```bash
!cp -r /kaggle/input/number-ml/* /kaggle/working/
%cd /kaggle/working
```

### Upload Data File

Upload `numberdata.csv` to `/kaggle/input/` or add as dataset

---

## ⚙️ Step 3: Install Dependencies

```bash
# Cell 2: Install packages
!pip install -q optuna catboost lightgbm xgboost scikit-learn==1.5.2 pandas numpy torch

# Verify installation
!python -c "import catboost; print(f'CatBoost: {catboost.__version__}')"
```

---

## 🔧 Step 4: Setup Environment

```bash
# Cell 3: Configure paths for Kaggle
import os
os.environ['ML_BASE_PATH'] = '/kaggle/working'

# Verify imports
!python -c "from src.config import BASE_PATH; print(f'✅ BASE_PATH: {BASE_PATH}')"
!python -c "from src.data_handler import load_and_clean_data; print('✅ Imports OK')"
```

---

## 🚀 Step 5: Run CatBoost Training

```bash
# Cell 4: Train CatBoost
!python train_catboost_only.py
```

**Output akan menampilkan:**
```
================================================================================
🚀 CATBOOST MODULAR TRAINING
================================================================================
📂 Project: /kaggle/working
🖥️  Environment: kaggle
================================================================================
✅ GPU Available: Tesla P100-PCIE-16GB (16.0 GB)

STEP 1: Loading Filtered Data
✅ Data loaded: 6100 rows

STEP 2: Feature Engineering
✅ Features created: 250+ features, 6100 samples

STEP 3-6: [Data split, preprocessing...]

🔥 STEP 7: CATBOOST OPTIMIZATION
⏱️  Expected duration: 1-2 hours
🎯 Optimization trials: 50
🔥 GPU enabled: True

[Progress bars will show optimization progress...]

✅ CATBOOST TRAINING COMPLETE!
⏱️  Total Time: 1.XX hours
📊 Best R²: 0.8X-0.8X
💾 Checkpoint: models/checkpoints/catboost_checkpoint.pkl
```

---

## 👀 Step 6: Monitor Progress (Optional)

**In separate cell while training:**

```python
# Cell 5: Monitor logs (run while training)
!tail -50 logs/catboost_*.log
```

**Check GPU usage:**

```bash
!nvidia-smi
```

---

## 📊 Step 7: Check Results

```python
# Cell 6: After training completes
import joblib

# Load checkpoint
checkpoint = joblib.load('models/checkpoints/catboost_checkpoint.pkl')

print(f"✅ CatBoost Model Loaded!")
print(f"   R² Score:  {checkpoint['r2_score']:.4f}")
print(f"   MAE:       {checkpoint['mae']:.2f}")
print(f"   RMSE:      {checkpoint['rmse']:.2f}")
print(f"   Training:  {checkpoint['training_time_hours']:.2f} hours")
```

---

## 🧪 Step 8: Test Prediction (Optional)

```python
# Cell 7: Test prediction
model = checkpoint['model']
preprocessor = checkpoint['preprocessor']

# Test with sample number
from src.features import create_all_features
import pandas as pd

test_number = "0899999999"
df_test = pd.DataFrame({'phone_number': [test_number]})
X_test, _, _ = create_all_features(df_test)
X_test_processed = preprocessor.transform(X_test)

price_log_pred = model.predict(X_test_processed)
price_pred = np.expm1(price_log_pred[0])

print(f"\n🔮 Prediction for {test_number}:")
print(f"   Predicted Price: ฿{price_pred:,.0f}")
```

---

## 💾 Step 9: Download Model

```bash
# Cell 8: Download checkpoint
from IPython.display import FileLink

FileLink('models/checkpoints/catboost_checkpoint.pkl')
```

Click the link to download!

---

## ✅ Success Checklist

**Before running:**
- [ ] GPU P100 enabled
- [ ] Internet ON
- [ ] Code uploaded to `/kaggle/working/`
- [ ] Data file exists (`data/raw/numberdata.csv`)
- [ ] Dependencies installed

**During training:**
- [ ] GPU showing activity in nvidia-smi
- [ ] Logs updating every few seconds
- [ ] No error messages
- [ ] Optuna progress bars showing

**After training:**
- [ ] R² score > 0.85
- [ ] Checkpoint file saved (should be ~50-100 MB)
- [ ] Can load and predict successfully
- [ ] Model downloaded to local

---

## 🐛 Troubleshooting

### Error: "No module named 'src'"

```bash
!pwd  # Should show /kaggle/working
%cd /kaggle/working
```

### Error: "File not found: numberdata.csv"

```bash
# Check data location
!ls -lh data/raw/

# If not found, copy from input
!mkdir -p data/raw
!cp /kaggle/input/*/numberdata.csv data/raw/
```

### Error: "GPU not available"

- Go to Settings → Accelerator → Select **GPU P100**
- Restart notebook
- Re-run cells

### Training too slow / timeout

Already optimized! 50 trials = 1-2 hours only.

### R² too low (<0.80)

This is expected for first model. We'll improve with:
- More trials (increase from 50 to 100)
- Ensemble with other models

---

## 📈 Expected Results

### Performance Targets:
- **R² Score**: 0.85-0.89
- **MAE**: ~฿800-1,200
- **RMSE**: ~฿1,500-2,500

### If R² < 0.80:
- Still much better than previous 0.4!
- Ensemble will boost to 0.90+
- Data filtering is working ✅

### If R² > 0.89:
- 🎉 Excellent! Better than expected!
- Ready to try ensemble
- Or train other models for comparison

---

## 🎯 Next Steps After CatBoost

**Option 1: Train More Models**
```bash
# Quick models (can run same session)
!python train_rf_only.py        # 1 hour
```

**Option 2: Create Ensemble** (if you have multiple models)
```bash
!python train_ensemble_only.py  # 15-30 min
```

**Option 3: Just Use CatBoost** (if R² good enough)
- Deploy checkpoint directly
- Update API
- Ship to production!

---

## 💡 Pro Tips

1. **Save notebook version** after training completes
2. **Download checkpoint** immediately (Kaggle deletes after 7 days)
3. **Copy logs** for documentation
4. **Check git status** - commit if needed

---

## 🔗 Related Guides

- `NEXT_SESSION.md` - Complete modular training guide
- `SESSION_012_SUMMARY.md` - Session 012 documentation
- `KAGGLE_SETUP.md` - General Kaggle setup (if exists)

---

**Created**: 2025-10-08
**Model**: CatBoost
**Optimized for**: Kaggle P100 GPU
**Duration**: 1-2 hours
**Ready to run!** 🚀
