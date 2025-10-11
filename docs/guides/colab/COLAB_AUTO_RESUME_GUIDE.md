# 🚀 Google Colab Auto-Resume Training Guide

> **Train ML models on Colab without losing progress when disconnected!**

---

## 🎯 Problem Solved

### Before (ปัญหาเดิม):
- ❌ Colab runtime timeout → ต้อง train ใหม่ทั้งหมด
- ❌ Connection lost → Progress หายหมด
- ❌ Train 50 epochs → หลุด → เริ่ม epoch 0 ใหม่
- ❌ เสียเวลา hours ทุกครั้งที่หลุด

### After (วิธีแก้ใหม่):
- ✅ Auto-save checkpoint ทุก 10 epochs → Google Drive
- ✅ Connection lost → Resume จาก epoch สุดท้าย
- ✅ Train 50 epochs → หลุด → Resume จาก epoch 50
- ✅ Zero data loss!

---

## 📋 Quick Start (5 Minutes)

### Step 1: Setup (One-Time)
```bash
# In Colab, run this cell:
!git clone https://github.com/YOUR_REPO/number-ML.git
!cd number-ML && python setup_colab_complete.py
```

### Step 2: Open Notebook
```
Open: notebooks/Colab_ML_Training_AutoResume.ipynb
```

### Step 3: Run Cells
```
Run Cell 1-6 sequentially
→ Training starts with auto-checkpoint
```

### Step 4: If Disconnected
```
1. Reconnect to Colab
2. Run Cell 1-6 again
3. Cell 4 detects checkpoint
4. Training resumes automatically!
```

**That's it!** 🎉

---

## 🎓 How It Works

### Auto-Checkpoint System

```
Training Loop
     │
     ▼
Epoch 1, 2, 3... → No save yet
     │
     ▼
Epoch 10 → ✅ Save checkpoint to Drive
     │
     ▼
Epoch 11, 12, 13... → Continue
     │
     ▼
Epoch 20 → ✅ Save checkpoint to Drive
     │
     ▼
   [CONNECTION LOST] ❌
     │
     ▼
Reconnect to Colab
     │
     ▼
Run Cell 1-4 again
     │
     ▼
Cell 4: "Found checkpoint_epoch_20.pkl"
     │
     ▼
Resume from Epoch 21 → ✅ Continue!
```

### Files Saved to Google Drive

```
/content/drive/MyDrive/ML_Phone_Number_Project/
├── checkpoints/
│   ├── checkpoint_epoch_10.pkl
│   ├── checkpoint_epoch_20.pkl
│   ├── checkpoint_epoch_30.pkl
│   ├── checkpoint_latest.pkl  ← Always most recent
│   ├── checkpoint_best.pkl    ← Best R² score
│   └── recovery_info.json     ← Resume instructions
├── models/
│   ├── xgboost_final.pkl
│   └── final_model_complete.pkl
├── logs/
│   └── training_log.txt
└── results/
    ├── evaluation_report.txt
    └── predictions.csv
```

---

## 📊 Notebook Structure (8 Cells)

### Cell 1: Mount Drive & Setup
- Mounts Google Drive
- Creates project directories
- Verifies Drive connection

### Cell 2: Upload Project
- Upload ZIP file OR
- Download from GitHub
- Extract to /content/number-ML

### Cell 3: Install Dependencies
- Installs all required packages
- Verifies imports work
- ~2-5 minutes

### Cell 4: Auto-Detect Checkpoint ⭐
**Most Important Cell!**
```python
# This cell checks:
if checkpoint_exists_in_drive():
    ✅ RESUME MODE
    Load checkpoint
    Start from last epoch
else:
    🆕 FRESH START
    Start from epoch 0
```

### Cell 5: Load Data
- Loads training data
- Feature engineering
- Train/test split

### Cell 6: Train with Auto-Checkpoint ⭐
**The Magic Happens Here!**
- Trains model
- Auto-saves every 10 epochs
- Syncs to Google Drive
- If disconnected → Just run again!

### Cell 7: Evaluate
- Calculates metrics
- Saves results
- Creates reports

### Cell 8: Download
- Downloads final model
- Optional: Download to local

---

## 🔄 Resume Scenarios

### Scenario 1: Normal Training (No Disconnection)
```
Session 1:
  Run Cell 1-6
  Train epoch 0 → 100
  Complete successfully ✅

Result: Model saved to Drive
```

### Scenario 2: Disconnect at Epoch 47
```
Session 1:
  Run Cell 1-6
  Train epoch 0 → 47
  [DISCONNECT] ❌
  Last checkpoint: epoch_40.pkl

Session 2 (after reconnect):
  Run Cell 1-6 again
  Cell 4: "Found checkpoint_epoch_40.pkl"
  Resume from epoch 41
  Train epoch 41 → 100
  Complete successfully ✅

Result: Lost only epochs 41-47 (7 epochs)
```

### Scenario 3: Multiple Disconnects
```
Session 1: Epoch 0 → 25 [disconnect]
Session 2: Epoch 26 → 53 [disconnect] (resumed from epoch_20)
Session 3: Epoch 54 → 78 [disconnect] (resumed from epoch_50)
Session 4: Epoch 79 → 100 ✅ (resumed from epoch_70)

Result: Successfully completed training!
```

---

## ⚙️ Configuration Options

### Adjust Save Frequency

In Cell 6, change `SAVE_EVERY`:
```python
SAVE_EVERY = 10  # Save every 10 epochs (default)
# or
SAVE_EVERY = 5   # Save every 5 epochs (more frequent)
# or
SAVE_EVERY = 20  # Save every 20 epochs (less frequent)
```

**Trade-off:**
- Smaller value = More checkpoints = Faster resume = Larger Drive usage
- Larger value = Fewer checkpoints = Slower resume = Less Drive usage

### Adjust Max Checkpoints

In Cell 4:
```python
checkpoint_manager = CheckpointManager(
    checkpoint_dir=CHECKPOINT_DIR,
    max_checkpoints=5,  # Keep last 5 checkpoints (default)
    save_every=10
)
```

**Example:**
- max_checkpoints=5 → Keeps: epoch_60, 70, 80, 90, 100
- max_checkpoints=10 → Keeps more history

### Change Model Type

In Cell 6:
```python
MODEL_TYPE = 'xgboost'  # Default
# or
MODEL_TYPE = 'lightgbm'
# or
MODEL_TYPE = 'catboost'
# or
MODEL_TYPE = 'random_forest'
```

---

## 🧪 Testing the System

### Test 1: Verify Checkpoint Save
```python
# In Cell 6, after training starts:
# Check Google Drive folder:
# /content/drive/MyDrive/ML_Phone_Number_Project/checkpoints/

# You should see:
# checkpoint_epoch_10.pkl
# checkpoint_latest.pkl
# recovery_info.json
```

### Test 2: Simulate Disconnect & Resume
```python
# 1. Start training (Cell 1-6)
# 2. Wait until epoch 15
# 3. Runtime → Disconnect and delete runtime
# 4. Reconnect to Colab
# 5. Run Cell 1-6 again
# 6. Cell 4 should show: "Found checkpoint_epoch_10.pkl"
# 7. Training resumes from epoch 11
```

### Test 3: Verify Recovery Info
```python
# In Cell 4, after detecting checkpoint:
checkpoint_manager.print_recovery_info()

# Should display:
# - Last epoch completed
# - Progress percentage
# - Metrics (R², loss)
# - Next steps
```

---

## 🐛 Troubleshooting

### Problem 1: Checkpoint Not Found

**Symptom:**
```
Cell 4: "No checkpoint found. Starting fresh."
```

**Solution:**
```bash
# Check if checkpoints exist in Drive:
!ls -lh /content/drive/MyDrive/ML_Phone_Number_Project/checkpoints/

# If empty:
# - Training hasn't reached save_every yet (epoch < 10)
# - Drive path is wrong
# - Checkpoint save failed

# Fix:
# 1. Verify Drive is mounted (Cell 1)
# 2. Check PROJECT_DIR path
# 3. Run training for at least 10 epochs
```

### Problem 2: Drive Not Mounted

**Symptom:**
```
FileNotFoundError: /content/drive/MyDrive/...
```

**Solution:**
```python
# Run Cell 1 again to mount Drive
from google.colab import drive
drive.mount('/content/drive', force_remount=True)
```

### Problem 3: Checkpoint Corrupted

**Symptom:**
```
Error loading checkpoint: ...
```

**Solution:**
```python
# Use older checkpoint:
# 1. Check available checkpoints:
!ls -lt /content/drive/MyDrive/ML_Phone_Number_Project/checkpoints/

# 2. Manually load specific checkpoint in Cell 4:
checkpoint_path = f"{PROJECT_DIR}/checkpoints/checkpoint_epoch_20.pkl"
checkpoint = checkpoint_manager.load_checkpoint(checkpoint_path)
```

### Problem 4: Out of Drive Storage

**Symptom:**
```
OSError: No space left on device
```

**Solution:**
```python
# 1. Reduce max_checkpoints:
max_checkpoints=3  # Keep fewer checkpoints

# 2. Or increase save_every:
save_every=20  # Save less frequently

# 3. Or cleanup old checkpoints:
!rm /content/drive/MyDrive/ML_Phone_Number_Project/checkpoints/checkpoint_epoch_10.pkl
```

---

## 💡 Best Practices

### 1. Always Start with Cell 1-4
```
✅ Run Cell 1-4 EVERY time you start
❌ Don't skip Cell 4 (checkpoint detection)
```

### 2. Check Recovery Info After Resume
```python
# In Cell 4, after detecting checkpoint:
checkpoint_manager.print_recovery_info()
# Verify epoch, metrics, timestamp
```

### 3. Save Checkpoints to Drive, Not /content/
```
✅ checkpoint_dir = '/content/drive/MyDrive/project/checkpoints'
❌ checkpoint_dir = '/content/checkpoints'  # Will be lost!
```

### 4. Use Descriptive Project Names
```
✅ PROJECT_NAME = 'ML_Phone_Thai_v2_Oct2025'
❌ PROJECT_NAME = 'test'
```

### 5. Backup Final Model
```python
# After training completes (Cell 7):
# Download final model to local:
files.download(f"{PROJECT_DIR}/models/final_model_complete.pkl")

# Or copy to another Drive folder:
!cp {PROJECT_DIR}/models/final_model_complete.pkl \
    /content/drive/MyDrive/Backups/
```

---

## 📈 Performance Tips

### Reduce Training Time
```python
# Use GPU (if available):
# Runtime → Change runtime type → GPU

# Reduce epochs for testing:
TOTAL_EPOCHS = 50  # Instead of 100

# Use fewer cross-validation folds:
cv_folds = 5  # Instead of 10
```

### Optimize Drive Sync
```python
# Checkpoint manager already optimized
# But you can monitor sync:

import os
checkpoint_path = f"{CHECKPOINT_DIR}/checkpoint_latest.pkl"
size_mb = os.path.getsize(checkpoint_path) / (1024 * 1024)
print(f"Checkpoint size: {size_mb:.2f} MB")
```

---

## 🎯 Success Criteria

**You know it's working when:**

1. ✅ Cell 1: "Google Drive mounted successfully!"
2. ✅ Cell 4: Shows checkpoint status clearly
3. ✅ Cell 6: Prints "Checkpoint saved: epoch X" every 10 epochs
4. ✅ Google Drive shows checkpoint files
5. ✅ After disconnect → Cell 4 shows "RESUME MODE ACTIVATED"

**If any of these fail → Check Troubleshooting section**

---

## 📊 Example Output

### First Run (Fresh Start):
```
Cell 4:
==========================================================
🆕 FRESH START MODE
==========================================================
No checkpoint found.
Will start training from epoch 0.
Checkpoints will be saved to Google Drive every 10 epochs.
==========================================================

Cell 6:
Epoch 10/100 | Train Loss: 0.1234 | Val Loss: 0.1456 | R²: 0.8543
✅ Checkpoint saved: epoch 10

Epoch 20/100 | Train Loss: 0.0987 | Val Loss: 0.1123 | R²: 0.8891
✅ Checkpoint saved: epoch 20
```

### After Disconnect & Resume:
```
Cell 4:
==========================================================
🔄 RESUME MODE ACTIVATED
==========================================================
Last completed epoch: 20
Will resume from epoch: 21
Checkpoint timestamp: 2025-10-04T12:30:00

Previous metrics:
  train_loss: 0.0987
  val_loss: 0.1123
  r2_score: 0.8891
==========================================================

Cell 6:
▶️  Resuming from epoch 21/100

Epoch 21/100 | Train Loss: 0.0954 | Val Loss: 0.1089 | R²: 0.8923
Epoch 30/100 | Train Loss: 0.0876 | Val Loss: 0.1012 | R²: 0.9012
✅ Checkpoint saved: epoch 30
```

---

## 🎉 Conclusion

**With this system, you can:**

1. ✅ Train for days without worry
2. ✅ Disconnect/reconnect anytime
3. ✅ Never lose progress
4. ✅ Resume exactly where you left off
5. ✅ Zero configuration needed

**Just run Cell 1-6 → Training is safe!** 🚀

---

## 📞 Need Help?

### Check These First:
1. `recovery_info.json` in checkpoints folder
2. Cell 4 output (checkpoint status)
3. Google Drive folder (verify files exist)

### Common Issues:
- Drive not mounted → Run Cell 1 again
- Checkpoint not found → Wait for epoch 10
- Loading error → Use older checkpoint

### Still Stuck?
- Check `TROUBLESHOOTING.md`
- Review notebook comments
- Verify all cells ran successfully

---

**Created:** 2025-10-04
**Version:** 1.0.0
**Tested On:** Google Colab Free & Pro

🎯 **Happy Training!** 🚀
