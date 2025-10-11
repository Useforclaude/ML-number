# ⚠️ KAGGLE CHECKPOINT REALITY - สิ่งที่ต้องรู้!

**Updated**: 2025-10-05 (หลังพบว่า /kaggle/working/ ถูกลบหมด!)

---

## 🔍 สิ่งที่คุณค้นพบ (และถูกต้อง 100%!)

> "/kaggle/working/ หลังปิด session ไปไม่เห็น save อะไรให้เลย"

**คำตอบ**: ใช่แล้ว! Kaggle **ลบไฟล์ทั้งหมดใน /kaggle/working/** เมื่อ session สิ้นสุด!

---

## 📋 ความจริงเกี่ยวกับ Kaggle Persistence

### ✅ สิ่งที่ Persist (อยู่ถาวร):
1. **Dataset Files** (อ่านอย่างเดียว):
   - `/kaggle/input/your-dataset/`
   - ไม่สามารถแก้ไขได้ระหว่างรัน
   - ต้อง upload เวอร์ชันใหม่เพื่ออัปเดต

2. **Output Files** (เมื่อ "Save Version"):
   - ต้องกด "Save Version" ใน Notebook Settings
   - Kaggle สร้าง snapshot ของ notebook + outputs
   - Download ได้ภายหลัง

3. **Notebook Code**:
   - Auto-save ทุก 30 วินาที
   - แต่ไม่ save output หรือไฟล์ใน /kaggle/working/

### ❌ สิ่งที่ไม่ Persist (หายเมื่อปิด session):
1. **ALL files in /kaggle/working/**:
   - ✗ Checkpoints
   - ✗ Models
   - ✗ Intermediate results
   - ✗ Logs
   - ✗ Anything you create during runtime

2. **Variables in memory**:
   - ✗ All Python variables
   - ✗ Loaded data
   - ✗ Trained models (ถ้าไม่ save แล้วกด "Save Version")

---

## 💡 Solution: วิธีที่ถูกต้องสำหรับ Kaggle

### Option 1: Training ครั้งเดียวจบ (Recommended!)

**ใช้เมื่อ**: Training time < 9 ชั่วโมง (Kaggle limit)

**Steps**:
```
1. Upload ULTRAFIX ZIP เป็น dataset ใหม่
2. Create notebook ใหม่ (หรือใช้เดิม)
3. เปลี่ยน dataset input เป็น ULTRAFIX version
4. Run Cell 1-6 ไปเรื่อยๆ
5. รอ 6-8 ชั่วโมง จนเทรนเสร็จ
6. กด "Save Version" ทันที (ก่อน session timeout!)
7. Download best_model.pkl จาก Output
```

**Pros**:
- ✅ ง่ายที่สุด
- ✅ ไม่ต้องกังวลเรื่อง checkpoint
- ✅ ได้ model เต็มรูปแบบ

**Cons**:
- ⚠️ ถ้า session timeout ก่อน 6-8 ชั่วโมง = เริ่มใหม่
- ⚠️ ต้องกด "Save Version" ทันทีหลังเทรนเสร็จ

---

### Option 2: Save Intermediate Models Manually

**ใช้เมื่อ**: กลัว session timeout

**Modified Training Loop**:
```python
# ใน Cell 6 - เพิ่ม manual save หลังแต่ละ model

# XGBoost
xgb_params = optimize_xgboost(...)
xgb_model = XGBRegressor(**xgb_params)
xgb_model.fit(X_train, y_train)
joblib.dump(xgb_model, '/kaggle/working/xgb_model_partial.pkl')
print("✅ XGBoost model saved!")

# LightGBM
lgbm_params = optimize_lightgbm(...)
lgbm_model = LGBMRegressor(**lgbm_params)
lgbm_model.fit(X_train, y_train)
joblib.dump(lgbm_model, '/kaggle/working/lgbm_model_partial.pkl')
print("✅ LightGBM model saved!")

# ... repeat for each model

# หลังแต่ละ model save เสร็จ → กด "Save Version" ทันที
```

**Then**:
1. หลัง XGBoost เสร็จ (2-3 ชม.) → กด "Save Version"
2. หลัง LightGBM เสร็จ (4-6 ชม.) → กด "Save Version" อีกครั้ง
3. หลัง CatBoost เสร็จ (6-8 ชม.) → กด "Save Version" อีกครั้ง

**Pros**:
- ✅ ถ้า timeout ระหว่างทาง ยังมี model บางตัว
- ✅ Download model ทีละตัวได้

**Cons**:
- ⚠️ ต้อง manual save + manual "Save Version"
- ⚠️ ยุ่งยาก

---

### Option 3: Split Training Across Multiple Notebooks

**ใช้เมื่อ**: แต่ละ model ใช้เวลานาน > 3 ชม.

**Approach**:
```
Notebook 1: Train XGBoost only
  → Save model → Save Version

Notebook 2: Train LightGBM only
  → Save model → Save Version

Notebook 3: Train CatBoost only
  → Save model → Save Version

Notebook 4: Load all models → Create Ensemble
  → Save best model → Save Version
```

**Pros**:
- ✅ แต่ละ notebook < 3 ชม. (ปลอดภัยจาก timeout)
- ✅ แยก model ชัดเจน

**Cons**:
- ⚠️ ยุ่งยาก ต้องจัดการหลาย notebooks
- ⚠️ ต้อง upload models เป็น datasets เพื่อ share ระหว่าง notebooks

---

## 🎯 คำแนะนำสำหรับคุณ

### สำหรับ ULTRAFIX Package:

**คำตอบคำถามของคุณ**:

1. **"ZIP ตัวใหม่สามารถ import เพื่อทำงานต่อใน notebook เดิมได้มั้ย?"**

   ✅ **ได้ครับ!** แต่ต้อง:
   ```
   1. Upload number-ML-kaggle-ULTRAFIX-20251005.zip เป็น dataset ใหม่
   2. ไปที่ notebook เดิม
   3. คลิก "Add Data" → เลือก ULTRAFIX dataset
   4. Remove dataset เก่า (MODERN version)
   5. แก้ไข Cell 2 path ให้ชี้ไปที่ ULTRAFIX dataset
   ```

2. **"เผื่อ checkpoint ยังอยู่จะได้รันต่อเลย?"**

   ❌ **ไม่ได้ครับ** - Checkpoint ไม่อยู่หลังปิด session!

   **เพราะ**:
   - Checkpoint บันทึกใน /kaggle/working/checkpoints/
   - Kaggle ลบ /kaggle/working/ ทั้งหมดเมื่อปิด session
   - Checkpoint จะหายไป 100%

3. **"มันต้องเปลี่ยน input dataset ใหม่ใช่มั้ย?"**

   ✅ **ใช่ครับ!** ต้อง:
   ```
   1. Upload ULTRAFIX ZIP เป็น dataset version ใหม่
      OR
   2. Create เป็น dataset คนละตัว (recommended)
   ```

4. **"หลังปิด session ไม่เห็น save อะไรให้เลย?"**

   ✅ **ถูกต้อง!** นี่คือพฤติกรรมปกติของ Kaggle!

   **วิธีแก้**:
   - ต้องกด **"Save Version"** ก่อนปิด session
   - หรือ download files ด้วยตัวเองก่อน session timeout

---

## 📝 Recommended Workflow (ที่ดีที่สุด)

### ขั้นตอนที่แนะนำ:

```
1. Upload ULTRAFIX ZIP
   → Kaggle → Datasets → New Dataset
   → Upload number-ML-kaggle-ULTRAFIX-20251005.zip
   → Title: "Phone Number ML - ULTRA FIX - Oct 2025"

2. Create New Notebook (หรือใช้เดิม)
   → Settings:
     - Accelerator: GPU P100 ✅
     - Persistence: Files only ✅
     - Environment: Latest ✅

3. Add ULTRAFIX Dataset
   → Add Data → Search "ultra fix"
   → Add

4. Run All Cells 1-6
   → รอ 6-8 ชั่วโมง
   → **ห้าม**ปิด browser
   → **ห้าม**ปิด Kaggle tab

5. เมื่อเทรนเสร็จ (R² > 0.90)
   → กด "Save Version" ทันที!
   → Kernel Type: Save & Run All (recommended)
   → Comment: "ULTRAFIX - R² = 0.93 - COMPLETE"

6. Download Model
   → ไปที่ Output tab
   → Download best_model.pkl
   → Download evaluation report

7. ใช้ Model Locally
   → Copy best_model.pkl ไปยัง local
   → Load และ predict
```

---

## ⚠️ Common Pitfalls (สิ่งที่ต้องระวัง!)

### 1. Session Timeout ก่อนเทรนเสร็จ
**สาเหตุ**: Kaggle limit 9 ชม., แต่ training ใช้ 6-8 ชม.
**วิธีป้องกัน**:
- เปิด notebook ตอนที่มีเวลาว่าง 8+ ชม.
- ไม่ต้องทำอย่างอื่นระหว่างรอ (ไปนอน ไปกินข้าว OK)
- เปิด tab ไว้ (ไม่ต้องดูตลอด แต่ไม่ปิด!)

### 2. ลืมกด "Save Version" หลังเทรนเสร็จ
**ผลกระทบ**: Model หาย = เทรนใหม่ทั้งหมด (6-8 ชม. สูญเปล่า!)
**วิธีป้องกัน**:
- ตั้ง alarm ก่อน training เสร็จ 30 นาที
- Check notebook ทุก 2 ชม.
- กด "Save Version" ทันทีเมื่อเห็น "Training Complete!"

### 3. Upload Dataset ผิดเวอร์ชัน
**ปัญหา**: ใช้ MODERN แทน ULTRAFIX → LightGBM crash!
**วิธีป้องกัน**:
- Check dataset name ให้ดี: "ultra-fix-oct-2025"
- Check file size: 130 KB (not 118 KB)
- Check ว่ามี training_callbacks.py ใน dataset

---

## 🎯 TL;DR (สรุปสั้นๆ)

### คำตอบคำถามของคุณ:

| คำถาม | คำตอบ |
|-------|-------|
| Import ZIP ใหม่ใน notebook เดิมได้มั้ย? | ✅ ได้ (เปลี่ยน dataset input) |
| Checkpoint อยู่หลังปิด session มั้ย? | ❌ ไม่อยู่ (Kaggle ลบ /kaggle/working/) |
| ต้องเปลี่ยน input dataset ใหม่มั้ย? | ✅ ใช่ (upload ULTRAFIX เป็น dataset) |
| ทำไม /kaggle/working/ หายหมด? | ✅ ปกติของ Kaggle (ไม่ persist) |

### วิธีที่ถูกต้อง:

```
1. Upload ULTRAFIX ZIP → New Dataset
2. Create/Use Notebook → Add ULTRAFIX dataset
3. Run All (6-8 ชม.) → ไม่ปิด browser!
4. Save Version ทันทีเมื่อเสร็จ!
5. Download model
```

### สิ่งที่ต้องจำ:

- ⚠️ Kaggle ไม่ persist /kaggle/working/
- ⚠️ ต้องกด "Save Version" เพื่อเก็บ outputs
- ⚠️ Checkpoint ใช้ไม่ได้จริง (design flaw ของเรา!)
- ✅ Training ต้องจบใน session เดียว
- ✅ Session limit = 9 ชม. (พอสำหรับ 6-8 ชม. training)

---

## 🔧 จะแก้ไข Checkpoint Issue ยังไง?

### วิธีที่เป็นไปได้ (ถ้าอยากใช้ checkpoint จริงๆ):

**Option A: Use Kaggle Datasets as Storage**
```python
# แทนที่จะ save ใน /kaggle/working/
# → Save ใน /kaggle/working/ + manual upload เป็น dataset

# หลังแต่ละ 10 trials:
joblib.dump(study, '/kaggle/working/checkpoint_trial_10.pkl')
# User: กด "Save Version" + Download checkpoint
# User: Upload checkpoint เป็น dataset ใหม่
# Next session: Load checkpoint จาก dataset
```

**Pros**: Checkpoint persist ได้จริง
**Cons**: ต้อง manual upload/download ทุกครั้ง (ยุ่งมาก!)

**Option B: Reduce Training Time**
```python
# ลด n_trials จาก 100 → 50
# Training time: 6-8 ชม. → 3-4 ชม.
# ปลอดภัยกว่า (ห่างจาก 9 ชม. limit)
```

**Pros**: ปลอดภัยจาก timeout
**Cons**: R² อาจต่ำกว่า (แต่น่าจะยังได้ > 0.90)

---

**สรุป**: Checkpoint system ที่เราสร้างมา มีประโยชน์สำหรับ **local training** หรือ **Colab with Drive mount** แต่ **ไม่ work กับ Kaggle** เพราะ Kaggle ลบ /kaggle/working/ หมด!

**Recommendation**: ใช้ **Option 1 (Training ครั้งเดียวจบ)** เป็นวิธีที่ดีที่สุด!
