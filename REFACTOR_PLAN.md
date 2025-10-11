# 🔄 Project Refactor Plan

**Created**: 2025-10-08
**Purpose**: Reorganize project structure for better management
**Current Issue**: 100+ files scattered in root directory

---

## 📊 Current Problems:

1. **50+ MD files in root** - Documentation scattered everywhere
2. **Training scripts mixed** - train_*.py files in root
3. **Setup scripts mixed** - setup_*.py files in root
4. **Session summaries everywhere** - SESSION_*.md files mixed
5. **Platform guides scattered** - Kaggle/Paperspace/Colab guides mixed

---

## 🎯 New Structure:

```
number-ML/
├── src/                           # ✅ Core source code (NO CHANGE)
│   ├── __init__.py
│   ├── config.py
│   ├── environment.py
│   ├── data_handler.py
│   ├── data_loader.py
│   ├── data_splitter.py
│   ├── data_filter.py
│   ├── features.py
│   ├── model_utils.py
│   ├── train.py
│   ├── train_production.py
│   ├── train_colab.py
│   ├── training_callbacks.py
│   ├── checkpoint_manager.py
│   ├── tier_models.py
│   ├── evaluate.py
│   ├── visualize.py
│   └── gpu_monitor.py
│
├── training/                      # 🆕 Training scripts (organized)
│   ├── modular/                   # Modular training scripts
│   │   ├── train_catboost_only.py
│   │   ├── train_xgboost_only.py
│   │   ├── train_lightgbm_only.py
│   │   ├── train_rf_only.py
│   │   └── train_ensemble_only.py
│   ├── train_terminal.py          # Terminal training
│   └── main.py                    # Main pipeline
│
├── setup/                         # 🆕 Setup scripts
│   ├── setup_local.py
│   ├── setup_paperspace.py
│   ├── setup_colab_complete.py
│   └── validate_paperspace.py
│
├── docs/                          # 🆕 All documentation (organized)
│   ├── guides/                    # Platform-specific guides
│   │   ├── kaggle/
│   │   │   ├── KAGGLE_SETUP.md
│   │   │   ├── KAGGLE_QUICK_START.md
│   │   │   ├── KAGGLE_CATBOOST_QUICKSTART.md
│   │   │   ├── KAGGLE_UPLOAD_INSTRUCTIONS.md
│   │   │   ├── KAGGLE_R2_LOW_FIX.md
│   │   │   ├── KAGGLE_CHECKPOINT_REALITY.md
│   │   │   └── CLAUDE_KAGGLE.md
│   │   ├── paperspace/
│   │   │   ├── PAPERSPACE_SETUP.md
│   │   │   ├── PAPERSPACE_START_FROM_ZERO.md
│   │   │   ├── PAPERSPACE_QUICK_START.md
│   │   │   ├── PAPERSPACE_TERMINAL_GUIDE.md
│   │   │   ├── PAPERSPACE_MODULAR_TRAINING_GUIDE.md
│   │   │   ├── PAPERSPACE_COMPLETE_GUIDE.md
│   │   │   ├── PAPERSPACE_SIMPLE_GUIDE.md
│   │   │   ├── PAPERSPACE_PRO_GUIDE.md
│   │   │   ├── PAPERSPACE_GPU_CONFIG_USAGE.md
│   │   │   ├── PAPERSPACE_ERROR_PREVENTION.md
│   │   │   ├── PAPERSPACE_FIX_GUIDE.md
│   │   │   ├── PAPERSPACE_FOLDER_STRUCTURE.md
│   │   │   ├── PAPERSPACE_UPDATE_011E.md
│   │   │   └── PAPERSPACE_PACKAGE_README.md
│   │   ├── colab/
│   │   │   ├── COLAB_SETUP.md
│   │   │   ├── COLAB_AUTO_RESUME_GUIDE.md
│   │   │   └── COLAB_AUTO_RESUME_COMPLETE.md
│   │   └── comparisons/
│   │       ├── KAGGLE_VS_PAPERSPACE_COMPARISON.md
│   │       ├── COLAB_VS_KAGGLE_COMPARISON.md
│   │       ├── TPU_VS_GPU_GUIDE.md
│   │       ├── GPU_PLATFORMS_GUIDE.md
│   │       └── PLATFORMS_PACKAGES_SUMMARY.md
│   │
│   ├── sessions/                  # Session summaries
│   │   ├── SESSION_002_SUMMARY.md
│   │   ├── SESSION_005_SUMMARY.md
│   │   ├── SESSION_011C_GPU_FIX.md
│   │   ├── SESSION_011D_SKLEARN17_FIX.md
│   │   ├── SESSION_011E_SKLEARN_COMPAT.md
│   │   ├── SESSION_011F_DATA_ISSUE.md
│   │   ├── SESSION_012_SUMMARY.md
│   │   ├── SESSION_012_COMPLETE.txt
│   │   ├── SESSION_SUMMARY.md
│   │   ├── SESSION_COMPLETION_REPORT.md
│   │   ├── SESSION_PAPERSPACE_SUMMARY.md
│   │   └── SESSION_CONTINUITY_GUIDE.md
│   │
│   ├── fixes/                     # Fix summaries
│   │   ├── SMARTFIX_SUMMARY.md
│   │   ├── ULTRAFIX_SUMMARY.md
│   │   ├── ULTRAFIX_DEPLOYMENT_STEPS.md
│   │   ├── UPDATE_SUMMARY.md
│   │   └── FINAL_SUMMARY.md
│   │
│   ├── protocols/                 # Session protocols
│   │   ├── PROTOCOL_FLOWCHART.md
│   │   ├── PROTOCOL_QUICK_REFERENCE.md
│   │   └── SESSION_CONTINUITY_GUIDE.md
│   │
│   └── implementation/            # Implementation docs
│       ├── implementation_guide.md
│       └── IMPLEMENTATION_COMPLETE.md
│
├── packages/                      # 🆕 Distribution packages
│   ├── kaggle/
│   │   ├── number-ML-kaggle-CatBoost.zip
│   │   └── notebooks/
│   │       └── Kaggle_CatBoost_Training.ipynb
│   └── paperspace/
│       └── (future packages)
│
├── notebooks/                     # ✅ Jupyter notebooks (NO CHANGE)
│   ├── Kaggle_ML_Training_AutoResume.ipynb
│   ├── Kaggle_CatBoost_Training.ipynb
│   ├── Colab_ML_Training_AutoResume.ipynb
│   ├── original_5000_lines.ipynb
│   └── paperspace_cell4_corrected.py
│
├── scripts/                       # ✅ Utility scripts (NO CHANGE)
│   ├── __init__.py
│   ├── batch_predict.py
│   └── predict_single.py
│
├── tests/                         # ✅ Tests (NO CHANGE)
│   └── (all test files)
│
├── api/                           # ✅ API (NO CHANGE)
│   ├── app.py
│   └── prediction.py
│
├── utils/                         # ✅ Utils (NO CHANGE)
│   ├── __init__.py
│   ├── checkpoint.py
│   └── helpers.py
│
├── data/                          # ✅ Data (NO CHANGE)
├── models/                        # ✅ Models (NO CHANGE)
├── results/                       # ✅ Results (NO CHANGE)
├── logs/                          # ✅ Logs (NO CHANGE)
├── checkpoints/                   # ✅ Checkpoints (NO CHANGE)
│
├── README.md                      # ✅ Main readme (KEEP IN ROOT)
├── CLAUDE.md                      # ✅ Claude instructions (KEEP IN ROOT)
├── NEXT_SESSION.md                # ✅ Next session guide (KEEP IN ROOT)
├── QUICK_START.md                 # ✅ Quick start (KEEP IN ROOT)
├── requirements.txt               # ✅ Dependencies (KEEP IN ROOT)
└── .project_state.json            # ✅ Project state (KEEP IN ROOT)
```

---

## 🔄 Migration Steps:

### Phase 1: Create New Folders
```bash
mkdir -p training/modular
mkdir -p setup
mkdir -p docs/guides/{kaggle,paperspace,colab,comparisons}
mkdir -p docs/sessions
mkdir -p docs/fixes
mkdir -p docs/protocols
mkdir -p docs/implementation
mkdir -p packages/{kaggle/notebooks,paperspace}
```

### Phase 2: Move Training Scripts
```bash
mv train_catboost_only.py training/modular/
mv train_xgboost_only.py training/modular/
mv train_lightgbm_only.py training/modular/
mv train_rf_only.py training/modular/
mv train_ensemble_only.py training/modular/
mv train_terminal.py training/
mv main.py training/
```

### Phase 3: Move Setup Scripts
```bash
mv setup_local.py setup/
mv setup_paperspace.py setup/
mv setup_colab_complete.py setup/
mv validate_paperspace.py setup/
```

### Phase 4: Move Documentation (Kaggle)
```bash
mv KAGGLE_*.md docs/guides/kaggle/
mv CLAUDE_KAGGLE.md docs/guides/kaggle/
```

### Phase 5: Move Documentation (Paperspace)
```bash
mv PAPERSPACE_*.md docs/guides/paperspace/
mv PAPERSPACE_*.txt docs/guides/paperspace/
```

### Phase 6: Move Documentation (Colab)
```bash
mv COLAB_*.md docs/guides/colab/
```

### Phase 7: Move Comparisons
```bash
mv KAGGLE_VS_*.md docs/guides/comparisons/
mv COLAB_VS_*.md docs/guides/comparisons/
mv TPU_VS_*.md docs/guides/comparisons/
mv GPU_PLATFORMS_GUIDE.md docs/guides/comparisons/
mv PLATFORMS_PACKAGES_SUMMARY.md docs/guides/comparisons/
```

### Phase 8: Move Sessions
```bash
mv SESSION_*.md docs/sessions/
mv SESSION_*.txt docs/sessions/
```

### Phase 9: Move Fixes
```bash
mv *FIX*.md docs/fixes/
mv UPDATE_SUMMARY.md docs/fixes/
mv FINAL_SUMMARY.md docs/fixes/
```

### Phase 10: Move Protocols
```bash
mv PROTOCOL_*.md docs/protocols/
mv SESSION_CONTINUITY_GUIDE.md docs/protocols/
```

### Phase 11: Move Implementation
```bash
mv implementation_guide.md docs/implementation/
mv IMPLEMENTATION_COMPLETE.md docs/implementation/
```

### Phase 12: Move Packages
```bash
mv number-ML-kaggle-CatBoost.zip packages/kaggle/
mv notebooks/Kaggle_CatBoost_Training.ipynb packages/kaggle/notebooks/
```

---

## 🔧 Import Path Updates:

**Files that need updates:**

1. **training/main.py**:
   - Add: `sys.path.insert(0, str(Path(__file__).parent.parent))`

2. **training/modular/*.py**:
   - Add: `sys.path.insert(0, str(Path(__file__).parent.parent.parent))`

3. **setup/*.py**:
   - Add: `sys.path.insert(0, str(Path(__file__).parent.parent))`

---

## ✅ Benefits:

1. **Organized Documentation**: Easy to find platform-specific guides
2. **Clear Training Structure**: Training scripts in dedicated folder
3. **Setup Scripts Grouped**: All setup in one place
4. **Clean Root**: Only essential files in root
5. **Easy Navigation**: Logical folder hierarchy
6. **Version Control Friendly**: Better .gitignore patterns

---

## 🧪 Testing Checklist:

- [ ] Training scripts still work: `python training/modular/train_catboost_only.py`
- [ ] Main pipeline works: `python training/main.py --help`
- [ ] Setup scripts work: `python setup/setup_local.py`
- [ ] Imports resolve correctly
- [ ] No broken links in documentation
- [ ] Kaggle package still works

---

## 📝 Post-Refactor Tasks:

1. Update `.gitignore` with new folder patterns
2. Update `README.md` with new structure
3. Update `CLAUDE.md` with new file locations
4. Update `NEXT_SESSION.md` with new paths
5. Create `docs/README.md` as documentation index
6. Create symlinks if needed for backward compatibility

---

**Status**: PLAN READY - Ready to execute migration
**Estimated Time**: 30 minutes
**Risk Level**: LOW (can be reverted easily)
