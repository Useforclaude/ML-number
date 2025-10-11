# Google Colab Setup Guide
## ML Phone Number Price Prediction

---

## 🚀 Quick Start (Copy-Paste Ready!)

### Method 1: Upload Project ZIP to Google Drive

#### Step 1: Prepare ZIP File (On Local Machine)
```bash
# On your local machine
cd /home/u-and-an/projects
zip -r number-ML.zip number-ML/ \
    -x "number-ML/.venv/*" \
    -x "number-ML/__pycache__/*" \
    -x "number-ML/.git/*" \
    -x "number-ML/checkpoints/*"

# Upload number-ML.zip to Google Drive
```

#### Step 2: Run in Colab (Cell 1 - Setup)
```python
# ============================================================================
# CELL 1: MOUNT DRIVE & EXTRACT PROJECT
# ============================================================================
from google.colab import drive
import os
import zipfile

# Mount Google Drive
drive.mount('/content/drive')

# Extract project
zip_path = '/content/drive/MyDrive/number-ML.zip'  # Adjust path
extract_path = '/content/number-ML'

if os.path.exists(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('/content/')
    print(f"✅ Project extracted to {extract_path}")
else:
    print(f"❌ ZIP file not found at {zip_path}")
    print("Please upload number-ML.zip to Google Drive first")

# Change to project directory
os.chdir(extract_path)
print(f"✅ Working directory: {os.getcwd()}")
```

#### Step 3: Install Dependencies (Cell 2)
```python
# ============================================================================
# CELL 2: INSTALL DEPENDENCIES
# ============================================================================
!pip install -q pandas numpy scikit-learn xgboost lightgbm catboost optuna joblib tqdm matplotlib seaborn openpyxl xlrd psutil

print("✅ All dependencies installed!")
```

#### Step 4: Test Imports (Cell 3)
```python
# ============================================================================
# CELL 3: TEST IMPORTS
# ============================================================================
import sys
import os

# Add project to path
sys.path.insert(0, '/content/number-ML')

# Test imports
!python tests/test_imports.py
```

#### Step 5: Run Quick Test (Cell 4)
```python
# ============================================================================
# CELL 4: QUICK TEST
# ============================================================================
!python quick_test.py
```

#### Step 6: Full Training (Cell 5)
```python
# ============================================================================
# CELL 5: FULL TRAINING WITH OPTIMIZATION
# ============================================================================
!python run_with_autosave.py --run-all --optimize --feature-selection --checkpoint-interval 15
```

#### Step 7: Save Model to Drive (Cell 6)
```python
# ============================================================================
# CELL 6: SAVE MODEL TO GOOGLE DRIVE
# ============================================================================
import shutil
from datetime import datetime

# Create backup directory
backup_dir = '/content/drive/MyDrive/number-ML-models'
os.makedirs(backup_dir, exist_ok=True)

# Copy trained model
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
model_file = 'models/deployed/best_model.pkl'

if os.path.exists(model_file):
    dest = f'{backup_dir}/best_model_{timestamp}.pkl'
    shutil.copy(model_file, dest)
    print(f"✅ Model saved to: {dest}")
else:
    print(f"❌ Model not found at {model_file}")

# Also save checkpoints
checkpoint_dir = 'checkpoints'
if os.path.exists(checkpoint_dir):
    dest_checkpoint = f'{backup_dir}/checkpoints_{timestamp}'
    shutil.copytree(checkpoint_dir, dest_checkpoint)
    print(f"✅ Checkpoints saved to: {dest_checkpoint}")
```

---

## Method 2: Clone from GitHub (If Available)

```python
# Cell 1: Clone repository
!git clone https://github.com/YOUR_USERNAME/number-ML.git
%cd number-ML

# Cell 2: Install dependencies
!pip install -q -r requirements.txt

# Cell 3-6: Same as above
```

---

## Method 3: Manual Upload (For Small Changes)

```python
# Upload files via Colab's file browser
# Then run same cells 2-6
```

---

## 🎯 Expected Results

After running Cell 5 (full training), you should see:

```
✅ Models trained: 6+ models
✅ R² Score > 0.90
✅ Best model: [XGBoost/LightGBM/CatBoost/Ensemble]
✅ Model saved to models/deployed/best_model.pkl
✅ Checkpoints saved every 15 minutes
```

---

## 🔧 Troubleshooting

### Issue 1: Import Errors
```python
# Make sure project path is in sys.path
import sys
sys.path.insert(0, '/content/number-ML')
```

### Issue 2: Data Not Found
```python
# Check if data exists
!ls -lh data/raw/

# If missing, upload via Colab file browser to data/raw/
```

### Issue 3: Out of Memory
```python
# Reduce feature count or use smaller sample
# Edit src/config.py:
# MODEL_CONFIG['max_features'] = 100  # Instead of 250
```

### Issue 4: Session Timeout
```python
# Use checkpoints! They auto-save every 15 minutes
# To resume:
import joblib
checkpoint = joblib.load('checkpoints/checkpoint_latest.json')
# Continue from last saved state
```

---

## 📊 Resource Requirements

- **RAM**: 12 GB (Colab free tier)
- **GPU**: Optional (CPU is fine, just slower)
- **Time**: 1-3 hours for full training
- **Storage**: ~200 MB for project + models

---

## 💡 Pro Tips

1. **Use GPU if available**:
   - Runtime > Change runtime type > GPU
   - CatBoost and XGBoost can use GPU

2. **Keep Colab active**:
   - Run a cell periodically to prevent timeout
   - Or use Colab Pro for longer sessions

3. **Save frequently**:
   - Auto-checkpoints save every 15 minutes
   - Manually save important results to Drive

4. **Monitor progress**:
   - Checkpoints show in `checkpoints/` directory
   - Check with: `!ls -lht checkpoints/`

---

## ✅ Verification Checklist

Before training:
- [ ] Project extracted successfully
- [ ] Dependencies installed
- [ ] Imports working (`python tests/test_imports.py`)
- [ ] Quick test passed (`python quick_test.py`)
- [ ] Data files present (`ls data/raw/`)

After training:
- [ ] R² > 0.90 achieved
- [ ] Model saved to `models/deployed/`
- [ ] Model backed up to Google Drive
- [ ] Checkpoints saved
- [ ] Can load and use model for prediction

---

*Ready to run on Google Colab! 🚀*
