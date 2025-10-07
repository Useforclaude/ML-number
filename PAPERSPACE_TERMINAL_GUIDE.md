# 🚀 Paperspace Terminal Guide - ML Phone Number Training

**สำหรับ**: Train ML models บน Paperspace ด้วย Terminal (ไม่ใช่ Notebook)
**GPU**: Free Tier (M4000) หรือ Growth Plan (RTX A4000, P5000)
**ระดับ**: เริ่มต้นจากศูนย์
**เวอร์ชัน**: 1.0 - Initial release (2025-10-08)

---

## 📋 ภาพรวม

**คู่มือนี้จะพาคุณทำตามลำดับ:**

```
1. Clone โปรเจกต์จาก GitHub (Terminal)      → 2 นาที
2. Setup Environment + Install Deps (Terminal) → 3-5 นาที
3. Upload/Prepare Data (Jupyter UI/Terminal)   → 2 นาที
4. สร้าง Training Script (Jupyter UI)         → 3 นาที
5. รัน Training (Terminal - Background)        → 9-12 ชม. ⚡
6. Monitor Progress (Terminal)                 → ทุก 30-60 นาที
7. Download Results (Jupyter UI)               → 2 นาที
───────────────────────────────────────────────────────
รวม: ~10-15 นาที setup + 9-12 ชม. training
```

**💡 เวลา Training ขึ้นกับ GPU:**
- **RTX A4000**: 9-12 ชม. (N_TRIALS=100)
- **RTX P5000**: 7-9 ชม. (N_TRIALS=100)
- **M4000** (Free): 12-15 ชม. (N_TRIALS=100)

**🔑 จุดเด่นของ Terminal Method:**
- ✅ ปิด browser ได้ (training ทำงานต่อ)
- ✅ ไม่มี idle timeout (รันได้นานไม่จำกัด)
- ✅ Monitor progress ตอนไหนก็ได้
- ✅ Production-ready (ใช้ได้จริง)

---

## 🤔 Terminal vs Notebook - ต่างกันยังไง?

### 📊 Paperspace Jupyter Lab มี 3 ส่วน

```
┌─────────────────────────────────────────┐
│     Paperspace Jupyter Lab              │
├─────────────────────────────────────────┤
│                                         │
│  1. Jupyter UI (File Browser)          │
│     → Upload/Download files            │
│     → สร้าง/ลบไฟล์                     │
│     → ไม่ใช่ Notebook!                 │
│                                         │
│  2. Terminal (Command Line)             │
│     → รันคำสั่ง, git, python           │
│     → ใช้ส่วนนี้เป็นหลัก! ⭐          │
│                                         │
│  3. Notebook (.ipynb) [ไม่ใช้ในคู่มือนี้]│
│     → Interactive cells                │
│     → มี idle timeout                  │
│                                         │
└─────────────────────────────────────────┘
```

---

### ✅ คู่มือนี้ใช้อะไรบ้าง?

| PART | ใช้อะไร | ทำอะไร |
|------|---------|--------|
| **PART 1** | **Terminal** | Clone GitHub repo |
| **PART 2** | **Terminal** | Setup venv + install dependencies |
| **PART 3** | **Jupyter UI** | Upload numberdata.csv (optional) |
| **PART 4** | **Jupyter UI** | สร้าง training script (.py) |
| **PART 5** | **Terminal** | รัน training (background) |
| **PART 6** | **Terminal** | Monitor progress |
| **PART 7** | **Jupyter UI** | Download models + results |

**🎯 สรุป:**
- ✅ **Terminal** - รันคำสั่งทั้งหมด (หลัก!)
- ✅ **Jupyter UI** - Upload/Download files
- ❌ **Notebook (.ipynb)** - ไม่ใช้เลย!

---

### 🔍 ความแตกต่าง Terminal vs Notebook

| | **Terminal** | **Notebook (.ipynb)** |
|---|--------------|---------------------|
| **รูปแบบ** | Command line | Interactive cells |
| **รันคำสั่ง** | `python train.py` | Cell-by-cell |
| **เหมาะกับ** | Long tasks (9-12 ชม.) | Quick experiments |
| **Timeout** | ❌ ไม่มี | ✅ มี (idle → disconnect) |
| **ปิด Browser** | ✅ ได้ (process ยังทำงาน) | ❌ ไม่ได้ (kernel ตาย) |
| **GPU** | ✅ ใช้ได้เต็มที่ | ✅ ใช้ได้เต็มที่ |
| **ประสิทธิภาพ** | **⚡⚡⚡⚡⚡** | **⚡⚡⚡⚡⚡** (เหมือนกัน!) |
| **ใช้ในคู่มือ** | ✅ ใช้เป็นหลัก | ❌ ไม่ใช้ |

---

### ⚡ ประสิทธิภาพ - เหมือนกันหรือไม่?

```
✅ เหมือนกันทุกอย่าง!

ทั้ง Terminal และ Notebook ใช้:
- GPU เดียวกัน (RTX A4000)
- RAM เดียวกัน
- CPU เดียวกัน
- VRAM เดียวกัน

ไม่มีความแตกต่างด้าน performance เลย!
```

**🔍 อธิบาย:**
- Terminal: รัน `python train.py` → ใช้ Python interpreter
- Notebook: รัน cell → ใช้ Python interpreter **เดียวกัน**
- ทั้งสองเข้าถึง GPU ได้เหมือนกัน

**ตัวอย่าง:**
```bash
# Terminal
python train_terminal.py
→ ใช้ GPU RTX A4000 ✓

# Notebook cell
!python train_terminal.py
→ ใช้ GPU RTX A4000 ✓  (เหมือนกัน!)
```

---

### 🤔 ถ้าเหมือนกัน ทำไม Notebook ถึง Timeout?

**ประสิทธิภาพ (Performance) ≠ Connection Management**

**ความแตกต่างที่แท้จริง:**

```
┌─────────────────────────────────────────────┐
│           Terminal Process                  │
├─────────────────────────────────────────────┤
│                                             │
│  Browser → Paperspace Server               │
│              ↓                              │
│         Terminal (bash)                     │
│              ↓                              │
│    python train.py (รันอิสระ)              │
│              ↓                              │
│            GPU ⚡                            │
│                                             │
│  ✅ ปิด browser → process ยังทำงานต่อ!      │
│  ✅ Network ขาด → process ยังทำงานต่อ!       │
│  ✅ Idle 10 ชม. → ไม่มี timeout!           │
│                                             │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│         Notebook Cell Process               │
├─────────────────────────────────────────────┤
│                                             │
│  Browser ↔ Jupyter Kernel ↔ Python Process │
│     ↕          ↕              ↕             │
│  Activity   Heartbeat        GPU ⚡          │
│                                             │
│  ❌ ปิด browser → kernel ตาย → process หยุด!│
│  ❌ Network ขาด → kernel ตาย → process หยุด!│
│  ❌ Idle นาน → kernel timeout → process หยุด!│
│                                             │
└─────────────────────────────────────────────┘
```

---

### 💡 อธิบายแบบง่าย:

**Terminal = ส่งพัสดุ (Drop & Go)**
```
คุณส่งงาน (python train.py) → Paperspace รับไว้ → คุณปิด browser
→ งานทำต่อเอง (ไม่ต้องติดตาม)
→ เสร็จแน่นอน ✓
```

**Notebook = แท็กซี่ (Stay Connected)**
```
คุณรันงาน → ขณะทำงาน...
→ คุณปิด browser → Jupyter คิดว่าไม่มีคน → หยุดงาน ✗
→ คุณ idle นาน → Jupyter timeout → หยุดงาน ✗
→ ต้องดูแลตลอด (มี activity) → เสร็จ ✓
```

---

### 🎯 ทำไมคู่มือนี้ใช้ Terminal?

**1. เหมาะกับ Long-running Tasks**
```
ML Training 9-12 ชม. → ใช้เวลานาน
→ Terminal: ทำงานได้ต่อเนื่อง ✓
→ Notebook: อาจ timeout (ถ้า idle) ✗
```

**2. Production-ready**
```
Terminal script สามารถ:
- Deploy ได้ทันที
- รันใน CI/CD
- Automate ได้
- Scale ได้
```

**3. ไม่ต้องกังวล**
```
→ ปิด browser ได้
→ ไปทำงานอื่น
→ กลับมาเช็คตอนไหนก็ได้
→ ไม่ต้องเปิดค้างทั้งวัน
```

---

## 🌍 Platform Comparison

| Platform | Terminal/SSH | ปิด Browser ได้ | Idle Timeout | GPU ฟรี |
|----------|--------------|-----------------|--------------|---------|
| **Paperspace** | ✅ มี | ✅ ได้ | ❌ ไม่มี | ✅ มี (Free) |
| **AWS/GCP** | ✅ มี (SSH) | ✅ ได้ | ❌ ไม่มี | ❌ เสียเงิน |
| **RunPod** | ✅ มี (SSH) | ✅ ได้ | ❌ ไม่มี | ❌ เสียเงิน |
| **Google Colab** | ❌ ไม่มี | ❌ ไม่ได้ | ✅ มี (90 min) | ✅ มี (จำกัด) |
| **Kaggle** | ❌ ไม่มี | ❌ ไม่ได้ | ✅ มี (9 hr) | ✅ มี (P100) |

**💡 กฎง่ายๆ:**
```
มี Terminal access → ปิด browser ได้ ✅
ไม่มี (Colab, Kaggle) → ปิดไม่ได้ ❌
```

---

## PART 1: Clone โปรเจกต์

**⚠️ สำคัญ: ทำใน Paperspace Notebook Terminal (ไม่ใช่เครื่องของคุณ!)**

### ✅ STEP 1: เปิด Terminal

**ใน Jupyter Lab:**

```
1. ด้านล่าง File Browser → มีปุ่ม "+" (New Launcher)
2. คลิกปุ่ม "+"
3. ใน Launcher → มองหา "Other" section
4. คลิก "Terminal"
5. Terminal เปิดขึ้นมา (หน้าจอดำๆ มี prompt)
```

---

### ✅ STEP 2: เช็ค GPU 🔥 **สำคัญมาก!**

**⚠️ ขั้นตอนนี้สำคัญที่สุด! ถ้า GPU ไม่ทำงาน → Training จะช้ามาก!**

**ใน Terminal - Copy คำสั่งนี้แล้ว Paste:**

```bash
nvidia-smi
```

**กด Enter**

**ควรเห็น:**
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI xxx.xx       Driver Version: xxx.xx       CUDA Version: xx.x    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        ...          | ...                  | ...                  |
|   0  Quadro M4000       ...   | ...                  | ...                  |
+-------------------------------+----------------------+----------------------+
```

**ถ้าเห็นข้อมูล GPU → ✅ พร้อมใช้งาน → ดำเนินการต่อได้**

**ถ้าไม่เห็น → ❌ STOP! ต้องแก้ก่อน:**
1. ปิด Notebook
2. Settings → Machine → เลือก GPU machine
3. Start Notebook ใหม่
4. รัน nvidia-smi อีกครั้ง → ต้องเห็น GPU

**💡 Double-check: เช็ค PyTorch เห็น GPU มั้ย**

```bash
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

**ควรเห็น:**
```
CUDA available: True
```

---

### ✅ STEP 3: Clone โปรเจกต์

**ใน Terminal:**

```bash
# Navigate to persistent storage
cd /storage

# Clone GitHub repository
git clone https://github.com/Useforclaude/ML-number.git

# Enter project directory
cd ML-number

# Check files
ls -lh
```

**ควรเห็น:**
```
total 500K
drwxr-xr-x 2 user user 4.0K Oct  8 10:00 data
drwxr-xr-x 2 user user 4.0K Oct  8 10:00 models
-rw-r--r-- 1 user user  15K Oct  8 10:00 NEXT_SESSION.md
-rw-r--r-- 1 user user  12K Oct  8 10:00 README.md
-rw-r--r-- 1 user user 1.5K Oct  8 10:00 requirements.txt
drwxr-xr-x 2 user user 4.0K Oct  8 10:00 src
...
```

✅ **ได้โปรเจกต์แล้ว!**

---

## PART 2: Setup Environment

### ✅ STEP 4: สร้าง Virtual Environment

**ใน Terminal (อยู่ที่ /storage/ML-number):**

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# ควรเห็น (.venv) ใน prompt:
# (.venv) user@paperspace:/storage/ML-number$
```

✅ **Virtual environment พร้อมแล้ว!**

---

### ✅ STEP 5: Install Dependencies

**ใน Terminal (venv activated):**

```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# ใช้เวลา 3-5 นาที
# จะเห็น: Installing collected packages: numpy, pandas, scikit-learn, ...
```

**✅ Dependencies ติดตั้งเสร็จ!**

---

### ✅ STEP 6: Verify Installation

**เช็คว่า imports ทำงาน:**

```bash
python -c "from src.config import BASE_PATH; print(f'✅ BASE_PATH: {BASE_PATH}')"
```

**ควรเห็น:**
```
✅ BASE_PATH: /storage/ML-number
```

**เช็ค GPU support:**

```bash
python -c "import torch; print('CUDA:', torch.cuda.is_available()); import xgboost as xgb; print('XGBoost version:', xgb.__version__)"
```

**ควรเห็น:**
```
CUDA: True
XGBoost version: 1.7.6
```

✅ **Setup เสร็จสมบูรณ์!**

---

## PART 3: Prepare Data

### ✅ STEP 7: เช็คข้อมูล

**ใน Terminal:**

```bash
# Check data file
ls -lh data/raw/

# ควรเห็น numberdata.csv
```

**ถ้ามีแล้ว → ✅ ข้ามไป PART 4**

**ถ้ายังไม่มี → ต้อง upload:**

---

### ✅ STEP 8: Upload Data (ถ้าจำเป็น)

**Option 1: ใช้ Jupyter UI (ง่ายที่สุด)**

```
1. ใน File Browser → Navigate to ML-number/data/raw/
2. คลิกขวาในพื้นที่ว่าง
3. เลือก "Upload"
4. เลือกไฟล์ numberdata.csv
5. รอจนอัปโหลดเสร็จ
```

**Option 2: ใช้ wget (ถ้ามี URL)**

```bash
cd /storage/ML-number/data/raw/
wget https://your-url.com/numberdata.csv
```

**Option 3: Copy จาก Downloads (ถ้า mount แล้ว)**

```bash
cp /path/to/numberdata.csv /storage/ML-number/data/raw/
```

---

### ✅ STEP 9: Verify Data

```bash
cd /storage/ML-number
python -c "import pandas as pd; df = pd.read_csv('data/raw/numberdata.csv'); print(f'✅ Data: {len(df)} rows, {df.shape[1]} columns')"
```

**ควรเห็น:**
```
✅ Data: 6112 rows, 2 columns
```

✅ **Data พร้อมแล้ว!**

---

## PART 4: สร้าง Training Script

### ✅ STEP 10: สร้างไฟล์ Script

**ใน Jupyter UI File Browser:**

```
1. Navigate ไปที่โฟลเดอร์ ML-number/
2. คลิกขวาในพื้นที่ว่าง
3. เลือก "New File"
4. ตั้งชื่อ: train_terminal.py
5. กด Enter
```

✅ **ได้ไฟล์ `train_terminal.py` แล้ว**

---

### ✅ STEP 11: เปิดไฟล์และวาง Code

**ใน File Browser:**

```
1. Double-click ไฟล์ train_terminal.py
   → เปิด Text Editor

2. Copy code ทั้งหมดด้านล่างนี้
   → Paste ลงในไฟล์

3. กด Ctrl+S (หรือ Cmd+S บน Mac) = Save
```

**Code ที่ต้อง Copy:**

```python
#!/usr/bin/env python3
"""
Paperspace ML Training - Terminal Version
Train phone number price prediction models with GPU support
"""

import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/training_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import project modules
try:
    from src.config import BASE_PATH, MODEL_CONFIG
    from src.environment import detect_environment, setup_base_path
    from src.data_handler import load_and_clean_data
    from src.features import create_all_features
    from src.data_splitter import split_data_stratified, create_validation_set
    from src.model_utils import AdvancedPreprocessor
    from src.train_production import train_production_pipeline
    import numpy as np
    import pandas as pd
    import torch
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error("Make sure virtual environment is activated: source .venv/bin/activate")
    sys.exit(1)


def print_header():
    """Print training header"""
    print("\n" + "="*80)
    print("🚀 PAPERSPACE ML TRAINING - TERMINAL MODE")
    print("="*80)
    print(f"📂 Project: ML Phone Number Price Prediction")
    print(f"📍 Path: {BASE_PATH}")
    print(f"🖥️  Environment: {detect_environment()}")
    print(f"🎯 Target: R² > 0.90")
    print("="*80 + "\n")


def check_gpu():
    """Check GPU availability"""
    logger.info("🔍 Checking GPU...")

    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        logger.info(f"✅ GPU Available: {gpu_name}")
        logger.info(f"   Memory: {gpu_memory:.1f} GB")
        return True
    else:
        logger.warning("⚠️  No GPU detected - Training will use CPU (much slower!)")
        return False


def main():
    """Main training pipeline"""
    start_time = time.time()

    # Print header
    print_header()

    # Check GPU
    use_gpu = check_gpu()

    # Step 1: Load data
    logger.info("\n" + "="*80)
    logger.info("STEP 1: Loading Data")
    logger.info("="*80)

    try:
        df_cleaned = load_and_clean_data()
        logger.info(f"✅ Data loaded: {len(df_cleaned)} rows")
    except Exception as e:
        logger.error(f"❌ Failed to load data: {e}")
        return 1

    # Step 2: Feature engineering
    logger.info("\n" + "="*80)
    logger.info("STEP 2: Feature Engineering")
    logger.info("="*80)

    try:
        X, y_log, sample_weights = create_all_features(df_cleaned)
        logger.info(f"✅ Features created: {X.shape[1]} features, {X.shape[0]} samples")
    except Exception as e:
        logger.error(f"❌ Failed to create features: {e}")
        return 1

    # Step 3: Split data
    logger.info("\n" + "="*80)
    logger.info("STEP 3: Train/Test Split")
    logger.info("="*80)

    try:
        X_train, X_test, y_log_train, y_log_test, sw_train, sw_test = split_data_stratified(
            X, y_log, sample_weights,
            test_size=0.2,
            random_state=42
        )
        logger.info(f"✅ Split complete: Train={len(X_train)}, Test={len(X_test)}")
    except Exception as e:
        logger.error(f"❌ Failed to split data: {e}")
        return 1

    # Step 4: Convert to actual prices
    logger.info("\n" + "="*80)
    logger.info("STEP 4: Converting to Actual Prices")
    logger.info("="*80)

    y_train = pd.Series(np.expm1(y_log_train))
    y_test = pd.Series(np.expm1(y_log_test))
    logger.info(f"✅ Train prices: ฿{y_train.min():,.0f} - ฿{y_train.max():,.0f}")
    logger.info(f"✅ Test prices: ฿{y_test.min():,.0f} - ฿{y_test.max():,.0f}")

    # Step 5: Create validation set
    logger.info("\n" + "="*80)
    logger.info("STEP 5: Creating Validation Set")
    logger.info("="*80)

    try:
        X_tr, X_val, y_tr, y_val, sw_tr, sw_val = create_validation_set(
            X_train, y_train, sw_train,
            val_size=0.15,
            random_state=42
        )
        logger.info(f"✅ Validation set: Train={len(X_tr)}, Val={len(X_val)}")
    except Exception as e:
        logger.error(f"❌ Failed to create validation set: {e}")
        return 1

    # Step 6: Preprocessing
    logger.info("\n" + "="*80)
    logger.info("STEP 6: Preprocessing")
    logger.info("="*80)

    try:
        preprocessor = AdvancedPreprocessor()
        X_tr_processed = preprocessor.fit_transform(X_tr)
        X_val_processed = preprocessor.transform(X_val)
        X_test_processed = preprocessor.transform(X_test)

        # Clean NaN/Inf
        for df in [X_tr_processed, X_val_processed, X_test_processed]:
            df.replace([np.inf, -np.inf], np.nan, inplace=True)
            if hasattr(df, 'median'):
                df.fillna(df.median(), inplace=True)
            else:
                df.fillna(X_tr_processed.median(), inplace=True)

        logger.info(f"✅ Preprocessed: {X_tr_processed.shape[1]} features")
    except Exception as e:
        logger.error(f"❌ Failed to preprocess: {e}")
        return 1

    # Step 7: PRODUCTION TRAINING
    logger.info("\n" + "="*80)
    logger.info("🔥 STEP 7: PRODUCTION TRAINING")
    logger.info("="*80)
    logger.info(f"⏱️  Expected duration: 9-12 hours")
    logger.info(f"🎯 Optimization trials: {MODEL_CONFIG.get('optuna_trials', 100)}")
    logger.info(f"🔥 GPU enabled: {use_gpu}")
    logger.info("="*80 + "\n")

    training_start = time.time()

    try:
        results = train_production_pipeline(
            X_tr_processed, y_tr,
            X_val_processed, y_val,
            optimize=True,
            n_trials=MODEL_CONFIG.get('optuna_trials', 100),
            use_gpu=use_gpu,
            verbose=True
        )

        training_time = (time.time() - training_start) / 3600

        # Final results
        logger.info("\n" + "="*80)
        logger.info("✅ TRAINING COMPLETE!")
        logger.info("="*80)
        logger.info(f"⏱️  Training Time: {training_time:.2f} hours")
        logger.info(f"🏆 Best Model: {results['best_model_name']}")
        logger.info(f"📊 Best R²: {results['best_score']:.4f}")
        logger.info(f"📉 MAE: {results['best_mae']:.2f}")
        logger.info(f"📉 RMSE: {results['best_rmse']:.2f}")
        logger.info("="*80)

        # Total time
        total_time = (time.time() - start_time) / 3600
        logger.info(f"\n⏱️  Total Time: {total_time:.2f} hours")
        logger.info("✅ All done! Models saved to models/ directory")

        return 0

    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    # Create logs directory
    os.makedirs("logs", exist_ok=True)

    # Run training
    exit_code = main()
    sys.exit(exit_code)
```

**กด Save (Ctrl+S)**

✅ **Script พร้อมแล้ว!**

---

## PART 5: รัน Training (Background)

### ✅ STEP 12: รัน Training ใน Background

**ใน Terminal (venv activated, อยู่ที่ /storage/ML-number):**

```bash
# Make script executable
chmod +x train_terminal.py

# Run in background with nohup
nohup python train_terminal.py > training_output.log 2>&1 &

# ได้ Process ID (PID) กลับมา เช่น:
# [1] 12345
```

**ความหมาย:**
- `nohup` = ทำงานต่อแม้ปิด terminal
- `> training_output.log` = บันทึก output ลงไฟล์
- `2>&1` = รวม stderr กับ stdout
- `&` = รันใน background

✅ **Training เริ่มแล้ว! สามารถปิด browser ได้!**

---

### ✅ STEP 13: เช็คว่ารันอยู่

**เช็ค process:**

```bash
ps aux | grep train_terminal
```

**ควรเห็น:**
```
user   12345  5.2 12.3  8123456 2048000 ?  R  10:30  1:23 python train_terminal.py
```

**เช็คว่า GPU ทำงาน:**

```bash
nvidia-smi
```

**ควรเห็น GPU Utilization > 0%:**
```
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|    0     12345      C   python                                     3456MiB |
+-----------------------------------------------------------------------------+
```

✅ **Training ทำงานปกติ!**

---

## PART 6: Monitor Progress

### ✅ STEP 14: ดู Log แบบ Real-time

**Option 1: tail -f (แนะนำ)**

```bash
tail -f training_output.log
```

**จะเห็น:**
```
2025-10-08 10:30:15 - INFO - ================================================================================
2025-10-08 10:30:15 - INFO - 🚀 PAPERSPACE ML TRAINING - TERMINAL MODE
2025-10-08 10:30:15 - INFO - ================================================================================
2025-10-08 10:30:16 - INFO - ✅ GPU Available: Quadro M4000
2025-10-08 10:30:17 - INFO - ✅ Data loaded: 6112 rows
2025-10-08 10:30:20 - INFO - ✅ Features created: 256 features, 6112 samples
2025-10-08 10:32:15 - INFO - 🔬 Optimizing XGBoost (100 trials)...
2025-10-08 10:32:20 - INFO - [0/100] Trial 0: R² = 0.8245
2025-10-08 10:32:25 - INFO - [1/100] Trial 1: R² = 0.8512
...
```

**กด Ctrl+C เพื่อหยุดดู (training ยังทำงานต่อ)**

---

**Option 2: less (scroll ได้)**

```bash
less +F training_output.log
```

**กด Ctrl+C เพื่อหยุด scroll → สามารถ scroll ขึ้น-ลงได้**
**กด Shift+F เพื่อกลับ follow mode**
**กด Q เพื่อออก**

---

**Option 3: head/tail (ดูบางส่วน)**

```bash
# ดู 50 บรรทัดแรก
head -50 training_output.log

# ดู 50 บรรทัดสุดท้าย
tail -50 training_output.log

# ดู 100 บรรทัดสุดท้าย
tail -100 training_output.log
```

---

### ✅ STEP 15: เช็คความคืบหน้า

**เช็คว่าถึง Trial ไหนแล้ว:**

```bash
grep -oP '\[\d+/\d+\]' training_output.log | tail -10
```

**ผลลัพธ์:**
```
[45/100]
[46/100]
[47/100]
...
```

---

**เช็ค R² score ล่าสุด:**

```bash
grep "R² =" training_output.log | tail -10
```

**ผลลัพธ์:**
```
Trial 45: R² = 0.8934
Trial 46: R² = 0.9012
Trial 47: R² = 0.8987
...
```

---

**เช็คเวลาที่ใช้ไป:**

```bash
grep "Training Time" training_output.log
```

**ผลลัพธ์:**
```
Training Time: 3.45 hours
```

---

### ✅ STEP 16: Monitor GPU Usage

**เช็ค GPU Utilization:**

```bash
watch -n 5 nvidia-smi
```

**อัปเดตทุก 5 วินาที**
**กด Ctrl+C เพื่อหยุด**

---

### ✅ STEP 17: Estimate Time Remaining

**Timeline ทั่วไป:**

```
XGBoost optimization:    2.5-3.5 hours (100 trials)
LightGBM optimization:   3-4 hours (100 trials)
CatBoost optimization:   1.5-2 hours (100 trials)
RandomForest:            1-1.5 hours (100 trials)
Ensemble:                15-30 minutes
───────────────────────────────────────────
Total:                   9-12 hours
```

**ดูว่าอยู่ขั้นตอนไหน:**

```bash
grep "Optimizing" training_output.log | tail -1
```

---

## PART 7: Download Results

### ✅ STEP 18: เช็คว่า Training เสร็จ

**เช็ค log:**

```bash
tail -20 training_output.log
```

**ควรเห็น:**
```
✅ TRAINING COMPLETE!
================================================================================
⏱️  Training Time: 10.23 hours
🏆 Best Model: XGBoost
📊 Best R²: 0.9234
📉 MAE: 0.0234
📉 RMSE: 0.0456
================================================================================
⏱️  Total Time: 10.45 hours
✅ All done! Models saved to models/ directory
```

✅ **Training เสร็จสมบูรณ์!**

---

### ✅ STEP 19: เช็ค Models

```bash
ls -lh models/deployed/
```

**ควรเห็น:**
```
total 50M
-rw-r--r-- 1 user user  25M Oct  8 20:30 best_model.pkl
-rw-r--r-- 1 user user  15M Oct  8 20:30 xgboost_model.pkl
-rw-r--r-- 1 user user  10M Oct  8 20:30 ensemble_model.pkl
...
```

---

### ✅ STEP 20: Download Files (Jupyter UI)

**ใน Jupyter File Browser:**

```
1. Navigate to ML-number/models/deployed/
2. คลิกขวาที่ best_model.pkl
3. เลือก "Download"
4. ไฟล์จะดาวน์โหลดไปที่เครื่องคุณ
```

**Download ไฟล์ที่สำคัญ:**
- `models/deployed/best_model.pkl` (โมเดลที่ดีที่สุด)
- `training_output.log` (log ทั้งหมด)
- `logs/training_*.log` (detailed log)
- `results/` (ผลลัพธ์ทั้งหมด)

✅ **ดาวน์โหลดเสร็จสมบูรณ์!**

---

## 🎯 สรุป Timeline

```
┌─────────────────────────────────────────────┐
│           Full ML Training Timeline         │
├─────────────────────────────────────────────┤
│                                             │
│  PART 1-3: Setup (10-15 นาที)              │
│  ├─ Clone repo (2 min)                      │
│  ├─ Install deps (3-5 min)                  │
│  └─ Upload data (2 min)                     │
│                                             │
│  PART 4: Create script (5 นาที)            │
│  ├─ Create file (1 min)                     │
│  └─ Paste code (1 min)                      │
│                                             │
│  PART 5: Start training (1 นาที)           │
│  └─ nohup python train.py &                 │
│                                             │
│  → ปิด browser ได้! 🎉                     │
│                                             │
│  PART 6: Training (9-12 ชม.)               │
│  ├─ XGBoost (2.5-3.5 hr)                    │
│  ├─ LightGBM (3-4 hr)                       │
│  ├─ CatBoost (1.5-2 hr)                     │
│  ├─ RandomForest (1-1.5 hr)                 │
│  └─ Ensemble (15-30 min)                    │
│                                             │
│  → เช็คได้ตอนไหนก็ได้ (tail -f log)        │
│                                             │
│  PART 7: Download (5 นาที)                 │
│  └─ Download models + logs                  │
│                                             │
└─────────────────────────────────────────────┘

Total hands-on time: ~20-30 นาที
Total training time: 9-12 ชม. (ไม่ต้องดูแล!)
```

---

## 🛠️ Troubleshooting

### ปัญหา 1: Training ไม่รัน

**อาการ:** รัน `nohup python train_terminal.py &` แล้วไม่เห็น process

**วิธีแก้:**
```bash
# เช็ค error ใน log
cat training_output.log

# เช็คว่า venv active
which python
# ควรเห็น: /storage/ML-number/.venv/bin/python

# ถ้าไม่ใช่ → activate ใหม่
source .venv/bin/activate
```

---

### ปัญหา 2: GPU ไม่ทำงาน

**อาการ:** nvidia-smi เห็น GPU แต่ training ไม่ใช้

**วิธีแก้:**
```bash
# เช็ค PyTorch CUDA
python -c "import torch; print(torch.cuda.is_available())"

# ถ้าเป็น False → ติดตั้ง PyTorch ใหม่
pip uninstall torch -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

### ปัญหา 3: Process หยุดเอง

**อาการ:** เช็ค `ps aux | grep train` ไม่เห็น process

**วิธีแก้:**
```bash
# ดู log หา error
tail -100 training_output.log

# เช็ค exit code
echo $?

# ถ้าเป็น OOM (Out of Memory)
# → ลด N_TRIALS หรือลด features
```

---

### ปัญหา 4: ปิด Terminal แล้ว process หยุด

**อาการ:** ปิด Terminal → training หยุด

**วิธีแก้:**
```bash
# ต้องใช้ nohup!
nohup python train_terminal.py > training_output.log 2>&1 &

# ไม่ใช่:
python train_terminal.py  # ← จะหยุดเมื่อปิด terminal
```

---

### ปัญหา 5: ไม่เห็น log อัปเดต

**อาการ:** tail -f ไม่เห็นอะไรเลย

**วิธีแก้:**
```bash
# Python อาจ buffer output
# เช็คว่า process ยังทำงานมั้ย
ps aux | grep train_terminal

# ถ้ายังทำงาน → ลอง cat
cat training_output.log

# หรือใช้ -u flag (unbuffered)
nohup python -u train_terminal.py > training_output.log 2>&1 &
```

---

## 📊 GPU Performance Comparison

| GPU Model | Training Time | Cost | Availability |
|-----------|---------------|------|--------------|
| **RTX 5000 Ada** | 7-8 hours | Growth Plan | High |
| **RTX A4000** | 9-10 hours | Growth Plan | High |
| **RTX P5000** | 9-10 hours | Growth Plan | Medium |
| **M4000** (Free) | 12-15 hours | Free | High |

**💡 แนะนำ:**
- **RTX A4000**: ดีที่สุดสำหรับ Growth Plan (ราคา/ประสิทธิภาพ)
- **M4000** (Free): ใช้ได้ แต่ช้ากว่า ~30-40%

---

## 🎯 Next Steps

**หลัง Training เสร็จ:**

1. **ทดสอบโมเดล:**
```bash
python scripts/predict_single.py 0899999999
```

2. **Batch Prediction:**
```bash
python scripts/batch_predict.py input.csv
```

3. **Deploy API:**
```bash
python main.py --deploy --api-type fastapi --port 8000
```

---

## ✅ Checklist

**Setup (PART 1-3):**
- [ ] GPU detected (`nvidia-smi`)
- [ ] Repository cloned (`/storage/ML-number`)
- [ ] Virtual environment created (`.venv`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Data uploaded (`data/raw/numberdata.csv`)
- [ ] Imports working (`from src.config import BASE_PATH`)

**Training (PART 4-5):**
- [ ] Script created (`train_terminal.py`)
- [ ] Training started (`nohup python train_terminal.py &`)
- [ ] Process running (`ps aux | grep train`)
- [ ] GPU active (`nvidia-smi`)
- [ ] Log updating (`tail -f training_output.log`)

**Monitoring (PART 6):**
- [ ] Progress visible (`grep Trial training_output.log`)
- [ ] GPU utilized (>50% in `nvidia-smi`)
- [ ] No errors in log

**Completion (PART 7):**
- [ ] Training completed (log shows "COMPLETE")
- [ ] Models saved (`models/deployed/best_model.pkl`)
- [ ] Results downloaded
- [ ] R² > 0.90 ✓

---

## 🎓 Advanced Tips

### Tip 1: Screen/Tmux (Better than nohup)

**ใช้ `screen` หรือ `tmux` สำหรับ session management:**

```bash
# Install screen
apt-get install screen

# Start screen session
screen -S ml_training

# Run training (ไม่ต้องใช้ nohup)
python train_terminal.py

# Detach: Ctrl+A, D
# → สามารถปิด browser ได้

# Reattach ภายหลัง
screen -r ml_training
```

---

### Tip 2: Checkpoint Resume

**ถ้า training หยุดกลางคัน:**

```bash
# Script มี checkpoint manager
# แก้ train_terminal.py เพิ่ม:
results = train_production_pipeline(
    ...,
    resume_from_checkpoint=True  # ← เพิ่มบรรทัดนี้
)
```

---

### Tip 3: Reduce Trials for Testing

**ทดสอบก่อนรันจริง:**

```python
# ใน train_terminal.py แก้:
n_trials=10,  # ← ลดจาก 100 เป็น 10
```

**จะเสร็จภายใน 1-2 ชม.** (สำหรับทดสอบ)

---

## 📚 คู่มืออื่นๆ

- **PAPERSPACE_QUICK_START.md**: Setup แบบ Notebook (interactive)
- **KAGGLE_SETUP.md**: Train บน Kaggle P100 GPU
- **README.md**: User-facing documentation
- **NEXT_SESSION.md**: Session progress tracking

---

**Created**: 2025-10-08
**Version**: 1.0
**Author**: Claude Code
**Status**: ✅ Ready to use

---

**🎉 พร้อมเทรนโมเดลแล้ว! ขอให้โชคดี!**
