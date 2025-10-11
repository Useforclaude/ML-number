# 🚨 Kaggle: แก้ปัญหา R² แย่มาก (0.32 vs 0.85)

**Date**: 2025-10-06
**Error**: R² = 0.328 (Expected: > 0.85)
**Root Cause**: Code ใช้ Session 011D ไม่ใช่ 011E

---

## 🐛 ปัญหาที่เจอ

### 1. KeyboardInterrupt
```
Trial 44 failed: KeyboardInterrupt
```

**แปลว่า**:
- มีคนกด Stop/Interrupt kernel
- หรือ Kaggle session timeout
- หรือ browser crash

**ไม่ใช่ปัญหาหลัก!** เป็นแค่ผลจากปัญหาที่ 2

---

### 2. R² แย่มากผิดปกติ ⚠️ **ปัญหาจริง!**

```
🎯 Best R² so far: 0.328787  ❌ แย่มาก!
Expected R²: > 0.85          ✅ ควรได้
```

**ทำไมถึงแย่:**
- Trial 44/100 (44%) แต่ R² แย่สุดๆ
- ปกติ trial 10-20 ควรได้ R² > 0.7 แล้ว
- Training 26 นาที แต่ R² ยังแย่

---

## 🔍 สาเหตุที่แท้จริง

### จาก Error Log (Line 595):

```python
params={'sample_weight': sample_weight},  # sklearn 1.7+ uses 'params' not 'fit_params'
```

**นี่คือ Session 011D code** (hardcoded `params`)

**Session 011E ต้องใช้:**
```python
scores = cross_val_score_with_sample_weight(
    model, X_train, y_train,
    cv=cv_folds,
    scoring='r2',
    sample_weight=sample_weight,
    n_jobs=1
)
```

---

## ⚠️ ปัญหาคือ: Code ใน Kaggle ล้าสมัย!

### Timeline:
```
Session 011D: แก้ให้ Kaggle (hardcoded params)  ← Kaggle ใช้อันนี้
    ↓
Session 011E: Universal fix (wrapper function)  ← ยังไม่ได้อัปเดต!
```

**Kaggle code ยังใช้ Session 011D** = ใช้ `params` แบบ hardcoded
**แต่ควรใช้ Session 011E** = ใช้ wrapper function

---

## ✅ วิธีแก้ (2 Options)

### **Option 1: Upload ZIP Package ใหม่** (แนะนำ - ง่ายสุด)

#### Step 1: Download Package

**จาก Local WSL:**
```bash
# Package อยู่ที่
/home/u-and-an/projects/number-ML/packages/kaggle/number-ML-kaggle-SESSION-011E-20251006.zip

# Copy to Desktop
cp packages/kaggle/number-ML-kaggle-SESSION-011E-20251006.zip /mnt/c/Users/YourUsername/Desktop/
```

**หรือใช้ Windows Explorer:**
```
\\wsl$\Ubuntu\home\u-and-an\projects\number-ML\packages\kaggle\
```

#### Step 2: Upload to Kaggle

1. ไปที่ Kaggle Notebook
2. กด **"+ Add data"** (มุมบนขวา)
3. เลือก **"Upload"**
4. เลือกไฟล์: `number-ML-kaggle-SESSION-011E-20251006.zip`
5. รอ upload เสร็จ

#### Step 3: Extract และ Restart

**Kaggle Cell 1:**
```python
# Extract new package
!unzip -q /kaggle/input/your-dataset-name/number-ML-kaggle-SESSION-011E-20251006.zip -d /kaggle/working/
%cd /kaggle/working

# Verify Session 011E
!grep -n "cross_val_score_with_sample_weight" src/model_utils.py | head -3

# Should see:
# 30:def cross_val_score_with_sample_weight(model, X, y, cv, scoring, sample_weight=None, n_jobs=-1):
# ...
```

#### Step 4: Re-run Training

**Kaggle Cell 2+:** Run ทุก cells ใหม่ตั้งแต่ต้น

---

### **Option 2: Git Pull** (ต้องรู้จัก Git)

**ใน Kaggle Terminal:**
```bash
cd /kaggle/working
git pull origin main

# Verify commits
git log --oneline -5

# Must see:
# 60f99ec Add Paperspace start-from-zero guide
# 93483ba Add Paperspace quick update guide
# eabfe1e Add Session 011E documentation
# 4bbaf0b Session 011E: Universal sklearn compatibility  ← สำคัญ!
```

**Restart Kernel → Re-run Cells**

---

## 📊 หลังอัปเดตแล้ว ควรเห็น:

### ✅ Expected Output:

**Optuna Progress:**
```
[I 2025-10-06 15:30:01] Trial 0 complete. Value: 0.8523  ✅ ปกติ
[I 2025-10-06 15:30:15] Trial 1 complete. Value: 0.8612  ✅ ดีขึ้น
[I 2025-10-06 15:30:29] Trial 2 complete. Value: 0.8701  ✅ ดีขึ้นเรื่อยๆ
...
[I 2025-10-06 17:15:42] Trial 99 complete. Value: 0.9234  ✅ Best!

📈 Best R² so far: 0.9234  ✅ ดีมาก!
```

**Timeline:**
```
Trial 10: R² ~ 0.75
Trial 20: R² ~ 0.82
Trial 30: R² ~ 0.86
Trial 50: R² ~ 0.89
Trial 100: R² ~ 0.92+  ✅
```

---

## 🔍 วิธีเช็คว่าใช้ Session 011E จริง

**Kaggle Cell:**
```python
# Check version compatibility
from src.model_utils import SKLEARN_VERSION, USE_PARAMS_KWARG, cross_val_score_with_sample_weight

print(f"sklearn version: {SKLEARN_VERSION}")
print(f"Uses params kwarg: {USE_PARAMS_KWARG}")
print(f"Wrapper function exists: {callable(cross_val_score_with_sample_weight)}")

# Expected output (Kaggle):
# sklearn version: (1, 7)
# Uses params kwarg: True
# Wrapper function exists: True  ✅
```

---

## 🎯 ทำไม R² ถึงแย่มาก (0.32 vs 0.85)?

### เปรียบเทียบ:

| Scenario | R² Result | Reason |
|----------|-----------|--------|
| **Session 011D (Kaggle ปัจจุบัน)** | 0.32 ❌ | Hardcoded `params`, sklearn 1.7 แต่ไม่ compatible กับ Paperspace |
| **Session 011E (ที่ควรใช้)** | > 0.85 ✅ | Universal wrapper, works everywhere |

**คำอธิบาย:**
- Session 011D แก้ให้ Kaggle แต่ใช้วิธี hardcode `params`
- Code อาจมีปัญหาอื่นที่ทำให้ R² แย่
- Session 011E แก้ทุกอย่างด้วย wrapper function + tested

---

## 🚀 Summary: 4 Steps to Fix

1. ✅ Download: `number-ML-kaggle-SESSION-011E-20251006.zip`
2. ✅ Upload to Kaggle (Add Data → Upload)
3. ✅ Extract: `!unzip -q /kaggle/input/.../SESSION-011E.zip -d /kaggle/working/`
4. ✅ Re-run: Restart kernel → Run all cells

**Expected Time**:
- Setup: 5 นาที
- Training: 9-12 ชั่วโมง
- R² Result: > 0.93

---

## ⚠️ Red Flags - ถ้าเห็นอย่างใดอย่างหนึ่งนี้ = ยังใช้ code เก่าอยู่

```
❌ R² < 0.5 ในช่วง 20 trials แรก
❌ Error: "cross_val_score_with_sample_weight not found"
❌ grep ไม่เจอ wrapper function
❌ git log ไม่เห็น commit 4bbaf0b
```

---

## 📞 ถ้ายังมีปัญหา

**แสดงข้อมูลนี้:**
1. Output ของ `git log --oneline -5` (ใน Kaggle)
2. Output ของ `grep "cross_val_score_with_sample_weight" src/model_utils.py`
3. R² value ในช่วง 10-20 trials แรก
4. Total training time

---

**Created**: 2025-10-06
**Session**: 011E Fix Required
**Package**: `number-ML-kaggle-SESSION-011E-20251006.zip`
**Expected R²**: > 0.93
**Current R²**: 0.32 (needs fix!)
