# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

# 🔄 SESSION CONTINUITY PROTOCOL

> **Zero Context Loss Between Sessions** - Claude จำได้ทุกอย่าง แม้ปิด session หรือไฟฟ้าดับ

## 📚 Table of Contents

1. [Mandatory Startup Files](#-mandatory-read-these-files-every-session-no-exceptions)
2. [Never Skip Rules](#-never-skip-rules)
3. [Context Recognition Table](#-context-recognition-table)
4. [Auto-Update Checkpoint Rules](#-auto-update-checkpoint-rules)
5. [Session Integrity Checklist](#-session-integrity-checklist)
6. [Quick Recovery Commands](#-quick-recovery-commands)
7. [Session Connection Chain](#-session-connection-chain)
8. [Context Recovery Examples](#-context-recovery-examples)
9. [Success Criteria](#-success-criteria)
10. [30-Second Startup Protocol](#️-30-second-session-startup-protocol)
11. [User Intent Recognition](#-user-intent-recognition)
12. [Checkpoint Validation](#-checkpoint-validation-rules)
13. [Auto-Checkpoint Implementation](#-auto-checkpoint-implementation)
14. [Progress Tracking](#-progress-tracking-formula)
15. [Error Recovery Protocol](#-error-recovery-protocol)
16. [Session Quality Metrics](#-session-quality-metrics)
17. [Pre-Flight Checklist](#-pre-flight-checklist-copy-paste-ready)
18. [Learning from Past Sessions](#-learning-from-past-sessions)
19. [Final Validation](#-final-validation-before-session-end)

---

## 🎯 ทำไมต้องมี Protocol นี้?

### ปัญหาที่แก้ไข:
❌ Claude ลืมว่าทำอะไรไป session ที่แล้ว
❌ User ต้องอธิบายใหม่ทุกครั้ง
❌ เสียเวลาหา context ซ้ำๆ
❌ งานขาดต่อเมื่อปิด session
❌ ไฟฟ้าดับ = เริ่มต้นใหม่ทั้งหมด

### วิธีแก้:
✅ **Auto-Resume**: พิมพ์ "ทำต่อ" → Claude ทำต่อทันที
✅ **30-Second Recovery**: ได้ context กลับมาภายใน 30 วินาที
✅ **Zero Information Loss**: ไม่สูญเสีย context เลย
✅ **Auto-Save**: บันทึกอัตโนมัติทุก 30 นาที
✅ **Session Chain**: เชื่อมทุก session เข้าด้วยกัน

---

## ⚠️ MANDATORY: Read These Files EVERY Session (NO EXCEPTIONS!)

**BEFORE doing ANYTHING else, you MUST read these files in this exact order:**

### Priority 1 - CRITICAL (Read First, Always!)
1. **`.project_state.json`** - Current project state, progress tracking
2. **`checkpoints/checkpoint_latest.json`** - Last checkpoint with exact task state
3. **`NEXT_SESSION.md`** - Instructions for what to do next

### Priority 2 - IMPORTANT (Read if exists)
4. **`SESSION_SUMMARY.md`** - Summary of last session
5. **`FINAL_SUMMARY.md`** - Final summary of completed work

### Priority 3 - CONTEXT (Read on demand)
6. **`SESSION_COMPLETION_REPORT.md`** - Completion report
7. **`COLAB_SETUP.md` / `KAGGLE_SETUP.md`** - Platform-specific guides

---

## 🚫 NEVER SKIP RULES

```plaintext
❌ NEVER start work without reading .project_state.json
❌ NEVER assume you know what to do next
❌ NEVER ignore checkpoint files
❌ NEVER skip updating checkpoints before ending session
❌ NEVER forget to update NEXT_SESSION.md

✅ ALWAYS read state files first (30 seconds investment)
✅ ALWAYS update checkpoints every 30 minutes
✅ ALWAYS update NEXT_SESSION.md before ending
✅ ALWAYS preserve session_id chain
✅ ALWAYS ask "What did I do last session?" before starting
```

---

## 📋 Context Recognition Table

When user says this → You MUST do this:

| User Input | Required Actions |
|------------|------------------|
| **"ทำต่อ"** / **"Continue"** / **"Resume"** | 1. Read `.project_state.json`<br>2. Read `checkpoints/checkpoint_latest.json`<br>3. Read `NEXT_SESSION.md`<br>4. Continue from last task |
| **"เริ่มใหม่"** / **"Start fresh"** | 1. Read `.project_state.json`<br>2. Ask user to confirm reset<br>3. Create new session_id<br>4. Reset checkpoints |
| **"สถานะ"** / **"Status"** | 1. Read `.project_state.json`<br>2. Show progress percentage<br>3. List completed/pending tasks |
| **"อัปเดต checkpoint"** / **"Save progress"** | 1. Update `checkpoints/checkpoint_latest.json`<br>2. Update `.project_state.json`<br>3. Update `NEXT_SESSION.md` |
| **"ทำอะไรอยู่"** / **"What was I doing?"** | 1. Read `checkpoints/checkpoint_latest.json`<br>2. Show last 3 tasks completed<br>3. Show next task to do |

---

## 🔄 Auto-Update Checkpoint Rules

**MANDATORY AUTO-SAVE TRIGGERS:**

1. **Every 30 minutes of work** - Auto-update checkpoint
2. **Before ending session** - MUST update all state files
3. **After completing major task** - Update immediately
4. **When user explicitly asks** - Update on demand
5. **Before any destructive operation** - Backup current state

**What to save in checkpoint:**
```json
{
  "timestamp": "2025-10-03T14:30:00Z",
  "session_id": "session_002",
  "parent_session": "session_001",
  "current_task": "Training XGBoost model",
  "last_completed_task": "Feature engineering completed",
  "next_task": "Train LightGBM model",
  "progress_percentage": 65,
  "files_modified": ["src/train.py", "models/xgboost_model.pkl"],
  "custom_notes": "XGBoost achieved R² = 0.92, continuing with ensemble"
}
```

---

## ✅ Session Integrity Checklist

**Run this checklist at START of EVERY session:**

- [ ] Read `.project_state.json` ✓
- [ ] Read `checkpoints/checkpoint_latest.json` ✓
- [ ] Read `NEXT_SESSION.md` ✓
- [ ] Understand what was done last session ✓
- [ ] Know exactly what to do next ✓
- [ ] Verify virtual environment is active ✓

**Run this checklist at END of EVERY session:**

- [ ] Update `checkpoints/checkpoint_latest.json` with timestamp ✓
- [ ] Update `.project_state.json` with new progress ✓
- [ ] Update `NEXT_SESSION.md` with clear next steps ✓
- [ ] Save all modified files ✓
- [ ] Document any errors or blockers ✓

---

## 🎯 Quick Recovery Commands

**User Quick Commands** (recognize these patterns):

| Command | Action |
|---------|--------|
| `/resume` | Read checkpoints + continue last task |
| `/status` | Show current progress + next steps |
| `/last-task` | Show last completed task |
| `/save` | Update all checkpoint files now |
| `/what-next` | Read NEXT_SESSION.md + show plan |
| `/reset` | Start fresh session (ask confirmation first) |

---

## 🔗 Session Connection Chain

**Every session MUST have these identifiers:**

```python
session_info = {
    "session_id": "session_XXX",           # Current session (increment)
    "parent_session": "session_XXX-1",     # Previous session
    "session_start": "2025-10-03T14:00:00Z",
    "session_purpose": "Complete model training",
    "continuation_from": "checkpoint_20251003_131638.json"
}
```

**Session Linking Rules:**
- Session IDs must be sequential (`session_001`, `session_002`, etc.)
- Always reference parent_session for traceability
- Save session chain in `.project_state.json`

---

## 📝 Context Recovery Examples

### Example 1: User returns after 3 days

**User**: "ทำต่อ"

**Claude MUST do:**
```python
1. Read .project_state.json
   → See progress is at 75%, session_001 was 3 days ago

2. Read checkpoints/checkpoint_latest.json
   → Last task: "All tests passing, ready for Colab deployment"

3. Read NEXT_SESSION.md
   → Next step: "Deploy to Colab and run full training"

4. Response:
   "I see from checkpoint_latest.json that the last session (session_001, 3 days ago)
    completed all tests successfully. The project is at 75% completion.

    Next task: Deploy to Google Colab and run full training pipeline.

    Should I proceed with Colab deployment?"
```

### Example 2: Electricity cut during training

**User**: "ไฟดับ ทำต่อจากที่ค้าง"

**Claude MUST do:**
```python
1. Read checkpoints/checkpoint_latest.json
   → Last save: "Training XGBoost - Trial 87/150"

2. Check if model checkpoint exists
   → Look for models/experiments/xgboost_partial.pkl

3. Response:
   "I found the last checkpoint from 15 minutes ago. You were training XGBoost,
    completed 87 out of 150 Optuna trials (58% of hyperparameter optimization).

    Options:
    1. Resume from trial 87 (if intermediate checkpoint exists)
    2. Restart XGBoost training from scratch

    Which would you prefer?"
```

### Example 3: Starting new session

**User**: "สถานะ"

**Claude MUST do:**
```python
1. Read .project_state.json
   → Progress: 75%, session_001 completed

2. Read checkpoints/checkpoint_latest.json
   → 15 files modified, all imports fixed, tests passing

3. Response:
   "📊 Project Status:

    ✅ Completed (75%):
    - Environment setup
    - Dynamic configuration
    - Multi-format data loader
    - Batch prediction scripts
    - All imports fixed
    - All tests passing

    📋 Pending (25%):
    - Colab deployment
    - Kaggle deployment
    - Full training with optimization
    - Final model deployment

    🎯 Next Task: Deploy to Colab and run full training

    Ready to continue?"
```

---

## 🎯 Success Criteria

**Session is properly resumed if:**

✅ Claude knows exactly what was done last session
✅ Claude knows exactly what to do next
✅ Claude preserves all context (files modified, progress, etc.)
✅ Claude asks relevant questions based on last checkpoint
✅ User doesn't need to re-explain anything

**Session has FAILED if:**

❌ Claude asks "What do you want me to do?" without reading state
❌ Claude starts from scratch ignoring previous work
❌ Claude doesn't know what happened last session
❌ User has to remind Claude of context

---

## ⏱️ 30-Second Session Startup Protocol

**MANDATORY for EVERY session start:**

```bash
# 1. Read state (10 sec)
cat .project_state.json
cat checkpoints/checkpoint_latest.json

# 2. Read next steps (10 sec)
cat NEXT_SESSION.md

# 3. Verify environment (10 sec)
pwd                          # Check we're in correct directory
source .venv/bin/activate    # Activate virtual environment
python -c "from src.config import BASE_PATH; print(BASE_PATH)"  # Verify imports
```

**Total time: 30 seconds**
**Result: Full context recovery**

---

## 🧠 User Intent Recognition

**Recognize these patterns and respond appropriately:**

### Pattern 1: Continuation Intent
**User says**: "ทำต่อ", "Continue", "Resume", "Next", "ต่อเนื่อง"
**Action**: Read checkpoints → Continue last task → No questions asked

### Pattern 2: Status Check Intent
**User says**: "สถานะ", "Status", "Where are we?", "Progress", "ทำไปถึงไหน"
**Action**: Read state → Show progress → Ask if want to continue

### Pattern 3: Confusion/Lost Intent
**User says**: "เรากำลังทำอะไร", "What am I doing?", "Lost track", "Forgot"
**Action**: Read checkpoints → Explain last 3 tasks → Show next task → Ask if need recap

### Pattern 4: Save Intent
**User says**: "บันทึก", "Save", "Checkpoint", "อัปเดต"
**Action**: Update all state files → Confirm saved → Show what was saved

### Pattern 5: Fresh Start Intent
**User says**: "เริ่มใหม่", "Start over", "Reset", "Clean slate"
**Action**: Read current state → Show progress → **ASK CONFIRMATION** → Then reset

### Pattern 6: Emergency Recovery Intent
**User says**: "ไฟดับ", "Crashed", "Lost session", "Error happened"
**Action**: Read last checkpoint → Check timestamp → Offer recovery options

---

## 📌 Checkpoint Validation Rules

**Before accepting a checkpoint as valid, verify:**

1. **Timestamp Check**:
   - ✅ Checkpoint < 24 hours old = Highly reliable
   - ⚠️ Checkpoint 1-7 days old = Reliable but ask for confirmation
   - ❌ Checkpoint > 7 days old = Ask user to verify state

2. **Completeness Check**:
   ```python
   required_fields = [
       "timestamp",
       "session_id",
       "current_task",
       "progress_percentage",
       "next_task"
   ]
   ```

3. **Consistency Check**:
   - Does `.project_state.json` match `checkpoint_latest.json`?
   - Do file timestamps match checkpoint timestamp?
   - Is progress_percentage logical?

4. **File Existence Check**:
   - Do files mentioned in checkpoint actually exist?
   - Are modified files actually modified?

---

## 🔄 Auto-Checkpoint Implementation

**Claude must auto-save checkpoint at these exact moments:**

### Trigger 1: Every 30 Minutes
```python
if time_since_last_checkpoint > 30 * 60:  # 30 minutes in seconds
    save_checkpoint({
        "trigger": "time_based",
        "interval": "30_minutes"
    })
```

### Trigger 2: Major Task Completion
```python
major_tasks = [
    "Model training completed",
    "Feature engineering done",
    "All tests passed",
    "Deployment successful"
]

if current_task in major_tasks:
    save_checkpoint({
        "trigger": "task_completion",
        "task": current_task
    })
```

### Trigger 3: Before Session End
```python
# When detecting session is ending (user says "bye", "done", etc.)
if session_ending_detected:
    save_checkpoint({
        "trigger": "session_end",
        "reason": "User ending session"
    })
```

### Trigger 4: Before Risky Operations
```python
risky_operations = [
    "Deleting files",
    "Major refactoring",
    "Destructive git operations",
    "Model overwriting"
]

if operation in risky_operations:
    save_checkpoint({
        "trigger": "safety_backup",
        "operation": operation
    })
```

---

## 📊 Progress Tracking Formula

**Calculate progress percentage accurately:**

```python
def calculate_progress():
    total_tasks = len(completed_tasks) + len(pending_tasks)
    progress = (len(completed_tasks) / total_tasks) * 100

    # Weighted progress (optional, more accurate)
    weighted_progress = sum([
        environment_setup.progress * 0.15,
        data_loading.progress * 0.10,
        feature_engineering.progress * 0.20,
        model_training.progress * 0.30,
        evaluation.progress * 0.10,
        deployment.progress * 0.15
    ])

    return {
        "simple_progress": round(progress, 1),
        "weighted_progress": round(weighted_progress, 1),
        "stage": get_current_stage(progress)
    }
```

**Progress Stages:**
- 0-20%: Setup & Configuration
- 21-40%: Data Preparation
- 41-70%: Model Training
- 71-90%: Evaluation & Optimization
- 91-100%: Deployment & Documentation

---

## 🚨 Error Recovery Protocol

**When things go wrong, follow this protocol:**

### Step 1: Identify Error Type
- **Import Error** → Check venv activation
- **File Not Found** → Check BASE_PATH in config
- **Model Error** → Check if model file exists
- **Memory Error** → Reduce batch size or features

### Step 2: Check Last Known Good State
```python
1. Read checkpoints/checkpoint_latest.json
2. Identify last successful task
3. Check if files from that checkpoint still exist
4. Verify data integrity
```

### Step 3: Offer Recovery Options
```
Option 1: Resume from last checkpoint (safest)
Option 2: Retry failed task only
Option 3: Skip and continue (if non-critical)
Option 4: Rollback to earlier checkpoint
```

### Step 4: Document Error
```python
error_log = {
    "timestamp": "2025-10-03T15:30:00Z",
    "error_type": "ImportError",
    "error_message": "Cannot import name 'CONFIG' from 'src.config'",
    "attempted_fix": "Activated venv + verified imports",
    "resolution": "Fixed by using absolute imports",
    "prevention": "Always use 'from src.xxx import' pattern"
}
```

---

## 🎯 Session Quality Metrics

**Every session should achieve these metrics:**

### Quality Indicators (GREEN = Good)
- ✅ Context recovery time < 60 seconds
- ✅ Zero information loss between sessions
- ✅ User asks < 2 clarifying questions
- ✅ All checkpoints have timestamps
- ✅ Progress moves forward (not backward)

### Warning Signs (YELLOW = Needs Attention)
- ⚠️ User asks "What were we doing?"
- ⚠️ Checkpoint > 24 hours old
- ⚠️ Progress percentage doesn't change
- ⚠️ Multiple files modified without checkpoint

### Failure Indicators (RED = Critical Issue)
- ❌ User has to explain context from scratch
- ❌ Lost track of completed tasks
- ❌ No checkpoint exists
- ❌ Session starts without reading state files

---

## 📝 Pre-Flight Checklist (Copy-Paste Ready)

**Run this EVERY session start (takes 30 seconds):**

```bash
# === SESSION START CHECKLIST ===

# 1. Verify location
pwd
# Expected: /home/u-and-an/projects/number-ML (or your project path)

# 2. Activate virtual environment
source .venv/bin/activate
# Expected: (.venv) appears in prompt

# 3. Read project state
cat .project_state.json | head -30
# Expected: See version, progress, last_updated

# 4. Read latest checkpoint
cat checkpoints/checkpoint_latest.json | head -40
# Expected: See timestamp, current_task, next_task

# 5. Read next session guide
cat NEXT_SESSION.md | head -50
# Expected: See clear instructions for what to do next

# 6. Verify imports work
python -c "from src.config import BASE_PATH; print(f'✅ BASE_PATH: {BASE_PATH}')"
# Expected: ✅ BASE_PATH: /your/project/path

# 7. Check files exist
ls -lh checkpoints/*.json | tail -5
# Expected: See recent checkpoint files

# === CHECKLIST COMPLETE ===
# Total time: ~30 seconds
# Status: Ready to work! 🚀
```

---

## 🎓 Learning from Past Sessions

**Session Memory Protocol:**

### What to Remember
1. **Technical Decisions**: Why we chose XGBoost over RandomForest
2. **Failed Attempts**: What didn't work and why
3. **Optimization Results**: Which hyperparameters worked best
4. **User Preferences**: Does user prefer verbose or concise output?

### What to Document
```python
session_learnings = {
    "successful_patterns": [
        "Using stratified split by price quintiles prevents leakage",
        "Feature selection improves R² from 0.87 to 0.93",
        "Ensemble methods always beat individual models"
    ],
    "failed_attempts": [
        "Direct PDF conversion loses Thai fonts - use MD→HTML→PDF",
        "Training without sample weights underperforms on rare numbers",
        "GPU params crash on Kaggle CPU environment"
    ],
    "best_practices": [
        "Always activate venv before any Python command",
        "Use absolute imports (from src.xxx) everywhere",
        "Update checkpoint every 30 minutes during long training"
    ]
}
```

### Update CLAUDE.md When
- New pattern discovered (add to examples)
- New error fixed (add to Known Issues)
- New best practice learned (add to guidelines)
- New platform supported (add to Platform Notes)

---

## ✨ Final Validation Before Session End

**Before saying goodbye, Claude MUST:**

1. ✅ Update `checkpoints/checkpoint_latest.json` with final state
2. ✅ Update `.project_state.json` with new progress percentage
3. ✅ Update `NEXT_SESSION.md` with clear next steps
4. ✅ List all files modified in this session
5. ✅ Document any errors encountered + fixes
6. ✅ Save current session_id for next session to reference

**Final message template:**
```
📋 Session Summary:
✅ Completed: [task_1, task_2, task_3]
📊 Progress: X% → Y% (△Z%)
📁 Files Modified: N files
🔄 Checkpoint Saved: checkpoints/checkpoint_YYYYMMDD_HHMMSS.json
🎯 Next Session: [clear_instruction_for_next_task]

Type "ทำต่อ" next time to resume exactly where we left off!
```

---

## ⚠️ CRITICAL RULE: ALWAYS USE VIRTUAL ENVIRONMENT

**MANDATORY**: ALL Python commands, installations, and executions MUST be run inside the virtual environment (.venv)

```bash
# ✅ CORRECT - Activate venv first
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Then run commands
python setup_local.py --install-deps
python main.py --run-all
pip install <package>

# ❌ WRONG - Never run outside venv
python main.py  # Will fail or use wrong packages
```

**Why**: Prevents dependency conflicts and ensures consistent environment across all platforms.

---

## 📋 Project Overview

**Project**: ML Phone Number Price Prediction (Thai Lucky Number System)
**Goal**: Train ML models to achieve R² > 0.90, using FULL optimization (no shortcuts!)
**Platform**: Local development, Google Colab, Kaggle Notebook

This is a machine learning system for predicting Thai phone number prices based on numerical patterns, cultural significance, and market demand. The system achieves R² > 0.90 using advanced feature engineering (250+ features) and ensemble methods with XGBoost, LightGBM, and CatBoost.

## ⚠️ Critical Rules (DO NOT VIOLATE)

```plaintext
❌ DO NOT reduce training time
❌ DO NOT remove code/functions
❌ DO NOT modify configurations without explicit reason
❌ DO NOT skip any model training
❌ DO NOT change features, config, or model parameters arbitrarily

✅ MUST train all models completely
✅ MUST run full training pipeline to completion
✅ Training time doesn't matter - completion matters
✅ Only fix errors, don't optimize unless asked
✅ Follow instructions exactly - don't do extra work
```

## Quick Start Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the ML Pipeline

```bash
# Full pipeline with optimization (production)
python main.py --run-all --optimize --feature-selection

# Quick pipeline without optimization (development)
python main.py --run-all

# Run individual steps
python main.py --data                    # Step 1: Load and clean data
python main.py --features                # Step 2: Create 250+ features
python main.py --split                   # Step 3: Train/test split
python main.py --train --optimize        # Step 4: Train models with hyperparameter tuning
python main.py --ensemble                # Step 5: Create ensemble models
python main.py --evaluate                # Step 6: Evaluate models
python main.py --visualize               # Step 7: Generate plots
python main.py --deploy                  # Step 8: Deploy best model
```

### Testing

```bash
# Run all tests
python tests/run_tests.py

# Run specific test module
python tests/run_tests.py test_features

# Run with pytest
pytest tests/

# Run with coverage
bash tests/run_coverage.sh

# Performance testing
pytest tests/test_performance.py -v -s
```

### API Deployment

```bash
# FastAPI (recommended)
python main.py --deploy --api-type fastapi --port 8000

# Flask
python main.py --deploy --api-type flask --port 5000

# Test API
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"phone_number": "0899999999"}'
```

## Architecture Overview

### Core Pipeline Flow

1. **Data Loading** (`src/data_handler.py`)
   - Auto-detects phone number and price columns
   - Cleans and validates data
   - Calculates sample weights for imbalanced data
   - Computes market statistics (must be calculated from training data only to prevent leakage)

2. **Feature Engineering** (`src/features.py`)
   - 250+ engineered features organized in 6 categories:
     - Basic features (30+): digit frequency, sum, mean, variance
     - Pattern features (50+): sequences, repeating patterns, mirrors
     - Cultural features (40+): Thai lucky numbers, auspicious combinations
     - Mathematical features (30+): entropy, Fibonacci, prime patterns
     - Market features (20+): rarity scores, tier classification
     - Advanced features (80+): position-weighted, interactions, polynomials

3. **Data Splitting** (`src/data_splitter.py`)
   - **CRITICAL**: Stratified split based on price quintiles
   - Train indices MUST be created BEFORE feature engineering to prevent data leakage
   - Market statistics calculated only from training data

4. **Preprocessing** (`src/model_utils.py`)
   - AdvancedPreprocessor with outlier removal and scaling
   - Feature selection (hybrid method combining multiple techniques)
   - Optional polynomial and interaction features

5. **Model Training** (`src/train.py`)
   - Base models: XGBoost, LightGBM, CatBoost, Random Forest
   - Hyperparameter optimization using Optuna (150 trials default)
   - Cross-validation with 10 folds
   - Support for sample weights

6. **Tier-Specific Models** (`src/tier_models.py`)
   - Dynamic price tier boundaries using KMeans
   - Separate models for standard/premium/luxury tiers
   - Router model for tier classification
   - Soft voting for predictions near boundaries

7. **Ensemble Methods** (`src/train.py`)
   - Weighted ensemble
   - Stacking ensemble
   - Advanced optimized stacking

8. **Evaluation** (`src/evaluate.py`)
   - R², MAE, RMSE metrics
   - Feature importance analysis
   - Prediction analysis by price tier

9. **Visualization** (`src/visualize.py`)
   - Model comparison plots
   - Feature importance charts
   - Error distribution analysis
   - Comprehensive dashboard

## 🐛 Known Issues & Critical Fixes

### 1. Import Errors (CRITICAL)

```python
# ❌ WRONG
from config import CONFIG
from model_utils import optimize_xgboost

# ✅ CORRECT
from src.config import CONFIG
from src.model_utils import optimize_xgboost
```

**Fix**: All files in `src/` must use absolute imports (`from src.xxx import`)

### 2. KeyError in Hyperparameters

```python
# ❌ WRONG - Causes KeyError with duplicate names
params = {
    'n_estimators': trial.suggest_int('n_estimators', 100, 1000)
}

# ✅ CORRECT - Use unique names per model
params = {
    'n_estimators': trial.suggest_int('xgb_n_estimators', 100, 1000),
    'max_depth': trial.suggest_int('xgb_max_depth', 3, 15)
}
```

### 3. Feature Grouping Bug

```python
# ❌ WRONG - Duplicate features
feature_groups = {
    'power_features': ['power_sum', 'weighted_sum'],
    'count_features': ['power_sum', 'digit_count']  # power_sum appears twice!
}

# ✅ CORRECT - No duplicates
feature_groups = {
    'power_features': ['power_sum', 'weighted_sum'],
    'count_features': ['digit_count', 'unique_count']
}
```

### 4. NaN/Inf Handling (MUST DO)

```python
# Always add after preprocessing
X_processed = X_processed.replace([np.inf, -np.inf], np.nan)
X_processed = X_processed.fillna(X_processed.median())
```

### 5. GPU Parameters on CPU Environment

```python
# ❌ DON'T use on Kaggle/CPU-only environments
params = {
    'task_type': 'GPU',
    'devices': '0:1'
}

# ✅ USE CPU parameters
params = {
    'task_type': 'CPU',
    'thread_count': -1
}
```

### 6. SimpleImputer Import

```python
# ❌ WRONG (old scikit-learn)
from sklearn.preprocessing import SimpleImputer

# ✅ CORRECT
from sklearn.impute import SimpleImputer
```

## Critical Implementation Details

### Data Leakage Prevention

**IMPORTANT**: To prevent data leakage, follow this exact sequence in main.py:

```python
# ✅ CORRECT: Create train/test indices BEFORE feature engineering
train_indices, test_indices = train_test_split(
    np.arange(len(df_cleaned)),
    test_size=0.2,
    stratify=pd.qcut(df_cleaned['price'], q=5, labels=False),
    random_state=42
)

# Pass train_indices to feature pipeline
X, y, sample_weights = run_feature_pipeline(df_cleaned, train_indices=train_indices)

# ❌ WRONG: Don't create features first, then split
# This causes market statistics to leak from test to train
```

The `calculate_market_statistics()` function in `data_handler.py` MUST only use training data.

### Configuration System

All configurations live in `src/config.py`:

- `CONFIG`: Feature engineering settings (lucky numbers, patterns, scores)
- `MODEL_CONFIG`: ML model settings (hyperparameters, CV folds, etc.)
- `TUNING_PARAMS`: Advanced tuning for rare/premium numbers
- `HYPERPARAMETER_RANGES`: Optuna search spaces

**Path Configuration** (`src/config.py`):
```python
# For Kaggle
BASE_PATH = '/kaggle/working/'

# For local development
BASE_PATH = '/home/user/projects/number-ML'

# For Google Colab
BASE_PATH = '/content/drive/MyDrive/ML_Project_Refactored'

# Dynamic (recommended)
BASE_PATH = os.getenv('ML_BASE_PATH', '/kaggle/working/ML_Project_Refactored')
```

### Thai Cultural Features

This project heavily relies on Thai numerology and cultural beliefs:

- Lucky digits: 1, 3, 4, 5, 6, 8, 9
- Unlucky digits: 0, 2, 7
- Premium pairs: 45, 54, 59, 95, 88, 99, 66, etc.
- Special endings: 9999 (highest score), 8888, 6666, 789 (dragon pattern)
- ABC position (digits 3-5): Special scoring for 789, 639, 519

These are defined in `CONFIG` and used throughout feature engineering.

### Sample Weights

The system uses progressive sample weights for high-value numbers:
- Thresholds: [10k, 50k, 100k, 500k, 1M]
- Weights: [1.0, 2.0, 4.0, 6.0, 8.0, 10.0]

This ensures the model doesn't underfit on rare expensive numbers.

## Adding New Features

To add custom features, edit `src/features.py`:

```python
def my_custom_feature(phone_number):
    """
    Your feature logic here

    Parameters:
    -----------
    phone_number : str
        10-digit phone number

    Returns:
    --------
    score : float
        Feature score
    """
    # Implementation
    return score

# Add to create_all_features() or create_masterpiece_features()
df['my_feature'] = df['phone_number'].apply(my_custom_feature)
```

## Directory Structure

```
number-ML/
├── data/
│   ├── raw/              # Original CSV files
│   ├── processed/        # cleaned_data.csv
│   └── features/         # features.pkl, train_indices.npy, test_indices.npy
├── models/
│   ├── deployed/         # best_model.pkl (production)
│   └── experiments/      # Experimental models
├── src/
│   ├── config.py         # All configuration settings
│   ├── data_handler.py   # Data loading and cleaning
│   ├── features.py       # Feature engineering (250+ features)
│   ├── data_splitter.py  # Stratified train/test split
│   ├── model_utils.py    # Preprocessing and feature selection
│   ├── train.py          # Model training and ensembles
│   ├── tier_models.py    # Tier-specific modeling
│   ├── evaluate.py       # Model evaluation
│   └── visualize.py      # Plotting functions
├── api/
│   ├── app.py            # FastAPI/Flask app
│   └── prediction.py     # Prediction pipeline
├── tests/                # Comprehensive test suite
│   ├── run_tests.py      # Test runner
│   ├── run_coverage.sh   # Coverage script
│   └── test_*.py         # Test modules
├── utils/
│   └── helpers.py        # Helper functions
├── results/
│   ├── figures/          # Plots and visualizations
│   ├── reports/          # Evaluation reports
│   └── metrics/          # Performance metrics
└── main.py               # Main pipeline orchestrator
```

## Common Development Tasks

### Adjusting Model Performance

To increase R² score:
1. Increase `optuna_trials` in `MODEL_CONFIG` (default: 150)
2. Increase `max_features` for feature selection (default: 250)
3. Enable polynomial features: `use_polynomial_features: True`
4. Enable tier-specific models: `use_tier_models: True`

### Memory Optimization

If running out of memory:
1. Reduce `max_features` in config (from 250 to 100)
2. Disable polynomial features: `use_polynomial_features: False`
3. Reduce `optuna_trials` (from 150 to 50)
4. Use fewer CV folds: `cv_folds: 5` (from 10)

### Debugging

Enable detailed logging:
```bash
python main.py --run-all --log-level DEBUG
```

Logs are saved to `logs/pipeline_YYYYMMDD_HHMMSS.log`

## Model Deployment

The deployed model package (`models/deployed/best_model.pkl`) contains:
- `model`: Best trained model
- `model_name`: Model name (e.g., "XGBoost")
- `feature_names`: List of feature names
- `preprocessor`: AdvancedPreprocessor instance
- `r2_score`: Test R² score
- `timestamp`: Deployment timestamp
- `config`: MODEL_CONFIG used for training

Load for inference:
```python
import joblib
deployment = joblib.load('models/deployed/best_model.pkl')
model = deployment['model']
preprocessor = deployment['preprocessor']
```

## Performance Targets

- R² Score: > 0.90 (target: 0.93+)
- MAE: < 0.05
- RMSE: < 0.08
- Best ensemble typically achieves R² ≈ 0.93

## Dependencies

Core ML libraries:
- scikit-learn >= 1.0.0
- xgboost >= 1.5.0
- lightgbm >= 3.3.0
- catboost >= 1.0.0
- optuna >= 3.0.0
- pandas >= 1.3.0
- numpy < 2.0.0 (compatibility)

See `requirements.txt` for full list.

## 🎯 Success Criteria

When training completes successfully, you should have:

```python
✅ Models trained: 6+ models (XGBoost, LightGBM, CatBoost, RF, ExtraTrees, GradientBoosting)
✅ Ensemble created
✅ R² Score > 0.90 (target: 0.93+)
✅ All models saved to models/deployed/
✅ No errors during training pipeline
```

## 📝 Development Philosophy

1. **Read original code carefully** - Don't change anything prematurely
2. **Fix only what's broken** - No optimization unless requested
3. **Test incrementally** - imports → functions → pipeline
4. **KISS principle** - Keep It Simple, Stupid!
5. **Don't overthink** - Follow instructions exactly

## 🔍 Debugging Workflow

If errors occur:

1. Read error message thoroughly
2. Identify root cause (usually imports or KeyError)
3. Fix at source, not everywhere that might be related
4. Test each component separately
5. Document error and solution

## Platform-Specific Notes

### For Kaggle Notebook

See `CLAUDE_KAGGLE.md` for complete Kaggle-specific setup instructions including:
- Cell 1: Complete environment setup
- Cell 2: Full training pipeline
- Import fixes for Kaggle paths
- Data preparation steps

### For Local Development

This is the default setup. Use commands in "Quick Start Commands" section above.

## 📚 Additional Resources

- `CLAUDE_KAGGLE.md` - Complete Kaggle notebook setup guide
- `README.md` - User-facing documentation
- `implementation_guide.md` - Original implementation notes
- `tests/test_summary.md` - Testing documentation
