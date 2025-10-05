"""
Visualization Functions for ML Project
By Alex - World-Class AI Expert
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ====================================================================================
# PREDICTION PLOTS
# ====================================================================================

def plot_predictions_vs_actual(y_true, y_pred, model_name="Model", 
                              figsize=(12, 5), save_path=None):
    """
    Plot predictions vs actual values
    
    Parameters:
    -----------
    y_true : array
        True values
    y_pred : array
        Predicted values
    model_name : str
        Model name for title
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save plot
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Calculate R²
    r2 = r2_score(y_true, y_pred)
    
    # Plot 1: Scatter plot
    ax1 = axes[0]
    ax1.scatter(y_true, y_pred, alpha=0.5, s=50)
    
    # Add perfect prediction line
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    ax1.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
    
    # Add regression line
    z = np.polyfit(y_true, y_pred, 1)
    p = np.poly1d(z)
    ax1.plot(y_true, p(y_true), "g-", lw=2, alpha=0.8, label=f'Fit: y={z[0]:.2f}x+{z[1]:.2f}')
    
    ax1.set_xlabel('Actual Values', fontsize=12)
    ax1.set_ylabel('Predicted Values', fontsize=12)
    ax1.set_title(f'{model_name}: Predictions vs Actual\nR² = {r2:.4f}', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Residual plot
    ax2 = axes[1]
    residuals = y_true - y_pred
    ax2.scatter(y_pred, residuals, alpha=0.5, s=50)
    ax2.axhline(y=0, color='r', linestyle='--', lw=2)
    
    # Add confidence bands
    std_residuals = np.std(residuals)
    ax2.axhline(y=2*std_residuals, color='orange', linestyle=':', alpha=0.7, label='±2σ')
    ax2.axhline(y=-2*std_residuals, color='orange', linestyle=':', alpha=0.7)
    
    ax2.set_xlabel('Predicted Values', fontsize=12)
    ax2.set_ylabel('Residuals', fontsize=12)
    ax2.set_title('Residual Plot', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Plot saved to: {save_path}")
    
    plt.show()

# ====================================================================================
# MODEL COMPARISON PLOTS
# ====================================================================================

def plot_model_comparison(results_df, metric='R2_test', figsize=(12, 6), save_path=None):
    """
    Plot model comparison
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        Results dataframe with model performance
    metric : str
        Metric to plot
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save plot
    """
    plt.figure(figsize=figsize)
    
    # Sort by metric
    results_sorted = results_df.sort_values(metric, ascending=True)
    
    # Create horizontal bar plot
    colors = plt.cm.viridis(np.linspace(0, 1, len(results_sorted)))
    bars = plt.barh(results_sorted['Model'], results_sorted[metric], color=colors)
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + 0.001, bar.get_y() + bar.get_height()/2, 
                f'{width:.4f}', ha='left', va='center', fontsize=10)
    
    plt.xlabel(metric, fontsize=12)
    plt.ylabel('Model', fontsize=12)
    plt.title(f'Model Comparison - {metric}', fontsize=14)
    plt.grid(True, axis='x', alpha=0.3)
    
    # Add vertical line for threshold
    if 'R2' in metric:
        plt.axvline(x=0.9, color='red', linestyle='--', alpha=0.5, label='Target R²=0.90')
        plt.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Plot saved to: {save_path}")
    
    plt.show()

# ====================================================================================
# FEATURE IMPORTANCE PLOTS
# ====================================================================================

def plot_feature_importance(feature_importance_df, top_n=20, figsize=(10, 8), save_path=None):
    """
    Plot feature importance
    
    Parameters:
    -----------
    feature_importance_df : pd.DataFrame
        Feature importance dataframe
    top_n : int
        Number of top features to show
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save plot
    """
    plt.figure(figsize=figsize)
    
    # Get top features
    top_features = feature_importance_df.nlargest(top_n, 'mean_importance')
    
    # Create horizontal bar plot
    y_pos = np.arange(len(top_features))
    plt.barh(y_pos, top_features['mean_importance'], 
            xerr=top_features['std_importance'], 
            align='center', alpha=0.8, capsize=5)
    
    plt.yticks(y_pos, top_features.index)
    plt.xlabel('Importance Score', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.title(f'Top {top_n} Feature Importance (with std dev)', fontsize=14)
    plt.grid(True, axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Plot saved to: {save_path}")
    
    plt.show()

# ====================================================================================
# ERROR DISTRIBUTION PLOTS
# ====================================================================================

def plot_error_distribution(y_true, y_pred, model_name="Model", 
                           figsize=(15, 5), save_path=None):
    """
    Plot error distribution
    
    Parameters:
    -----------
    y_true : array
        True values
    y_pred : array
        Predicted values
    model_name : str
        Model name
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save plot
    """
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    
    # Calculate errors
    errors = y_true - y_pred
    abs_errors = np.abs(errors)
    pct_errors = (abs_errors / (np.abs(y_true) + 1e-8)) * 100
    
    # Plot 1: Error distribution
    ax1 = axes[0]
    ax1.hist(errors, bins=50, alpha=0.7, edgecolor='black')
    ax1.axvline(x=0, color='red', linestyle='--', lw=2)
    ax1.set_xlabel('Prediction Error', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.set_title('Error Distribution', fontsize=14)
    ax1.grid(True, alpha=0.3)
    
    # Add statistics
    mean_error = np.mean(errors)
    std_error = np.std(errors)
    ax1.text(0.05, 0.95, f'Mean: {mean_error:.4f}\nStd: {std_error:.4f}', 
             transform=ax1.transAxes, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Plot 2: Q-Q plot
    ax2 = axes[1]
    from scipy import stats
    stats.probplot(errors, dist="norm", plot=ax2)
    ax2.set_title('Q-Q Plot (Normality Check)', fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Percentage error distribution
    ax3 = axes[2]
    ax3.hist(pct_errors, bins=50, alpha=0.7, edgecolor='black')
    ax3.set_xlabel('Absolute Percentage Error (%)', fontsize=12)
    ax3.set_ylabel('Frequency', fontsize=12)
    ax3.set_title('Percentage Error Distribution', fontsize=14)
    ax3.grid(True, alpha=0.3)
    
    # Add percentile lines
    percentiles = [50, 90, 95]
    colors = ['green', 'orange', 'red']
    for p, c in zip(percentiles, colors):
        val = np.percentile(pct_errors, p)
        ax3.axvline(x=val, color=c, linestyle='--', alpha=0.7, 
                   label=f'{p}th percentile: {val:.1f}%')
    ax3.legend()
    
    plt.suptitle(f'{model_name} - Error Analysis', fontsize=16)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Plot saved to: {save_path}")
    
    plt.show()

# ====================================================================================
# ENSEMBLE COMPARISON PLOTS
# ====================================================================================

def plot_ensemble_comparison(ensemble_predictions, y_test, figsize=(15, 10), save_path=None):
    """
    Compare ensemble predictions
    
    Parameters:
    -----------
    ensemble_predictions : dict
        Dictionary of ensemble predictions
    y_test : array
        Test target values
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save plot
    """
    n_ensembles = len(ensemble_predictions)
    n_cols = 3
    n_rows = (n_ensembles + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten() if n_ensembles > 1 else [axes]
    
    for idx, (name, predictions) in enumerate(ensemble_predictions.items()):
        ax = axes[idx]
        
        # Calculate R²
        r2 = r2_score(y_test, predictions)
        
        # Scatter plot
        ax.scatter(y_test, predictions, alpha=0.5, s=30)
        
        # Perfect prediction line
        min_val = min(y_test.min(), predictions.min())
        max_val = max(y_test.max(), predictions.max())
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)
        
        ax.set_xlabel('Actual', fontsize=10)
        ax.set_ylabel('Predicted', fontsize=10)
        ax.set_title(f'{name}\nR² = {r2:.4f}', fontsize=12)
        ax.grid(True, alpha=0.3)
    
    # Hide empty subplots
    for idx in range(n_ensembles, len(axes)):
        axes[idx].set_visible(False)
    
    plt.suptitle('Ensemble Methods Comparison', fontsize=16)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Plot saved to: {save_path}")
    
    plt.show()

# ====================================================================================
# PRICE ANALYSIS PLOTS
# ====================================================================================

def plot_price_prediction_analysis(y_test_log, predictions_log, figsize=(15, 10), save_path=None):
    """
    Analyze predictions in original price scale
    
    Parameters:
    -----------
    y_test_log : array
        Test values (log scale)
    predictions_log : array
        Predictions (log scale)
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save plot
    """
    # Convert to original scale
    y_test_price = np.expm1(y_test_log)
    predictions_price = np.expm1(predictions_log)
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # Plot 1: Price distribution comparison
    ax1 = axes[0, 0]
    ax1.hist(y_test_price, bins=50, alpha=0.5, label='Actual', edgecolor='black')
    ax1.hist(predictions_price, bins=50, alpha=0.5, label='Predicted', edgecolor='black')
    ax1.set_xlabel('Price (฿)', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.set_title('Price Distribution Comparison', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Price vs Error
    ax2 = axes[0, 1]
    errors = y_test_price - predictions_price
    ax2.scatter(y_test_price, errors, alpha=0.5, s=30)
    ax2.axhline(y=0, color='red', linestyle='--', lw=2)
    ax2.set_xlabel('Actual Price (฿)', fontsize=12)
    ax2.set_ylabel('Prediction Error (฿)', fontsize=12)
    ax2.set_title('Prediction Error by Price Range', fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Log scale comparison
    ax3 = axes[1, 0]
    ax3.scatter(y_test_log, predictions_log, alpha=0.5, s=30)
    min_val = min(y_test_log.min(), predictions_log.min())
    max_val = max(y_test_log.max(), predictions_log.max())
    ax3.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)
    ax3.set_xlabel('Actual (log scale)', fontsize=12)
    ax3.set_ylabel('Predicted (log scale)', fontsize=12)
    ax3.set_title('Log Scale Predictions', fontsize=14)
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Percentage error by price bins
    ax4 = axes[1, 1]
    pct_errors = np.abs(errors) / y_test_price * 100
    price_bins = pd.qcut(y_test_price, q=10, duplicates='drop')
    
    error_by_bin = pd.DataFrame({
        'price_bin': price_bins,
        'pct_error': pct_errors
    }).groupby('price_bin')['pct_error'].mean()
    
    error_by_bin.plot(kind='bar', ax=ax4)
    ax4.set_xlabel('Price Range', fontsize=12)
    ax4.set_ylabel('Mean Absolute % Error', fontsize=12)
    ax4.set_title('Error by Price Range', fontsize=14)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # Rotate x labels
    ax4.set_xticklabels(ax4.get_xticklabels(), rotation=45, ha='right')
    
    plt.suptitle('Price Prediction Analysis', fontsize=16)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Plot saved to: {save_path}")
    
    plt.show()

# ====================================================================================
# LEARNING CURVES
# ====================================================================================

def plot_learning_curves(model, X_train, y_train, cv=5, 
                        train_sizes=np.linspace(0.1, 1.0, 10),
                        figsize=(10, 6), save_path=None):
    """
    Plot learning curves
    
    Parameters:
    -----------
    model : sklearn model
        Model to evaluate
    X_train : array
        Training features
    y_train : array
        Training target
    cv : int
        Cross-validation folds
    train_sizes : array
        Training set sizes
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save plot
    """
    from sklearn.model_selection import learning_curve
    
    # Calculate learning curves
    train_sizes_abs, train_scores, val_scores = learning_curve(
        model, X_train, y_train, cv=cv, 
        train_sizes=train_sizes, scoring='r2',
        n_jobs=-1, random_state=42
    )
    
    # Calculate mean and std
    train_mean = train_scores.mean(axis=1)
    train_std = train_scores.std(axis=1)
    val_mean = val_scores.mean(axis=1)
    val_std = val_scores.std(axis=1)
    
    # Plot
    plt.figure(figsize=figsize)
    
    plt.plot(train_sizes_abs, train_mean, 'o-', color='blue', 
             label='Training score', markersize=8)
    plt.fill_between(train_sizes_abs, train_mean - train_std, 
                     train_mean + train_std, alpha=0.1, color='blue')
    
    plt.plot(train_sizes_abs, val_mean, 'o-', color='green', 
             label='Validation score', markersize=8)
    plt.fill_between(train_sizes_abs, val_mean - val_std, 
                     val_mean + val_std, alpha=0.1, color='green')
    
    plt.xlabel('Training Set Size', fontsize=12)
    plt.ylabel('R² Score', fontsize=12)
    plt.title('Learning Curves', fontsize=14)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    
    # Add horizontal line for target R²
    plt.axhline(y=0.9, color='red', linestyle='--', alpha=0.5, label='Target R²=0.90')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Plot saved to: {save_path}")
    
    plt.show()

# ====================================================================================
# CREATE DASHBOARD
# ====================================================================================

def create_dashboard(y_test, predictions, model_name="Model", 
                    feature_importance_df=None, save_path=None):
    """
    Create a comprehensive dashboard
    
    Parameters:
    -----------
    y_test : array
        Test values
    predictions : array or dict
        Predictions (single array or dict of multiple predictions)
    model_name : str
        Model name
    feature_importance_df : pd.DataFrame, optional
        Feature importance
    save_path : str, optional
        Path to save dashboard
    """
    # Handle both single predictions and multiple predictions
    if isinstance(predictions, dict):
        # Use best prediction
        r2_scores = {name: r2_score(y_test, pred) for name, pred in predictions.items()}
        best_model = max(r2_scores, key=r2_scores.get)
        best_predictions = predictions[best_model]
        model_name = f"{model_name} - {best_model}"
    else:
        best_predictions = predictions
    
    # Create figure
    fig = plt.figure(figsize=(20, 12))
    
    # Define grid
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Main prediction plot
    ax1 = fig.add_subplot(gs[0, :2])
    plot_predictions_vs_actual(y_test, best_predictions, model_name, 
                              figsize=None, save_path=None)
    
    # 2. Residual distribution
    ax2 = fig.add_subplot(gs[0, 2])
    residuals = y_test - best_predictions
    ax2.hist(residuals, bins=30, alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Residuals')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Residual Distribution')
    ax2.grid(True, alpha=0.3)
    
    # 3. Feature importance (if provided)
    if feature_importance_df is not None:
        ax3 = fig.add_subplot(gs[1, :])
        top_features = feature_importance_df.nlargest(15, 'mean_importance')
        ax3.barh(range(len(top_features)), top_features['mean_importance'])
        ax3.set_yticks(range(len(top_features)))
        ax3.set_yticklabels(top_features.index)
        ax3.set_xlabel('Importance Score')
        ax3.set_title('Top 15 Feature Importance')
        ax3.grid(True, axis='x', alpha=0.3)
    
    # 4. Error metrics
    ax4 = fig.add_subplot(gs[2, 0])
    metrics = {
        'R² Score': r2_score(y_test, best_predictions),
        'MAE': np.mean(np.abs(residuals)),
        'RMSE': np.sqrt(np.mean(residuals**2)),
        'MAPE': np.mean(np.abs(residuals / (y_test + 1e-8))) * 100
    }
    
    y_pos = np.arange(len(metrics))
    ax4.barh(y_pos, list(metrics.values()))
    ax4.set_yticks(y_pos)
    ax4.set_yticklabels(list(metrics.keys()))
    ax4.set_xlabel('Value')
    ax4.set_title('Performance Metrics')
    
    for i, v in enumerate(metrics.values()):
        ax4.text(v + 0.01, i, f'{v:.4f}', va='center')
    
    # 5. Cumulative error distribution
    ax5 = fig.add_subplot(gs[2, 1:])
    pct_errors = np.abs(residuals) / (np.abs(y_test) + 1e-8) * 100
    sorted_errors = np.sort(pct_errors)
    cumulative = np.arange(1, len(sorted_errors) + 1) / len(sorted_errors) * 100
    
    ax5.plot(sorted_errors, cumulative, lw=2)
    ax5.set_xlabel('Absolute Percentage Error (%)')
    ax5.set_ylabel('Cumulative Percentage of Samples (%)')
    ax5.set_title('Cumulative Error Distribution')
    ax5.grid(True, alpha=0.3)
    
    # Add reference lines
    for threshold in [10, 20, 30]:
        pct_within = np.mean(pct_errors <= threshold) * 100
        ax5.axvline(x=threshold, color='red', linestyle='--', alpha=0.5)
        ax5.text(threshold, 50, f'{pct_within:.1f}%', rotation=90, va='bottom')
    
    plt.suptitle(f'Model Performance Dashboard - {model_name}', fontsize=20)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Dashboard saved to: {save_path}")
    
    plt.show()
