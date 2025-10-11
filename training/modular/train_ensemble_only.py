#!/usr/bin/env python3
"""
Ensemble Only Training - Modular Script
Load trained models and create ensemble
Final step in modular training pipeline
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
        logging.FileHandler(f'logs/ensemble_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import project modules
try:
    from src.config import BASE_PATH
    from src.environment import detect_environment
    from src.data_handler import load_and_clean_data
    from src.features import create_all_features
    from src.data_splitter import split_data_stratified, create_validation_set
    from src.model_utils import AdvancedPreprocessor
    import numpy as np
    import pandas as pd
    from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
    from sklearn.ensemble import VotingRegressor, StackingRegressor
    from sklearn.linear_model import Ridge
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error("Make sure virtual environment is activated: source .venv/bin/activate")
    sys.exit(1)


def load_checkpoints():
    """Load all trained model checkpoints"""
    checkpoints = {}
    checkpoint_dir = "models/checkpoints"

    model_files = {
        'XGBoost': 'xgboost_checkpoint.pkl',
        'LightGBM': 'lightgbm_checkpoint.pkl',
        'CatBoost': 'catboost_checkpoint.pkl',
        'RandomForest': 'random_forest_checkpoint.pkl'
    }

    for name, filename in model_files.items():
        filepath = os.path.join(checkpoint_dir, filename)
        if os.path.exists(filepath):
            try:
                checkpoint = joblib.load(filepath)
                checkpoints[name] = checkpoint
                logger.info(f"✅ Loaded {name}: R²={checkpoint['r2_score']:.4f}")
            except Exception as e:
                logger.warning(f"⚠️  Failed to load {name}: {e}")
        else:
            logger.warning(f"⚠️  Checkpoint not found: {filepath}")

    if len(checkpoints) == 0:
        raise FileNotFoundError("❌ No checkpoints found! Train models first.")

    return checkpoints


def main():
    """Main ensemble creation pipeline"""
    start_time = time.time()

    logger.info("\n" + "="*80)
    logger.info("🚀 ENSEMBLE CREATION - MODULAR")
    logger.info("="*80)
    logger.info(f"📂 Project: {BASE_PATH}")
    logger.info(f"🖥️  Environment: {detect_environment()}")
    logger.info("="*80)

    # Step 1: Load checkpoints
    logger.info("\n" + "="*80)
    logger.info("STEP 1: Loading Model Checkpoints")
    logger.info("="*80)

    try:
        checkpoints = load_checkpoints()
        logger.info(f"✅ Loaded {len(checkpoints)} models")
    except Exception as e:
        logger.error(f"❌ Failed to load checkpoints: {e}")
        return 1

    # Step 2: Load data for evaluation
    logger.info("\n" + "="*80)
    logger.info("STEP 2: Loading Data")
    logger.info("="*80)

    try:
        df_raw, df_cleaned = load_and_clean_data(filter_outliers_param=True, max_price=100000)
        logger.info(f"✅ Data loaded: raw={len(df_raw)} rows, cleaned={len(df_cleaned)} rows")
        X, y_log, sample_weights = create_all_features(df_cleaned)

        X_train, X_test, y_log_train, y_log_test, sw_train, sw_test = split_data_stratified(
            X, y_log, sample_weights, test_size=0.2, random_state=42
        )

        y_train = pd.Series(np.expm1(y_log_train))
        y_test = pd.Series(np.expm1(y_log_test))

        X_tr, X_val, y_tr, y_val, sw_tr, sw_val = create_validation_set(
            X_train, y_train, sw_train, val_size=0.15, random_state=42
        )

        # Get preprocessor from any checkpoint
        preprocessor = list(checkpoints.values())[0]['preprocessor']
        X_val_processed = preprocessor.transform(X_val)

        # Clean NaN/Inf
        X_val_processed.replace([np.inf, -np.inf], np.nan, inplace=True)
        X_val_processed.fillna(X_val_processed.median(), inplace=True)

        logger.info(f"✅ Data prepared: Val={len(X_val)}")
    except Exception as e:
        logger.error(f"❌ Failed to load data: {e}")
        return 1

    # Step 3: Create ensembles
    logger.info("\n" + "="*80)
    logger.info("STEP 3: Creating Ensembles")
    logger.info("="*80)

    # Extract models
    models_list = [(name, checkpoint['model']) for name, checkpoint in checkpoints.items()]

    # Ensemble 1: Voting
    try:
        logger.info("\n🏗️  Creating Voting Ensemble...")
        voting = VotingRegressor(estimators=models_list, n_jobs=1)  # n_jobs=1 for GPU models
        voting.fit(X_val_processed, y_val)
        voting_pred = voting.predict(X_val_processed)
        voting_r2 = r2_score(y_val, voting_pred)
        voting_mae = mean_absolute_error(y_val, voting_pred)
        voting_rmse = np.sqrt(mean_squared_error(y_val, voting_pred))
        logger.info(f"✅ Voting Ensemble: R²={voting_r2:.4f}, MAE={voting_mae:.2f}")
    except Exception as e:
        logger.error(f"❌ Voting ensemble failed: {e}")
        voting = None
        voting_r2 = 0.0

    # Ensemble 2: Stacking
    try:
        logger.info("\n🏗️  Creating Stacking Ensemble...")
        stacking = StackingRegressor(
            estimators=models_list,
            final_estimator=Ridge(alpha=1.0),
            n_jobs=1  # n_jobs=1 for GPU models
        )
        stacking.fit(X_val_processed, y_val)
        stacking_pred = stacking.predict(X_val_processed)
        stacking_r2 = r2_score(y_val, stacking_pred)
        stacking_mae = mean_absolute_error(y_val, stacking_pred)
        stacking_rmse = np.sqrt(mean_squared_error(y_val, stacking_pred))
        logger.info(f"✅ Stacking Ensemble: R²={stacking_r2:.4f}, MAE={stacking_mae:.2f}")
    except Exception as e:
        logger.error(f"❌ Stacking ensemble failed: {e}")
        stacking = None
        stacking_r2 = 0.0

    # Step 4: Select best model
    logger.info("\n" + "="*80)
    logger.info("STEP 4: Selecting Best Model")
    logger.info("="*80)

    all_models = {**checkpoints}
    all_scores = {name: checkpoint['r2_score'] for name, checkpoint in checkpoints.items()}

    if voting:
        all_models['Voting_Ensemble'] = {'model': voting, 'r2_score': voting_r2}
        all_scores['Voting_Ensemble'] = voting_r2

    if stacking:
        all_models['Stacking_Ensemble'] = {'model': stacking, 'r2_score': stacking_r2}
        all_scores['Stacking_Ensemble'] = stacking_r2

    # Find best
    best_name = max(all_scores.items(), key=lambda x: x[1])[0]
    best_score = all_scores[best_name]
    best_model = all_models[best_name]['model']

    logger.info(f"\n🏆 Best Model: {best_name}")
    logger.info(f"   R² Score: {best_score:.4f}")

    # Print rankings
    logger.info("\n📊 Model Rankings:")
    sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
    for i, (name, score) in enumerate(sorted_scores, 1):
        logger.info(f"   {i}. {name:25s} R²={score:.4f}")

    # Step 5: Save best model
    logger.info("\n" + "="*80)
    logger.info("STEP 5: Saving Best Model")
    logger.info("="*80)

    try:
        os.makedirs("models/deployed", exist_ok=True)
        deployment = {
            'model': best_model,
            'model_name': best_name,
            'r2_score': best_score,
            'preprocessor': preprocessor,
            'feature_names': X_val_processed.columns.tolist() if hasattr(X_val_processed, 'columns') else None,
            'timestamp': datetime.now().isoformat(),
            'all_scores': all_scores
        }

        deployment_path = "models/deployed/best_model.pkl"
        joblib.dump(deployment, deployment_path)
        logger.info(f"💾 Deployed model saved: {deployment_path}")

        # Also save ensemble details
        ensemble_path = "models/deployed/ensemble_models.pkl"
        ensemble_data = {
            'voting': voting,
            'stacking': stacking,
            'individual_models': {name: checkpoint['model'] for name, checkpoint in checkpoints.items()},
            'scores': all_scores
        }
        joblib.dump(ensemble_data, ensemble_path)
        logger.info(f"💾 Ensemble details saved: {ensemble_path}")

    except Exception as e:
        logger.error(f"❌ Failed to save models: {e}")
        return 1

    # Final summary
    total_time = (time.time() - start_time) / 60
    logger.info("\n" + "="*80)
    logger.info("✅ ENSEMBLE CREATION COMPLETE!")
    logger.info("="*80)
    logger.info(f"⏱️  Total Time: {total_time:.1f} minutes")
    logger.info(f"🏆 Best Model: {best_name}")
    logger.info(f"📊 Best R²: {best_score:.4f}")
    logger.info(f"💾 Deployed: {deployment_path}")
    logger.info("="*80)

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
