"""
Model Evaluation Functions for ML Project
By Alex - World-Class AI Expert
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.metrics import explained_variance_score, max_error
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ====================================================================================
# EVALUATION METRICS
# ====================================================================================

def calculate_metrics(y_true, y_pred, prefix=""):
    """
    Calculate comprehensive evaluation metrics
    
    Parameters:
    -----------
    y_true : array
        True values
    y_pred : array
        Predicted values
    prefix : str
        Prefix for metric names
    
    Returns:
    --------
    metrics : dict
        Dictionary of metrics
    """
    # Basic metrics
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mse = mean_squared_error(y_true, y_pred)
    
    # Additional metrics
    explained_var = explained_variance_score(y_true, y_pred)
    max_err = max_error(y_true, y_pred)
    
    # Custom metrics
    mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100
    
    # Percentage within threshold
    errors = np.abs(y_true - y_pred)
    within_10_pct = np.mean(errors <= 0.1 * np.abs(y_true)) * 100
    within_20_pct = np.mean(errors <= 0.2 * np.abs(y_true)) * 100
    
    # Create metrics dictionary
    metrics = {
        f'{prefix}r2': r2,
        f'{prefix}mae': mae,
        f'{prefix}rmse': rmse,
        f'{prefix}mse': mse,
        f'{prefix}explained_variance': explained_var,
        f'{prefix}max_error': max_err,
        f'{prefix}mape': mape,
        f'{prefix}within_10_pct': within_10_pct,
        f'{prefix}within_20_pct': within_20_pct
    }
    
    return metrics

# ====================================================================================
# MODEL EVALUATION
# ====================================================================================

def evaluate_model_performance(model, X_train, y_train, X_test, y_test, 
                              model_name="Model", verbose=True):
    """
    Comprehensive model evaluation
    
    Parameters:
    -----------
    model : sklearn model
        Trained model
    X_train, y_train : arrays
        Training data
    X_test, y_test : arrays
        Test data
    model_name : str
        Model name
    verbose : bool
        Print results
    
    Returns:
    --------
    evaluation : dict
        Evaluation results
    """
    # Make predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Calculate metrics
    train_metrics = calculate_metrics(y_train, y_train_pred, prefix="train_")
    test_metrics = calculate_metrics(y_test, y_test_pred, prefix="test_")
    
    # Combine metrics
    evaluation = {
        'model_name': model_name,
        **train_metrics,
        **test_metrics,
        'overfit_score': train_metrics['train_r2'] - test_metrics['test_r2']
    }
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"📊 {model_name} Evaluation")
        print(f"{'='*60}")
        print(f"Training R²:   {train_metrics['train_r2']:.6f}")
        print(f"Test R²:       {test_metrics['test_r2']:.6f}")
        print(f"Overfit Score: {evaluation['overfit_score']:.6f}")
        print(f"Test MAE:      {test_metrics['test_mae']:.4f}")
        print(f"Test RMSE:     {test_metrics['test_rmse']:.4f}")
        print(f"Test MAPE:     {test_metrics['test_mape']:.2f}%")
        print(f"Within 10%:    {test_metrics['test_within_10_pct']:.1f}%")
        print(f"Within 20%:    {test_metrics['test_within_20_pct']:.1f}%")
    
    return evaluation

# ====================================================================================
# ENSEMBLE EVALUATION
# ====================================================================================

def evaluate_ensemble_predictions(ensemble_predictions, y_test, y_test_original=None):
    """
    Evaluate all ensemble predictions
    
    Parameters:
    -----------
    ensemble_predictions : dict
        Dictionary of ensemble predictions
    y_test : array
        Test target (log-transformed)
    y_test_original : array, optional
        Original test target (not log-transformed)
    
    Returns:
    --------
    results : pd.DataFrame
        Evaluation results
    """
    results = []
    
    for name, predictions in ensemble_predictions.items():
        # Calculate metrics on log scale
        metrics = calculate_metrics(y_test, predictions)
        
        # If original scale provided, calculate metrics there too
        if y_test_original is not None:
            pred_original = np.expm1(predictions)
            metrics_original = calculate_metrics(
                y_test_original, 
                pred_original, 
                prefix="original_"
            )
            metrics.update(metrics_original)
        
        # Add to results
        result = {'Method': name, **metrics}
        results.append(result)
    
    # Create dataframe and sort by R²
    results_df = pd.DataFrame(results).sort_values('r2', ascending=False)
    
    return results_df

# ====================================================================================
# PREDICTION ANALYSIS
# ====================================================================================

def analyze_predictions(y_true, y_pred, model_name="Model", 
                       save_plots=False, plot_path=None):
    """
    Detailed analysis of predictions
    
    Parameters:
    -----------
    y_true : array
        True values
    y_pred : array
        Predicted values
    model_name : str
        Model name
    save_plots : bool
        Whether to save plots
    plot_path : str
        Path to save plots
    
    Returns:
    --------
    analysis : dict
        Analysis results
    """
    # Calculate residuals
    residuals = y_true - y_pred
    abs_residuals = np.abs(residuals)
    pct_errors = (abs_residuals / (np.abs(y_true) + 1e-8)) * 100
    
    # Statistical tests
    # 1. Normality test for residuals
    _, normality_p = stats.normaltest(residuals)
    
    # 2. Homoscedasticity test (Breusch-Pagan)
    # Simplified version - correlation between predictions and absolute residuals
    heteroscedasticity = np.corrcoef(y_pred, abs_residuals)[0, 1]
    
    # 3. Autocorrelation (Durbin-Watson)
    # Simplified version
    dw_stat = np.sum(np.diff(residuals)**2) / np.sum(residuals**2)
    
    # Error analysis
    error_percentiles = np.percentile(pct_errors, [25, 50, 75, 90, 95, 99])
    
    # Outlier detection
    outlier_threshold = 3 * np.std(residuals)
    n_outliers = np.sum(abs_residuals > outlier_threshold)
    outlier_pct = (n_outliers / len(residuals)) * 100
    
    # Create analysis dictionary
    analysis = {
        'model_name': model_name,
        'r2_score': r2_score(y_true, y_pred),
        'mean_residual': np.mean(residuals),
        'std_residual': np.std(residuals),
        'normality_p_value': normality_p,
        'residuals_normal': normality_p > 0.05,
        'heteroscedasticity': abs(heteroscedasticity),
        'durbin_watson': dw_stat,
        'error_pct_25': error_percentiles[0],
        'error_pct_50': error_percentiles[1],
        'error_pct_75': error_percentiles[2],
        'error_pct_90': error_percentiles[3],
        'error_pct_95': error_percentiles[4],
        'error_pct_99': error_percentiles[5],
        'n_outliers': n_outliers,
        'outlier_pct': outlier_pct
    }
    
    # Print analysis
    print(f"\n{'='*60}")
    print(f"🔍 Prediction Analysis: {model_name}")
    print(f"{'='*60}")
    print(f"R² Score: {analysis['r2_score']:.6f}")
    print(f"\nResidual Analysis:")
    print(f"  Mean: {analysis['mean_residual']:.6f}")
    print(f"  Std:  {analysis['std_residual']:.6f}")
    print(f"  Normality: {'Yes' if analysis['residuals_normal'] else 'No'} (p={analysis['normality_p_value']:.4f})")
    print(f"  Heteroscedasticity: {analysis['heteroscedasticity']:.4f}")
    print(f"\nError Distribution:")
    print(f"  25th percentile: {analysis['error_pct_25']:.2f}%")
    print(f"  50th percentile: {analysis['error_pct_50']:.2f}%")
    print(f"  75th percentile: {analysis['error_pct_75']:.2f}%")
    print(f"  90th percentile: {analysis['error_pct_90']:.2f}%")
    print(f"  95th percentile: {analysis['error_pct_95']:.2f}%")
    print(f"\nOutliers: {analysis['n_outliers']} ({analysis['outlier_pct']:.2f}%)")
    
    return analysis

# ====================================================================================
# FEATURE IMPORTANCE ANALYSIS
# ====================================================================================

def analyze_feature_importance(trained_models, feature_names, top_n=30):
    """
    Analyze feature importance across all models
    
    Parameters:
    -----------
    trained_models : dict
        Dictionary of trained models
    feature_names : list
        List of feature names
    top_n : int
        Number of top features to return
    
    Returns:
    --------
    importance_df : pd.DataFrame
        Feature importance dataframe
    """
    importance_dict = {}
    
    for name, model in trained_models.items():
        # Get feature importance based on model type
        if hasattr(model, 'feature_importances_'):
            # Tree-based models
            importance_dict[name] = model.feature_importances_
        elif hasattr(model, 'coef_'):
            # Linear models
            importance_dict[name] = np.abs(model.coef_)
        else:
            # Skip models without feature importance
            continue
    
    # Create dataframe
    if importance_dict:
        importance_df = pd.DataFrame(importance_dict, index=feature_names)
        
        # Calculate average importance
        importance_df['mean_importance'] = importance_df.mean(axis=1)
        importance_df['std_importance'] = importance_df.std(axis=1)
        
        # Sort by mean importance
        importance_df = importance_df.sort_values('mean_importance', ascending=False)
        
        # Get top features
        top_features_df = importance_df.head(top_n)
        
        print(f"\n{'='*60}")
        print(f"📊 Top {top_n} Features by Importance")
        print(f"{'='*60}")
        
        for i, (feature, row) in enumerate(top_features_df.iterrows()):
            print(f"{i+1:2d}. {feature:40s} - Mean: {row['mean_importance']:.6f}")
        
        return importance_df
    else:
        print("⚠️ No models with feature importance found")
        return None

# ====================================================================================
# CROSS-VALIDATION EVALUATION
# ====================================================================================

def cross_validate_models(models, X, y, cv_folds=5, sample_weight=None):
    """
    Cross-validate multiple models
    
    Parameters:
    -----------
    models : list or dict
        Models to evaluate
    X : array
        Features
    y : array
        Target
    cv_folds : int
        Number of CV folds
    sample_weight : array, optional
        Sample weights
    
    Returns:
    --------
    cv_results : pd.DataFrame
        Cross-validation results
    """
    from sklearn.model_selection import cross_val_score, KFold
    
    cv_results = []
    kf = KFold(n_splits=cv_folds, shuffle=True, random_state=42)
    
    # Handle both list and dict inputs
    if isinstance(models, dict):
        models = [(name, model) for name, model in models.items()]
    
    for name, model in models:
        print(f"\nCross-validating {name}...")
        
        # Perform cross-validation
        if sample_weight is not None:
            scores = cross_val_score(
                model, X, y, cv=kf, scoring='r2',
                params={'sample_weight': sample_weight}  # sklearn 1.7+ uses 'params' not 'fit_params'
            )
        else:
            scores = cross_val_score(model, X, y, cv=kf, scoring='r2')
        
        # Store results
        result = {
            'Model': name,
            'CV_Mean': scores.mean(),
            'CV_Std': scores.std(),
            'CV_Min': scores.min(),
            'CV_Max': scores.max()
        }
        cv_results.append(result)
        
        print(f"  Mean R²: {scores.mean():.6f} (+/- {scores.std():.6f})")
    
    # Create dataframe
    cv_results_df = pd.DataFrame(cv_results).sort_values('CV_Mean', ascending=False)
    
    return cv_results_df

# ====================================================================================
# ERROR ANALYSIS
# ====================================================================================

def analyze_errors_by_price_range(y_true, y_pred, price_original, n_bins=10):
    """
    Analyze prediction errors by price range
    
    Parameters:
    -----------
    y_true : array
        True values (log-transformed)
    y_pred : array
        Predicted values (log-transformed)
    price_original : array
        Original prices
    n_bins : int
        Number of price bins
    
    Returns:
    --------
    error_analysis : pd.DataFrame
        Error analysis by price range
    """
    # Create price bins
    price_bins = pd.qcut(price_original, q=n_bins, duplicates='drop')
    
    # Calculate errors
    errors = y_true - y_pred
    abs_errors = np.abs(errors)
    pct_errors = (abs_errors / (np.abs(y_true) + 1e-8)) * 100
    
    # Group by price bin
    error_df = pd.DataFrame({
        'price_bin': price_bins,
        'price': price_original,
        'error': errors,
        'abs_error': abs_errors,
        'pct_error': pct_errors
    })
    
    # Aggregate by bin
    error_analysis = error_df.groupby('price_bin').agg({
        'price': ['min', 'max', 'mean', 'count'],
        'error': ['mean', 'std'],
        'abs_error': ['mean', 'std'],
        'pct_error': ['mean', 'median', 'std']
    }).round(4)
    
    print("\n📊 Error Analysis by Price Range")
    print("="*80)
    print(error_analysis)
    
    return error_analysis

# ====================================================================================
# GENERATE EVALUATION REPORT
# ====================================================================================

def generate_evaluation_report(trained_models, test_predictions, ensemble_predictions,
                             X_test, y_test, feature_names, save_path=None):
    """
    Generate comprehensive evaluation report
    
    Parameters:
    -----------
    trained_models : dict
        Trained models
    test_predictions : dict
        Test predictions from individual models
    ensemble_predictions : dict
        Ensemble predictions
    X_test : array
        Test features
    y_test : array
        Test target
    feature_names : list
        Feature names
    save_path : str, optional
        Path to save report
    
    Returns:
    --------
    report : dict
        Comprehensive evaluation report
    """
    print("\n" + "="*100)
    print("📋 GENERATING COMPREHENSIVE EVALUATION REPORT")
    print("="*100)
    
    report = {
        'timestamp': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        'n_test_samples': len(y_test),
        'n_features': len(feature_names)
    }
    
    # 1. Individual model performance
    print("\n1. Evaluating individual models...")
    individual_results = []
    
    for name, pred in test_predictions.items():
        metrics = calculate_metrics(y_test, pred)
        individual_results.append({'Model': name, **metrics})
    
    report['individual_models'] = pd.DataFrame(individual_results).sort_values('r2', ascending=False)
    
    # 2. Ensemble performance
    print("\n2. Evaluating ensemble models...")
    ensemble_results = evaluate_ensemble_predictions(ensemble_predictions, y_test)
    report['ensemble_models'] = ensemble_results
    
    # 3. Best model identification
    all_results = pd.concat([
        report['individual_models'],
        ensemble_results.rename(columns={'Method': 'Model'})
    ], ignore_index=True)
    
    best_model_idx = all_results['r2'].idxmax()
    report['best_model'] = {
        'name': all_results.loc[best_model_idx, 'Model'],
        'r2': all_results.loc[best_model_idx, 'r2'],
        'mae': all_results.loc[best_model_idx, 'mae'],
        'rmse': all_results.loc[best_model_idx, 'rmse']
    }
    
    print(f"\n🏆 Best Model: {report['best_model']['name']} (R² = {report['best_model']['r2']:.6f})")
    
    # 4. Feature importance
    print("\n3. Analyzing feature importance...")
    importance_df = analyze_feature_importance(trained_models, feature_names, top_n=20)
    if importance_df is not None:
        report['feature_importance'] = importance_df.head(20)
    
    # 5. Save report
    if save_path:
        import os
        import json
        
        os.makedirs(save_path, exist_ok=True)
        
        # Save as JSON (convert DataFrames to dict)
        report_json = {
            k: v.to_dict() if isinstance(v, pd.DataFrame) else v 
            for k, v in report.items()
        }
        
        report_path = os.path.join(save_path, 'evaluation_report.json')
        with open(report_path, 'w') as f:
            json.dump(report_json, f, indent=2, default=str)
        
        print(f"\n✅ Report saved to: {report_path}")
    
    return report
