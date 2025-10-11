# 📦 วิธีใช้ไฟล์สำหรับ Kaggle

**Created**: 2025-10-08
**Model**: CatBoost Training
**Duration**: 1-2 hours

---

## 📋 ไฟล์ที่คุณได้รับ:

1. **`Kaggle_CatBoost_Training.ipynb`** - Notebook พร้อมรัน (9 cells)
2. **`number-ML-kaggle-CatBoost.zip`** - Dataset package (0.14 MB)

---

## 🚀 วิธีใช้งาน (3 ขั้นตอน)

### ขั้นตอนที่ 1: Upload Dataset

1. ไปที่ https://www.kaggle.com/datasets
2. คลิก **"New Dataset"**
3. คลิก **"Upload"** → เลือก `number-ML-kaggle-CatBoost.zip`
4. ตั้งชื่อ: **`number-ml-kaggle-dataset`** (ต้องตรงกับชื่อนี้!)
5. Visibility: **Public** หรือ **Private**
6. คลิก **"Create"**

---

### ขั้นตอนที่ 2: สร้าง Notebook

1. ไปที่ https://www.kaggle.com/code
2. คลิก **"New Notebook"**
3. **ตั้งค่า:**
   - Settings → Accelerator → **GPU P100** ✅
   - Settings → Internet → **ON** ✅
4. **Add Dataset:**
   - ขวามือ → Add Data → ค้นหา `number-ml-kaggle-dataset`
   - คลิก **Add**

---

### ขั้นตอนที่ 3: Copy Notebook Code

1. เปิดไฟล์ `Kaggle_CatBoost_Training.ipynb` ในเครื่อง
2. Copy code จาก Cell 1-9 ทั้งหมด
3. Paste ลงใน Kaggle Notebook
4. **Run All** (Ctrl+Enter ทีละ cell หรือ Run All)

---

## 📝 Notebook Cells Overview:

| Cell | Description | Duration |
|------|-------------|----------|
| 1 | Copy dataset to working directory | 10s |
| 2 | Install dependencies | 2-3 min |
| 3 | Configure environment | 5s |
| 4 | **Train CatBoost** | **1-2 hours** |
| 5 | Check results | 5s |
| 6 | Test predictions | 10s |
| 7 | View logs (optional) | 5s |
| 8 | Download model | 5s |
| 9 | Check GPU (during training) | 5s |

---

## ⏱️ Timeline:

```
00:00 - Setup (Cells 1-3)           → 3 minutes
00:03 - Training (Cell 4)           → 1-2 hours  ⏰
01:03 - Results (Cells 5-8)         → 1 minute
──────────────────────────────────────────────────
Total: ~1-2 hours
```

---

## ✅ ตรวจสอบก่อนรัน:

- [ ] GPU P100 enabled (Settings → Accelerator)
- [ ] Internet ON (Settings → Internet)
- [ ] Dataset `number-ml-kaggle-dataset` added
- [ ] All 9 cells copied to notebook
- [ ] Ready to run! 🚀

---

## 📊 Expected Results:

**CatBoost Performance:**
- R² Score: **0.85-0.89**
- MAE: ~฿800-1,200
- RMSE: ~฿1,500-2,500
- Training Time: 1-2 hours

**Checkpoint File:**
- Location: `models/checkpoints/catboost_checkpoint.pkl`
- Size: ~50-100 MB
- Contains: model, preprocessor, params, scores

---

## 🎯 หลังจากเทรนเสร็จ:

### ถ้า R² ≥ 0.85:
✅ **สำเร็จ!** Data filtering ได้ผล!

**ทำอะไรต่อ:**
1. Download model (Cell 8)
2. Test predictions (Cell 6)
3. (Optional) Train more models: XGBoost, LightGBM
4. (Optional) Create ensemble

### ถ้า R² < 0.85:
⚠️ **ต่ำกว่าคาด** แต่ยังดีกว่า 0.4 เดิม!

**Solutions:**
1. เพิ่ม trials: แก้ line 173 ใน `train_catboost_only.py`
   ```python
   n_trials = 100  # เพิ่มจาก 50
   ```
2. Train ensemble (รวมหลายโมเดล → R² สูงขึ้น)
3. Check logs สำหรับ errors

---

## 💾 Download Model:

**Option 1: ใน Notebook (Cell 8)**
```python
from IPython.display import FileLink
display(FileLink('models/checkpoints/catboost_checkpoint.pkl'))
```

**Option 2: Kaggle UI**
- Right sidebar → Output
- Click **"Download"**
- เลือก `catboost_checkpoint.pkl`

---

## 🐛 Troubleshooting:

### Error: "No module named 'src'"
```bash
# ใน Cell 3 ตรวจสอบ:
import sys
sys.path.insert(0, '/kaggle/working')
```

### Error: "File not found: numberdata.csv"
```bash
# ตรวจสอบว่า dataset copy แล้ว:
!ls -lh /kaggle/working/data/raw/
```

### Error: "GPU not available"
- Settings → Accelerator → เลือก **GPU P100**
- Restart Kernel
- Re-run cells

### Training too slow
- 1-2 ชม. เป็นเวลาปกติสำหรับ 50 trials
- ถ้าเกิน 3 ชม. → อาจมีปัญหา GPU
- Check: `!nvidia-smi` (Cell 9)

---

## 📚 ไฟล์อื่นๆ ที่เกี่ยวข้อง:

- `KAGGLE_CATBOOST_QUICKSTART.md` - Detailed guide
- `NEXT_SESSION.md` - Full modular training guide
- `SESSION_012_SUMMARY.md` - Technical documentation
- `train_catboost_only.py` - Training script (ใน ZIP)

---

## 🎓 Tips:

1. **Save notebook version** หลังเทรนเสร็จ (File → Save Version)
2. **Download checkpoint ทันที** (Kaggle ลบหลัง 7 วัน)
3. **Copy logs** ไว้เผื่อ debug (`logs/catboost_*.log`)
4. **Monitor GPU** ระหว่างเทรน (Cell 9: `!nvidia-smi`)
5. **Check progress** ผ่าน Optuna progress bars

---

## 🔗 Quick Links:

- Kaggle Datasets: https://www.kaggle.com/datasets
- Kaggle Notebooks: https://www.kaggle.com/code
- GPU Quota: https://www.kaggle.com/settings (check remaining hours)

---

## 📞 Support:

**ถ้าเจอปัญหา:**
1. Check logs (Cell 7)
2. Run `!nvidia-smi` (Cell 9)
3. Check dataset copied (Cell 1 output)
4. Verify imports (Cell 3 output)

**Error messages:**
- Copy error message
- Check `KAGGLE_CATBOOST_QUICKSTART.md` troubleshooting
- Ask for help with error message

---

## ✨ Success Checklist:

**Setup Phase:**
- [x] Dataset uploaded: `number-ml-kaggle-dataset`
- [x] Notebook created with GPU P100
- [x] Internet enabled
- [x] Dataset added to notebook
- [x] All cells copied

**Training Phase:**
- [ ] Cell 1-3 completed (setup)
- [ ] Cell 4 running (training 1-2 hrs)
- [ ] GPU showing activity
- [ ] Optuna progress bars updating
- [ ] No error messages

**Completion Phase:**
- [ ] Training finished
- [ ] R² score ≥ 0.85 ✅
- [ ] Checkpoint saved (~50-100 MB)
- [ ] Predictions working (Cell 6)
- [ ] Model downloaded (Cell 8)
- [ ] Notebook version saved

---

**Created**: 2025-10-08
**Files**: 2 (Notebook + ZIP)
**Ready to upload!** 🚀

**เริ่มได้เลย!** Upload → Add Dataset → Copy Cells → Run! 🎯
