"""
ULTRA-POWER Production Training Pipeline
Full optimization with Optuna, Ensemble, Cross-validation
NO DATA LEAKAGE - Split before feature engineering

By Claude + Alex - World-Class AI
"""

import numpy as np
import pandas as pd
import time
from datetime import datetime
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import cross_val_score, KFold

# Import optimization functions
from src.model_utils import (
    optimize_xgboost, optimize_lightgbm, optimize_catboost, optimize_random_forest
)

# Import training functions
from src.train import train_individual_models, create_ensemble_models

# Import training callbacks for verbose monitoring
from src.training_callbacks import (
    create_training_callbacks,
    print_training_header,
    print_training_footer
)

# ML Models
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor

import warnings
warnings.filterwarnings('ignore')

# ====================================================================================
# PROGRESSIVE SAMPLE WEIGHTS
# ====================================================================================

def calculate_progressive_weights(y_prices, mode='log'):
    """
    Calculate progressive sample weights for imbalanced price data

    Parameters:
    -----------
    y_prices : array-like
        Target prices (actual prices, not log-transformed)
    mode : str
        'log' or 'linear' weighting

    Returns:
    --------
    weights : np.ndarray
        Sample weights
    """
    y_prices = np.array(y_prices)

    if mode == 'log':
        # Log-based progressive weighting
        weights = np.ones(len(y_prices))

        # Define price thresholds and weights
        thresholds = [10000, 50000, 100000, 500000, 1000000]
        weight_values = [1.0, 2.0, 4.0, 6.0, 8.0, 10.0]

        for i, price in enumerate(y_prices):
            for j, threshold in enumerate(thresholds):
                if price <= threshold:
                    weights[i] = weight_values[j]
                    break
            else:
                weights[i] = weight_values[-1]

    elif mode == 'linear':
        # Linear scaling based on price percentile
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler(feature_range=(1.0, 10.0))
        weights = scaler.fit_transform(y_prices.reshape(-1, 1)).flatten()

    else:
        weights = np.ones(len(y_prices))

    # Normalize
    weights = weights / weights.mean()

    return weights

# ====================================================================================
# FULL POWER TRAINING PIPELINE
# ====================================================================================

def train_production_pipeline(X_train, y_train, X_val, y_val,
                               optimize=True, n_trials=100,
                               use_gpu=False, verbose=True):
    """
    ULTRA-POWER Production Training Pipeline

    Features:
    - Optuna hyperparameter optimization (50-150 trials per model)
    - Multiple models: XGBoost, LightGBM, CatBoost, RF, ET, GB
    - Ensemble methods: Voting, Stacking, Weighted Average
    - Cross-validation (10-fold)
    - Progressive sample weights
    - Early stopping
    - Automatic best model selection

    Parameters:
    -----------
    X_train, X_val : array-like
        Training and validation features
    y_train, y_val : array-like
        Training and validation targets (ACTUAL PRICES, not log)
    optimize : bool
        Use Optuna hyperparameter optimization (slower but better)
    n_trials : int
        Number of Optuna trials per model (50-150)
    use_gpu : bool
        Use GPU acceleration if available
    verbose : bool
        Print detailed progress

    Returns:
    --------
    result : dict
        Complete training results with all models and metrics
    """

    if verbose:
        print("\n" + "="*80)
        print("🚀 ULTRA-POWER PRODUCTION TRAINING PIPELINE")
        print("="*80)
        print(f"Training samples: {len(X_train)}")
        print(f"Validation samples: {len(X_val)}")
        print(f"Features: {X_train.shape[1]}")
        print(f"Optimization: {'ON' if optimize else 'OFF'} ({n_trials} trials per model)")
        print(f"GPU: {'ENABLED' if use_gpu else 'DISABLED'}")
        print("="*80)

    start_time = time.time()

    # ====================================================================================
    # 1. CALCULATE SAMPLE WEIGHTS
    # ====================================================================================

    if verbose:
        print("\n📊 Step 1: Calculating progressive sample weights...")

    sample_weights = calculate_progressive_weights(y_train, mode='log')

    if verbose:
        print(f"   Weight range: {sample_weights.min():.2f} - {sample_weights.max():.2f}")
        print(f"   Mean weight: {sample_weights.mean():.2f}")

    # ====================================================================================
    # 2. HYPERPARAMETER OPTIMIZATION
    # ====================================================================================

    if optimize:
        if verbose:
            print("\n🔧 Step 2: Hyperparameter Optimization (this may take hours!)")
            print(f"   Each model will run {n_trials} Optuna trials with CV...")

        # Create training callbacks for real-time monitoring
        callbacks = create_training_callbacks(
            checkpoint_manager=None,  # No checkpoint manager yet
            n_trials=n_trials,
            use_gpu=use_gpu
        )

        # Optimize XGBoost
        if verbose:
            print_training_header("XGBoost", n_trials, use_gpu)

        start_time = time.time()
        xgb_params = optimize_xgboost(X_train, y_train, n_trials=n_trials,
                                      cv_folds=10, sample_weight=sample_weights,
                                      use_gpu=use_gpu, callbacks=callbacks)
        elapsed = time.time() - start_time

        if verbose:
            print_training_footer("XGBoost", xgb_params.get('best_cv_score', 0.0) if isinstance(xgb_params, dict) else 0.0, elapsed)

        # Optimize LightGBM (with automatic GPU fallback)
        if verbose:
            print_training_header("LightGBM", n_trials, use_gpu)

        start_time = time.time()
        lgb_params = optimize_lightgbm(X_train, y_train, n_trials=n_trials,
                                       cv_folds=10, sample_weight=sample_weights,
                                       use_gpu=use_gpu, callbacks=callbacks)
        elapsed = time.time() - start_time

        # Check if GPU fallback occurred
        if verbose and use_gpu and not lgb_params.get('_gpu_used', False):
            print(f"\n{'='*80}")
            print(f"ℹ️  Note: LightGBM automatically used CPU (GPU compatibility issue)")
            print(f"ℹ️  XGBoost and CatBoost will still use GPU normally")
            print(f"{'='*80}\n")

        if verbose:
            print_training_footer("LightGBM", lgb_params.get('best_cv_score', 0.0) if isinstance(lgb_params, dict) else 0.0, elapsed)

        # Optimize CatBoost
        if verbose:
            print_training_header("CatBoost", max(50, n_trials//2), use_gpu)

        start_time = time.time()
        cat_params = optimize_catboost(X_train, y_train, n_trials=max(50, n_trials//2),
                                       cv_folds=10, sample_weight=sample_weights,
                                       use_gpu=use_gpu, callbacks=callbacks)
        elapsed = time.time() - start_time

        if verbose:
            print_training_footer("CatBoost", cat_params.get('best_cv_score', 0.0) if isinstance(cat_params, dict) else 0.0, elapsed)

        # Optimize Random Forest
        if verbose:
            print_training_header("RandomForest", max(50, n_trials//2), use_gpu)

        start_time = time.time()
        rf_params = optimize_random_forest(X_train, y_train, n_trials=max(50, n_trials//2),
                                           cv_folds=10, sample_weight=sample_weights,
                                           use_gpu=use_gpu, callbacks=callbacks)
        elapsed = time.time() - start_time

        if verbose:
            print_training_footer("RandomForest", rf_params.get('best_cv_score', 0.0) if isinstance(rf_params, dict) else 0.0, elapsed)

    else:
        # Use default parameters (much faster)
        if verbose:
            print("\n🔧 Step 2: Using default parameters (fast mode)")

        xgb_params = {
            'n_estimators': 500, 'learning_rate': 0.05, 'max_depth': 8,
            'subsample': 0.8, 'colsample_bytree': 0.8, 'random_state': 42,
            'device': 'cuda' if use_gpu else 'cpu',
            'tree_method': 'hist'
        }

        lgb_params = {
            'n_estimators': 500, 'learning_rate': 0.05, 'max_depth': 8,
            'subsample': 0.8, 'colsample_bytree': 0.8, 'random_state': 42
        }

        cat_params = {
            'iterations': 500, 'learning_rate': 0.05, 'depth': 8,
            'random_state': 42, 'verbose': False,
            'task_type': 'GPU' if use_gpu else 'CPU'
        }

        rf_params = {
            'n_estimators': 300, 'max_depth': 20, 'min_samples_split': 5,
            'min_samples_leaf': 2, 'random_state': 42, 'n_jobs': -1
        }

    # ====================================================================================
    # 3. TRAIN INDIVIDUAL MODELS
    # ====================================================================================

    if verbose:
        print("\n🎯 Step 3: Training Individual Models...")

    base_models = [
        ('XGBoost', XGBRegressor(**xgb_params)),
        ('LightGBM', LGBMRegressor(**lgb_params)),
        ('CatBoost', CatBoostRegressor(**cat_params)),
        ('RandomForest', RandomForestRegressor(**rf_params)),
        ('ExtraTrees', ExtraTreesRegressor(**rf_params)),
        ('GradientBoosting', GradientBoostingRegressor(
            n_estimators=300, learning_rate=0.05, max_depth=8,
            subsample=0.8, random_state=42
        ))
    ]

    trained_models, test_predictions, results_df = train_individual_models(
        base_models, X_train, X_val, y_train, y_val,
        sample_weight=sample_weights, verbose=verbose
    )

    # ====================================================================================
    # 4. CREATE ENSEMBLE MODELS
    # ====================================================================================

    if verbose:
        print("\n🏗️  Step 4: Creating Ensemble Models...")

    ensemble_models, ensemble_predictions = create_ensemble_models(
        trained_models, X_train, y_train, X_val, y_val,
        test_predictions, sample_weights, n_top_models=5
    )

    # ====================================================================================
    # 5. SELECT BEST MODEL
    # ====================================================================================

    if verbose:
        print("\n🏆 Step 5: Selecting Best Model...")

    # Combine all predictions
    all_predictions = {**test_predictions, **ensemble_predictions}

    # Calculate R² for all models
    all_scores = {}
    for name, pred in all_predictions.items():
        r2 = r2_score(y_val, pred)
        mae = mean_absolute_error(y_val, pred)
        rmse = np.sqrt(mean_squared_error(y_val, pred))
        all_scores[name] = {'r2': r2, 'mae': mae, 'rmse': rmse}

    # Find best model
    best_model_name = max(all_scores.items(), key=lambda x: x[1]['r2'])[0]
    best_score = all_scores[best_model_name]

    # Get best model object
    if best_model_name in trained_models:
        best_model = trained_models[best_model_name]
    elif best_model_name in ensemble_models:
        best_model = ensemble_models[best_model_name]
    else:
        # For simple/weighted average, use Voting ensemble as fallback
        best_model = ensemble_models.get('Voting_Ensemble', list(trained_models.values())[0])

    # ====================================================================================
    # 6. FINAL SUMMARY
    # ====================================================================================

    elapsed_time = time.time() - start_time

    if verbose:
        print("\n" + "="*80)
        print("✅ TRAINING COMPLETE!")
        print("="*80)
        print(f"\n🏆 Best Model: {best_model_name}")
        print(f"   R² Score:  {best_score['r2']:.4f}")
        print(f"   MAE:       {best_score['mae']:.2f}")
        print(f"   RMSE:      {best_score['rmse']:.2f}")
        print(f"\n⏱️  Total Time: {elapsed_time/3600:.2f} hours ({elapsed_time/60:.1f} minutes)")
        print("\n📊 Top 5 Models:")
        sorted_scores = sorted(all_scores.items(), key=lambda x: x[1]['r2'], reverse=True)
        for i, (name, scores) in enumerate(sorted_scores[:5], 1):
            print(f"   {i}. {name:20s} R²={scores['r2']:.4f}  MAE={scores['mae']:.2f}")
        print("="*80)

    # ====================================================================================
    # RETURN RESULTS
    # ====================================================================================

    return {
        'best_model': best_model,
        'best_model_name': best_model_name,
        'best_score': best_score['r2'],
        'best_mae': best_score['mae'],
        'best_rmse': best_score['rmse'],
        'trained_models': trained_models,
        'ensemble_models': ensemble_models,
        'all_predictions': all_predictions,
        'all_scores': all_scores,
        'results_df': results_df,
        'training_time_hours': elapsed_time / 3600,
        'sample_weights': sample_weights,
        'hyperparameters': {
            'xgboost': xgb_params,
            'lightgbm': lgb_params,
            'catboost': cat_params,
            'random_forest': rf_params
        } if optimize else None
    }
