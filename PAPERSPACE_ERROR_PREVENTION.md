# 🔍 Paperspace - Error Prediction & Prevention Guide

**Session 008F - SMARTFIX for Paperspace**
**Created**: 2025-10-05
**Status**: Error prevention analysis complete

---

## 🎯 Overview

คู่มือนี้ predict errors ทั้งหมดที่อาจเกิดบน Paperspace และวิธีแก้ **ก่อนที่จะรัน**

---

## ⚠️ Critical Errors (จะเกิดแน่นอนถ้าไม่แก้!)

### Error 1: Import Path Error 🔴 **CRITICAL**

**สาเหตุ:**
```python
# Paperspace path structure
/notebooks/            # ← Working directory (ephemeral)
/storage/number-ML/    # ← Persistent storage
```

Python อยู่ที่ `/notebooks` แต่ code อยู่ที่ `/storage/number-ML/src`

**Error ที่จะเจอ:**
```python
ModuleNotFoundError: No module named 'src'
ModuleNotFoundError: No module named 'config'
ModuleNotFoundError: No module named 'data_handler'
```

**แก้ไข (3 วิธี):**

#### วิธีที่ 1: เพิ่ม sys.path (แนะนำ!)
```python
# Cell 1 ของทุก notebook
import sys
import os

# Add project path
project_path = '/storage/number-ML'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Verify
print(f"✅ Python path updated: {project_path}")

# Now imports work
from src.config import CONFIG
from src.data_handler import load_and_clean_data
```

#### วิธีที่ 2: Change working directory
```python
# Cell 1
import os
os.chdir('/storage/number-ML')

# Now relative imports work
from src.config import CONFIG
```

#### วิธีที่ 3: Absolute imports everywhere
```python
# แก้ทุกไฟล์ใน src/ ใช้ absolute imports
# src/train_production.py
from src.config import CONFIG  # ← absolute
from src.model_utils import optimize_xgboost  # ← absolute

# Instead of
from config import CONFIG  # ← relative (จะ error!)
```

**ที่ต้องแก้:**
- ✅ ทุก notebook ต้องมี sys.path.insert
- ✅ หรือแก้ทุกไฟล์ใช้ absolute imports

---

### Error 2: Data File Not Found 🔴 **CRITICAL**

**สาเหตุ:**
```python
# Code อ่านจาก relative path
df = pd.read_csv('data/raw/numberdata.csv')  # ← ERROR!
```

Paperspace ไม่รู้ว่า path อยู่ไหน

**Error ที่จะเจอ:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/raw/numberdata.csv'
```

**แก้ไข:**

```python
# ใช้ absolute path
data_path = '/storage/number-ML/data/raw/numberdata.csv'
df = pd.read_csv(data_path)

# หรือใช้ config
from src.config import DATA_PATH
data_file = os.path.join(DATA_PATH, 'raw/numberdata.csv')
df = pd.read_csv(data_file)
```

**ที่ต้องแก้:**
- ✅ `src/config.py` - ตั้ง BASE_PATH = '/storage/number-ML'
- ✅ ทุกไฟล์ที่อ่าน data - ใช้ absolute path

---

### Error 3: CUDA/GPU Not Available 🟡 **WARNING**

**สาเหตุ:**
- Notebook settings ไม่ได้เลือก GPU
- หรือ queue รอ GPU อยู่

**Error ที่จะเจอ:**
```python
RuntimeError: CUDA error: no CUDA-capable device is detected
RuntimeError: Expected all tensors to be on the same device, but found at least two devices, cuda:0 and cpu!
```

**แก้ไข:**

```python
# Cell 1: GPU availability check
import torch

def check_gpu_availability():
    """Check if GPU is available and ready"""
    if not torch.cuda.is_available():
        print("⚠️  WARNING: GPU not available!")
        print("   Solutions:")
        print("   1. Check Notebook Settings → Instance Type = Free-GPU or Pro")
        print("   2. Wait for queue (5-30 minutes)")
        print("   3. Continue with CPU (slower)")
        return False

    gpu_name = torch.cuda.get_device_name(0)
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)

    print(f"✅ GPU Available: {gpu_name}")
    print(f"✅ GPU Memory: {gpu_memory:.1f} GB")

    # Determine tier
    if 'M4000' in gpu_name:
        print("ℹ️  Detected: Paperspace Free tier (M4000)")
    elif 'P5000' in gpu_name or 'P4000' in gpu_name:
        print("ℹ️  Detected: Paperspace Pro tier ($8/month)")
    elif 'RTX' in gpu_name:
        print("ℹ️  Detected: Paperspace Growth tier")

    return True

# Run check
gpu_ok = check_gpu_availability()

# Auto-configure
use_gpu = gpu_ok  # Will be False if GPU not available
```

**SMARTFIX Auto-Fallback:**
- LightGBM จะ test GPU และ fallback เป็น CPU อัตโนมัติ
- ไม่ต้องกังวล - training จะทำงานได้แน่นอน

---

### Error 4: Checkpoint Directory Not Found 🟡 **WARNING**

**สาเหตุ:**
```python
# Code พยายามเขียน checkpoint
checkpoint_path = 'checkpoints/checkpoint_trial_10.pkl'  # ← relative path
joblib.dump(model, checkpoint_path)  # ← ERROR!
```

**Error ที่จะเจอ:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'checkpoints/'
```

**แก้ไข:**

```python
# สร้าง directory ก่อนเขียน
import os
from pathlib import Path

checkpoint_dir = '/storage/number-ML/checkpoints'
Path(checkpoint_dir).mkdir(parents=True, exist_ok=True)

# ตอนนี้เขียนได้แล้ว
checkpoint_path = os.path.join(checkpoint_dir, 'checkpoint_trial_10.pkl')
joblib.dump(model, checkpoint_path)
```

**ที่ต้องแก้:**
- ✅ `setup_paperspace.py` - สร้าง directories ทั้งหมด
- ✅ หรือเพิ่ม `Path(...).mkdir()` ก่อนเขียนไฟล์

---

### Error 5: Storage Full (5 GB Limit) 🟡 **WARNING**

**สาเหตุ:**
- Paperspace Free tier = 5 GB เท่านั้น!
- Checkpoint files + models + data = เกิน 5 GB

**Error ที่จะเจอ:**
```
OSError: [Errno 28] No space left on device
```

**แก้ไข:**

```python
# Monitor storage before training
import subprocess

def check_storage():
    """Check /storage disk usage"""
    result = subprocess.run(
        ['df', '-h', '/storage'],
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Parse usage
    lines = result.stdout.strip().split('\n')
    if len(lines) > 1:
        parts = lines[1].split()
        used = parts[2]
        avail = parts[3]
        percent = parts[4]

        print(f"\n📊 Storage Status:")
        print(f"   Used: {used}")
        print(f"   Available: {avail}")
        print(f"   Usage: {percent}")

        # Warning if > 80%
        usage_pct = int(percent.rstrip('%'))
        if usage_pct > 80:
            print(f"\n⚠️  WARNING: Storage > 80% full!")
            print("   Clean up old files before training")

# Run before training
check_storage()
```

**Auto-cleanup:**
```python
# Keep only last 3 checkpoints
import glob

def cleanup_old_checkpoints(keep_last=3):
    """Delete old checkpoints, keep only recent ones"""
    checkpoints = sorted(glob.glob('/storage/number-ML/checkpoints/*.pkl'))

    if len(checkpoints) > keep_last:
        for old_file in checkpoints[:-keep_last]:
            os.remove(old_file)
            print(f"🗑️  Deleted: {os.path.basename(old_file)}")

# Run after each training
cleanup_old_checkpoints(keep_last=3)
```

**Solution for Pro tier:**
- Upgrade to $8/month = 50 GB storage
- No storage issues!

---

## 🟢 Potential Errors (อาจเกิด - ขึ้นกับสถานการณ์)

### Error 6: LightGBM GPU Compilation Hang

**สาเหตุ:**
- OpenCL compatibility (same as Kaggle)

**Error ที่จะเจอ:**
```
"1 warning generated" infinitely
GPU: 1% IDLE
Progress: 0/100 (frozen)
```

**แก้ไข:**
✅ **SMARTFIX already handles this!**
- GPU test with 30-second timeout
- Auto-fallback to CPU if fails
- User notification

No manual fix needed!

---

### Error 7: Dependencies Not Installed

**สาเหตุ:**
- ไม่ได้รัน `pip install -r requirements.txt`
- หรือ requirements.txt missing

**Error ที่จะเจอ:**
```python
ModuleNotFoundError: No module named 'xgboost'
ModuleNotFoundError: No module named 'lightgbm'
```

**แก้ไข:**

```python
# Cell 1: Install dependencies first
!pip install -q -r /storage/number-ML/requirements.txt

# Verify imports
try:
    import xgboost
    import lightgbm
    import catboost
    print("✅ All ML libraries installed")
except ImportError as e:
    print(f"❌ Missing library: {e}")
    print("   Run: !pip install <missing-library>")
```

---

### Error 8: Model File Too Large

**สาเหตุ:**
- Ensemble model > 100 MB
- Download ช้า หรือ timeout

**Error ที่จะเจอ:**
```
Browser timeout during download
Gateway timeout 504
```

**แก้ไข:**

```python
# Compress model before download
import joblib
import gzip

model_path = '/storage/number-ML/models/deployed/best_model.pkl'
compressed_path = model_path + '.gz'

# Save + compress
with gzip.open(compressed_path, 'wb') as f:
    joblib.dump(model, f)

print(f"📦 Compressed model: {compressed_path}")
print(f"   Size: {os.path.getsize(compressed_path) / (1024**2):.1f} MB")

# Download compressed file (smaller, faster)
```

---

## ✅ Pre-Flight Validation Script

รัน script นี้ **ก่อนเริ่ม training** เพื่อ check ทุกอย่าง:

```python
"""
Paperspace Pre-Flight Validation
Run this BEFORE training to catch all errors early
"""

import os
import sys
import subprocess
from pathlib import Path

def validate_paperspace_environment():
    """Validate Paperspace setup - catch errors before training"""

    print("="*80)
    print("🔍 PAPERSPACE PRE-FLIGHT VALIDATION")
    print("="*80)

    errors = []
    warnings = []

    # 1. Check Python path
    print("\n1️⃣  Checking Python path...")
    project_path = '/storage/number-ML'
    if project_path not in sys.path:
        errors.append("Project path not in sys.path")
        print(f"   ❌ {project_path} not in sys.path")
        print(f"      Fix: sys.path.insert(0, '{project_path}')")
    else:
        print(f"   ✅ Python path configured correctly")

    # 2. Check data file exists
    print("\n2️⃣  Checking data file...")
    data_file = '/storage/number-ML/data/raw/numberdata.csv'
    if not os.path.exists(data_file):
        errors.append(f"Data file not found: {data_file}")
        print(f"   ❌ Data file missing: {data_file}")
    else:
        size_mb = os.path.getsize(data_file) / (1024**2)
        print(f"   ✅ Data file found ({size_mb:.1f} MB)")

    # 3. Check GPU availability
    print("\n3️⃣  Checking GPU...")
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print(f"   ✅ GPU: {gpu_name} ({gpu_mem:.1f} GB)")
        else:
            warnings.append("GPU not available - training will be slower on CPU")
            print(f"   ⚠️  GPU not available (will use CPU)")
    except ImportError:
        errors.append("PyTorch not installed")
        print(f"   ❌ PyTorch not installed")

    # 4. Check storage space
    print("\n4️⃣  Checking storage...")
    result = subprocess.run(
        ['df', '-h', '/storage'],
        capture_output=True,
        text=True
    )
    lines = result.stdout.strip().split('\n')
    if len(lines) > 1:
        parts = lines[1].split()
        avail = parts[3]
        percent = parts[4]
        usage_pct = int(percent.rstrip('%'))

        print(f"   Storage: {avail} available ({100-usage_pct}% free)")

        if usage_pct > 80:
            warnings.append(f"Storage > 80% full ({percent})")
            print(f"   ⚠️  Storage > 80% full - clean up files")
        else:
            print(f"   ✅ Storage OK")

    # 5. Check imports
    print("\n5️⃣  Checking ML libraries...")
    required_libs = ['xgboost', 'lightgbm', 'catboost', 'optuna', 'sklearn']
    missing_libs = []

    for lib in required_libs:
        try:
            __import__(lib)
            print(f"   ✅ {lib}")
        except ImportError:
            missing_libs.append(lib)
            print(f"   ❌ {lib} (not installed)")

    if missing_libs:
        errors.append(f"Missing libraries: {', '.join(missing_libs)}")

    # 6. Check directories exist
    print("\n6️⃣  Checking directories...")
    required_dirs = [
        '/storage/number-ML/checkpoints',
        '/storage/number-ML/models/deployed',
        '/storage/number-ML/results'
    ]

    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            warnings.append(f"Directory missing: {dir_path}")
            print(f"   ⚠️  {dir_path} (will create)")
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        else:
            print(f"   ✅ {dir_path}")

    # Summary
    print("\n" + "="*80)
    print("📋 VALIDATION SUMMARY")
    print("="*80)

    if errors:
        print(f"\n❌ ERRORS FOUND ({len(errors)}):")
        for i, error in enumerate(errors, 1):
            print(f"   {i}. {error}")
        print("\n⚠️  FIX ERRORS BEFORE TRAINING!")
        return False

    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"   {i}. {warning}")
        print("\nℹ️  Warnings can be ignored, but recommended to fix")

    if not errors:
        print("\n✅ ALL CHECKS PASSED - READY TO TRAIN!")
        return True

# Run validation
validation_ok = validate_paperspace_environment()

if not validation_ok:
    print("\n🛑 Please fix errors above before training")
else:
    print("\n🚀 You're good to go!")
```

---

## 📋 Checklist: Error Prevention

**Before uploading to Paperspace:**
- [x] All imports use absolute paths (`from src.config import ...`)
- [x] `src/config.py` has `BASE_PATH = '/storage/number-ML'`
- [x] `setup_paperspace.py` creates all directories
- [x] SMARTFIX auto-fallback included
- [x] Pre-flight validation script ready

**After uploading to Paperspace:**
- [ ] Run `setup_paperspace.py` first
- [ ] Add `sys.path.insert(0, '/storage/number-ML')` to Cell 1
- [ ] Run pre-flight validation
- [ ] Check GPU availability
- [ ] Check storage space
- [ ] Install dependencies: `!pip install -r requirements.txt`

**During training:**
- [ ] Monitor storage every hour
- [ ] Check checkpoints being saved
- [ ] Verify GPU utilization (should be 70-90%)
- [ ] Watch for SMARTFIX fallback messages

---

## 🎯 Summary: Errors You WON'T See

Thanks to preparation:
- ✅ No import errors (sys.path configured)
- ✅ No file not found (absolute paths)
- ✅ No GPU hangs (SMARTFIX fallback)
- ✅ No storage full (monitoring + cleanup)
- ✅ No missing dependencies (pre-install)
- ✅ No checkpoint errors (directories created)

**Result:** Training runs smoothly from start to finish! 🚀

---

**Created**: 2025-10-05
**Session**: 008F - Paperspace Error Prevention
**Status**: ✅ All potential errors identified and prevented
