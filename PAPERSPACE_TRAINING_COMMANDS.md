# 🎯 Paperspace Training Commands (ทีละโมเดล)

**Important**: รันทีละโมเดล ไม่ต้องรอทั้งหมดเสร็จ หยุดได้ตลอดเวลา!

---

## 📋 การรัน: ทีละโมเดล (แยกอิสระ)

**ข้อดี:**
- ✅ รันเสร็จ 1 โมเดล → ได้ checkpoint ทันที
- ✅ Paperspace ดับก็ไม่เสียงาน (checkpoint saved!)
- ✅ รันต่อเมื่อไหร่ก็ได้
- ✅ เลือกรันโมเดลไหนก่อนก็ได้

---

## 🔧 เตรียมพร้อมก่อนเริ่ม (ครั้งแรกเท่านั้น)

### **ติดตั้ง PyTorch (ต้องทำครั้งแรก!):**
```bash
cd /notebooks/ML-number
source .venv/bin/activate

# ติดตั้ง PyTorch (CPU version - สำหรับ Paperspace)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# หรือถ้ามี GPU (M4000/P5000):
# pip install torch torchvision torchaudio

# Verify installation
python -c "import torch; print(f'✅ PyTorch {torch.__version__} installed')"
```

**ต้องทำครั้งเดียวตอนแรก! หลังจากนั้นไม่ต้องติดตั้งอีก**

---

## 🚀 คำสั่งสำหรับแต่ละโมเดล

### **เตรียมตัวก่อนทุกครั้ง:**
```bash
cd /notebooks/ML-number
source .venv/bin/activate
```

---

### **โมเดลที่ 1: XGBoost (~2-3 hours)**

```bash
# Activate environment
cd /notebooks/ML-number
source .venv/bin/activate

# Run XGBoost ONLY
echo "=== XGBoost Training ==="
echo "Start: $(date)"
python training/modular/train_xgboost_only.py 2>&1 | tee logs/xgb.log
echo "End: $(date)"

# Verify
ls -lh models/checkpoints/xgboost_checkpoint.pkl
grep "R² Score" logs/xgb.log
```

**Expected:**
- ✅ Checkpoint: `models/checkpoints/xgboost_checkpoint.pkl`
- ✅ R² ~0.88-0.92
- ✅ Time: 2-3 hours

---

### **โมเดลที่ 2: LightGBM (~3-4 hours)**

```bash
# Activate environment
cd /notebooks/ML-number
source .venv/bin/activate

# Run LightGBM ONLY
echo "=== LightGBM Training ==="
echo "Start: $(date)"
python training/modular/train_lightgbm_only.py 2>&1 | tee logs/lgb.log
echo "End: $(date)"

# Verify
ls -lh models/checkpoints/lightgbm_checkpoint.pkl
grep "R² Score" logs/lgb.log
```

**Expected:**
- ✅ Checkpoint: `models/checkpoints/lightgbm_checkpoint.pkl`
- ✅ R² ~0.86-0.90
- ✅ Time: 3-4 hours

---

### **โมเดลที่ 3: CatBoost (~1-2 hours)**

```bash
# Activate environment
cd /notebooks/ML-number
source .venv/bin/activate

# Run CatBoost ONLY
echo "=== CatBoost Training ==="
echo "Start: $(date)"
python training/modular/train_catboost_only.py 2>&1 | tee logs/cat.log
echo "End: $(date)"

# Verify
ls -lh models/checkpoints/catboost_checkpoint.pkl
grep "R² Score" logs/cat.log
```

**Expected:**
- ✅ Checkpoint: `models/checkpoints/catboost_checkpoint.pkl`
- ✅ R² ~0.85-0.89
- ✅ Time: 1-2 hours

---

### **โมเดลที่ 4: RandomForest (~1 hour)**

```bash
# Activate environment
cd /notebooks/ML-number
source .venv/bin/activate

# Run RandomForest ONLY
echo "=== RandomForest Training ==="
echo "Start: $(date)"
python training/modular/train_rf_only.py 2>&1 | tee logs/rf.log
echo "End: $(date)"

# Verify
ls -lh models/checkpoints/random_forest_checkpoint.pkl
grep "R² Score" logs/rf.log
```

**Expected:**
- ✅ Checkpoint: `models/checkpoints/random_forest_checkpoint.pkl`
- ✅ R² ~0.82-0.86
- ✅ Time: 1 hour

---

### **โมเดลที่ 5: Ensemble (~15-30 minutes)**

**⚠️ รันได้เฉพาะเมื่อมี 4 checkpoints ครบแล้ว!**

```bash
# Activate environment
cd /notebooks/ML-number
source .venv/bin/activate

# Verify all 4 checkpoints exist
echo "=== Checking Checkpoints ==="
ls -lh models/checkpoints/xgboost_checkpoint.pkl
ls -lh models/checkpoints/lightgbm_checkpoint.pkl
ls -lh models/checkpoints/catboost_checkpoint.pkl
ls -lh models/checkpoints/random_forest_checkpoint.pkl

# If all 4 exist, run ensemble
echo "=== Ensemble Training ==="
echo "Start: $(date)"
python training/modular/train_ensemble_only.py 2>&1 | tee logs/ensemble.log
echo "End: $(date)"

# Verify
ls -lh models/deployed/best_model.pkl
grep "Best Model" logs/ensemble.log
```

**Expected:**
- ✅ Best model: `models/deployed/best_model.pkl`
- ✅ R² ~0.90-0.93 (ดีที่สุด!)
- ✅ Time: 15-30 minutes

---

## 🎯 แผนการรัน (แนะนำ)

### **Option 1: รันเร็วก่อน (Fast First)**
```
1. RandomForest (1h)      → Checkpoint 1
2. CatBoost (2h)          → Checkpoint 2
3. XGBoost (3h)           → Checkpoint 3
4. LightGBM (4h)          → Checkpoint 4
5. Ensemble (30min)       → Best Model ✅
```

### **Option 2: รันช้าก่อน (Slow First)**
```
1. LightGBM (4h)          → Checkpoint 1
2. XGBoost (3h)           → Checkpoint 2
3. CatBoost (2h)          → Checkpoint 3
4. RandomForest (1h)      → Checkpoint 4
5. Ensemble (30min)       → Best Model ✅
```

### **Option 3: รันตาม R² สูงสุดก่อน (Best First)**
```
1. XGBoost (3h)           → R² ~0.90 (highest!)
2. LightGBM (4h)          → R² ~0.88
3. CatBoost (2h)          → R² ~0.87
4. RandomForest (1h)      → R² ~0.84
5. Ensemble (30min)       → R² ~0.93 (best!)
```

---

## 📊 ตรวจสอบความคืบหน้า

### **เช็คว่ารันโมเดลไหนไปแล้วบ้าง:**
```bash
cd /notebooks/ML-number
ls -lh models/checkpoints/

# Should see:
# xgboost_checkpoint.pkl      (if XGBoost done)
# lightgbm_checkpoint.pkl     (if LightGBM done)
# catboost_checkpoint.pkl     (if CatBoost done)
# random_forest_checkpoint.pkl (if RandomForest done)
```

### **เช็ค R² scores:**
```bash
grep "R² Score" logs/xgb.log
grep "R² Score" logs/lgb.log
grep "R² Score" logs/cat.log
grep "R² Score" logs/rf.log
```

### **เช็คว่าครบ 4 checkpoints หรือยัง:**
```bash
ls models/checkpoints/*.pkl | wc -l
# Expected: 4 (if all models trained)
```

---

## 🔄 การทำงานต่อจากที่หยุด

### **กรณีที่ 1: Paperspace Shutdown**
```bash
# เมื่อ Paperspace เปิดใหม่
cd /notebooks/ML-number
source .venv/bin/activate

# เช็คว่ามี checkpoint ไหนแล้ว
ls -lh models/checkpoints/

# รันโมเดลที่ยังไม่ได้รันต่อ
# ตัวอย่าง: ถ้ามีแค่ XGBoost แล้ว → รัน LightGBM ต่อ
python training/modular/train_lightgbm_only.py 2>&1 | tee logs/lgb.log
```

### **กรณีที่ 2: ต้องการรันเพิ่ม**
```bash
# เพิ่มโมเดลที่ยังไม่ได้รัน
cd /notebooks/ML-number
source .venv/bin/activate

# ดู checkpoint ที่มี
ls models/checkpoints/

# รันโมเดลที่ขาด
python training/modular/train_catboost_only.py 2>&1 | tee logs/cat.log
```

---

## ✅ Checklist

**ก่อนรันแต่ละโมเดล:**
- [ ] `cd /notebooks/ML-number`
- [ ] `source .venv/bin/activate`
- [ ] ดูว่า checkpoint เก่ามีหรือยัง (`ls models/checkpoints/`)

**หลังรันเสร็จแต่ละโมเดล:**
- [ ] เช็ค checkpoint saved: `ls -lh models/checkpoints/*.pkl`
- [ ] เช็ค R²: `grep "R² Score" logs/*.log`
- [ ] บันทึกเวลาที่ใช้
- [ ] รันโมเดลถัดไปหรือหยุด (ตามสะดวก)

**เมื่อครบ 4 checkpoints:**
- [ ] Verify: `ls models/checkpoints/*.pkl | wc -l` = 4
- [ ] รัน ensemble: `python training/modular/train_ensemble_only.py`
- [ ] เช็ค best model: `ls -lh models/deployed/best_model.pkl`

---

## 📝 ตัวอย่างการใช้งานจริง

### **Session A: รัน XGBoost**
```bash
cd /notebooks/ML-number
source .venv/bin/activate
python training/modular/train_xgboost_only.py 2>&1 | tee logs/xgb.log

# หลังรันเสร็จ (2-3h):
ls -lh models/checkpoints/xgboost_checkpoint.pkl
# → ได้ checkpoint แล้ว! ปิด Paperspace ได้เลย

# Paperspace shutdown...
```

### **Session B: รัน CatBoost (วันถัดไป)**
```bash
cd /notebooks/ML-number
source .venv/bin/activate

# เช็คว่ามี checkpoint เก่าไหม
ls models/checkpoints/
# → เจอ xgboost_checkpoint.pkl ✅

# รัน CatBoost ต่อ
python training/modular/train_catboost_only.py 2>&1 | tee logs/cat.log

# หลังรันเสร็จ (1-2h):
ls models/checkpoints/
# → ได้ 2 checkpoints แล้ว!
```

### **Session C-E: รันต่อ...**
```bash
# รัน RandomForest
python training/modular/train_rf_only.py 2>&1 | tee logs/rf.log

# รัน LightGBM
python training/modular/train_lightgbm_only.py 2>&1 | tee logs/lgb.log

# รัน Ensemble (เมื่อครบ 4)
python training/modular/train_ensemble_only.py 2>&1 | tee logs/ensemble.log

# เสร็จ! ✅
```

---

## 🎯 สรุป

**ข้อดีของการรันทีละโมเดล:**
- ✅ ไม่กลัว timeout (แต่ละโมเดล < 6h)
- ✅ Checkpoint saved ทุกครั้ง
- ✅ ยืดหยุ่น (รันเมื่อไหร่ก็ได้)
- ✅ ปิด Paperspace ได้ตลอดเวลา

**ทำตามนี้:**
1. เลือกโมเดลที่จะรัน
2. Copy คำสั่ง → Paste ใน Paperspace
3. รอเสร็จ → ได้ checkpoint
4. รันโมเดลถัดไปหรือหยุด (ตามสะดวก)
5. เมื่อครบ 4 → รัน ensemble → เสร็จ! 🎉

---

---

## 🔧 Troubleshooting (แก้ปัญหาที่พบบ่อย)

### **Error 1: No module named 'torch'**
```
ERROR - Import error: No module named 'torch'
```

**Solution:**
```bash
cd /notebooks/ML-number
source .venv/bin/activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
python -c "import torch; print('✅ PyTorch installed')"
```

### **Error 2: FileNotFoundError - Data file not found**
```
FileNotFoundError: ❌ ไม่พบไฟล์ข้อมูล!
```

**Solution:**
```bash
# Check if data file exists
ls -lh /notebooks/ML-number/data/raw/numberdata.csv

# If missing, upload it via Paperspace web UI
# Or check the path in training script is correct
```

### **Error 3: Virtual environment not activated**
```
Command 'python' not found
```

**Solution:**
```bash
cd /notebooks/ML-number
source .venv/bin/activate
# Now (.venv) should appear in prompt
```

### **Error 4: Out of memory**
```
MemoryError or Killed
```

**Solution:**
- Reduce n_trials in training script (100 → 50)
- Train one model at a time (not parallel)
- Restart Paperspace session

### **Error 5: Git pull conflicts**
```
error: Your local changes would be overwritten
```

**Solution:**
```bash
git stash
git pull origin main
git stash pop
```

---

**Created**: 2025-10-11
**Updated**: 2025-10-11 (Added PyTorch installation + Troubleshooting)
**Purpose**: คำสั่งรันทีละโมเดลสำหรับ Paperspace
**Status**: Ready to use ✅
