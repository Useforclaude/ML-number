#!/usr/bin/env python3
"""
XGBoost Only Training - Modular Script
Train only XGBoost model with Optuna optimization
Prevents timeout by splitting training into smaller pieces
"""

import os
import sys
import time
import logging
import joblib
from datetime import datetime
from pathlib import Path

# Setup logging
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/xgboost_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import project modules
try:
    from src.config import BASE_PATH, MODEL_CONFIG
    from src.environment import detect_environment
    from src.data_handler import load_and_clean_data
    from src.data_splitter import create_validation_set
    from src.model_utils import AdvancedPreprocessor, optimize_xgboost
    from src.training_callbacks import create_training_callbacks, print_training_header, print_training_footer
    from training.main import run_feature_pipeline
    from sklearn.model_selection import train_test_split
    from xgboost import XGBRegressor
    import numpy as np
    import pandas as pd
    import torch
    from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error("Make sure virtual environment is activated: source .venv/bin/activate")
    sys.exit(1)


def check_gpu():
    """Check GPU availability"""
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        logger.info(f"✅ GPU Available: {gpu_name} ({gpu_memory:.1f} GB)")
        return True
    else:
        logger.warning("⚠️  No GPU detected - Will use CPU")
        return False


def main():
    """Main XGBoost training pipeline"""
    start_time = time.time()

    logger.info("\n" + "="*80)
    logger.info("🚀 XGBOOST MODULAR TRAINING")
    logger.info("="*80)
    logger.info(f"📂 Project: {BASE_PATH}")
    logger.info(f"🖥️  Environment: {detect_environment()}")
    logger.info("="*80)

    # Check GPU
    use_gpu = check_gpu()

    # Step 1: Load filtered data
    logger.info("\n" + "="*80)
    logger.info("STEP 1: Loading Filtered Data")
    logger.info("="*80)

    try:
        df_raw, df_cleaned = load_and_clean_data(
            file_path='/notebooks/ML-number/data/raw/numberdata.csv',
            filter_outliers_param=True,
            max_price=100000
        )
        logger.info(f"✅ Data loaded: raw={len(df_raw)} rows, cleaned={len(df_cleaned)} rows")
    except Exception as e:
        logger.error(f"❌ Failed to load data: {e}")
        return 1

    # Step 2: Feature engineering + stratified split
    logger.info("\n" + "="*80)
    logger.info("STEP 2: Feature Engineering")
    logger.info("="*80)

    try:
        price_bins = pd.qcut(
            df_cleaned['price'],
            q=5,
            labels=False,
            duplicates='drop'
        )
        train_indices, test_indices = train_test_split(
            np.arange(len(df_cleaned)),
            test_size=MODEL_CONFIG.get('test_size', 0.2),
            stratify=price_bins,
            random_state=MODEL_CONFIG.get('random_state', 42)
        )

        X, y_log, sample_weights = run_feature_pipeline(
            df_cleaned,
            train_indices=train_indices
        )
        sample_weights = pd.Series(sample_weights, index=X.index)

        X_train = X.iloc[train_indices]
        X_test = X.iloc[test_indices]
        y_log_train = y_log.iloc[train_indices]
        y_log_test = y_log.iloc[test_indices]
        sw_train = sample_weights.iloc[train_indices]
        sw_test = sample_weights.iloc[test_indices]

        logger.info(
            "✅ Features created with stratified indices: "
            f"{X.shape[1]} features | Train={len(X_train)} | Test={len(X_test)}"
        )
    except Exception as e:
        logger.error(f"❌ Failed to prepare features and splits: {e}")
        return 1

    # Step 3: Convert to actual prices
    logger.info("\n" + "="*80)
    logger.info("STEP 3: Converting to Actual Prices")
    logger.info("="*80)

    y_train = pd.Series(np.expm1(y_log_train))
    y_test = pd.Series(np.expm1(y_log_test))
    logger.info(f"✅ Train prices: ฿{y_train.min():,.0f} - ฿{y_train.max():,.0f}")

    # Step 4: Create validation set
    logger.info("\n" + "="*80)
    logger.info("STEP 4: Creating Validation Set")
    logger.info("="*80)

    try:
        X_tr, X_val, y_tr, y_val, sw_tr, sw_val = create_validation_set(
            X_train, y_train, sw_train,
            val_size=0.15,
            random_state=42
        )
        sw_tr_array = sw_tr.values if hasattr(sw_tr, "values") else sw_tr
        logger.info(f"✅ Validation set: Train={len(X_tr)}, Val={len(X_val)}")
    except Exception as e:
        logger.error(f"❌ Failed to create validation set: {e}")
        return 1

    # Step 5: Preprocessing
    logger.info("\n" + "="*80)
    logger.info("STEP 5: Preprocessing")
    logger.info("="*80)

    try:
        preprocessor = AdvancedPreprocessor()
        X_tr_processed = preprocessor.fit_transform(X_tr)
        X_val_processed = preprocessor.transform(X_val)
        X_test_processed = preprocessor.transform(X_test)

        # Clean NaN/Inf
        for df in [X_tr_processed, X_val_processed, X_test_processed]:
            df.replace([np.inf, -np.inf], np.nan, inplace=True)
            if hasattr(df, 'median'):
                df.fillna(df.median(), inplace=True)
            else:
                df.fillna(X_tr_processed.median(), inplace=True)

        logger.info(f"✅ Preprocessed: {X_tr_processed.shape[1]} features")
    except Exception as e:
        logger.error(f"❌ Failed to preprocess: {e}")
        return 1

    # Step 6: XGBOOST OPTIMIZATION
    logger.info("\n" + "="*80)
    logger.info("🔥 STEP 6: XGBOOST OPTIMIZATION")
    logger.info("="*80)

    n_trials = MODEL_CONFIG.get('optuna_trials', 100)
    logger.info(f"⏱️  Expected duration: 2-3 hours")
    logger.info(f"🎯 Optimization trials: {n_trials}")
    logger.info(f"🔥 GPU enabled: {use_gpu}")
    logger.info("="*80 + "\n")

    # Create callbacks
    callbacks = create_training_callbacks(
        checkpoint_manager=None,
        n_trials=n_trials,
        use_gpu=use_gpu
    )

    # Print header
    print_training_header("XGBoost", n_trials, use_gpu)

    optimization_start = time.time()

    try:
        # Optimize XGBoost
        xgb_params = optimize_xgboost(
            X_tr_processed, y_tr,
            n_trials=n_trials,
            cv_folds=10,
            sample_weight=sw_tr_array,
            use_gpu=use_gpu,
            callbacks=callbacks
        )

        optimization_time = time.time() - optimization_start
        print_training_footer("XGBoost", xgb_params.get('best_cv_score', 0.0) if isinstance(xgb_params, dict) else 0.0, optimization_time)

        # Train final model with best params
        logger.info("\n" + "="*80)
        logger.info("🎯 Training Final XGBoost Model")
        logger.info("="*80)

        model = XGBRegressor(**xgb_params)
        model.fit(X_tr_processed, y_tr, sample_weight=sw_tr_array)

        # Evaluate
        y_val_pred = model.predict(X_val_processed)
        r2 = r2_score(y_val, y_val_pred)
        mae = mean_absolute_error(y_val, y_val_pred)
        rmse = np.sqrt(mean_squared_error(y_val, y_val_pred))

        logger.info(f"✅ XGBoost trained successfully!")
        logger.info(f"   R² Score:  {r2:.4f}")
        logger.info(f"   MAE:       {mae:.2f}")
        logger.info(f"   RMSE:      {rmse:.2f}")

        # Save checkpoint
        os.makedirs("models/checkpoints", exist_ok=True)
        checkpoint_path = "models/checkpoints/xgboost_checkpoint.pkl"

        checkpoint = {
            'model': model,
            'params': xgb_params,
            'r2_score': r2,
            'mae': mae,
            'rmse': rmse,
            'training_time_hours': optimization_time / 3600,
            'timestamp': datetime.now().isoformat(),
            'preprocessor': preprocessor,
            'feature_names': X_tr_processed.columns.tolist() if hasattr(X_tr_processed, 'columns') else None
        }

        joblib.dump(checkpoint, checkpoint_path)
        logger.info(f"\n💾 Checkpoint saved: {checkpoint_path}")

        # Total time
        total_time = (time.time() - start_time) / 3600
        logger.info("\n" + "="*80)
        logger.info("✅ XGBOOST TRAINING COMPLETE!")
        logger.info("="*80)
        logger.info(f"⏱️  Total Time: {total_time:.2f} hours")
        logger.info(f"📊 Best R²: {r2:.4f}")
        logger.info(f"💾 Checkpoint: {checkpoint_path}")
        logger.info("="*80)

        return 0

    except Exception as e:
        logger.error(f"❌ XGBoost optimization failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
