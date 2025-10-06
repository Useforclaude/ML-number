# Cell 4: Full Training Pipeline - CORRECTED VERSION
# Fixed all 5 errors identified in Session 011

import numpy as np
import pandas as pd
import time

# Imports
from src.features import create_all_features
from src.data_splitter import split_data_stratified, create_validation_set
from src.model_utils import AdvancedPreprocessor
from src.train_production import train_production_pipeline

print("="*80)
print("🚀 FULL TRAINING PIPELINE (CORRECTED)")
print("="*80)

# STEP 1: Create Features
print("\n📊 STEP 1: Feature Engineering...")
X, y_log, sample_weights = create_all_features(df_cleaned)
print(f"   ✅ Features: {X.shape[1]} features, {X.shape[0]} samples")
print(f"   ✅ Target: {y_log.min():.2f} - {y_log.max():.2f} (log-scale)")

# STEP 2: Split Train/Test
print("\n📊 STEP 2: Train/Test Split...")
X_train, X_test, y_log_train, y_log_test, sw_train, sw_test = split_data_stratified(
    X, y_log, sample_weights,
    test_size=0.2,
    random_state=42
)

# STEP 3: Convert to Actual Prices (CRITICAL FIX!)
print("\n📊 STEP 3: Converting to actual prices...")
y_train = pd.Series(np.expm1(y_log_train))  # log → actual + wrap Series
y_test = pd.Series(np.expm1(y_log_test))
print(f"   ✅ Train prices: ฿{y_train.min():,.0f} - ฿{y_train.max():,.0f}")
print(f"   ✅ Test prices: ฿{y_test.min():,.0f} - ฿{y_test.max():,.0f}")

# STEP 4: Split Train/Validation (NEW!)
print("\n📊 STEP 4: Creating validation set...")
X_tr, X_val, y_tr, y_val, sw_tr, sw_val = create_validation_set(
    X_train, y_train, sw_train,
    val_size=0.15,  # 15% of training for validation
    random_state=42
)
print(f"   ✅ Final train: {len(X_tr):,} samples")
print(f"   ✅ Validation: {len(X_val):,} samples")
print(f"   ✅ Test: {len(X_test):,} samples")

# STEP 5: Preprocessing (FIXED!)
print("\n📊 STEP 5: Preprocessing...")
preprocessor = AdvancedPreprocessor()  # ✅ No parameters (was: remove_outliers, etc.)
X_tr_processed = preprocessor.fit_transform(X_tr)
X_val_processed = preprocessor.transform(X_val)
X_test_processed = preprocessor.transform(X_test)

# Clean NaN/Inf
print("   🧹 Cleaning NaN/Inf values...")
for df in [X_tr_processed, X_val_processed, X_test_processed]:
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    if hasattr(df, 'median'):
        df.fillna(df.median(), inplace=True)
    else:
        df.fillna(X_tr_processed.median(), inplace=True)

print(f"   ✅ Processed: {X_tr_processed.shape[1]} features")

# STEP 6: PRODUCTION TRAINING
print("\n" + "="*80)
print("🔥 STARTING PRODUCTION TRAINING")
print("="*80)
print(f"⚠️  Estimated time: 9-12 hours")
print(f"⚠️  DO NOT close this notebook!")
print(f"⚠️  Progress will be displayed during training")
print("="*80 + "\n")

start_time = time.time()

results = train_production_pipeline(
    X_tr_processed, y_tr,  # ✅ Actual prices (not log)
    X_val_processed, y_val,  # ✅ Actual prices (not log)
    optimize=True,
    n_trials=100,
    use_gpu=True,
    verbose=True
)

elapsed_hours = (time.time() - start_time) / 3600

# FINAL RESULTS
print("\n" + "="*80)
print("✅ TRAINING COMPLETE!")
print("="*80)
print(f"⏱️  Total Time: {elapsed_hours:.2f} hours")
print(f"🏆 Best Model: {results['best_model_name']}")
print(f"📊 Best R²: {results['best_score']:.4f}")  # ✅ Correct key (was: best_r2_val)
print(f"📉 MAE: {results['best_mae']:.2f}")
print(f"📉 RMSE: {results['best_rmse']:.2f}")
print("\n💾 Models saved to: /storage/ML-number/models/")
print("="*80)

# Save best model for later use
best_model = results['best_model']
print(f"\n✅ Best model ready for predictions!")
print(f"   Use: best_model.predict(X_test_processed)")
