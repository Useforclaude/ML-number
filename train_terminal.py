#!/usr/bin/env python3
"""
Paperspace ML Training - Terminal Version
Train phone number price prediction models with GPU support
"""

import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

# Create logs directory
os.makedirs("logs", exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/training_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import project modules
try:
    from src.config import BASE_PATH, MODEL_CONFIG
    from src.environment import detect_environment, setup_base_path
    from src.data_handler import load_and_clean_data
    from src.features import create_all_features
    from src.data_splitter import split_data_stratified, create_validation_set
    from src.model_utils import AdvancedPreprocessor
    from src.train_production import train_production_pipeline
    import numpy as np
    import pandas as pd
    import torch
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error("Make sure virtual environment is activated: source .venv/bin/activate")
    sys.exit(1)


def print_header():
    """Print training header"""
    print("\n" + "="*80)
    print("🚀 PAPERSPACE ML TRAINING - TERMINAL MODE")
    print("="*80)
    print(f"📂 Project: ML Phone Number Price Prediction")
    print(f"📍 Path: {BASE_PATH}")
    print(f"🖥️  Environment: {detect_environment()}")
    print(f"🎯 Target: R² > 0.90")
    print("="*80 + "\n")


def check_gpu():
    """Check GPU availability"""
    logger.info("🔍 Checking GPU...")

    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        logger.info(f"✅ GPU Available: {gpu_name}")
        logger.info(f"   Memory: {gpu_memory:.1f} GB")
        return True
    else:
        logger.warning("⚠️  No GPU detected - Training will use CPU (much slower!)")
        return False


def main():
    """Main training pipeline"""
    start_time = time.time()

    # Print header
    print_header()

    # Check GPU
    use_gpu = check_gpu()

    # Step 1: Load data
    logger.info("\n" + "="*80)
    logger.info("STEP 1: Loading Data")
    logger.info("="*80)

    try:
        df_cleaned = load_and_clean_data(filter_outliers_param=True, max_price=100000)
        logger.info(f"✅ Data loaded: {len(df_cleaned)} rows")
    except Exception as e:
        logger.error(f"❌ Failed to load data: {e}")
        return 1

    # Step 2: Feature engineering
    logger.info("\n" + "="*80)
    logger.info("STEP 2: Feature Engineering")
    logger.info("="*80)

    try:
        X, y_log, sample_weights = create_all_features(df_cleaned)
        logger.info(f"✅ Features created: {X.shape[1]} features, {X.shape[0]} samples")
    except Exception as e:
        logger.error(f"❌ Failed to create features: {e}")
        return 1

    # Step 3: Split data
    logger.info("\n" + "="*80)
    logger.info("STEP 3: Train/Test Split")
    logger.info("="*80)

    try:
        X_train, X_test, y_log_train, y_log_test, sw_train, sw_test = split_data_stratified(
            X, y_log, sample_weights,
            test_size=0.2,
            random_state=42
        )
        logger.info(f"✅ Split complete: Train={len(X_train)}, Test={len(X_test)}")
    except Exception as e:
        logger.error(f"❌ Failed to split data: {e}")
        return 1

    # Step 4: Convert to actual prices
    logger.info("\n" + "="*80)
    logger.info("STEP 4: Converting to Actual Prices")
    logger.info("="*80)

    y_train = pd.Series(np.expm1(y_log_train))
    y_test = pd.Series(np.expm1(y_log_test))
    logger.info(f"✅ Train prices: ฿{y_train.min():,.0f} - ฿{y_train.max():,.0f}")
    logger.info(f"✅ Test prices: ฿{y_test.min():,.0f} - ฿{y_test.max():,.0f}")

    # Step 5: Create validation set
    logger.info("\n" + "="*80)
    logger.info("STEP 5: Creating Validation Set")
    logger.info("="*80)

    try:
        X_tr, X_val, y_tr, y_val, sw_tr, sw_val = create_validation_set(
            X_train, y_train, sw_train,
            val_size=0.15,
            random_state=42
        )
        logger.info(f"✅ Validation set: Train={len(X_tr)}, Val={len(X_val)}")
    except Exception as e:
        logger.error(f"❌ Failed to create validation set: {e}")
        return 1

    # Step 6: Preprocessing
    logger.info("\n" + "="*80)
    logger.info("STEP 6: Preprocessing")
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

    # Step 7: PRODUCTION TRAINING
    logger.info("\n" + "="*80)
    logger.info("🔥 STEP 7: PRODUCTION TRAINING")
    logger.info("="*80)
    logger.info(f"⏱️  Expected duration: 9-12 hours")
    logger.info(f"🎯 Optimization trials: {MODEL_CONFIG.get('optuna_trials', 100)}")
    logger.info(f"🔥 GPU enabled: {use_gpu}")
    logger.info("="*80 + "\n")

    training_start = time.time()

    try:
        results = train_production_pipeline(
            X_tr_processed, y_tr,
            X_val_processed, y_val,
            optimize=True,
            n_trials=MODEL_CONFIG.get('optuna_trials', 100),
            use_gpu=use_gpu,
            verbose=True
        )

        training_time = (time.time() - training_start) / 3600

        # Final results
        logger.info("\n" + "="*80)
        logger.info("✅ TRAINING COMPLETE!")
        logger.info("="*80)
        logger.info(f"⏱️  Training Time: {training_time:.2f} hours")
        logger.info(f"🏆 Best Model: {results['best_model_name']}")
        logger.info(f"📊 Best R²: {results['best_score']:.4f}")
        logger.info(f"📉 MAE: {results['best_mae']:.2f}")
        logger.info(f"📉 RMSE: {results['best_rmse']:.2f}")
        logger.info("="*80)

        # Total time
        total_time = (time.time() - start_time) / 3600
        logger.info(f"\n⏱️  Total Time: {total_time:.2f} hours")
        logger.info("✅ All done! Models saved to models/ directory")

        return 0

    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    # Create logs directory
    os.makedirs("logs", exist_ok=True)

    # Run training
    exit_code = main()
    sys.exit(exit_code)
