"""
Helper functions for ML Project
By Alex - World-Class AI Expert
"""
import os
import sys
import time
import logging
import warnings
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from contextlib import contextmanager
import psutil
import gc

# ====================================================================================
# LOGGING SETUP
# ====================================================================================
def setup_logging(log_level='INFO', log_file=None):
    """Setup logging configuration"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    if log_file:
        logging.basicConfig(
            level=getattr(logging, log_level),
            format=log_format,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
    else:
        logging.basicConfig(
            level=getattr(logging, log_level),
            format=log_format,
            handlers=[logging.StreamHandler(sys.stdout)]
        )
    
    return logging.getLogger(__name__)

# ====================================================================================
# TIMER CONTEXT MANAGER
# ====================================================================================
@contextmanager
def timer(name):
    """Timer context manager for measuring execution time"""
    t0 = time.time()
    print(f"\n⏱️ [{name}] Starting...")
    yield
    elapsed = time.time() - t0
    print(f"✅ [{name}] Done in {elapsed:.2f} seconds")

# ====================================================================================
# MEMORY USAGE
# ====================================================================================
def memory_usage():
    """Print current memory usage"""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return f"Memory Usage: {mem_info.rss / 1024 / 1024:.1f} MB"

def reduce_memory_usage(df, verbose=True):
    """Reduce memory usage of dataframe"""
    start_mem = df.memory_usage().sum() / 1024**2
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    
    end_mem = df.memory_usage().sum() / 1024**2
    
    if verbose:
        print(f'Memory usage decreased from {start_mem:.2f} Mb to {end_mem:.2f} Mb ({100 * (start_mem - end_mem) / start_mem:.1f}% reduction)')
    
    return df

# ====================================================================================
# THAI FONT SETUP
# ====================================================================================
def setup_thai_font():
    """Setup Thai font for matplotlib"""
    try:
        # Try to find Thai fonts
        thai_fonts = ['Sarabun', 'TH Sarabun New', 'Angsana New', 'CordiaUPC', 'BrowalliaUPC']
        
        import matplotlib.font_manager as fm
        available_fonts = [f.name for f in fm.fontManager.ttflist]
        
        for font in thai_fonts:
            if font in available_fonts:
                plt.rcParams['font.family'] = font
                print(f"✅ Thai font '{font}' set successfully")
                return font
        
        # If no Thai font found, use default
        print("⚠️ No Thai font found, using default font")
        return None
        
    except Exception as e:
        print(f"⚠️ Error setting Thai font: {str(e)}")
        return None

# ====================================================================================
# AUTO SAVE CHECKPOINT
# ====================================================================================
def auto_save_checkpoint(cell_number, globals_dict=None):
    """
    ฟังก์ชันสำหรับบันทึก checkpoint อัตโนมัติหลังรัน cell เสร็จ
    
    Parameters:
    -----------
    cell_number : int
        หมายเลข cell ที่รันเสร็จ (1-7)
    globals_dict : dict, optional
        globals() dictionary จาก notebook
    """
    import pickle
    import joblib
    from datetime import datetime

    # Import paths from config
    try:
        from src.config import BASE_PATH
        checkpoint_dir = os.path.join(BASE_PATH, 'checkpoints')
    except ImportError:
        # Fallback to environment detection
        if os.path.exists('/content/drive/MyDrive'):
            checkpoint_dir = "/content/drive/MyDrive/ML_Checkpoints"
        elif os.path.exists('/kaggle/working'):
            checkpoint_dir = "/kaggle/working/checkpoints"
        else:
            checkpoint_dir = "./checkpoints"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(checkpoint_dir, exist_ok=True)
    
    # Define what to save for each cell
    checkpoints = {
        1: ['CONFIG', 'MODEL_CONFIG', 'TUNING_PARAMS'],
        2: ['df_raw', 'df_cleaned', 'test_features'],
        3: ['X_train_selected', 'X_test_selected', 'y_train_log', 'y_test_log', 
            'selected_features', 'best_xgb_params', 'best_lgb_params', 
            'best_cat_params', 'best_rf_params'],
        4: ['trained_models', 'test_predictions', 'ensemble_predictions', 
            'final_r2', 'results_df'],
        5: ['results_df', 'feature_importance_df'],
        6: ['best_model', 'feature_names', 'feature_selector', 'preprocessor'],
        7: ['deployed_models']
    }
    
    if cell_number not in checkpoints:
        print(f"❌ Invalid cell number: {cell_number}")
        return
    
    # Check prerequisites
    prerequisites = {
        2: ['CONFIG'],
        3: ['df_cleaned'],
        4: ['X_train_selected', 'y_train_log'],
        5: ['results_df'],
        6: ['trained_models'],
        7: ['best_model']
    }
    
    if cell_number in prerequisites:
        for var in prerequisites[cell_number]:
            if globals_dict and var not in globals_dict:
                print(f"❌ ไม่พบตัวแปร '{var}' - กรุณารัน Cell ก่อนหน้านี้")
                return
    
    # Save checkpoint
    checkpoint_data = {}
    vars_to_save = checkpoints[cell_number]
    
    if globals_dict:
        for var in vars_to_save:
            if var in globals_dict:
                checkpoint_data[var] = globals_dict[var]
    
    if checkpoint_data:
        filename = f"{checkpoint_dir}/checkpoint_cell{cell_number}_{timestamp}.pkl"
        joblib.dump(checkpoint_data, filename)
        print(f"✅ Checkpoint saved: {filename}")
        print(f"   Variables saved: {list(checkpoint_data.keys())}")
    else:
        print(f"⚠️ No variables to save for Cell {cell_number}")

# ====================================================================================
# MODEL RESULTS PRINTER
# ====================================================================================
def print_model_results(model_name, r2, mae, rmse, predictions=None, y_true=None):
    """Print model evaluation results in a nice format"""
    print(f"\n{'='*60}")
    print(f"📊 {model_name} Results")
    print(f"{'='*60}")
    print(f"R² Score:  {r2:.6f}")
    print(f"MAE:       {mae:.4f}")
    print(f"RMSE:      {rmse:.4f}")
    
    if predictions is not None and y_true is not None:
        # Calculate additional metrics
        mape = np.mean(np.abs((y_true - predictions) / y_true)) * 100
        max_error = np.max(np.abs(y_true - predictions))
        
        print(f"MAPE:      {mape:.2f}%")
        print(f"Max Error: {max_error:.4f}")
    
    print(f"{'='*60}")

# ====================================================================================
# FEATURE IMPORTANCE PLOTTER
# ====================================================================================
def plot_feature_importance(feature_importance_df, top_n=20, save_path=None):
    """Plot feature importance"""
    plt.figure(figsize=(10, 8))
    
    # Select top features
    top_features = feature_importance_df.nlargest(top_n, 'importance')
    
    # Create plot
    sns.barplot(data=top_features, x='importance', y='feature', palette='viridis')
    plt.title(f'Top {top_n} Feature Importance', fontsize=16)
    plt.xlabel('Importance Score', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Feature importance plot saved to: {save_path}")
    
    plt.show()

# ====================================================================================
# RESULTS SUMMARY
# ====================================================================================
def create_results_summary(results_df, save_path=None):
    """Create a summary of model results"""
    summary = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'models_evaluated': len(results_df),
        'best_model': results_df.loc[results_df['R2_test'].idxmax(), 'Model'],
        'best_r2': results_df['R2_test'].max(),
        'average_r2': results_df['R2_test'].mean(),
        'models': results_df.to_dict('records')
    }
    
    if save_path:
        import json
        with open(save_path, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"✅ Results summary saved to: {save_path}")
    
    return summary

# ====================================================================================
# DATA VALIDATION
# ====================================================================================
def validate_data(df, required_columns=None):
    """Validate dataframe"""
    issues = []
    
    # Check if dataframe is empty
    if df.empty:
        issues.append("DataFrame is empty")
    
    # Check for required columns
    if required_columns:
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            issues.append(f"Missing columns: {missing_cols}")
    
    # Check for NaN values
    nan_counts = df.isna().sum()
    if nan_counts.any():
        issues.append(f"NaN values found in: {nan_counts[nan_counts > 0].to_dict()}")
    
    # Check for duplicates
    if df.duplicated().any():
        issues.append(f"Duplicate rows found: {df.duplicated().sum()}")
    
    if issues:
        print("⚠️ Data validation issues found:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ Data validation passed")
        return True

# ====================================================================================
# GARBAGE COLLECTION
# ====================================================================================
def clean_memory():
    """Clean up memory"""
    gc.collect()
    print(f"🧹 Memory cleaned. {memory_usage()}")
