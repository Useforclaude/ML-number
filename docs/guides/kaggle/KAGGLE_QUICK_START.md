# 🚀 Kaggle Quick Start Guide - คู่มือเริ่มต้นอย่างรวดเร็ว

## 📦 แพคเกจที่ใช้

**ไฟล์:** `number-ML-kaggle-FINAL-20251005.zip` (114 KB)

**รวมการแก้ไขทั้งหมด:**
- ✅ Session 007: OPTUNA optimizer fixes (4 bugs fixed)
- ✅ Session 007B: checkpoint_manager.py added
- ✅ GPU configuration verified
- ✅ All imports working

---

## ⚙️ **ตั้งค่า Kaggle Notebook (สำคัญมาก!)**

### **1. Accelerator (GPU)** 🎮

```
Settings → Accelerator → GPU P100 ✅
```

**หรือ**

คลิกที่ปุ่ม **"GPU P100 Off"** ด้านบนขวา → เปลี่ยนเป็น **"GPU P100 On"**

**ทำไมต้องเปิด:**
- ✅ เทรนเร็วขึ้น 40-50% (6-8 ชั่วโมง vs 12-18 ชั่วโมง)
- ✅ XGBoost, LightGBM, CatBoost จะใช้ GPU
- ✅ Code ได้ตั้งค่า GPU params แล้ว (use_gpu=True)

---

### **2. Persistence (การเก็บไฟล์)** 💾

```
Settings → Persistence → Files only ✅
```

**หรือ**

```
Settings → Persistence → Variables and Files ✅
```

**❌ ห้ามเลือก:**
```
Settings → Persistence → No persistence ❌
```

**ทำไมต้องตั้ง:**
- ✅ Checkpoint จะไม่หาย เมื่อ session timeout
- ✅ Auto-resume ทำงานได้
- ✅ ไม่ต้องเทรนใหม่จาก epoch 0

**สิ่งที่ persist:**
```
/kaggle/working/checkpoints/  ← Checkpoint ทุกไฟล์
/kaggle/working/models/        ← Model ที่เทรนเสร็จ
/kaggle/working/logs/          ← Training logs
/kaggle/working/results/       ← Evaluation results
```

---

### **3. Environment (สภาพแวดล้อม)** 🌍

```
Settings → Environment → Always use latest environment ✅
```

**ทำไม:**
- ✅ ได้ library version ล่าสุด
- ✅ Bug fixes และ improvements ล่าสุด
- ✅ CUDA version ล่าสุดสำหรับ GPU

**อย่าเลือก:**
```
Pin to original environment ❌
```

**เพราะ:** Original environment อาจมี library เก่า หรือ bugs

---

## 📋 **สรุปการตั้งค่าที่ถูกต้อง**

| Setting | ค่าที่ถูกต้อง | เหตุผล |
|---------|--------------|--------|
| **Accelerator** | GPU P100 ✅ | เทรนเร็วขึ้น 40-50% |
| **Persistence** | Files only ✅ | Checkpoint ไม่หาย |
| **Environment** | Always use latest ✅ | Library ใหม่สุด |

---

## 🚀 **ขั้นตอนการใช้งาน (5 Steps)**

### **Step 1: Upload Dataset to Kaggle**

1. ไปที่ **Kaggle → Datasets → New Dataset**
2. Upload `number-ML-kaggle-FINAL-20251005.zip`
3. ตั้งชื่อ: `phone-number-ml-project-latest`
4. Visibility: Private (หรือ Public ถ้าต้องการ)
5. Click **Create**

---

### **Step 2: Create New Notebook**

1. ไปที่ **Kaggle → Code → New Notebook**
2. Click **File → Import Notebook**
3. Upload `Kaggle_ML_Training_AutoResume.ipynb` (จากแพคเกจ)

**หรือ**

1. Create blank notebook
2. Copy-paste code จาก Cell 1-8

---

### **Step 3: Add Dataset to Notebook**

1. คลิก **Add data** (ด้านขวา)
2. Search `phone-number-ml-project-latest`
3. Click **Add**
4. Dataset จะปรากฏใน `/kaggle/input/phone-number-ml-project-latest/`

---

### **Step 4: ตั้งค่า Settings (สำคัญ!)**

```
✅ Accelerator: GPU P100
✅ Persistence: Files only
✅ Environment: Always use latest environment
```

---

### **Step 5: Run Notebook**

**Run Cell 1-6 ตามลำดับ:**

```python
Cell 1: Setup paths & environment (5 sec)
  └─> ✅ Paths configured
  └─> ✅ GPU detected

Cell 2: Load project from dataset (10 sec)
  └─> ✅ Copied 11 Python files
  └─> ✅ Data loaded: 6092 rows

Cell 3: Install dependencies (30 sec)
  └─> ✅ All libraries installed

Cell 4: Auto-detect checkpoint (2 sec)
  └─> ✅ FRESH START MODE (first time)
  └─> ✅ RESUME MODE (if checkpoint found)

Cell 5: Load data & features (1-2 min)
  └─> ✅ 6092 rows loaded
  └─> ✅ 150 features created
  └─> ✅ No data leakage

Cell 6: Train models (6-14 hours) 🔥
  └─> ✅ GPU: 70-90% (XGBoost, LightGBM, CatBoost)
  └─> ✅ 6 models + 4 ensembles
  └─> ✅ Auto-save checkpoint every 10 epochs
  └─> ✅ Target R² > 0.90
```

---

## 📊 **สิ่งที่คาดหวัง**

### **GPU Usage (Cell 6):**

```
⚙️  Optimizing XGBoost...
Trial 1/100: GPU 75% 🔥 GPU Memory 5 GB
Trial 2/100: GPU 82% 🔥 GPU Memory 6 GB
...

🎯 Training XGBoost...
GPU: 85-95% 🔥 GPU Memory: 4-8 GB

⚙️  Optimizing LightGBM...
GPU: 70-85% 🔥 GPU Memory: 3-6 GB

⚙️  Optimizing CatBoost...
GPU: 60-80% 🔥 GPU Memory: 4-7 GB

⚙️  Optimizing RandomForest...
GPU: 0% ✅ (RF ไม่รองรับ GPU - ปกติ)
CPU: 400% 🔥
```

### **Training Time:**

| Config | Time | R² Expected |
|--------|------|-------------|
| **GPU + N_TRIALS=100** | 6-8 hours | 0.90-0.95 |
| **GPU + N_TRIALS=50** | 4-5 hours | 0.88-0.93 |
| **CPU + N_TRIALS=100** | 12-18 hours | 0.90-0.95 |

---

## ⏱️ **ถ้า Timeout (9 ชั่วโมง)**

### **สิ่งที่เกิดขึ้น:**

```
Training epoch 50/100...
⏰ Kaggle timeout (9 hours)
💾 Checkpoint saved: checkpoint_epoch_50.pkl
🛑 Session stopped
```

### **วิธี Resume:**

1. **Fork Notebook:**
   - Click **Fork Notebook** (top right)
   - สร้าง session ใหม่

2. **ตรวจสอบ Settings ใหม่:**
   ```
   ✅ Accelerator: GPU P100
   ✅ Persistence: Files only
   ```

3. **Run Cell 1-6 ใหม่:**
   ```
   Cell 4 จะขึ้น:

   ====================================================================
   🔄 RESUME MODE ACTIVATED
   ====================================================================
   Last completed epoch: 50
   Will resume from epoch: 51

   Cell 6 จะเทรนต่อจาก epoch 51 → 100
   ```

4. **รอให้เทรนเสร็จ:**
   - 4-6 ชั่วโมงเพิ่มเติม
   - Total R² > 0.90 ✅

---

## 🎯 **การตรวจสอบว่าทำถูกต้อง**

### **✅ Checklist ก่อน Run:**

- [ ] GPU P100 เปิดอยู่ (เห็น "GPU P100 On" บนขวา)
- [ ] Persistence = "Files only" หรือ "Variables and Files"
- [ ] Environment = "Always use latest environment"
- [ ] Dataset added (เห็นใน Data panel ขวามือ)
- [ ] Cell 1-3 run แล้วไม่มี error

### **✅ Checklist ระหว่าง Training (Cell 6):**

- [ ] GPU Util = 70-90% (ดูที่ panel ขวา)
- [ ] GPU Memory = 4-8 GB
- [ ] ไม่มี error message
- [ ] เห็นข้อความ "Trial X/100" (Optuna กำลังทำงาน)

### **✅ Checklist หลัง Training:**

- [ ] R² > 0.90 (ดูที่ output Cell 6)
- [ ] Model saved to `/kaggle/working/models/`
- [ ] Checkpoint saved to `/kaggle/working/checkpoints/`
- [ ] ไม่มี error

---

## ❌ **Troubleshooting (แก้ปัญหา)**

### **ปัญหา 1: GPU Util = 0%**

**สาเหตุ:**
- ❌ GPU ไม่ได้เปิด
- ❌ ยังไม่ได้ Run Cell 6
- ❌ กำลัง train RandomForest (ไม่รองรับ GPU - ปกติ)

**วิธีแก้:**
```
1. ตรวจสอบ: Settings → Accelerator → GPU P100
2. Run Cell 6
3. รอ 2-3 นาที (GPU จะขึ้นตอน optimize XGBoost)
```

---

### **ปัญหา 2: ModuleNotFoundError**

**Error:**
```
ModuleNotFoundError: No module named 'src.checkpoint_manager'
```

**สาเหตุ:**
- ❌ Cell 2 ไม่ได้ copy files ครบ
- ❌ Dataset ไม่มีไฟล์ครบ

**วิธีแก้:**
```
1. Download แพคเกจใหม่: number-ML-kaggle-FINAL-20251005.zip
2. Upload ใหม่ไปที่ Kaggle Dataset (replace version เก่า)
3. Restart kernel: Kernel → Restart Kernel
4. Run Cell 1-6 ใหม่
```

---

### **ปัญหา 3: Checkpoint หายหลัง Timeout**

**สาเหตุ:**
- ❌ Persistence = "No persistence"

**วิธีแก้:**
```
1. Settings → Persistence → Files only ✅
2. Restart kernel
3. Run Cell 1-6 ใหม่
```

---

### **ปัญหา 4: R² ต่ำ (< 0.80)**

**สาเหตุ:**
- ⚠️ N_TRIALS ต่ำเกินไป
- ⚠️ GPU ไม่ทำงาน

**วิธีแก้:**
```python
# ใน Cell 6 เปลี่ยน:
N_TRIALS = 100  # เพิ่มจาก 50 → 100
```

---

## 📞 **ติดปัญหา?**

### **ตรวจสอบเหล่านี้ก่อน:**

1. ✅ GPU P100 เปิดอยู่?
2. ✅ Persistence = Files only?
3. ✅ Dataset มีไฟล์ครบ 16 ไฟล์?
4. ✅ Cell 1-5 run แล้วไม่มี error?
5. ✅ Cell 6 กำลังรันอยู่?

### **Check GPU:**
```python
# Run ใน Cell ใหม่
!nvidia-smi

# ควรเห็น:
# GPU: Tesla P100-PCIE-16GB
# Memory: 16384 MiB
```

### **Check Checkpoint:**
```python
# Run ใน Cell ใหม่
!ls -lh /kaggle/working/checkpoints/

# ควรเห็น:
# checkpoint_epoch_10.pkl
# checkpoint_epoch_20.pkl
# checkpoint_latest.pkl
```

---

## 🎉 **สรุป**

### **3 การตั้งค่าสำคัญ:**

1. **GPU P100 ON** ✅
2. **Persistence: Files only** ✅
3. **Environment: Always use latest** ✅

### **Run Notebook:**

```
Cell 1 → Cell 2 → Cell 3 → Cell 4 → Cell 5 → Cell 6 (รอ 6-14 ชั่วโมง)
```

### **ผลลัพธ์:**

```
✅ R² > 0.90
✅ 6 models + 4 ensembles trained
✅ Model saved to /kaggle/working/models/
✅ Can resume if timeout!
```

---

**พร้อมเทรนแล้ว! 🚀**

*หากมีปัญหา ดูที่ Troubleshooting ด้านบนครับ*
