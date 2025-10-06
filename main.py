#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ML Project Refactored - Main Pipeline Script
By Alex - World-Class AI Expert

This script orchestrates the entire ML pipeline from data loading to model deployment.
Supports both full pipeline execution and individual steps.
"""

import os
import sys
import argparse
import logging
import json
import pickle
import joblib
from datetime import datetime
import warnings
import traceback
from pathlib import Path

# Scientific computing
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Machine Learning
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor

# Advanced ML Libraries
import xgboost as xgb
import lightgbm as lgb
import catboost as cb

# Suppress warnings
warnings.filterwarnings('ignore')

# ====================================================================================
# PROJECT SETUP
# ====================================================================================

# Add project root to Python path
PROJECT_ROOT = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(PROJECT_ROOT))

# Import project modules
try:
    from src.config import CONFIG, MODEL_CONFIG, BASE_PATH, DATA_PATH, MODEL_PATH, RESULTS_PATH
    from src.data_handler import load_and_clean_data
    from src.features import create_all_features
    from src.data_splitter import split_data_stratified
    from src.model_utils import (
        AdvancedPreprocessor, enhanced_feature_selection,
        create_polynomial_features, create_interaction_features
    )
    from src.train import train_all_models, create_ensemble_models, save_models
    from src.evaluate import (
        evaluate_ensemble_predictions, analyze_predictions,
        generate_evaluation_report
    )
    from src.visualize import (
        plot_model_comparison, plot_feature_importance,
        plot_error_distribution, create_dashboard
    )
    from utils.helpers import setup_logging, timer, memory_usage, clean_memory
    from api.prediction import PredictionPipeline
    from api.app import create_app
    
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Make sure all refactored modules are in place")
    traceback.print_exc()
    sys.exit(1)

# ====================================================================================
# PIPELINE FUNCTIONS
# ====================================================================================

def run_data_pipeline(data_path=None):
    """
    Run data loading and cleaning pipeline
    
    Parameters:
    -----------
    data_path : str, optional
        Path to data file
    
    Returns:
    --------
    df_raw, df_cleaned : pd.DataFrame
        Raw and cleaned dataframes
    """
    with timer("Data Pipeline"):
        df_raw, df_cleaned = load_and_clean_data(data_path)
        
        # Save cleaned data
        cleaned_path = os.path.join(DATA_PATH, 'processed', 'cleaned_data.csv')
        df_cleaned.to_csv(cleaned_path, index=False)
        
        return df_raw, df_cleaned

def run_feature_pipeline(df_cleaned, train_indices=None, market_stats=None):
    """
    Run feature engineering pipeline
    
    Parameters:
    -----------
    df_cleaned : pd.DataFrame
        Cleaned dataframe
    train_indices : array-like, optional
        Training indices for calculating statistics
    market_stats : dict, optional
        Pre-calculated market statistics
    """
    with timer("Feature Engineering"):
        # If train_indices provided, calculate stats from training data only
        if train_indices is not None and market_stats is None:
            train_df = df_cleaned.iloc[train_indices]
            
            # Calculate sample weights for training data
            from src.data_handler import calculate_sample_weights, calculate_market_statistics
            train_df = calculate_sample_weights(train_df)
            
            # Calculate market statistics from training data
            market_stats = calculate_market_statistics(train_df)
            
            # Add weights to full dataframe
            df_cleaned = calculate_sample_weights(df_cleaned, is_train=False)
            df_cleaned.iloc[train_indices, df_cleaned.columns.get_loc('sample_weight')] = train_df['sample_weight']
        
        # Create features with market stats
        X, y, sample_weights = create_all_features(df_cleaned, market_stats)
        
        # ... rest of code remains the same
        
        # Save features
        features_path = os.path.join(DATA_PATH, 'features', 'features.pkl')
        os.makedirs(os.path.dirname(features_path), exist_ok=True)
        
        joblib.dump({
            'X': X,
            'y': y,
            'sample_weights': sample_weights,
            'feature_names': list(X.columns)
        }, features_path)
        
        return X, y, sample_weights

def run_preprocessing_pipeline(X_train, X_test, config):
    """
    Run preprocessing pipeline
    
    Parameters:
    -----------
    X_train, X_test : pd.DataFrame
        Train and test features
    config : dict
        Configuration dictionary
    
    Returns:
    --------
    X_train_processed, X_test_processed, preprocessor
    """
    with timer("Preprocessing"):
        # Initialize preprocessor
        preprocessor = AdvancedPreprocessor()
        
        # Fit and transform
        X_train_processed = preprocessor.fit_transform(X_train)
        X_test_processed = preprocessor.transform(X_test)
        
        # Add polynomial features if enabled
        if config.get('use_polynomial_features', False):
            print("\n📊 Creating polynomial features...")
            X_train_processed = create_polynomial_features(
                X_train_processed, 
                degree=config.get('polynomial_degree', 2)
            )
            X_test_processed = create_polynomial_features(
                X_test_processed, 
                degree=config.get('polynomial_degree', 2)
            )
        
        # Add interaction features if enabled
        if config.get('use_feature_interactions', False):
            print("\n📊 Creating interaction features...")
            X_train_processed = create_interaction_features(X_train_processed)
            X_test_processed = create_interaction_features(X_test_processed)
        
        return X_train_processed, X_test_processed, preprocessor

def run_training_pipeline(X_train, y_train, X_test, y_test, sample_weight=None, config=None):
    """
    Run model training pipeline
    
    Parameters:
    -----------
    X_train, y_train : arrays
        Training data
    X_test, y_test : arrays
        Test data
    sample_weight : array, optional
        Sample weights
    config : dict, optional
        Configuration
    
    Returns:
    --------
    trained_models, test_predictions, results_df, best_params
    """
    with timer("Model Training"):
        # Train models
        trained_models, test_predictions, results_df, best_params = train_all_models(
            X_train, y_train, X_test, y_test,
            sample_weight=sample_weight,
            optimize=config.get('optimize', True),
            n_trials=config.get('optuna_trials', 100),
            config=config
        )
        
        return trained_models, test_predictions, results_df, best_params

def run_ensemble_pipeline(trained_models, test_predictions, X_train, y_train, 
                         X_test, y_test, sample_weight=None):
    """
    Run ensemble creation pipeline
    
    Parameters:
    -----------
    trained_models : dict
        Trained models
    test_predictions : dict
        Test predictions
    X_train, y_train : arrays
        Training data
    X_test, y_test : arrays
        Test data
    sample_weight : array, optional
        Sample weights
    
    Returns:
    --------
    ensemble_predictions, ensemble_results
    """
    with timer("Ensemble Creation"):
        ensemble_predictions, ensemble_results = create_ensemble_models(
            trained_models, test_predictions,
            X_train, y_train, X_test, y_test,
            sample_weight=sample_weight
        )
        
        return ensemble_predictions, ensemble_results

def run_evaluation_pipeline(trained_models, test_predictions, ensemble_predictions,
                          X_test, y_test, feature_names):
    """
    Run evaluation pipeline
    
    Parameters:
    -----------
    trained_models : dict
        Trained models
    test_predictions : dict
        Individual model predictions
    ensemble_predictions : dict
        Ensemble predictions
    X_test : array
        Test features
    y_test : array
        Test target
    feature_names : list
        Feature names
    
    Returns:
    --------
    evaluation_report : dict
        Comprehensive evaluation report
    """
    with timer("Model Evaluation"):
        # Generate evaluation report
        evaluation_report = generate_evaluation_report(
            trained_models, test_predictions, ensemble_predictions,
            X_test, y_test, feature_names,
            save_path=RESULTS_PATH
        )
        
        # Additional analysis
        best_predictions = ensemble_predictions.get(
            'Optimized_Weighted',
            list(ensemble_predictions.values())[0]
        )
        
        analysis = analyze_predictions(
            y_test, best_predictions,
            model_name="Best Ensemble"
        )
        
        evaluation_report['prediction_analysis'] = analysis
        
        return evaluation_report

def run_visualization_pipeline(results_df, y_test, predictions, feature_importance_df=None):
    """
    Run visualization pipeline
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        Model results
    y_test : array
        Test target
    predictions : array or dict
        Predictions
    feature_importance_df : pd.DataFrame, optional
        Feature importance
    """
    with timer("Visualization"):
        # Create output directory
        fig_path = os.path.join(RESULTS_PATH, 'figures')
        os.makedirs(fig_path, exist_ok=True)
        
        # 1. Model comparison
        plot_model_comparison(
            results_df,
            save_path=os.path.join(fig_path, 'model_comparison.png')
        )
        
        # 2. Feature importance
        if feature_importance_df is not None:
            plot_feature_importance(
                feature_importance_df,
                save_path=os.path.join(fig_path, 'feature_importance.png')
            )
        
        # 3. Error distribution
        if isinstance(predictions, dict):
            best_predictions = predictions.get(
                'Optimized_Weighted',
                list(predictions.values())[0]
            )
        else:
            best_predictions = predictions
        
        plot_error_distribution(
            y_test, best_predictions,
            save_path=os.path.join(fig_path, 'error_distribution.png')
        )
        
        # 4. Dashboard
        create_dashboard(
            y_test, best_predictions,
            feature_importance_df=feature_importance_df,
            save_path=os.path.join(fig_path, 'dashboard.png')
        )

def deploy_model(trained_models, results_df, feature_names, preprocessor=None):
    """
    Deploy best model
    
    Parameters:
    -----------
    trained_models : dict
        Trained models
    results_df : pd.DataFrame
        Results dataframe
    feature_names : list
        Feature names
    preprocessor : object, optional
        Preprocessor
    
    Returns:
    --------
    deployment_path : str
        Path to deployed model
    """
    with timer("Model Deployment"):
        # Get best model
        best_model_name = results_df.iloc[0]['Model']
        best_model = trained_models[best_model_name]
        
        # Create deployment package
        deployment_data = {
            'model': best_model,
            'model_name': best_model_name,
            'feature_names': feature_names,
            'preprocessor': preprocessor,
            'r2_score': results_df.iloc[0]['R2_test'],
            'timestamp': datetime.now().isoformat(),
            'config': MODEL_CONFIG
        }
        
        # Save to deployed directory
        deployment_path = os.path.join(MODEL_PATH, 'deployed', 'best_model.pkl')
        os.makedirs(os.path.dirname(deployment_path), exist_ok=True)
        
        joblib.dump(deployment_data, deployment_path)
        print(f"\n✅ Model deployed to: {deployment_path}")
        
        return deployment_path

# ====================================================================================
# MAIN PIPELINE
# ====================================================================================

def run_full_pipeline(args):
    """
    Run complete ML pipeline
    """
    print("\n" + "="*100)
    print("🚀 STARTING ML PIPELINE EXECUTION")
    print("="*100)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Configuration: {args}")
    print("="*100)
    
    # Step 1: Load and clean data
    if args.data or args.run_all:
        print("\n" + "="*80)
        print("📂 STEP 1: LOADING AND CLEANING DATA")
        print("="*80)
        
        df_raw, df_cleaned = run_data_pipeline(args.data_path)
        print(f"✅ Data loaded and cleaned: {len(df_cleaned):,} samples")
    else:
        # Load existing cleaned data
        cleaned_path = os.path.join(DATA_PATH, 'processed', 'cleaned_data.csv')
        if not os.path.exists(cleaned_path):
            raise FileNotFoundError(f"Cleaned data not found at {cleaned_path}. Run with --data first.")
        df_cleaned = pd.read_csv(cleaned_path)
        print(f"✅ Loaded existing cleaned data: {len(df_cleaned):,} samples")
    
    # Step 2: Feature engineering
    if args.features or args.run_all:
        print("\n" + "="*80)
        print("🔧 STEP 2: FEATURE ENGINEERING")
        print("="*80)
        
        # 🔴 Create train indices FIRST (before feature engineering)
        from sklearn.model_selection import train_test_split
        train_indices, test_indices = train_test_split(
            np.arange(len(df_cleaned)),
            test_size=MODEL_CONFIG.get('test_size', 0.2),
            stratify=pd.qcut(df_cleaned['price'], q=5, labels=False),
            random_state=MODEL_CONFIG.get('random_state', 42)
        )
        
        # 🔴 Pass train indices to feature pipeline
        X, y, sample_weights = run_feature_pipeline(df_cleaned, train_indices=train_indices)
        print(f"✅ Features created: {X.shape[1]} features")
        
        # 🔴 Store indices for later use
        np.save(os.path.join(DATA_PATH, 'features', 'train_indices.npy'), train_indices)
        np.save(os.path.join(DATA_PATH, 'features', 'test_indices.npy'), test_indices)
    else:
        # Load existing features
        features_path = os.path.join(DATA_PATH, 'features', 'features.pkl')
        if not os.path.exists(features_path):
            raise FileNotFoundError(f"Features not found at {features_path}. Run with --features first.")
        
        features_data = joblib.load(features_path)
        X = features_data['X']
        y = features_data['y']
        sample_weights = features_data['sample_weights']
        print(f"✅ Loaded existing features: {X.shape[1]} features")
        
        # Load indices if available
        try:
            train_indices = np.load(os.path.join(DATA_PATH, 'features', 'train_indices.npy'))
            test_indices = np.load(os.path.join(DATA_PATH, 'features', 'test_indices.npy'))
        except:
            train_indices, test_indices = None, None
    
    # Step 3: Train/test split
    if args.split or args.run_all:
        print("\n" + "="*80)
        print("📊 STEP 3: TRAIN/TEST SPLIT")
        print("="*80)
        
        # 🔴 Use pre-computed indices if available
        if train_indices is not None and test_indices is not None:
            X_train = X.iloc[train_indices]
            X_test = X.iloc[test_indices]
            y_train = y.iloc[train_indices]
            y_test = y.iloc[test_indices]
            sw_train = sample_weights.iloc[train_indices]
            sw_test = sample_weights.iloc[test_indices]
            print("✅ Using pre-computed train/test indices (no data leakage)")
        else:
            # Fallback to regular split
            X_train, X_test, y_train, y_test, sw_train, sw_test = split_data_stratified(
                X, y, sample_weights,
                test_size=MODEL_CONFIG.get('test_size', 0.2),
                random_state=MODEL_CONFIG.get('random_state', 42)
            )
    
    # ... rest of the code remains the same
    
    # Step 4: Preprocessing and feature selection
    if args.train or args.run_all:
        print("\n" + "="*80)
        print("🔧 STEP 4: PREPROCESSING AND FEATURE SELECTION")
        print("="*80)
        
        # Preprocessing
        X_train_processed, X_test_processed, preprocessor = run_preprocessing_pipeline(
            X_train, X_test, MODEL_CONFIG
        )
        
        # Feature selection
        if args.feature_selection:
            print("\n🎯 Performing feature selection...")
            X_train_selected, X_test_selected, selected_features, feature_selector = enhanced_feature_selection(
                X_train_processed, y_train, X_test_processed,
                n_features=MODEL_CONFIG.get('max_features', 150),
                sample_weight=sw_train
            )
            feature_names = selected_features
        else:
            X_train_selected = X_train_processed
            X_test_selected = X_test_processed
            feature_names = list(X_train_processed.columns)
            feature_selector = None
        
        print(f"✅ Final feature count: {len(feature_names)}")
    
    # Step 5: Model training
    if args.train or args.run_all:
        print("\n" + "="*80)
        print("🎯 STEP 5: MODEL TRAINING")
        print("="*80)
        
        # Train models
        trained_models, test_predictions, results_df, best_params = run_training_pipeline(
            X_train_selected, y_train, X_test_selected, y_test,
            sample_weight=sw_train,
            config={**MODEL_CONFIG, 'optimize': args.optimize}
        )
        
        # Save models
        save_models(
            trained_models, best_params, feature_names,
            save_path=MODEL_PATH,
            results_df=results_df
        )
    
    # Step 6: Ensemble creation
    if args.ensemble or args.run_all:
        print("\n" + "="*80)
        print("🏆 STEP 6: ENSEMBLE CREATION")
        print("="*80)
        
        ensemble_predictions, ensemble_results = run_ensemble_pipeline(
            trained_models, test_predictions,
            X_train_selected, y_train, X_test_selected, y_test,
            sample_weight=sw_train
        )
    
    # Step 7: Evaluation
    if args.evaluate or args.run_all:
        print("\n" + "="*80)
        print("📊 STEP 7: MODEL EVALUATION")
        print("="*80)
        
        # Feature importance analysis
        from src.evaluate import analyze_feature_importance
        feature_importance_df = analyze_feature_importance(
            trained_models, feature_names, top_n=30
        )
        
        # Generate evaluation report
        evaluation_report = run_evaluation_pipeline(
            trained_models, test_predictions, ensemble_predictions,
            X_test_selected, y_test, feature_names
        )
    
    # Step 8: Visualization
    if args.visualize or args.run_all:
        print("\n" + "="*80)
        print("📈 STEP 8: VISUALIZATION")
        print("="*80)
        
        run_visualization_pipeline(
            results_df, y_test, ensemble_predictions,
            feature_importance_df
        )
    
    # Step 9: Model deployment
    if args.deploy or args.run_all:
        print("\n" + "="*80)
        print("🚀 STEP 9: MODEL DEPLOYMENT")
        print("="*80)
        
        deployment_path = deploy_model(
            trained_models, results_df, feature_names, preprocessor
        )
        
        # Start API if requested
        if args.api_type:
            print(f"\n🌐 Starting {args.api_type.upper()} API server...")
            
            app = create_app(framework=args.api_type)
            
            if args.api_type == "fastapi":
                import uvicorn
                uvicorn.run(app, host="0.0.0.0", port=args.port)
            else:
                app.run(host="0.0.0.0", port=args.port, debug=False)
    
    # Final summary
    print("\n" + "="*100)
    print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*100)
    
    if 'evaluation_report' in locals():
        best_model = evaluation_report['best_model']
        print(f"\n🏆 Best Model: {best_model['name']}")
        print(f"   R² Score: {best_model['r2']:.6f}")
        print(f"   MAE: {best_model['mae']:.4f}")
        print(f"   RMSE: {best_model['rmse']:.4f}")
    
    print(f"\n📊 Results saved to: {RESULTS_PATH}")
    print(f"📦 Models saved to: {MODEL_PATH}")
    
    # Memory cleanup
    clean_memory()

# ====================================================================================
# MAIN FUNCTION
# ====================================================================================

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="ML Pipeline for Phone Number Price Prediction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full pipeline with optimization
  python main.py --run-all --optimize
  
  # Run specific steps
  python main.py --data --features --split
  python main.py --train --optimize --ensemble
  
  # Deploy model and start API
  python main.py --deploy --api-type fastapi --port 8000
  
  # Use custom data file
  python main.py --data --data-path /path/to/data.csv
        """
    )
    
    # Pipeline steps
    parser.add_argument("--run-all", action="store_true", help="Run entire pipeline")
    parser.add_argument("--data", action="store_true", help="Load and clean data")
    parser.add_argument("--features", action="store_true", help="Create features")
    parser.add_argument("--split", action="store_true", help="Split data")
    parser.add_argument("--train", action="store_true", help="Train models")
    parser.add_argument("--ensemble", action="store_true", help="Create ensembles")
    parser.add_argument("--evaluate", action="store_true", help="Evaluate models")
    parser.add_argument("--visualize", action="store_true", help="Create visualizations")
    parser.add_argument("--deploy", action="store_true", help="Deploy best model")
    
    # Options
    parser.add_argument("--optimize", action="store_true", help="Optimize hyperparameters")
    parser.add_argument("--feature-selection", action="store_true", help="Perform feature selection")
    parser.add_argument("--n-trials", type=int, default=100, help="Number of optimization trials")
    
    # Data options
    parser.add_argument("--data-path", type=str, help="Path to data file")
    
    # Model options
    parser.add_argument("--models", nargs="+", help="Specific models to train")
    
    # API options
    parser.add_argument("--api-type", choices=["fastapi", "flask"], help="API framework")
    parser.add_argument("--port", type=int, default=8000, help="API port")
    
    # Logging
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    
    args = parser.parse_args()
    
    # Setup logging
    log_file = os.path.join(PROJECT_ROOT, 'logs', f'pipeline_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logger = setup_logging(log_level=args.log_level, log_file=log_file)
    
    # Run pipeline
    try:
        run_full_pipeline(args)
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
