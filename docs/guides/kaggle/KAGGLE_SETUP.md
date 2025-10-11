# 🔥 Kaggle ML Training with Auto-Resume - Complete Setup Guide

**เทรนบน Kaggle พร้อม Auto-Resume - ไม่ต้องกลัวหลุดการเชื่อมต่อ!**

---

## 🎯 Why Kaggle?

### Advantages over Google Colab
- ✅ **P100 GPU** (30% faster than Colab's T4)
- ✅ **More RAM**: 16-30 GB (vs Colab's 12 GB)
- ✅ **More Stable**: Fewer disconnections
- ✅ **Longer Runtime**: 9 hours vs Colab's 4-6 hours
- ✅ **Unlimited Dataset Storage**
- ✅ **Pre-installed ML libraries** (scikit-learn, XGBoost, etc.)
- ✅ **Auto-commit**: Save notebook progress permanently

---

## 📦 Quick Start (3 Steps)

### Step 1: Upload Data as Kaggle Dataset

**Option A: Upload CSV File**
1. Go to https://www.kaggle.com/datasets
2. Click **"New Dataset"**
3. Upload `numberdata.csv`
4. Title: `phone-number-price-data`
5. Click **"Create"**
6. Note the dataset path (e.g., `yourusername/phone-number-price-data`)

**Option B: Upload Project ZIP**
1. Download `number-ML-kaggle-package.zip`
2. Upload as dataset: `phone-number-ml-project`
3. This includes all code + data

### Step 2: Create New Kaggle Notebook

1. Go to https://www.kaggle.com/code
2. Click **"New Notebook"**
3. Click **"File" → "Import Notebook"**
4. Upload `Kaggle_ML_Training_AutoResume.ipynb`
5. OR copy-paste cells from the notebook

### Step 3: Add Datasets to Notebook

1. In notebook, click **"Add Data"** (right sidebar)
2. Search for your dataset: `phone-number-price-data`
3. Click **"Add"**
4. Dataset will be available at `/kaggle/input/phone-number-price-data/`

---

## 🚀 Using the Notebook

### Cell-by-Cell Guide

#### Cell 1: Environment Setup
```python
# Auto-detects Kaggle environment
# Sets up paths automatically
# No mounting needed (unlike Colab)!
```
**Output**: Shows Kaggle paths and GPU info

#### Cell 2: Load Project Code
```python
# If you uploaded project as dataset
# Extracts all Python files from src/
```
**Output**: Lists all imported modules

#### Cell 3: Install Dependencies
```python
# Only installs what's missing
# Most libraries pre-installed on Kaggle
```
**Output**: Shows installed packages

#### Cell 4: 🔄 Auto-Detect Checkpoint (CRITICAL!)
```python
# Checks if checkpoint exists in /kaggle/working/
# If found → RESUME MODE
# If not found → FRESH START
```

**Expected Outputs**:

**First Run (No Checkpoint)**:
```
📂 Checkpoint Manager initialized
   Environment: KAGGLE
   Directory: /kaggle/working/ML_Phone_Number_Project/checkpoints
   Max checkpoints: 5
   Save every: 10 epochs

ℹ️  No checkpoint found. Starting fresh.
🆕 FRESH START MODE
   Starting from epoch: 0
   Total epochs to train: 100
```

**After Disconnect & Reconnect (Checkpoint Found)**:
```
📂 Checkpoint Manager initialized
   Environment: KAGGLE

✅ Checkpoint loaded: checkpoint_latest.pkl
   Epoch: 50
   Timestamp: 2025-10-04T10:30:00
   Metrics: {'loss': 0.12, 'r2': 0.89}

🔄 RESUME MODE ACTIVATED
   Resuming from epoch: 51
   Remaining epochs: 50
   Previous best R²: 0.89
```

#### Cell 5: Load Data & Features
```python
# Loads from /kaggle/input/
# Creates 250+ features
```
**Output**: Shows data shape and feature count

#### Cell 6: 🎯 Train with Auto-Resume (MAIN TRAINING)
```python
# Uses P100 GPU automatically
# Auto-saves checkpoint every 10 epochs
# Continues from last checkpoint if available
```

**Training Output**:
```
🎯 Training XGBoost Model
   Using GPU: True (P100)
   Start epoch: 0 (or 51 if resumed)
   End epoch: 100

Epoch 10/100: Loss=0.15, R²=0.85 ✅ Checkpoint saved
Epoch 20/100: Loss=0.13, R²=0.87 ✅ Checkpoint saved
Epoch 30/100: Loss=0.11, R²=0.89 ✅ Checkpoint saved
...
```

#### Cell 7: Evaluate & Save
```python
# Evaluates final model
# Saves to /kaggle/working/
```
**Output**: Shows R², MAE, RMSE metrics

#### Cell 8: Commit Notebook
```python
# Instructions for saving progress permanently
```
**Action Required**: Click **"Save Version"** → **"Save & Run All"**

---

## 🔄 Resume After Disconnect/Timeout

### What Happens During Disconnect?
- Kaggle kernels time out after **9 hours**
- All RAM is cleared
- But **/kaggle/working/** is persistent!

### How to Resume (2 Steps)

**Step 1: Restart Kernel**
- In notebook, click **"Run All"** or run cells individually

**Step 2: Cell 4 Auto-Detects Checkpoint**
- Automatically finds latest checkpoint
- Shows resume info
- Training continues from last saved epoch!

### Example Resume Scenario

**Original Training Session** (disconnected at epoch 67):
```
Epoch 60/100: Loss=0.09, R²=0.91 ✅ Checkpoint saved
Epoch 67/100: Loss=0.08, R²=0.92 [DISCONNECTED]
```

**After Reconnect** (run cells again):
```
Cell 4 output:
✅ Checkpoint loaded: checkpoint_epoch_60.pkl
   Epoch: 60

🔄 RESUME MODE ACTIVATED
   Resuming from epoch: 61
   Remaining epochs: 40

Cell 6 output:
Epoch 61/100: Loss=0.08, R²=0.92 [continues from here!]
Epoch 70/100: Loss=0.07, R²=0.93 ✅ Checkpoint saved
...
```

**Data Loss**: Only epochs 61-67 (7 epochs) need to be retrained!

---

## ⚙️ Configuration Options

### Change Checkpoint Frequency

In **Cell 4**, modify:
```python
checkpoint_manager = CheckpointManager(
    checkpoint_dir=CHECKPOINT_DIR,
    max_checkpoints=5,      # Keep last 5 checkpoints
    save_every=10,          # Save every 10 epochs (change this!)
    auto_sync=True
)
```

**Examples**:
- `save_every=5` → Save every 5 epochs (more frequent, safer)
- `save_every=20` → Save every 20 epochs (less frequent, faster)
- `max_checkpoints=10` → Keep last 10 checkpoints (more history)

### Change Total Epochs

In **Cell 6**, modify:
```python
trainer = KaggleTrainer(
    checkpoint_manager=checkpoint_manager,
    total_epochs=100,       # Change this!
    device='gpu'
)
```

### Enable/Disable GPU

In **Cell 6**, modify model parameters:
```python
# Use GPU (default)
model_params = {
    'tree_method': 'gpu_hist',
    'predictor': 'gpu_predictor'
}

# Use CPU only
model_params = {
    'tree_method': 'hist',
    'predictor': 'cpu_predictor'
}
```

---

## 🐛 Troubleshooting

### Problem 1: "No checkpoint found" after disconnect

**Cause**: Checkpoints not saved to `/kaggle/working/`

**Solution**:
```python
# In Cell 4, verify checkpoint directory
print(f"Checkpoint dir: {checkpoint_manager.checkpoint_dir}")
print(f"Exists: {checkpoint_manager.checkpoint_dir.exists()}")

# List checkpoints
import glob
checkpoints = glob.glob(str(CHECKPOINT_DIR / '*.pkl'))
print(f"Found {len(checkpoints)} checkpoints")
```

### Problem 2: "ImportError: No module named 'src'"

**Cause**: Project code not in Python path

**Solution**: In Cell 2, add:
```python
import sys
sys.path.insert(0, '/kaggle/working/number-ML')
```

### Problem 3: GPU not detected

**Cause**: GPU not enabled in notebook settings

**Solution**:
1. Click **"Settings"** (right sidebar)
2. Under **"Accelerator"**, select **"GPU P100"**
3. Click **"Save"**
4. Restart kernel

**Verify GPU**:
```python
import torch
print(f"GPU available: {torch.cuda.is_available()}")
print(f"GPU name: {torch.cuda.get_device_name(0)}")
```

### Problem 4: "Out of Memory" error

**Cause**: Model/data too large for RAM

**Solution**:
```python
# Reduce batch size in Cell 6
trainer = KaggleTrainer(
    checkpoint_manager=checkpoint_manager,
    total_epochs=100,
    batch_size=128  # Default: 256, try 128 or 64
)
```

### Problem 5: Checkpoints not loading correctly

**Cause**: Corrupted checkpoint file

**Solution**:
```python
# In Cell 4, load specific checkpoint
checkpoint = checkpoint_manager.load_checkpoint(
    '/kaggle/working/ML_Phone_Number_Project/checkpoints/checkpoint_epoch_50.pkl'
)
```

---

## 📊 Monitoring Training Progress

### View Recovery Info

After each checkpoint save, a `recovery_info.json` is created:

```python
# In any cell, run:
checkpoint_manager.print_recovery_info()
```

**Output**:
```
==================================================
📋 RECOVERY INFORMATION
==================================================
Last Epoch: 60/100
Progress: 60.0%
Timestamp: 2025-10-04T10:30:00

Metrics:
  loss: 0.09
  r2: 0.91

Next Steps: Continue training from epoch 61

Resume Command:
  Load checkpoint_epoch_60.pkl and continue from epoch 61
==================================================
```

### Download Checkpoints

```python
# In Cell 7, download checkpoint to local machine
from IPython.display import FileLink

checkpoint_path = '/kaggle/working/ML_Phone_Number_Project/checkpoints/checkpoint_latest.pkl'
FileLink(checkpoint_path)
```

---

## 💾 Saving Results Permanently

### Important: Kaggle's /kaggle/working/ is temporary!

After kernel restarts, `/kaggle/working/` is cleared **unless you commit the notebook**.

### How to Save Permanently (2 Options)

#### Option 1: Commit Notebook (Recommended)
1. Click **"Save Version"** (top right)
2. Select **"Save & Run All"** (runs all cells and saves output)
3. Click **"Save"**
4. Output data in `/kaggle/working/` is preserved in notebook version

#### Option 2: Download to Local
```python
# In Cell 8, download final model
from IPython.display import FileLink

model_path = '/kaggle/working/ML_Phone_Number_Project/models/best_model.pkl'
FileLink(model_path)
```

---

## 🎯 Best Practices

### 1. Commit Notebook Every Hour
- Click **"Save Version"** → **"Quick Save"**
- Preserves checkpoint progress in case of unexpected disconnect

### 2. Use Meaningful Checkpoint Names
```python
# Custom checkpoint naming
checkpoint_manager.save_checkpoint(
    epoch=50,
    model=model,
    metrics={'loss': 0.09, 'r2': 0.91},
    is_best=True  # Saves as checkpoint_best.pkl
)
```

### 3. Monitor GPU Usage
```python
# Check GPU memory
!nvidia-smi
```

### 4. Test Resume Before Long Training
```python
# Quick test: train 20 epochs, disconnect, resume
trainer = KaggleTrainer(
    checkpoint_manager=checkpoint_manager,
    total_epochs=20,  # Short test
    device='gpu'
)
```

### 5. Keep Multiple Checkpoint Versions
```python
checkpoint_manager = CheckpointManager(
    max_checkpoints=10,  # Keep more history
    save_every=5         # Save more frequently
)
```

---

## 🔍 Advanced Features

### Custom Checkpoint Data

Save additional data with checkpoint:
```python
extra_data = {
    'hyperparameters': {'learning_rate': 0.01},
    'feature_names': ['feature1', 'feature2'],
    'scaler': fitted_scaler
}

checkpoint_manager.save_checkpoint(
    epoch=50,
    model=model,
    optimizer=optimizer,
    metrics={'loss': 0.09},
    extra_data=extra_data
)
```

### Load Specific Checkpoint

```python
# Load best checkpoint instead of latest
best_checkpoint = checkpoint_manager.load_checkpoint(
    str(CHECKPOINT_DIR / 'checkpoint_best.pkl')
)

if best_checkpoint:
    model.load_state_dict(best_checkpoint['model_state'])
    print(f"Loaded best model with R²={best_checkpoint['metrics']['r2']}")
```

### Manual Checkpoint Cleanup

```python
# Remove old checkpoints manually
checkpoints = checkpoint_manager.find_all_checkpoints()
for ckpt in checkpoints[:-3]:  # Keep only last 3
    os.remove(ckpt)
    print(f"Deleted: {ckpt}")
```

---

## 📝 Example Full Workflow

### Session 1: Start Training (Fresh)
```bash
1. Upload data as Kaggle Dataset
2. Import notebook
3. Add dataset to notebook
4. Enable GPU P100 in settings
5. Run Cell 1-3 (setup)
6. Run Cell 4 → Shows "FRESH START"
7. Run Cell 5 (load data)
8. Run Cell 6 (training starts)
   - Epoch 10: ✅ Checkpoint saved
   - Epoch 20: ✅ Checkpoint saved
   - Epoch 30: ✅ Checkpoint saved
   - [TIMEOUT after 9 hours at epoch 87]
```

### Session 2: Resume After Timeout
```bash
1. Open same notebook
2. Click "Run All" (or run cells 1-7)
3. Cell 4 → Shows "RESUME MODE - Epoch 80" (last checkpoint)
4. Cell 6 → Training continues from epoch 81!
   - Epoch 81-100: Completes remaining epochs
   - Epoch 90: ✅ Checkpoint saved
   - Epoch 100: ✅ Training complete!
5. Cell 7 → Evaluates final model (R² = 0.93)
6. Click "Save Version" → Commit notebook
7. Download best_model.pkl
```

**Total Time Lost**: Only 7 epochs (80-87) need retraining!

---

## 🎓 Tips for Maximum Efficiency

### 1. Optimize Checkpoint Frequency
- Early epochs (1-50): Save every 10 epochs
- Late epochs (51-100): Save every 5 epochs (closer to finish)

### 2. Use Early Stopping
```python
# In Cell 6, add early stopping
best_r2 = 0
patience = 10
no_improve = 0

for epoch in range(start_epoch, total_epochs):
    # Train...
    if current_r2 > best_r2:
        best_r2 = current_r2
        no_improve = 0
    else:
        no_improve += 1

    if no_improve >= patience:
        print(f"Early stopping at epoch {epoch}")
        break
```

### 3. Enable Auto-Commit (Kaggle Feature)
- Go to notebook settings
- Enable **"Auto-save every 10 minutes"**
- Checkpoints preserved even if you forget to commit

### 4. Test on Small Dataset First
```python
# In Cell 5, use only 1000 samples for testing
df_sample = df.sample(1000)
X, y = create_features(df_sample)
```

---

## 📚 Additional Resources

### Files in Kaggle Package
- `src/checkpoint_manager.py` - Checkpoint management
- `src/train_colab.py` - Training script (works on Kaggle too!)
- `Kaggle_ML_Training_AutoResume.ipynb` - Main notebook
- `KAGGLE_SETUP.md` - This guide
- `requirements.txt` - Dependencies (minimal)

### Related Documentation
- `COLAB_AUTO_RESUME_GUIDE.md` - Colab version guide
- `COLAB_VS_KAGGLE_COMPARISON.md` - Platform comparison
- `README.md` - Project overview

### Support & Troubleshooting
- Check `recovery_info.json` for training state
- Review checkpoint files in `/kaggle/working/ML_Phone_Number_Project/checkpoints/`
- Test checkpoint loading before long training runs

---

## 🏆 Success Criteria

After completing training, you should have:

- ✅ Trained model with R² > 0.90
- ✅ Checkpoint files in `/kaggle/working/`
- ✅ Recovery info JSON with progress tracking
- ✅ Final model saved as `best_model.pkl`
- ✅ Notebook committed with all outputs
- ✅ Zero data loss from disconnections!

---

**Remember**: Kaggle automatically saves checkpoints to `/kaggle/working/` and can resume from any point. Train with confidence! 🚀

*Last Updated*: 2025-10-04
*Version*: 1.0.0
