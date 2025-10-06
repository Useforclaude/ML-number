# 🚀 Quick Start Guide
## ML Phone Number Price Prediction

**Choose your platform** and follow the steps below:

---

## 📍 Where to Run?

### 🖥️ Local Machine (Testing Only)
- ✅ For code development and testing
- ✅ Quick tests complete in < 2 minutes
- ❌ NOT for full training (specs too low)

### ☁️ Google Colab (Recommended for Beginners)
- ✅ Free GPU (T4)
- ✅ Easy to use
- ✅ No setup required
- ⏱️ Training time: 2-3 hours

### 🏆 Kaggle (Recommended for Best Performance)
- ✅ Free GPU (T4 x2)
- ✅ Pre-installed packages
- ✅ Best for heavy training
- ⏱️ Training time: 1-2 hours

---

## 🏠 Local Machine (Testing)

### Step 1: Activate venv
```bash
cd /home/u-and-an/projects/number-ML
source .venv/bin/activate
```

### Step 2: Test Everything
```bash
# Test imports (should take ~5 seconds)
python tests/test_imports.py

# Quick test (should take ~30 seconds)
python quick_test.py
```

### Expected Output:
```
✅ ALL TESTS PASSED!
✅ Environment: local
✅ Data loaded: 3,596 records
✅ Features created: 150 features
✅ Model trained: R² = 0.1971
✅ Checkpoint system: Working
```

### ⚠️ Important:
**DO NOT run full training on this machine!**
Use Colab or Kaggle for production training.

---

## ☁️ Google Colab

### Quick Setup (5 minutes)

1. **Upload project to Google Drive**
   ```bash
   # On local machine
   cd /home/u-and-an/projects
   zip -r number-ML.zip number-ML/ -x "number-ML/.venv/*"

   # Upload number-ML.zip to Google Drive
   ```

2. **Open Google Colab**
   - Go to: https://colab.research.google.com
   - New Notebook

3. **Copy-Paste Cells**
   See [COLAB_SETUP.md](COLAB_SETUP.md) for detailed instructions

4. **Run Training**
   ```python
   !python run_with_autosave.py --run-all --optimize --checkpoint-interval 15
   ```

5. **Download Model**
   - Model saved to: `/content/drive/MyDrive/number-ML-models/`
   - Download `best_model_YYYYMMDD_HHMMSS.pkl`

### ⏱️ Time: 2-3 hours total

---

## 🏆 Kaggle (Best Option)

### Quick Setup (5 minutes)

1. **Create Kaggle Dataset**
   ```bash
   # On local machine
   cd /home/u-and-an/projects
   zip -r number-ML-kaggle.zip number-ML/ -x "number-ML/.venv/*"

   # Upload to Kaggle Datasets
   # https://kaggle.com/datasets → New Dataset
   ```

2. **Create Kaggle Notebook**
   - Go to: https://kaggle.com/code
   - New Notebook
   - Add your dataset

3. **Copy-Paste Cells**
   See [KAGGLE_SETUP.md](KAGGLE_SETUP.md) for detailed instructions

4. **Enable GPU** (Optional but recommended)
   - Settings → Accelerator → GPU T4 x2

5. **Run Training**
   ```python
   !python run_with_autosave.py --run-all --optimize --checkpoint-interval 10
   ```

6. **Download Model**
   - Model saved to: `/kaggle/working/best_model.pkl`
   - Download from Output tab

### ⏱️ Time: 1-2 hours total

---

## 📊 Expected Results

After training completes on Colab/Kaggle:

```
✅ Models trained: 6+ models
✅ Best model: XGBoost/LightGBM/CatBoost/Ensemble
✅ R² Score: > 0.90 (target: 0.93+)
✅ MAE: < 0.05
✅ RMSE: < 0.08
✅ Model size: ~50 MB
✅ Training time: 1-3 hours
```

---

## 🔍 Verify Training Success

### Check R² Score
```python
import joblib
model_data = joblib.load('best_model.pkl')
print(f"R² Score: {model_data['r2_score']:.4f}")  # Should be > 0.90
```

### Test Prediction
```python
from src.features import create_masterpiece_features
import pandas as pd
import numpy as np

# Load model
model = model_data['model']
preprocessor = model_data.get('preprocessor')

# Test number
df = pd.DataFrame({'phone_number': ['0899999999']})
features = create_masterpiece_features(df)
X = preprocessor.transform(features) if preprocessor else features.values

pred_log = model.predict(X)[0]
pred_price = np.expm1(pred_log)

print(f"Predicted price: {pred_price:,.0f} THB")  # Should be reasonable
```

---

## 🎯 Platform Comparison

| Feature | Local | Colab | Kaggle |
|---------|-------|-------|--------|
| **Setup Time** | 0 min | 5 min | 5 min |
| **Training Time** | ❌ N/A | 2-3 hrs | 1-2 hrs |
| **GPU** | ❌ No | ✅ T4 | ✅ T4 x2 |
| **Cost** | Free | Free | Free |
| **R² Score** | ~0.20* | > 0.90 | > 0.90 |
| **Best For** | Testing | Beginners | Production |

*Local only for quick tests, not full training

---

## 🆘 Troubleshooting

### Issue: Import Errors
```bash
# Make sure venv is activated
source .venv/bin/activate

# Test imports
python tests/test_imports.py
```

### Issue: Data Not Found
```bash
# Check if data exists
ls -lh data/raw/numberdata.csv

# Should show: 60K file size
```

### Issue: Out of Memory (Colab/Kaggle)
```python
# Edit src/config.py
MODEL_CONFIG['max_features'] = 100  # Reduce from 250
MODEL_CONFIG['optuna_trials'] = 50  # Reduce from 150
```

### Issue: Session Timeout
```python
# Checkpoints auto-save every 10-15 minutes
# Resume from latest checkpoint if session ends
import joblib
checkpoint = joblib.load('checkpoints/checkpoint_latest.json')
# Continue from saved state
```

---

## 📞 Need Help?

1. **Check Documentation**:
   - [CLAUDE.md](CLAUDE.md) - Development guidelines
   - [COLAB_SETUP.md](COLAB_SETUP.md) - Colab instructions
   - [KAGGLE_SETUP.md](KAGGLE_SETUP.md) - Kaggle instructions
   - [SESSION_COMPLETION_REPORT.md](SESSION_COMPLETION_REPORT.md) - Latest changes

2. **Check Logs**:
   ```bash
   # View latest checkpoint
   cat checkpoints/checkpoint_latest.json

   # View training logs
   ls -lht results/reports/
   ```

3. **Run Tests**:
   ```bash
   # Test everything
   python quick_test.py
   ```

---

## ✅ Success Checklist

### Before Training:
- [ ] Environment detected correctly
- [ ] All imports working
- [ ] Data loaded successfully
- [ ] Quick test passed

### After Training:
- [ ] R² > 0.90 achieved
- [ ] Model saved successfully
- [ ] Can load and use model
- [ ] Predictions are reasonable

---

## 🎉 Ready to Start!

**Recommended Path**:
1. Test locally first: `python quick_test.py`
2. If tests pass, run on Kaggle for best performance
3. Download trained model
4. Use for predictions!

**Next Steps**:
- 🏠 Local: Already tested ✅
- ☁️ Colab: See [COLAB_SETUP.md](COLAB_SETUP.md)
- 🏆 Kaggle: See [KAGGLE_SETUP.md](KAGGLE_SETUP.md)

---

*Choose your platform and start training! 🚀*
