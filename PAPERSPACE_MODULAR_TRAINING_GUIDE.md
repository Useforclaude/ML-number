# 🚀 Paperspace Modular Training - คู่มือฉบับสมบูรณ์

**สำหรับ:** ML Phone Number Prediction (แยกเทรนทีละโมเดล)
**Platform:** Paperspace Terminal (Free GPU M4000 หรือ Growth Plan)
**Last Updated:** 2025-10-08

---

## 📋 สารบัญ

1. [เตรียม Paperspace Account](#1-เตรียม-paperspace-account)
2. [สร้าง Notebook ใหม่](#2-สร้าง-notebook-ใหม่)
3. [Setup Environment](#3-setup-environment)
4. [รัน Modular Training](#4-รัน-modular-training-แยกทีละโมเดล)
5. [Monitor Progress](#5-monitor-progress)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. เตรียม Paperspace Account

### ตัวเลือก Plan:

| Plan | GPU | Cost | Training Time | แนะนำ |
|------|-----|------|---------------|-------|
| **Free** | M4000 (8 GB) | ฟรี | 11-14 ชม. | ✅ ใช้ได้ ช้าหน่อย |
| **Growth** | A4000/P5000 (16 GB) | $8/เดือน | 8-11 ชม. | ✅ เร็วกว่า |

### ลงทะเบียน:

```
1. ไปที่: https://www.paperspace.com/
2. สมัคร (Email + Password)
3. เลือก Plan:
   - Free: M4000 GPU (ฟรี)
   - Growth: A4000 GPU ($8/เดือน - ถ้าต้องการเร็ว)
```

---

## 2. สร้าง Notebook ใหม่

### 2.1 Create Notebook

```
1. ไปที่ Gradient → Notebooks
2. คลิก "Create"
3. เลือก Template: "PyTorch" หรือ "Python 3"
4. เลือก GPU:
   - Free: Free-GPU (M4000) ← ฟรี
   - Growth: RTX A4000 ← เร็วกว่า
5. คลิก "Start Notebook"
```

### 2.2 เปิด Terminal

```
1. รอ Notebook start (1-2 นาที)
2. เมื่อเปิดแล้ว → ไปที่ "Terminal" tab (ด้านล่าง)
   หรือ: Menu → View → Terminal
3. จะเห็น prompt: root@xxxxxxxx:/notebooks#
```

**✅ พร้อมใช้งาน!**

---

## 3. Setup Environment

### 3.1 Clone โปรเจกต์

```bash
# เข้าโฟลเดอร์ /storage (persistent storage)
cd /storage

# Clone repository
git clone https://github.com/Useforclaude/ML-number.git

# เข้าโฟลเดอร์โปรเจกต์
cd ML-number

# ตรวจสอบ
pwd
# Output: /storage/ML-number
```

### 3.2 สร้าง Virtual Environment

```bash
# สร้าง venv
python3 -m venv .venv

# Activate
source .venv/bin/activate

# จะเห็น (.venv) ใน prompt:
# (.venv) root@xxxxxxxx:/storage/ML-number#
```

### 3.3 ติดตั้ง Dependencies

```bash
# ติดตั้ง packages ทั้งหมด
pip install -r requirements.txt

# รอ 5-10 นาที (ขึ้นกับความเร็ว internet)
```

### 3.4 ตรวจสอบ GPU

```bash
# เช็ค GPU
nvidia-smi

# ควรเห็น:
# +-----------------------------------------------------------------------------+
# | NVIDIA-SMI 525.x.xx    Driver Version: 525.x.xx    CUDA Version: 12.0     |
# |-------------------------------+----------------------+----------------------+
# | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
# | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
# |===============================+======================+======================|
# |   0  Quadro M4000        Off  | 00000000:00:05.0 Off |                  N/A |
# | 46%   32C    P8    11W / 120W |      0MiB /  8192MiB |      0%      Default |
# +-----------------------------------------------------------------------------+

# ถ้าเห็น Quadro M4000 (Free) หรือ RTX A4000 (Growth) → ✅ OK!
```

### 3.5 สร้างโฟลเดอร์สำหรับ logs

```bash
# สร้างโฟลเดอร์ logs
mkdir -p logs

# ตรวจสอบ
ls -la | grep logs
# drwxr-xr-x  2 root root 4096 Oct  8 10:00 logs
```

**✅ Setup เสร็จสมบูรณ์!**

---

## 4. รัน Modular Training (แยกทีละโมเดล)

### 4.1 ภาพรวม Pipeline

```
Total Training Time: 8-14 hours (ขึ้นกับ GPU)
├── XGBoost:     2-4 hours  → models/checkpoints/xgboost_checkpoint.pkl
├── LightGBM:    3-5 hours  → models/checkpoints/lightgbm_checkpoint.pkl
├── CatBoost:    1-3 hours  → models/checkpoints/catboost_checkpoint.pkl
├── RandomForest: 1-2 hours  → models/checkpoints/random_forest_checkpoint.pkl
└── Ensemble:    15-30 min  → models/deployed/best_model.pkl
```

### 4.2 รันทีละโมเดล (แนะนำ!)

#### Step 1: XGBoost (2-4 hours)

```bash
# รันแบบ background (ใช้ nohup)
nohup python train_xgboost_only.py > logs/xgb.log 2>&1 &

# จะได้ PID (เช่น [1] 12345)
# จด PID ไว้เผื่อต้องใช้

# Monitor progress
tail -f logs/xgb.log

# จะเห็น:
# 2025-10-08 10:00:00 - INFO - Starting XGBoost training...
# 2025-10-08 10:00:05 - INFO - Loading data...
# 2025-10-08 10:00:10 - INFO - Data loaded: 6,100 samples
# 2025-10-08 10:00:15 - INFO - Feature engineering...
# ...
# Trial 001: R² = 0.8456
# Trial 010: R² = 0.8723
# ...

# กด Ctrl+C เพื่อหยุด monitor (โมเดลยังรันต่อ!)
```

**รอจนเสร็จ (~2-4 ชม.)** ก่อนไป Step ถัดไป

**วิธีเช็คว่าเสร็จหรือยัง:**
```bash
# เช็ค process
ps aux | grep train_xgboost

# ถ้ายังมี → ยังทำงานอยู่
# ถ้าไม่มี → เสร็จแล้ว

# เช็ค checkpoint file
ls -lh models/checkpoints/xgboost_checkpoint.pkl
# ถ้ามีไฟล์ → เสร็จแล้ว!
```

---

#### Step 2: LightGBM (3-5 hours)

```bash
# รอ XGBoost เสร็จก่อน!

# รัน LightGBM
nohup python train_lightgbm_only.py > logs/lgb.log 2>&1 &

# Monitor
tail -f logs/lgb.log

# รอจนเสร็จ (~3-5 ชม.)
```

**เช็คว่าเสร็จ:**
```bash
ls -lh models/checkpoints/lightgbm_checkpoint.pkl
```

---

#### Step 3: CatBoost (1-3 hours)

```bash
# รัน CatBoost
nohup python train_catboost_only.py > logs/cat.log 2>&1 &

# Monitor
tail -f logs/cat.log

# รอจนเสร็จ (~1-3 ชม.)
```

**เช็คว่าเสร็จ:**
```bash
ls -lh models/checkpoints/catboost_checkpoint.pkl
```

---

#### Step 4: RandomForest (1-2 hours)

```bash
# รัน RandomForest
nohup python train_rf_only.py > logs/rf.log 2>&1 &

# Monitor
tail -f logs/rf.log

# รอจนเสร็จ (~1-2 ชม.)
```

**เช็คว่าเสร็จ:**
```bash
ls -lh models/checkpoints/random_forest_checkpoint.pkl
```

---

#### Step 5: Ensemble (15-30 minutes)

```bash
# รอทุกโมเดลเสร็จก่อน! (XGB, LGB, CAT, RF)

# เช็คว่าครบ 4 checkpoints
ls -lh models/checkpoints/
# ควรเห็น:
# xgboost_checkpoint.pkl
# lightgbm_checkpoint.pkl
# catboost_checkpoint.pkl
# random_forest_checkpoint.pkl

# รัน Ensemble (ไม่ต้อง nohup เพราะเร็ว)
python train_ensemble_only.py

# จะเห็น:
# Loading checkpoints...
# ✅ Loaded XGBoost (R² = 0.92)
# ✅ Loaded LightGBM (R² = 0.89)
# ✅ Loaded CatBoost (R² = 0.87)
# ✅ Loaded RandomForest (R² = 0.84)
# Creating ensembles...
# Best model: Stacking Ensemble (R² = 0.93)
# Saved to: models/deployed/best_model.pkl
```

**✅ เทรนเสร็จสมบูรณ์!**

---

### 4.3 รันแบบรวด (ถ้าไม่กลัว timeout)

```bash
# รันทั้งหมดพร้อมกัน (ไม่แนะนำ)
nohup python train_xgboost_only.py > logs/xgb.log 2>&1 &
nohup python train_lightgbm_only.py > logs/lgb.log 2>&1 &
nohup python train_catboost_only.py > logs/cat.log 2>&1 &
nohup python train_rf_only.py > logs/rf.log 2>&1 &

# Monitor all
tail -f logs/xgb.log logs/lgb.log logs/cat.log logs/rf.log

# รอทุกโมเดลเสร็จ → รัน ensemble
python train_ensemble_only.py
```

**⚠️ Pros:** เร็วกว่า (รันพร้อมกัน)
**⚠️ Cons:** ใช้ RAM/GPU เยอะ อาจหมดทรัพยากร

---

## 5. Monitor Progress

### 5.1 เช็ค Logs แบบ Real-time

```bash
# เช็ค log ทีละไฟล์
tail -f logs/xgb.log

# เช็คหลายไฟล์พร้อมกัน
tail -f logs/xgb.log logs/lgb.log

# เช็ค 50 บรรทัดล่าสุด
tail -50 logs/xgb.log

# เช็คว่ามี error มั้ย
grep -i error logs/xgb.log
```

### 5.2 เช็ค GPU Usage

```bash
# เช็คครั้งเดียว
nvidia-smi

# เช็คทุก 2 วินาที (real-time)
watch -n 2 nvidia-smi

# จะเห็น:
# +-----------------------------------------------------------------------------+
# |   0  Quadro M4000        Off  | 00000000:00:05.0 Off |                  N/A |
# | 85%   72C    P0   112W / 120W |   6800MiB /  8192MiB |     95%      Default |
# +-----------------------------------------------------------------------------+
#                                  ↑ GPU Usage         ↑ Memory Used

# ถ้า GPU-Util > 70% → กำลังใช้ GPU ✅
# ถ้า GPU-Util < 10% → ไม่ได้ใช้ GPU (อาจมีปัญหา)

# กด Ctrl+C เพื่อหยุด
```

### 5.3 เช็ค Running Processes

```bash
# เช็คว่าโมเดลไหนกำลังรัน
ps aux | grep train_

# Output:
# root  12345  98.5  15.2  python train_xgboost_only.py
# root  12346  85.2  12.1  python train_lightgbm_only.py

# เช็คว่ามี process กี่ตัว
ps aux | grep train_ | wc -l
# Output: 2 (กำลังรัน 2 โมเดลพร้อมกัน)
```

### 5.4 เช็ค Checkpoints

```bash
# เช็คว่าโมเดลไหนเสร็จแล้ว
ls -lh models/checkpoints/

# Output:
# -rw-r--r-- 1 root root 245M Oct  8 12:34 xgboost_checkpoint.pkl
# -rw-r--r-- 1 root root 312M Oct  8 15:12 lightgbm_checkpoint.pkl
# -rw-r--r-- 1 root root 189M Oct  8 17:45 catboost_checkpoint.pkl
# -rw-r--r-- 1 root root 156M Oct  8 19:01 random_forest_checkpoint.pkl

# เช็คว่ามีกี่ไฟล์
ls models/checkpoints/*.pkl | wc -l
# Output: 4 (ครบทั้ง 4 โมเดลแล้ว)
```

### 5.5 เช็ค Disk Space

```bash
# เช็คพื้นที่ว่าง
df -h /storage

# Output:
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1        50G   5G   45G  10% /storage

# ถ้า Use% > 90% → พื้นที่เหลือน้อย
```

---

## 6. Troubleshooting

### ปัญหา 1: Process หยุดทำงาน (Killed)

**อาการ:**
```bash
tail -f logs/xgb.log
# ...
# Trial 050: R² = 0.8923
# Killed
```

**สาเหตุ:** หมดหน่วยความจำ (RAM/GPU)

**แก้ไข:**
```bash
# 1. ตรวจสอบว่ารันกี่โมเดลพร้อมกัน
ps aux | grep train_

# 2. ถ้ารันหลายโมเดลพร้อมกัน → หยุด 1-2 ตัว
kill <PID>

# 3. รันทีละโมเดลแทน (แนะนำ!)
```

---

### ปัญหา 2: GPU ไม่ทำงาน (0% usage)

**อาการ:**
```bash
nvidia-smi
# GPU-Util: 0%
```

**สาเหตุ:** โมเดลไม่ได้ใช้ GPU

**แก้ไข:**
```bash
# 1. เช็ค log ว่ามี warning มั้ย
grep -i "gpu" logs/xgb.log

# 2. ตรวจสอบว่า XGBoost detect GPU มั้ย
python -c "import xgboost; print(xgboost.__version__)"

# 3. ถ้ายังไม่ได้ → ติดตั้ง xgboost ใหม่
pip install --upgrade xgboost
```

---

### ปัญหา 3: ไม่พบไฟล์ train_xgboost_only.py

**อาการ:**
```bash
python train_xgboost_only.py
# Error: No such file or directory
```

**แก้ไข:**
```bash
# 1. เช็คว่าอยู่ในโฟลเดอร์ที่ถูกต้อง
pwd
# Output: /storage/ML-number

# ถ้าไม่ใช่ → cd กลับ
cd /storage/ML-number

# 2. เช็คว่ามีไฟล์มั้ย
ls train_*.py
# ควรเห็น:
# train_xgboost_only.py
# train_lightgbm_only.py
# ...

# 3. ถ้าไม่มี → git pull ใหม่
git pull origin main
```

---

### ปัญหา 4: ModuleNotFoundError

**อาการ:**
```bash
python train_xgboost_only.py
# ModuleNotFoundError: No module named 'xgboost'
```

**แก้ไข:**
```bash
# 1. เช็คว่า activate venv แล้วรึยัง
which python
# Output: /storage/ML-number/.venv/bin/python ← ✅ ถูกต้อง
# Output: /usr/bin/python ← ❌ ยังไม่ activate

# 2. ถ้ายังไม่ activate → activate
source .venv/bin/activate

# 3. ถ้ายัง error → ติดตั้งใหม่
pip install -r requirements.txt
```

---

### ปัญหา 5: Session timeout / Browser ปิด

**อาการ:** ปิด browser → กลับมาใหม่ → ไม่รู้ว่าเทรนไปถึงไหน

**แก้ไข:**
```bash
# 1. เช็ค process ที่ยังรันอยู่
ps aux | grep train_

# 2. เช็ค log ล่าสุด
tail -50 logs/xgb.log

# 3. เช็ค checkpoint
ls -lh models/checkpoints/

# ✅ ถ้าใช้ nohup → โมเดลยังรันต่อแม้ปิด browser!
```

---

### ปัญหา 6: Training ช้ามาก

**อาการ:** XGBoost ใช้เวลา >5 ชม. (ปกติ 2-3 ชม.)

**สาเหตุ:**
1. ใช้ Free Plan (M4000) → ช้ากว่า Growth Plan (A4000)
2. GPU ไม่ทำงาน (ใช้ CPU แทน)

**แก้ไข:**
```bash
# 1. เช็ค GPU usage
nvidia-smi
# ถ้า GPU-Util < 10% → ไม่ได้ใช้ GPU

# 2. เช็ค log
grep -i "device" logs/xgb.log
# ควรเห็น: Device: cuda
# ถ้าเห็น: Device: cpu → มีปัญหา

# 3. ถ้าช้าแต่ใช้ GPU แล้ว → ปกติ (M4000 ช้า)
# หรือ → อัพเกรดเป็น Growth Plan (A4000)
```

---

## 7. Expected Results

### เวลาเทรนแต่ละโมเดล:

| GPU | XGBoost | LightGBM | CatBoost | RandomForest | Ensemble | Total |
|-----|---------|----------|----------|--------------|----------|-------|
| **M4000** (Free) | 3-4 ชม. | 4-5 ชม. | 2-3 ชม. | 1.5 ชม. | 30 นาที | **11-14 ชม.** |
| **A4000** (Growth) | 2-3 ชม. | 3-4 ชม. | 1-2 ชม. | 1 ชม. | 15 นาที | **8-11 ชม.** |

### R² Scores:

| Model | Expected R² |
|-------|-------------|
| XGBoost | 0.88-0.92 |
| LightGBM | 0.86-0.90 |
| CatBoost | 0.85-0.89 |
| RandomForest | 0.82-0.86 |
| **Ensemble** | **0.90-0.93** ✅ |

---

## 8. Quick Commands Reference

```bash
# === SETUP ===
cd /storage
git clone https://github.com/Useforclaude/ML-number.git
cd ML-number
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p logs

# === TRAINING ===
nohup python train_xgboost_only.py > logs/xgb.log 2>&1 &
nohup python train_lightgbm_only.py > logs/lgb.log 2>&1 &
nohup python train_catboost_only.py > logs/cat.log 2>&1 &
nohup python train_rf_only.py > logs/rf.log 2>&1 &
python train_ensemble_only.py

# === MONITORING ===
tail -f logs/xgb.log              # Monitor log
watch -n 2 nvidia-smi             # Monitor GPU
ps aux | grep train_              # Check processes
ls -lh models/checkpoints/        # Check checkpoints

# === TROUBLESHOOTING ===
kill <PID>                        # Stop process
grep -i error logs/xgb.log        # Find errors
df -h /storage                    # Check disk space
```

---

## 9. After Training

### 9.1 ดาวน์โหลด Best Model

```bash
# เช็คว่ามี best model
ls -lh models/deployed/best_model.pkl

# ดาวน์โหลดผ่าน Jupyter File Browser:
# 1. ไปที่ File Browser (ด้านซ้าย)
# 2. Navigate: /storage/ML-number/models/deployed/
# 3. คลิกขวา best_model.pkl → Download
```

### 9.2 ทดสอบ Model

```python
# ใน Python shell หรือ Jupyter notebook
import joblib

# Load model
model_pkg = joblib.load('models/deployed/best_model.pkl')

print(f"Model: {model_pkg['model_name']}")
print(f"R² Score: {model_pkg['metrics']['test_r2']:.4f}")
print(f"MAE: {model_pkg['metrics']['test_mae']:.2f}")

# Test prediction
phone = "0899999999"
# ... (ต้องเตรียม features เหมือนตอน training)
```

---

## 10. Summary Checklist

**ก่อนเริ่ม:**
- [ ] สมัคร Paperspace account
- [ ] สร้าง Notebook (Free GPU หรือ Growth)
- [ ] เปิด Terminal

**Setup:**
- [ ] Clone repository
- [ ] สร้าง venv + activate
- [ ] ติดตั้ง requirements
- [ ] เช็ค GPU (nvidia-smi)
- [ ] สร้างโฟลเดอร์ logs

**Training:**
- [ ] รัน XGBoost (2-4 ชม.)
- [ ] รัน LightGBM (3-5 ชม.)
- [ ] รัน CatBoost (1-3 ชม.)
- [ ] รัน RandomForest (1-2 ชม.)
- [ ] รัน Ensemble (15-30 นาที)

**Verification:**
- [ ] เช็ค logs ไม่มี error
- [ ] เช็ค checkpoints ครบ 4 ไฟล์
- [ ] เช็ค best_model.pkl ใน deployed/
- [ ] R² > 0.90 ✅

**✅ เสร็จสมบูรณ์!**

---

**Created:** 2025-10-08
**Session:** 012 - Paperspace Modular Training Guide
**Total Time:** 8-14 hours (ขึ้นกับ GPU)
**Expected R²:** 0.90-0.93 ✅
