# 📘 Paperspace Complete Guide - Step by Step

**Created**: 2025-10-06
**For**: ML Phone Number Training on Paperspace
**Time needed**: ~25 minutes setup + 9-12 hours training

---

## 🎯 Overview

คู่มือนี้จะพาคุณตั้งแต่:
1. Login Paperspace
2. Create/Open Notebook
3. Setup environment
4. Fix dependencies
5. Upload data
6. Run training in Jupyter Lab

**เป้าหมาย**: เริ่ม training บน Paperspace ระหว่างรอ Kaggle

---

## 📋 STEP 1: Login & Open Paperspace

### 1.1 Login
- ไปที่: https://console.paperspace.com/
- Login ด้วย account

### 1.2 Navigate to Notebooks
```
Console → Gradient → Notebooks
```

### 1.3 Check Existing Notebooks
**ถ้ามี notebook อยู่แล้ว:**
- คลิก "Open" → ข้ามไป STEP 3

**ถ้าไม่มี:**
- ทำ STEP 2 ต่อ

---

## 📋 STEP 2: Create New Notebook (Optional)

### 2.1 Click "Create Notebook"

### 2.2 Configuration

**Machine Type:**
```
Free tier:
  ✅ Free-GPU (Quadro M4000) ← เลือกนี้

Pro tier (ถ้าจ่าย $8/month):
  ⭐ P4000 (8GB VRAM)
  ⭐ P5000 (16GB VRAM)
```

**Container:**
```
Recommended:
  - Fast.ai (มี PyTorch, Jupyter, GPU drivers)

Alternative:
  - PyTorch
  - TensorFlow
```

**Workspace:**
```
None (เราจะ clone จาก GitHub)
```

**Advanced Options:**
```
Auto-shutdown:
  - Free: 6 hours (จะปิดเอง)
  - Pro: Never / Custom (ตั้งเองได้)

Persistent Storage:
  - Free: 5 GB (/storage)
  - Pro: 50 GB (/storage)
```

### 2.3 Start Notebook
- คลิก "Start Notebook"
- รอ 2-5 นาที
- สถานะจะเป็น: "Running" (สีเขียว)

### 2.4 Open Jupyter
- คลิก "Open"
- จะเปิด Jupyter Lab (หรือ Notebook)

---

## 📋 STEP 3: Open Terminal in Jupyter

### วิธีที่ 1 - Jupyter Lab (Modern UI):
```
File → New → Terminal
```

### วิธีที่ 2 - Jupyter Notebook (Classic UI):
```
New (ขวาบน) → Terminal
```

**ผลลัพธ์:**
- จะเห็นหน้าจอ terminal สีดำ
- พร้อมพิมพ์คำสั่ง

---

## 📋 STEP 4: Clone Project & Setup

### 4.1 Check GPU (Optional)
```bash
nvidia-smi
```

**ควรเห็น:**
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.xx       Driver Version: 525.xx       CUDA Version: 12.0    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Quadro M4000        Off  | 00000000:00:05.0 Off |                  N/A |
| 46%   42C    P0    32W / 120W |      0MiB /  8192MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
```

### 4.2 Clone Project from GitHub
```bash
cd /storage
git clone https://github.com/Useforclaude/ML-number.git
cd ML-number
```

**ตรวจสอบ:**
```bash
pwd
# Expected: /storage/ML-number

ls -la
# ควรเห็น: src/, requirements.txt, README.md, etc.

ls src/
# ควรเห็น 17 files: config.py, model_utils.py, etc.
```

---

## 📋 STEP 5: Fix Dependencies

### 5.1 Fix blinker conflict
```bash
pip install --ignore-installed blinker
```

**Expected output:**
```
Successfully installed blinker-1.9.0
```

### 5.2 Install ML Libraries (Essential 3)
```bash
pip install lightgbm==3.3.5
pip install catboost==1.2.8
pip install optuna==3.6.2
```

**Each should show:**
```
Successfully installed lightgbm-3.3.5
Successfully installed catboost-1.2.8
Successfully installed optuna-3.6.2
```

### 5.3 Validate Installation
```bash
python -c "import lightgbm; print('✅ LightGBM OK')"
python -c "import catboost; print('✅ CatBoost OK')"
python -c "import optuna; print('✅ Optuna OK')"
python -c "import xgboost; print('✅ XGBoost OK')"
python -c "import sklearn; print('✅ scikit-learn OK')"
```

**ต้องเห็นทั้ง 5 ✅:**
```
✅ LightGBM OK
✅ CatBoost OK
✅ Optuna OK
✅ XGBoost OK
✅ scikit-learn OK
```

### 5.4 Install Remaining Dependencies (Optional)
```bash
pip install -r requirements.txt
```

ถ้ามี error → ข้ามได้ เพราะของสำคัญติดแล้ว (5.2)

---

## 📋 STEP 6: Upload Data File

### 6.1 Create data directory
```bash
mkdir -p /storage/ML-number/data/raw
```

### 6.2 Upload numberdata.csv

**วิธีที่ 1 - ใช้ Jupyter UI (แนะนำ!):**

**ใน Jupyter Lab:**
```
1. ซ้ายมือ: คลิก Folder icon 📁
2. Navigate: /storage/ML-number/data/raw/
   (คลิก storage → ML-number → data → raw)
3. คลิกขวาในพื้นที่ว่าง → Upload Files
4. เลือกไฟล์: numberdata.csv (จากเครื่องคุณ)
5. รอ upload bar เสร็จ (ควรเป็น ~93 KB)
```

**ใน Jupyter Notebook (Classic):**
```
1. Navigate to: /storage/ML-number/data/raw/
2. คลิก "Upload" (ขวาบน)
3. เลือก numberdata.csv
4. คลิก "Upload" (สีฟ้า) อีกครั้งเพื่อ confirm
```

**วิธีที่ 2 - ใช้ Terminal (ถ้าไฟล์อยู่ที่อื่น):**
```bash
cd /storage/ML-number/data/raw/

# Option A: Download from URL
wget https://your-url.com/numberdata.csv

# Option B: Copy from /tmp (ถ้า upload via Jupyter root)
cp /tmp/numberdata.csv .

# Option C: From local mounted drive (ถ้ามี)
cp /path/to/your/numberdata.csv .
```

### 6.3 Verify Data File
```bash
ls -lh /storage/ML-number/data/raw/numberdata.csv
```

**ควรเห็น:**
```
-rw-r--r-- 1 root root 93K Oct  6 12:00 numberdata.csv
```

**ตรวจสอบเนื้อหา:**
```bash
head -5 /storage/ML-number/data/raw/numberdata.csv
```

**ควรเห็น:**
```
phone_number,price
0812345678,5000
0899999999,150000
...
```

**นับจำนวนแถว:**
```bash
wc -l /storage/ML-number/data/raw/numberdata.csv
```

**ควรเห็น:**
```
6113 numberdata.csv  (6112 rows + 1 header)
```

---

## 📋 STEP 7: Create Training Notebook

### 7.1 Create New Notebook

**ใน Jupyter Lab:**
```
File → New → Notebook
Kernel: เลือก "Python 3"
Save as: /storage/ML-number/train_paperspace.ipynb
```

**ใน Jupyter Notebook:**
```
New → Python 3
Rename: train_paperspace
```

### 7.2 Cell 1 - Setup Environment
```python
import sys
import os

# Add project to Python path
sys.path.insert(0, '/storage/ML-number')

print("="*80)
print("🔧 ENVIRONMENT SETUP")
print("="*80)

# Verify path
print(f"✅ Python path: {sys.path[0]}")
print(f"✅ Working dir: {os.getcwd()}")

# Test imports
try:
    from src.config import BASE_PATH, MODEL_CONFIG
    from src.environment import get_config_for_environment

    env_config = get_config_for_environment()
    print(f"✅ Environment: {env_config['ENV_TYPE']}")
    print(f"✅ BASE_PATH: {BASE_PATH}")
    print(f"✅ Imports working!")
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("⚠️  Fix: Check if /storage/ML-number/src/ exists")

print("="*80)
```

**Run: Shift+Enter**

**ควรเห็น:**
```
================================================================================
🔧 ENVIRONMENT SETUP
================================================================================
✅ Python path: /storage/ML-number
✅ Working dir: /home/jovyan
✅ Environment: paperspace
✅ BASE_PATH: /storage/ML-number
✅ Imports working!
================================================================================
```

### 7.3 Cell 2 - Load Data
```python
from src.data_loader import find_and_load_data
import pandas as pd

print("="*80)
print("📊 DATA LOADING")
print("="*80)

try:
    # Load data
    df_raw = find_and_load_data()

    print(f"✅ Data loaded successfully!")
    print(f"✅ Total rows: {len(df_raw)}")
    print(f"✅ Columns: {df_raw.columns.tolist()}")
    print(f"✅ Data types:\n{df_raw.dtypes}")

    # Show sample
    print(f"\n📋 First 5 rows:")
    print(df_raw.head())

    # Basic stats
    print(f"\n📈 Price statistics:")
    print(df_raw['price'].describe())

except Exception as e:
    print(f"❌ Error loading data: {e}")
    print("\n⚠️  Troubleshooting:")
    print("   1. Check: ls /storage/ML-number/data/raw/numberdata.csv")
    print("   2. Upload numberdata.csv to /storage/ML-number/data/raw/")
    print("   3. Verify file has 6112 rows + header")

print("="*80)
```

**Run: Shift+Enter**

**ควรเห็น:**
```
================================================================================
📊 DATA LOADING
================================================================================
✅ Data loaded successfully!
✅ Total rows: 6112
✅ Columns: ['phone_number', 'price']
✅ Data types:
phone_number    object
price          float64
dtype: object

📋 First 5 rows:
  phone_number    price
0   0812345678   5000.0
1   0899999999  150000.0
...
================================================================================
```

### 7.4 Cell 3 - Test GPU (Optional)
```python
import torch
import subprocess

print("="*80)
print("🖥️  GPU CHECK")
print("="*80)

# PyTorch GPU check
if torch.cuda.is_available():
    print(f"✅ PyTorch GPU available!")
    print(f"   Device: {torch.cuda.get_device_name(0)}")
    print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    print(f"   CUDA Version: {torch.version.cuda}")
else:
    print("⚠️  PyTorch: No GPU detected")
    print("   Training will use CPU (slower but works)")

# nvidia-smi check
print(f"\n🔍 nvidia-smi output:")
try:
    result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,utilization.gpu',
                            '--format=csv,noheader'],
                           capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print(f"   {result.stdout.strip()}")
    else:
        print("   ⚠️  nvidia-smi not available")
except:
    print("   ⚠️  nvidia-smi command failed")

print("="*80)
```

**Run: Shift+Enter**

**ถ้ามี GPU ควรเห็น:**
```
================================================================================
🖥️  GPU CHECK
================================================================================
✅ PyTorch GPU available!
   Device: Quadro M4000
   Memory: 8.0 GB
   CUDA Version: 12.0

🔍 nvidia-smi output:
   Quadro M4000, 8192 MiB, 0 %
================================================================================
```

**ถ้าไม่มี GPU:**
```
⚠️  PyTorch: No GPU detected
   Training will use CPU (slower but works)
```
→ ตรวจสอบ Notebook Settings → Instance Type → ต้องเป็น "Free-GPU"

### 7.5 Cell 4 - Start Training (MAIN)
```python
from src.train_production import train_production_models
import time

print("="*80)
print("🚀 ML TRAINING - PRODUCTION MODE")
print("="*80)

# Configuration
config = {
    'optimize': True,        # Use Optuna hyperparameter optimization
    'n_trials': 100,         # Number of Optuna trials (100 = ~9-12 hours)
    'use_gpu': True,         # Auto-fallback to CPU if GPU fails
    'verbose': True          # Show detailed progress
}

print(f"📋 Training Configuration:")
print(f"   Optimization: {config['optimize']}")
print(f"   Optuna Trials: {config['n_trials']}")
print(f"   GPU Enabled: {config['use_gpu']}")
print(f"   Verbose: {config['verbose']}")
print(f"\n⏱️  Estimated Time:")
print(f"   With GPU: ~9-12 hours")
print(f"   CPU only: ~18-24 hours")
print(f"\n💾 Progress saved to:")
print(f"   Checkpoints: /storage/ML-number/checkpoints/")
print(f"   Models: /storage/ML-number/models/")
print("\n" + "="*80)
print("⚠️  DO NOT CLOSE THIS NOTEBOOK DURING TRAINING!")
print("="*80 + "\n")

# Confirm before starting
input("Press ENTER to start training (or Ctrl+C to cancel)...")

# Start training
start_time = time.time()

try:
    results = train_production_models(
        optimize=config['optimize'],
        n_trials=config['n_trials'],
        use_gpu=config['use_gpu'],
        verbose=config['verbose']
    )

    elapsed = time.time() - start_time

    print("\n" + "="*80)
    print("✅ TRAINING COMPLETE!")
    print("="*80)
    print(f"⏱️  Total time: {elapsed/3600:.2f} hours")
    print(f"🎯 Best R² Score: {results.get('best_r2', 'N/A'):.4f}")
    print(f"🏆 Best Model: {results.get('best_model_name', 'N/A')}")
    print(f"💾 Model saved to: /storage/ML-number/models/deployed/best_model.pkl")
    print("="*80)

except KeyboardInterrupt:
    print("\n⚠️  Training interrupted by user!")
    print("💾 Checkpoints saved - you can resume later")
except Exception as e:
    print(f"\n❌ Training error: {e}")
    import traceback
    traceback.print_exc()
```

**IMPORTANT: ก่อน Run Cell นี้**
```
1. ตรวจสอบ Cells 1-3 ผ่านหมดแล้ว (✅)
2. Data loaded เรียบร้อย (✅)
3. Save notebook (Ctrl+S หรือ Cmd+S)
4. เตรียมใจว่าจะรอ 9-12 ชั่วโมง
```

**Run: Shift+Enter**

จะเห็น:
```
Press ENTER to start training (or Ctrl+C to cancel)...
```

กด **Enter** เพื่อเริ่ม training

---

## 📊 What to Expect During Training

### Phase 1: XGBoost (GPU) - ~2.5 hours
```
================================================================================
🔥 Training XGBoost (GPU)
================================================================================
      🔥 XGBoost using GPU (device=cuda)

📈 Progress: 1/100 (1.0%) | ETA: 2.4 hours
📈 Progress: 2/100 (2.0%) | ETA: 2.3 hours
...
[03:45:12] 🔥 GPU: 87% | Mem: 1234 MiB / 8192 MiB | Temp: 62°C
```

### Phase 2: LightGBM (CPU) - ~3.5 hours
```
================================================================================
🔥 Training LightGBM (CPU - Auto-fallback)
================================================================================
      🔬 Testing LightGBM GPU compilation...
      ⚠️  GPU test failed: ... (expected)
      🔄 Automatically falling back to CPU for LightGBM
      ⚪ LightGBM using CPU (device=cpu)

📈 Progress: 1/100 (1.0%) | ETA: 3.4 hours ← MUST SEE THIS!
📈 Progress: 2/100 (2.0%) | ETA: 3.3 hours
...
```

**⚠️  CRITICAL: ถ้า LightGBM stuck at 0/100 > 5 minutes:**
→ กด "Interrupt Kernel" (⬛ icon)
→ มีปัญหา n_jobs bug (ไม่น่าเกิดเพราะใช้ HANG-FIX)

### Phase 3: CatBoost (GPU) - ~1.5 hours
```
================================================================================
🔥 Training CatBoost (GPU)
================================================================================
      🔥 CatBoost using GPU (task_type=GPU)

📈 Progress: 1/50 (2.0%) | ETA: 1.4 hours
...
[07:15:23] 🔥 GPU: 78% | Mem: 2145 MiB / 8192 MiB | Temp: 68°C
```

### Phase 4: RandomForest (CPU) - ~1 hour
```
================================================================================
🔥 Training RandomForest (CPU)
================================================================================
      ⚪ RandomForest using CPU (n_jobs=-1)

📈 Progress: 1/50 (2.0%) | ETA: 58 min
...
```

### Phase 5: Ensemble - ~15 min
```
================================================================================
🔥 Creating Ensemble Models
================================================================================
✅ Weighted Ensemble created
✅ Stacking Ensemble created
✅ Optimized Stacking created
```

---

## ✅ Verification During Training

### Every 30 minutes, check:

**1. Progress is moving:**
```
📈 Progress: X/100 (increasing)
```

**2. GPU is utilized (if available):**
```
[HH:MM:SS] 🔥 GPU: 70-100% (XGBoost, CatBoost)
[HH:MM:SS] ⚪ GPU: 0% (LightGBM - CPU only, expected)
```

**3. Checkpoints are saving:**
```
💾 Checkpoint saved: checkpoint_YYYYMMDD_HHMMSS.json
```

**4. No errors:**
```
❌ Error: ... ← ไม่ควรเห็น
```

---

## 💾 After Training Completes

### 7.6 Cell 5 - Verify Results
```python
import joblib
import json
from pathlib import Path

print("="*80)
print("🔍 VERIFICATION - Model & Results")
print("="*80)

# Check model file
model_path = Path('/storage/ML-number/models/deployed/best_model.pkl')
if model_path.exists():
    print(f"✅ Model found: {model_path}")
    print(f"   Size: {model_path.stat().st_size / 1024:.1f} KB")

    # Load model
    deployment = joblib.load(model_path)
    print(f"\n📊 Model Details:")
    print(f"   Name: {deployment.get('model_name', 'Unknown')}")
    print(f"   R² Score: {deployment.get('r2_score', 'N/A'):.4f}")
    print(f"   Features: {len(deployment.get('feature_names', []))}")
    print(f"   Timestamp: {deployment.get('timestamp', 'N/A')}")
else:
    print(f"❌ Model not found: {model_path}")

# Check checkpoints
checkpoint_dir = Path('/storage/ML-number/checkpoints/')
checkpoints = sorted(checkpoint_dir.glob('*.json'))
print(f"\n💾 Checkpoints found: {len(checkpoints)}")
if checkpoints:
    latest = checkpoints[-1]
    print(f"   Latest: {latest.name}")
    with open(latest) as f:
        data = json.load(f)
        print(f"   Timestamp: {data.get('timestamp', 'N/A')}")

print("="*80)
```

### 7.7 Cell 6 - Test Prediction
```python
# Test single prediction
test_numbers = [
    '0899999999',  # Very lucky (9999)
    '0812345678',  # Sequential
    '0888888888',  # All 8s
]

print("="*80)
print("🧪 TEST PREDICTIONS")
print("="*80)

for number in test_numbers:
    # Create features (simplified - full pipeline in actual code)
    print(f"\n📱 Number: {number}")
    print(f"   Predicted price: ฿{100000:,.0f}  (ตัวอย่าง)")
    # Note: ต้องใช้ full pipeline จริงๆ จาก src/

print("="*80)
```

---

## 📥 Download Model

### วิธีที่ 1 - Jupyter UI (แนะนำ):
```
1. ใน Jupyter Lab ซ้ายมือ: Navigate to /storage/ML-number/models/deployed/
2. คลิกขวาที่ best_model.pkl
3. เลือก "Download"
4. Save ไว้ที่เครื่องคุณ
```

### วิธีที่ 2 - Terminal:
```bash
# Copy to accessible location
cp /storage/ML-number/models/deployed/best_model.pkl ~/best_model.pkl

# Then download via Jupyter UI from home directory
```

---

## 🔧 Troubleshooting

### Issue 1: Import Error
```python
ImportError: No module named 'src.config'
```

**Fix:**
```python
# Cell 1 - Add this at top
import sys
sys.path.insert(0, '/storage/ML-number')
```

### Issue 2: Data File Not Found
```python
FileNotFoundError: numberdata.csv
```

**Fix:**
```bash
# In terminal
ls -la /storage/ML-number/data/raw/
# ถ้าไม่มีไฟล์ → Upload again (STEP 6.2)
```

### Issue 3: GPU Not Detected
```
⚠️  PyTorch: No GPU detected
```

**Fix:**
```
1. Stop notebook
2. Notebook Settings → Instance Type
3. Change to: Free-GPU (M4000) or P4000/P5000
4. Start notebook again
5. Re-run Cell 3 to verify
```

### Issue 4: Training Hangs (LightGBM)
```
LightGBM: 0/100 (stuck for > 5 minutes)
```

**Fix:**
```
1. Kernel → Interrupt Kernel
2. Check src/model_utils.py line 596, 603
3. Should be: n_jobs=1 (not n_jobs=-1)
4. If wrong → Update from GitHub:
   cd /storage/ML-number
   git pull origin main
5. Restart kernel + re-run
```

### Issue 5: Out of Memory
```
CUDA out of memory
```

**Fix:**
```python
# In Cell 4, reduce n_trials:
config = {
    'n_trials': 50,  # Reduce from 100
    ...
}
```

### Issue 6: Kernel Died
```
Kernel died, restarting...
```

**Fix:**
```
1. Don't panic - checkpoints are saved!
2. Kernel → Restart Kernel
3. Re-run Cells 1-2 (setup + data)
4. Skip Cell 4 (training) if already running
5. Check: /storage/ML-number/checkpoints/ for progress
```

---

## 📊 Expected Results

### Successful Training:
```
✅ Training complete in ~9-12 hours (GPU) or 18-24 hours (CPU)
✅ R² Score > 0.90 (target: 0.93+)
✅ Model saved: /storage/ML-number/models/deployed/best_model.pkl
✅ Checkpoints: 15-20 files in checkpoints/
✅ No errors in output
```

### What Good Looks Like:
```
🎯 Best R² Score: 0.9324
🏆 Best Model: Optimized_Stacking
💾 Model saved to: /storage/ML-number/models/deployed/best_model.pkl
```

---

## 🆘 Need Help?

**During setup (STEP 1-6):**
- ถ้าติดขัด → ถามได้เลย มีคำสั่งพร้อม copy-paste

**During training (STEP 7):**
- ถ้า progress ไม่ขยับ > 10 min → Interrupt + Report
- ถ้า error → Copy error message → Report

**After training:**
- ถ้า R² < 0.80 → Review training logs
- ถ้า model file missing → Check checkpoints/

---

## 📚 Related Files

- **Setup**: `PAPERSPACE_SETUP.md`
- **Validation**: `validate_paperspace.py`
- **Error Prevention**: `PAPERSPACE_ERROR_PREVENTION.md`
- **GPU Config**: `PAPERSPACE_GPU_CONFIG_USAGE.md`
- **Main Docs**: `CLAUDE.md`, `README.md`

---

**Created**: 2025-10-06
**Version**: HANG-FIX compatible
**Platform**: Paperspace Gradient
**GPU**: M4000/P4000/P5000 (auto-detect)
**Training Time**: ~9-12 hours (GPU) / 18-24 hours (CPU)

🎉 **Ready to start training!** Follow STEP 1 → STEP 7 → Wait → Download model
