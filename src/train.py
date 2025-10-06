"""
Training Pipeline for Phone Number Price Prediction
By Alex - World-Class AI Expert

Complete training pipeline with all functions
"""
import os
import sys
import numpy as np
import pandas as pd
import joblib
import json
from datetime import datetime
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from src.config import MODEL_CONFIG
from sklearn.ensemble import (
    RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor,
    HistGradientBoostingRegressor, VotingRegressor
)
from sklearn.linear_model import Ridge, Lasso, ElasticNet, BayesianRidge, HuberRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
import warnings
warnings.filterwarnings('ignore')

# ====================================================================================
# TRAIN INDIVIDUAL MODELS
# ====================================================================================

def train_individual_models(base_models, X_train, X_test, y_train, y_test, 
                           sample_weight=None, verbose=True):
    """
    Train individual models and evaluate performance
    
    Parameters:
    -----------
    base_models : list of tuples
        List of (name, model) tuples
    X_train, X_test : pd.DataFrame
        Training and test features
    y_train, y_test : pd.Series
        Training and test targets
    sample_weight : array-like, optional
        Sample weights for training
    verbose : bool
        Print training progress
    
    Returns:
    --------
    trained_models : dict
        Dictionary of trained models
    test_predictions : dict
        Test predictions for each model
    results_df : pd.DataFrame
        Results summary
    """
    if verbose:
        print("\n" + "="*80)
        print("🎯 TRAINING INDIVIDUAL MODELS")
        print("="*80)
    
    trained_models = {}
    test_predictions = {}
    results = []
    
    for name, model in base_models:
        if verbose:
            print(f"\n📊 Training {name}...")
        
        try:
            # Clone model to avoid issues
            from sklearn.base import clone
            model_clone = clone(model)
            
            # Train with sample weights if supported
            if sample_weight is not None:
                try:
                    # Check if model supports sample_weight
                    fit_params = model_clone.fit.__code__.co_varnames
                    if 'sample_weight' in fit_params:
                        model_clone.fit(X_train, y_train, sample_weight=sample_weight)
                    else:
                        model_clone.fit(X_train, y_train)
                except:
                    model_clone.fit(X_train, y_train)
            else:
                model_clone.fit(X_train, y_train)
            
            # Make predictions
            y_pred_train = model_clone.predict(X_train)
            y_pred_test = model_clone.predict(X_test)
            
            # Calculate metrics
            train_r2 = r2_score(y_train, y_pred_train)
            test_r2 = r2_score(y_test, y_pred_test)
            test_mae = mean_absolute_error(y_test, y_pred_test)
            test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
            
            # Store results
            trained_models[name] = model_clone
            test_predictions[name] = y_pred_test
            
            result = {
                'Model': name,
                'R2_train': train_r2,
                'R2_test': test_r2,
                'MAE_test': test_mae,
                'RMSE_test': test_rmse,
                'Overfit': train_r2 - test_r2
            }
            results.append(result)
            
            if verbose:
                print(f"   ✅ R² Train: {train_r2:.6f}")
                print(f"   ✅ R² Test:  {test_r2:.6f}")
                print(f"   📊 MAE:      {test_mae:.4f}")
                print(f"   📊 RMSE:     {test_rmse:.4f}")
            
        except Exception as e:
            print(f"   ❌ Error training {name}: {str(e)}")
            continue
    
    # Create results dataframe
    results_df = pd.DataFrame(results).sort_values('R2_test', ascending=False)
    
    if verbose:
        print("\n" + "="*80)
        print("📊 MODEL COMPARISON")
        print("="*80)
        print(results_df.to_string(index=False))
    
    return trained_models, test_predictions, results_df

# ====================================================================================
# TRAIN ALL MODELS WITH OPTIMIZATION
# ====================================================================================

def train_all_models(X_train, X_test, y_train, y_test, sample_weight=None, 
                    optimize=True, n_trials=100):
    """
    Train all models with hyperparameter optimization
    
    Parameters:
    -----------
    X_train, X_test : pd.DataFrame
        Training and test features
    y_train, y_test : pd.Series
        Training and test targets
    sample_weight : array-like, optional
        Sample weights for training
    optimize : bool
        Whether to perform hyperparameter optimization
    n_trials : int
        Number of optimization trials
    
    Returns:
    --------
    trained_models : dict
        Dictionary of trained models
    test_predictions : dict
        Test predictions for each model
    results_df : pd.DataFrame
        Results summary
    """
    print("\n" + "="*80)
    print("🚀 TRAINING ALL MODELS WITH OPTIMIZATION")
    print("="*80)
    
    # 1. Hyperparameter optimization
    best_params = {}
    
    if optimize:
        print("\n🔧 Optimizing hyperparameters...")
        
        # Import optimization functions
        try:
            from src.model_utils import (
                optimize_xgboost, optimize_lightgbm, 
                optimize_catboost, optimize_random_forest
            )
        except ImportError:
            # If import fails, use default parameters
            print("⚠️ Could not import optimization functions. Using default parameters.")
            optimize = False
    
    if optimize:
        best_params = {
            'xgb': optimize_xgboost(X_train, y_train, n_trials),
            'lgb': optimize_lightgbm(X_train, y_train, n_trials),
            'cat': optimize_catboost(X_train, y_train, n_trials//2),
            'rf': optimize_random_forest(X_train, y_train, n_trials//2)
        }
        print("✅ Optimization completed!")
    else:
        # Default parameters
        best_params = {
            'xgb': {
                'n_estimators': 1000,
                'max_depth': 10,
                'learning_rate': 0.05,
                'subsample': 0.8,
                'colsample_bytree': 0.8,
                'random_state': 42
            },
            'lgb': {
                'n_estimators': 1000,
                'max_depth': 10,
                'learning_rate': 0.05,
                'num_leaves': 100,
                'subsample': 0.8,
                'colsample_bytree': 0.8,
                'random_state': 42,
                'verbosity': -1
            },
            'cat': {
                'iterations': 1000,
                'depth': 10,
                'learning_rate': 0.05,
                'random_state': 42,
                'verbose': False
            },
            'rf': {
                'n_estimators': 500,
                'max_depth': 20,
                'min_samples_split': 5,
                'min_samples_leaf': 2,
                'random_state': 42,
                'n_jobs': -1
            }
        }
    
    # 2. Create base models with optimized parameters
    base_models = [
        ('XGBoost_Opt', XGBRegressor(**best_params['xgb'])),
        ('LightGBM_Opt', LGBMRegressor(**best_params['lgb'])),
        ('CatBoost_Opt', CatBoostRegressor(**best_params['cat'])),
        ('RandomForest_Opt', RandomForestRegressor(**best_params['rf'])),
        ('ExtraTrees_Opt', ExtraTreesRegressor(
            n_estimators=1000,
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            max_features='sqrt',
            bootstrap=False,
            random_state=42,
            n_jobs=-1
        )),
        ('GradientBoosting', GradientBoostingRegressor(
            n_estimators=1000,
            max_depth=5,
            learning_rate=0.05,
            subsample=0.8,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42
        )),
        ('HistGradientBoosting', HistGradientBoostingRegressor(
            max_iter=1000,
            max_depth=10,
            learning_rate=0.05,
            min_samples_leaf=20,
            l2_regularization=0.1,
            random_state=42
        )),
        ('Ridge', Ridge(alpha=1.0, random_state=42)),
        ('BayesianRidge', BayesianRidge()),
        ('HuberRegressor', HuberRegressor(max_iter=1000))
    ]
    
    # 3. Train individual models
    trained_models, test_predictions, results_df = train_individual_models(
        base_models, X_train, X_test, y_train, y_test, sample_weight
    )
    
    return trained_models, test_predictions, results_df

# ====================================================================================
# CREATE ENSEMBLE MODELS
# ====================================================================================

def create_ensemble_models(trained_models, X_train, y_train, X_test, y_test, 
                          test_predictions, sample_weight=None, n_top_models=5):
                          #                                    ^^^^^^^^^^^^^^^ เพิ่มตรงนี้
    """
    Create various ensemble models
    
    Parameters:
    -----------
    trained_models : dict
        Dictionary of trained models
    X_train, X_test : pd.DataFrame
        Training and test features
    y_train, y_test : pd.Series
        Training and test targets
    test_predictions : dict
        Test predictions from individual models
    sample_weight : array-like, optional
        Sample weights
    
    Returns:
    --------
    ensemble_models : dict
        Dictionary of ensemble models
    ensemble_predictions : dict
        Ensemble predictions
    """
    print("\n" + "="*80)
    print("🏗️ CREATING ENSEMBLE MODELS")
    print("="*80)
    
    ensemble_models = {}
    ensemble_predictions = {}
    
    # Get top 5 models based on test predictions
    model_scores = []
    for name, pred in test_predictions.items():
        score = r2_score(y_test, pred)
        model_scores.append((name, score))
    
    model_scores.sort(key=lambda x: x[1], reverse=True)
    top_models = [name for name, _ in model_scores[:n_top_models]]  # แก้ใหม่
    
    # 1. Simple Average Ensemble
    print("\n📊 Creating Simple Average Ensemble...")
    predictions_array = np.column_stack([test_predictions[name] for name in top_models])
    ensemble_predictions['Simple_Average'] = np.mean(predictions_array, axis=1)
    
    # 2. Weighted Average Ensemble (weighted by R² scores)
    print("\n📊 Creating Weighted Average Ensemble...")
    weights = np.array([score for _, score in model_scores[:5]])
    weights = weights / weights.sum()
    ensemble_predictions['Weighted_Average'] = np.average(predictions_array, axis=1, weights=weights)
    
    # 3. Voting Ensemble
    print("\n📊 Creating Voting Ensemble...")
    voting_models = [(name, trained_models[name]) for name in top_models]
    voting_ensemble = VotingRegressor(voting_models, n_jobs=1)  # Prevent GPU conflict (was: -1)
    
    if sample_weight is not None:
        voting_ensemble.fit(X_train, y_train, sample_weight=sample_weight)
    else:
        voting_ensemble.fit(X_train, y_train)
    
    ensemble_models['Voting_Ensemble'] = voting_ensemble
    ensemble_predictions['Voting_Ensemble'] = voting_ensemble.predict(X_test)
    
    # 4. Stacking Ensemble (if available)
    try:
        from src.model_utils import AdvancedStackingEnsemble
        
        print("\n📊 Creating Stacking Ensemble...")
        stacking_ensemble = AdvancedStackingEnsemble(
            base_models=voting_models[:5],
            cv_folds=5
        )
        stacking_ensemble.fit(X_train, y_train, sample_weight)
        ensemble_models['Stacking_Ensemble'] = stacking_ensemble
        ensemble_predictions['Stacking_Ensemble'] = stacking_ensemble.predict(X_test)
        
    except ImportError:
        print("   ⚠️ AdvancedStackingEnsemble not available. Skipping...")

    # 4.5 Tier-Specific Model (เพิ่มใหม่)
    if MODEL_CONFIG.get('use_tier_models', False):
        print("\n📊 Creating Tier-Specific Model...")
        
        # Import tier model
        try:
            from src.tier_specific_models import TierSpecificPricePredictor
            
            # Calculate progressive weights
            y_prices = np.expm1(y_train)  # Convert log to actual prices
            
            # Progressive weights based on price
            progressive_weights = np.ones(len(y_prices))
            thresholds = MODEL_CONFIG['tier_config']['progressive_weights']['thresholds']
            weight_values = MODEL_CONFIG['tier_config']['progressive_weights']['weights']
            
            for i, price in enumerate(y_prices):
                for j, threshold in enumerate(thresholds):
                    if price <= threshold:
                        progressive_weights[i] = weight_values[j]
                        break
                else:
                    progressive_weights[i] = weight_values[-1]
            
            # Combine with existing sample weight
            if sample_weight is not None:
                enhanced_weight = progressive_weights * sample_weight
            else:
                enhanced_weight = progressive_weights
            
            # Normalize weights
            enhanced_weight = enhanced_weight / enhanced_weight.mean()
            
            # Create and train tier model
            tier_predictor = TierSpecificPricePredictor(
                use_dynamic_boundaries=MODEL_CONFIG['tier_config']['use_dynamic_boundaries'],
                use_soft_voting=MODEL_CONFIG['tier_config']['use_soft_voting']
            )
            
            # Train with enhanced weights
            tier_predictor.train_tier_models(
                X_train, y_train, y_prices, sample_weight=enhanced_weight
            )
            
            # Store model and predictions
            ensemble_models['Tier_Specific'] = tier_predictor
            ensemble_predictions['Tier_Specific'] = tier_predictor.predict(X_test)
            
            # Evaluate
            tier_r2 = r2_score(y_test, ensemble_predictions['Tier_Specific'])
            print(f"   Tier-Specific R² = {tier_r2:.6f}")
            
        except ImportError:
            print("   ⚠️ TierSpecificPricePredictor not available. Skipping...")
        except Exception as e:
            print(f"   ⚠️ Error creating tier model: {str(e)}")
    
    # 5. Super Ensemble (combination of all ensemble methods)
    print("\n📊 Creating Super Ensemble...")
    ensemble_array = np.column_stack(list(ensemble_predictions.values()))
    ensemble_predictions['Super_Ensemble'] = np.mean(ensemble_array, axis=1)
    
    # Calculate and display ensemble results
    print("\n📊 Ensemble Results:")
    for name, pred in ensemble_predictions.items():
        r2 = r2_score(y_test, pred)
        mae = mean_absolute_error(y_test, pred)
        print(f"   {name}: R² = {r2:.6f}, MAE = {mae:.4f}")
    
    print("\n✅ All ensemble models created successfully!")
    
    return ensemble_models, ensemble_predictions

    # เพิ่มใน create_ensemble_models() หลังจาก ensemble อื่นๆ
    if MODEL_CONFIG.get('use_tier_models', False):
        # Import จาก tier_specific_models.py
        from src.tier_specific_models import TierSpecificPricePredictor
        
        # สร้าง tier predictor
        tier_predictor = TierSpecificPricePredictor()
        
        # Train
        tier_predictor.train_tier_models(
            X_train, y_train, np.expm1(y_train)
        )
        
        # เพิ่มเข้า ensemble
        ensemble_models['Tier_Specific'] = tier_predictor
        ensemble_predictions['Tier_Specific'] = tier_predictor.predict(X_test)

# ====================================================================================
# SAVE MODELS AND RESULTS
# ====================================================================================

def save_models(models, results, feature_names, preprocessor=None, save_dir='models/'):
    """
    Save trained models and metadata
    
    Parameters:
    -----------
    models : dict
        Dictionary of trained models
    results : pd.DataFrame
        Results summary
    feature_names : list
        List of feature names
    preprocessor : object, optional
        Preprocessor object
    save_dir : str
        Directory to save models
    
    Returns:
    --------
    saved_paths : dict
        Paths to saved models
    """
    print("\n" + "="*80)
    print("💾 SAVING MODELS AND RESULTS")
    print("="*80)
    
    # Create save directory
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(os.path.join(save_dir, 'individual'), exist_ok=True)
    os.makedirs(os.path.join(save_dir, 'ensemble'), exist_ok=True)
    
    saved_paths = {}
    
    # Separate individual and ensemble models
    individual_models = {k: v for k, v in models.items() if 'Ensemble' not in k}
    ensemble_models = {k: v for k, v in models.items() if 'Ensemble' in k}
    
    # 1. Save individual models
    for model_name, model in individual_models.items():
        try:
            # Get model metrics
            model_results = results[results['Model'] == model_name]
            if len(model_results) == 0:
                r2_score_val = 0.0
            else:
                r2_score_val = float(model_results.iloc[0].get('R2_test', 0))
            
            model_data = {
                'model': model,
                'model_name': model_name,
                'feature_names': feature_names,
                'r2_score': r2_score_val,
                'timestamp': datetime.now().isoformat()
            }
            
            filename = f"{model_name.lower().replace(' ', '_')}.pkl"
            filepath = os.path.join(save_dir, 'individual', filename)
            
            joblib.dump(model_data, filepath)
            saved_paths[model_name] = filepath
            print(f"   ✅ Saved {model_name} to {filepath}")
            
        except Exception as e:
            print(f"   ❌ Error saving {model_name}: {str(e)}")
    
    # 2. Save ensemble models
    for model_name, model in ensemble_models.items():
        try:
            model_data = {
                'model': model,
                'model_name': model_name,
                'feature_names': feature_names,
                'timestamp': datetime.now().isoformat()
            }
            
            filename = f"{model_name.lower().replace(' ', '_')}.pkl"
            filepath = os.path.join(save_dir, 'ensemble', filename)
            
            joblib.dump(model_data, filepath)
            saved_paths[model_name] = filepath
            print(f"   ✅ Saved {model_name} to {filepath}")
            
        except Exception as e:
            print(f"   ❌ Error saving {model_name}: {str(e)}")
    
    # 3. Save best model
    if len(results) > 0:
        # Find best model
        if 'r2' in results.columns:
            best_idx = results['r2'].idxmax()
        elif 'R2_test' in results.columns:
            best_idx = results['R2_test'].idxmax()
        else:
            best_idx = 0
            
        best_model_name = results.iloc[best_idx]['Model']
        
        # Check if it's in individual or ensemble models
        if best_model_name in models:
            best_model = models[best_model_name]
            
            best_model_data = {
                'model': best_model,
                'model_name': best_model_name,
                'feature_names': feature_names,
                'preprocessor': preprocessor,
                'r2_score': float(results.iloc[best_idx].get('R2_test', results.iloc[best_idx].get('r2', 0))),
                'results_summary': results.to_dict(),
                'timestamp': datetime.now().isoformat()
            }
            
            best_path = os.path.join(save_dir, 'best_model.pkl')
            joblib.dump(best_model_data, best_path)
            saved_paths['best_model'] = best_path
            print(f"\n   🏆 Saved best model ({best_model_name}) to {best_path}")
    
    # 4. Save metadata
    metadata = {
        'training_date': datetime.now().isoformat(),
        'n_features': len(feature_names) if feature_names else 0,
        'feature_names': feature_names if feature_names else [],
        'models_trained': list(models.keys()),
        'best_model': best_model_name if 'best_model_name' in locals() else 'Unknown',
        'best_r2': float(results.iloc[0].get('R2_test', results.iloc[0].get('r2', 0))) if len(results) > 0 else 0,
        'all_results': results.to_dict('records') if len(results) > 0 else []
    }
    
    metadata_path = os.path.join(save_dir, 'training_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n   📋 Saved metadata to {metadata_path}")
    
    # 5. Save results CSV
    results_path = os.path.join(save_dir, 'model_results.csv')
    results.to_csv(results_path, index=False)
    print(f"   📊 Saved results to {results_path}")
    
    print(f"\n✅ All models saved successfully!")
    
    return saved_paths

# ====================================================================================
# MAIN TRAINING PIPELINE
# ====================================================================================

def run_training_pipeline(X_train, X_test, y_train, y_test, sample_weight=None,
                         feature_names=None, preprocessor=None, 
                         optimize=True, save_models_flag=True):
    """
    Run complete training pipeline
    
    This is the main function that orchestrates the entire training process
    
    Parameters:
    -----------
    X_train, X_test : pd.DataFrame
        Training and test features
    y_train, y_test : pd.Series
        Training and test targets (log-transformed)
    sample_weight : array-like, optional
        Sample weights for training
    feature_names : list, optional
        List of feature names
    preprocessor : object, optional
        Preprocessor object for feature transformation
    optimize : bool
        Whether to perform hyperparameter optimization
    save_models_flag : bool
        Whether to save trained models
    
    Returns:
    --------
    dict : Dictionary containing:
        - models: All trained models
        - predictions: All predictions
        - results: Evaluation results
        - saved_paths: Paths to saved models
    """
    print("\n" + "="*100)
    print("🎯 RUNNING COMPLETE TRAINING PIPELINE")
    print("="*100)
    
    # Get feature names if not provided
    if feature_names is None:
        feature_names = list(X_train.columns)
    
    # 1. Train all models
    trained_models, test_predictions, results_df = train_all_models(
        X_train, X_test, y_train, y_test, 
        sample_weight=sample_weight, 
        optimize=optimize
    )
    
    # 2. Create ensemble models
    ensemble_models, ensemble_predictions = create_ensemble_models(
        trained_models, X_train, y_train, X_test, y_test,
        test_predictions, sample_weight
    )
    
    # 3. Combine all models and predictions
    all_models = {**trained_models, **ensemble_models}
    all_predictions = {**test_predictions, **ensemble_predictions}
    
    # 4. Evaluate ensemble models and create combined results
    ensemble_results = []
    for name, pred in ensemble_predictions.items():
        r2 = r2_score(y_test, pred)
        mae = mean_absolute_error(y_test, pred)
        rmse = np.sqrt(mean_squared_error(y_test, pred))
        
        ensemble_results.append({
            'Model': name,
            'R2_test': r2,
            'MAE_test': mae,
            'RMSE_test': rmse,
            'R2_train': np.nan,  # Not calculated for ensembles
            'Overfit': 0
        })
    
    # Combine all results
    ensemble_df = pd.DataFrame(ensemble_results)
    all_results = pd.concat([results_df, ensemble_df], ignore_index=True)
    all_results = all_results.sort_values('R2_test', ascending=False).reset_index(drop=True)
    
    # 5. Save models if requested
    saved_paths = {}
    if save_models_flag:
        saved_paths = save_models(
            all_models, all_results, feature_names, 
            preprocessor, save_dir='models/deployed/'
        )
    
    # 6. Print final summary
    print("\n" + "="*100)
    print("📊 TRAINING PIPELINE COMPLETED!")
    print("="*100)
    print(f"\n🏆 Best Model: {all_results.iloc[0]['Model']}")
    print(f"   R² Score: {all_results.iloc[0]['R2_test']:.6f}")
    print(f"   MAE: {all_results.iloc[0]['MAE_test']:.4f}")
    print(f"   RMSE: {all_results.iloc[0]['RMSE_test']:.4f}")
    
    # Print top 5 models
    print("\n📊 Top 5 Models:")
    print(all_results[['Model', 'R2_test', 'MAE_test']].head().to_string(index=False))
    
    # Target achievement check
    target_r2 = 0.90
    if all_results.iloc[0]['R2_test'] >= target_r2:
        print(f"\n✅ TARGET ACHIEVED! R² = {all_results.iloc[0]['R2_test']:.6f} ≥ {target_r2}")
    else:
        gap = target_r2 - all_results.iloc[0]['R2_test']
        print(f"\n❌ Target not reached. Gap = {gap:.6f}")
    
    return {
        'models': all_models,
        'predictions': all_predictions,
        'results': all_results,
        'saved_paths': saved_paths,
        'best_model': all_models[all_results.iloc[0]['Model']],
        'best_model_name': all_results.iloc[0]['Model'],
        'best_r2': all_results.iloc[0]['R2_test']
    }

# ====================================================================================
# UTILITY FUNCTIONS
# ====================================================================================

def load_training_results(model_dir='models/deployed/'):
    """Load saved training results and metadata"""
    metadata_path = os.path.join(model_dir, 'training_metadata.json')
    
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        print("📋 Training Metadata:")
        print(f"   Training Date: {metadata['training_date']}")
        print(f"   Best Model: {metadata['best_model']}")
        print(f"   Best R²: {metadata['best_r2']:.6f}")
        print(f"   Total Models: {len(metadata['models_trained'])}")
        
        return metadata
    else:
        print("❌ No training metadata found")
        return None

def quick_train(X_train, X_test, y_train, y_test, sample_weight=None):
    """Quick training without optimization for testing"""
    return run_training_pipeline(
        X_train, X_test, y_train, y_test,
        sample_weight=sample_weight,
        optimize=False,
        save_models_flag=False
    )

# ====================================================================================
# MAIN ENTRY POINT
# ====================================================================================

if __name__ == "__main__":
    print("🚀 Training Pipeline Module")
    print("   Use run_training_pipeline() to train all models")
    print("   Use quick_train() for quick testing without optimization")
