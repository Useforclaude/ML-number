# 🤖 GPU Auto-Configuration Usage Guide

**How to use GPU recommendations (NOT hardcoded)**

---

## 🎯 Concept

**`gpu_config_auto.json`** = **Recommendation only** (ไม่ใช่ hardcode!)

- ✅ System แนะนำว่า model ไหนควรใช้ GPU/CPU
- ✅ คุณเลือกเองได้ว่าจะตาม recommendation หรือไม่
- ✅ ปรับแต่งได้ตอนรัน training

---

## 📊 Example: gpu_config_auto.json

```json
{
  "has_gpu": true,
  "gpu_name": "NVIDIA Quadro P5000",
  "gpu_memory_gb": 16.0,
  "tier": "Paperspace Pro ($8/month)",
  "expected_time": "7-8 hours",
  "model_gpu_settings": {
    "xgboost": true,
    "lightgbm": true,
    "catboost": true,
    "randomforest": false
  },
  "_note": "This is a RECOMMENDATION based on your GPU. You can override these settings when training.",
  "_usage": "In notebook: Load this file and modify model_gpu_settings as needed"
}
```

---

## 💡 How to Use in Notebook

### Option 1: Use Recommendations As-Is (แนะนำสำหรับมือใหม่)

```python
# Cell 2: Load auto-configuration
import json

with open('/storage/number-ML/gpu_config_auto.json', 'r') as f:
    gpu_config = json.load(f)

print("🤖 Auto-configured settings:")
for model, use_gpu in gpu_config['model_gpu_settings'].items():
    device = "GPU" if use_gpu else "CPU"
    print(f"  {model}: {device}")

# Use recommendations
xgb_use_gpu = gpu_config['model_gpu_settings']['xgboost']
lgb_use_gpu = gpu_config['model_gpu_settings']['lightgbm']
cat_use_gpu = gpu_config['model_gpu_settings']['catboost']

print(f"\n✅ Using recommended settings for {gpu_config['tier']}")
```

---

### Option 2: Override Specific Models (ถ้าต้องการปรับแต่ง)

```python
# Cell 2: Load and MODIFY
import json

with open('/storage/number-ML/gpu_config_auto.json', 'r') as f:
    gpu_config = json.load(f)

print("🤖 Original recommendations:")
print(gpu_config['model_gpu_settings'])

# OVERRIDE: Force LightGBM to use GPU (even if recommended CPU)
gpu_config['model_gpu_settings']['lightgbm'] = True

print("\n✏️  Modified settings:")
print(gpu_config['model_gpu_settings'])

# Use modified settings
xgb_use_gpu = gpu_config['model_gpu_settings']['xgboost']
lgb_use_gpu = gpu_config['model_gpu_settings']['lightgbm']  # ← overridden!
cat_use_gpu = gpu_config['model_gpu_settings']['catboost']

print("\n✅ Using CUSTOM settings (overridden)")
```

---

### Option 3: Completely Manual (ไม่ใช้ recommendation เลย)

```python
# Cell 2: Ignore recommendations, set manually
import json

# อ่านแค่เพื่อดูข้อมูล GPU
with open('/storage/number-ML/gpu_config_auto.json', 'r') as f:
    gpu_config = json.load(f)

print(f"GPU detected: {gpu_config['gpu_name']}")
print(f"Memory: {gpu_config['gpu_memory_gb']} GB")

# ตั้งค่าเองทั้งหมด (ignore recommendations)
xgb_use_gpu = True   # ← Manual choice
lgb_use_gpu = False  # ← Manual choice
cat_use_gpu = True   # ← Manual choice

print("\n✅ Using MANUAL settings (ignoring recommendations)")
```

---

## 🔍 Understanding Recommendations

### Free Tier (M4000)

**Recommendation:**
```python
{
  "xgboost": True,    # ← GPU (benefits most)
  "lightgbm": False,  # ← CPU (SMARTFIX will fallback anyway)
  "catboost": True,   # ← GPU (good support)
  "randomforest": False  # ← CPU (sklearn doesn't support GPU)
}
```

**Why?**
- M4000 is slow → Use GPU selectively
- LightGBM GPU often fails → Better to use CPU
- XGBoost + CatBoost benefit most from GPU

---

### Pro Tier (P5000)

**Recommendation:**
```python
{
  "xgboost": True,    # ← GPU (fast)
  "lightgbm": True,   # ← GPU (with SMARTFIX fallback)
  "catboost": True,   # ← GPU (fast)
  "randomforest": False  # ← CPU (sklearn)
}
```

**Why?**
- P5000 is fast → Use GPU for everything
- LightGBM GPU might work → Try with SMARTFIX fallback
- Maximum acceleration

---

## ⚙️ Advanced: Per-Model Configuration

```python
# Cell 2: Fine-grained control
import json

with open('/storage/number-ML/gpu_config_auto.json', 'r') as f:
    gpu_config = json.load(f)

# Create custom configuration
custom_config = {
    'xgboost': {
        'use_gpu': True,
        'reason': 'XGBoost has excellent GPU support'
    },
    'lightgbm': {
        'use_gpu': False,  # Override recommendation
        'reason': 'Unstable on this GPU, use CPU'
    },
    'catboost': {
        'use_gpu': True,
        'reason': 'CatBoost GPU is very fast'
    },
    'randomforest': {
        'use_gpu': False,
        'reason': 'sklearn RandomForest does not support GPU'
    }
}

print("🎨 Custom configuration:")
for model, settings in custom_config.items():
    device = "GPU" if settings['use_gpu'] else "CPU"
    print(f"  {model}: {device} - {settings['reason']}")

# Extract use_gpu flags
xgb_use_gpu = custom_config['xgboost']['use_gpu']
lgb_use_gpu = custom_config['lightgbm']['use_gpu']
cat_use_gpu = custom_config['catboost']['use_gpu']
```

---

## 🎯 Integration with Training

```python
# Cell 6: Training with GPU configuration
from src.train_production import train_all_models_optimized

# Use GPU settings from earlier cells
models, results = train_all_models_optimized(
    X, y,
    sample_weights=sample_weights,
    n_trials=100,
    use_gpu={
        'xgboost': xgb_use_gpu,      # ← From Cell 2
        'lightgbm': lgb_use_gpu,     # ← From Cell 2
        'catboost': cat_use_gpu,     # ← From Cell 2
        'randomforest': False        # ← Always False (sklearn)
    },
    verbose=True
)
```

---

## 📋 Decision Matrix

| Scenario | Recommended Action |
|----------|-------------------|
| **ไว้ใจ auto-config** | Use Option 1 (recommendations as-is) |
| **รู้ว่า GPU ของเราทำงานดี** | Override lightgbm → True |
| **ต้องการประหยัด GPU memory** | Override some models → False |
| **LightGBM ค้าง** | Keep lightgbm → False |
| **ทดสอบเท่านั้น** | All → False (CPU) |
| **Full speed ไม่สน error** | All → True (GPU) |

---

## ✅ Best Practices

### 1. Start with Recommendations
```python
# First run: Use recommendations
# ถ้าทำงานได้ดี → ใช้ต่อ
# ถ้ามี error → ปรับแต่ง
```

### 2. Monitor GPU Usage
```python
# ดู GPU usage ระหว่าง training
# ถ้า GPU = 0% → ปรับให้ใช้ GPU
# ถ้า GPU = 100% + out of memory → ปรับให้ใช้ CPU
```

### 3. Document Your Changes
```python
# ถ้า override recommendations
# เขียน comment ว่าทำไม
custom_config['lightgbm']['use_gpu'] = False
custom_config['lightgbm']['reason'] = "GPU hangs after 30 trials - use CPU"
```

---

## 🆘 Troubleshooting

### Problem: Recommendations seem wrong

**Solution:**
```python
# Check GPU info
print(f"GPU: {gpu_config['gpu_name']}")
print(f"Memory: {gpu_config['gpu_memory_gb']} GB")

# If recommendations don't make sense, ignore them
# Use manual settings (Option 3)
```

---

### Problem: Want to try all GPU

**Solution:**
```python
# Override all to True
for model in gpu_config['model_gpu_settings']:
    if model != 'randomforest':  # RF can't use GPU
        gpu_config['model_gpu_settings'][model] = True

# ⚠️ Warning: LightGBM might fail → SMARTFIX will fallback to CPU
```

---

### Problem: Want to force all CPU

**Solution:**
```python
# Simple override
xgb_use_gpu = False
lgb_use_gpu = False
cat_use_gpu = False

# Training will be slower but guaranteed to work
```

---

## 🎉 Summary

**Key Points:**
- ✅ `gpu_config_auto.json` = **Recommendation** (NOT hardcoded)
- ✅ You can **modify** anytime in notebook
- ✅ You can **ignore** completely if you want
- ✅ SMARTFIX will **fallback** if GPU fails
- ✅ **Flexible** - your choice!

**Common Usage:**
```python
# Load recommendations
gpu_config = json.load(...)

# Modify if needed
gpu_config['model_gpu_settings']['lightgbm'] = False  # Override

# Use in training
train_all_models_optimized(..., use_gpu=gpu_config['model_gpu_settings'])
```

**Result:** Best of both worlds! 🚀
- Auto-recommendations for beginners
- Full control for advanced users
- SMARTFIX safety net for everyone

---

**Created**: 2025-10-05
**Purpose**: GPU configuration flexibility guide
**Status**: ✅ Complete - User has full control
