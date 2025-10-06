"""
Data Splitting Module for ML Project
By Alex - World-Class AI Expert
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
import warnings
warnings.filterwarnings('ignore')

# ====================================================================================
# DATA SPLITTING FUNCTIONS
# ====================================================================================

def split_data_stratified(X, y, sample_weights=None, test_size=0.2, random_state=42):
    """
    Split data with stratification based on price bins
    
    Parameters:
    -----------
    X : pd.DataFrame
        Feature matrix
    y : pd.Series
        Target variable (log-transformed prices)
    sample_weights : np.array, optional
        Sample weights
    test_size : float
        Test set size (default: 0.2)
    random_state : int
        Random seed
    
    Returns:
    --------
    X_train, X_test, y_train, y_test, sw_train, sw_test
    """
    print("\n" + "="*100)
    print("📊 SPLITTING DATA WITH STRATIFICATION")
    print("="*100)
    
    # Create stratification bins based on target
    n_bins = 10
    y_bins = pd.qcut(y, q=n_bins, labels=False, duplicates='drop')
    
    print(f"\n📊 Creating {n_bins} stratification bins based on price")
    
    # Show bin distribution
    bin_counts = pd.Series(y_bins).value_counts().sort_index()
    print("\n📈 Price bin distribution:")
    for bin_idx, count in bin_counts.items():
        price_range = np.expm1(pd.Series(y[y_bins == bin_idx]).quantile([0, 1]))
        print(f"   Bin {bin_idx}: {count:,} samples (฿{price_range[0]:,.0f} - ฿{price_range[1]:,.0f})")
    
    # Split with stratification
    if sample_weights is not None:
        X_train, X_test, y_train, y_test, sw_train, sw_test = train_test_split(
            X, y, sample_weights,
            test_size=test_size,
            stratify=y_bins,
            random_state=random_state
        )
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=test_size,
            stratify=y_bins,
            random_state=random_state
        )
        sw_train = np.ones(len(X_train))
        sw_test = np.ones(len(X_test))
    
    # Validate split
    print(f"\n✅ Data split completed:")
    print(f"   - Train set: {len(X_train):,} samples ({len(X_train)/len(X)*100:.1f}%)")
    print(f"   - Test set: {len(X_test):,} samples ({len(X_test)/len(X)*100:.1f}%)")
    
    # Check stratification
    train_bins = pd.qcut(y_train, q=n_bins, labels=False, duplicates='drop')
    test_bins = pd.qcut(y_test, q=n_bins, labels=False, duplicates='drop')
    
    print("\n📊 Stratification check:")
    print("   Train distribution:", pd.Series(train_bins).value_counts(normalize=True).sort_index().values)
    print("   Test distribution:", pd.Series(test_bins).value_counts(normalize=True).sort_index().values)
    
    # Price range check
    print(f"\n💰 Price ranges:")
    print(f"   - Train: ฿{np.expm1(y_train.min()):,.0f} - ฿{np.expm1(y_train.max()):,.0f}")
    print(f"   - Test: ฿{np.expm1(y_test.min()):,.0f} - ฿{np.expm1(y_test.max()):,.0f}")
    
    print("\n✅ Data split successful and balanced!")
    
    return X_train, X_test, y_train, y_test, sw_train, sw_test

# ====================================================================================
# CROSS-VALIDATION SPLITTER
# ====================================================================================

def get_cv_splitter(n_splits=5, shuffle=True, random_state=42):
    """
    Get cross-validation splitter with stratification
    
    Parameters:
    -----------
    n_splits : int
        Number of CV folds
    shuffle : bool
        Whether to shuffle before splitting
    random_state : int
        Random seed
    
    Returns:
    --------
    cv_splitter : StratifiedKFold object
    """
    return StratifiedKFold(
        n_splits=n_splits,
        shuffle=shuffle,
        random_state=random_state
    )

# ====================================================================================
# TIME-BASED SPLITTING (for time-series data)
# ====================================================================================

def split_time_series(X, y, sample_weights=None, test_size=0.2, gap=0):
    """
    Split data based on time (if applicable)
    
    Parameters:
    -----------
    X : pd.DataFrame
        Feature matrix
    y : pd.Series
        Target variable
    sample_weights : np.array, optional
        Sample weights
    test_size : float
        Test set size
    gap : int
        Gap between train and test sets
    
    Returns:
    --------
    X_train, X_test, y_train, y_test, sw_train, sw_test
    """
    n_samples = len(X)
    test_samples = int(n_samples * test_size)
    train_samples = n_samples - test_samples - gap
    
    # Split indices
    train_idx = slice(0, train_samples)
    test_idx = slice(train_samples + gap, n_samples)
    
    # Split data
    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]
    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]
    
    if sample_weights is not None:
        sw_train = sample_weights[train_idx]
        sw_test = sample_weights[test_idx]
    else:
        sw_train = np.ones(len(X_train))
        sw_test = np.ones(len(X_test))
    
    return X_train, X_test, y_train, y_test, sw_train, sw_test

# ====================================================================================
# VALIDATION SET CREATION
# ====================================================================================

def create_validation_set(X_train, y_train, sw_train=None, val_size=0.2, random_state=42):
    """
    Create validation set from training data
    
    Parameters:
    -----------
    X_train : pd.DataFrame
        Training features
    y_train : pd.Series
        Training target
    sw_train : np.array, optional
        Training sample weights
    val_size : float
        Validation set size
    random_state : int
        Random seed
    
    Returns:
    --------
    X_tr, X_val, y_tr, y_val, sw_tr, sw_val
    """
    # Create stratification bins
    y_bins = pd.qcut(y_train, q=5, labels=False, duplicates='drop')
    
    if sw_train is not None:
        X_tr, X_val, y_tr, y_val, sw_tr, sw_val = train_test_split(
            X_train, y_train, sw_train,
            test_size=val_size,
            stratify=y_bins,
            random_state=random_state
        )
    else:
        X_tr, X_val, y_tr, y_val = train_test_split(
            X_train, y_train,
            test_size=val_size,
            stratify=y_bins,
            random_state=random_state
        )
        sw_tr = np.ones(len(X_tr))
        sw_val = np.ones(len(X_val))
    
    print(f"\n📊 Validation set created:")
    print(f"   - Training: {len(X_tr):,} samples")
    print(f"   - Validation: {len(X_val):,} samples")
    
    return X_tr, X_val, y_tr, y_val, sw_tr, sw_val

# ====================================================================================
# HOLDOUT SET CREATION
# ====================================================================================

def create_holdout_set(X, y, sample_weights=None, holdout_size=0.1, random_state=42):
    """
    Create a holdout set for final evaluation
    
    Parameters:
    -----------
    X : pd.DataFrame
        Full feature matrix
    y : pd.Series
        Full target variable
    sample_weights : np.array, optional
        Sample weights
    holdout_size : float
        Holdout set size
    random_state : int
        Random seed
    
    Returns:
    --------
    X_main, X_holdout, y_main, y_holdout, sw_main, sw_holdout
    """
    # Create stratification bins
    y_bins = pd.qcut(y, q=10, labels=False, duplicates='drop')
    
    if sample_weights is not None:
        X_main, X_holdout, y_main, y_holdout, sw_main, sw_holdout = train_test_split(
            X, y, sample_weights,
            test_size=holdout_size,
            stratify=y_bins,
            random_state=random_state
        )
    else:
        X_main, X_holdout, y_main, y_holdout = train_test_split(
            X, y,
            test_size=holdout_size,
            stratify=y_bins,
            random_state=random_state
        )
        sw_main = np.ones(len(X_main))
        sw_holdout = np.ones(len(X_holdout))
    
    print(f"\n🔒 Holdout set created:")
    print(f"   - Main data: {len(X_main):,} samples ({len(X_main)/len(X)*100:.1f}%)")
    print(f"   - Holdout: {len(X_holdout):,} samples ({len(X_holdout)/len(X)*100:.1f}%)")
    
    return X_main, X_holdout, y_main, y_holdout, sw_main, sw_holdout

# ====================================================================================
# DATA SPLIT VALIDATOR
# ====================================================================================

def validate_split(X_train, X_test, y_train, y_test, feature_names=None):
    """
    Validate train/test split
    
    Parameters:
    -----------
    X_train, X_test : pd.DataFrame
        Feature matrices
    y_train, y_test : pd.Series
        Target variables
    feature_names : list, optional
        Feature names to check
    """
    print("\n🔍 Validating data split...")
    
    # Basic checks
    assert len(X_train) == len(y_train), "X_train and y_train length mismatch"
    assert len(X_test) == len(y_test), "X_test and y_test length mismatch"
    assert X_train.shape[1] == X_test.shape[1], "Feature count mismatch"
    
    print("✅ Basic validation passed")
    
    # Feature consistency
    if isinstance(X_train, pd.DataFrame):
        train_cols = set(X_train.columns)
        test_cols = set(X_test.columns)
        
        if train_cols != test_cols:
            missing_in_test = train_cols - test_cols
            missing_in_train = test_cols - train_cols
            
            if missing_in_test:
                print(f"⚠️ Missing in test: {missing_in_test}")
            if missing_in_train:
                print(f"⚠️ Missing in train: {missing_in_train}")
        else:
            print("✅ Feature consistency check passed")
    
    # Distribution check
    print("\n📊 Distribution comparison:")
    print(f"   Train - Mean: {y_train.mean():.4f}, Std: {y_train.std():.4f}")
    print(f"   Test  - Mean: {y_test.mean():.4f}, Std: {y_test.std():.4f}")
    
    # Check for data leakage
    if isinstance(X_train, pd.DataFrame) and isinstance(X_test, pd.DataFrame):
        if X_train.index.intersection(X_test.index).any():
            print("⚠️ WARNING: Found overlapping indices between train and test!")
        else:
            print("✅ No data leakage detected")
    
    return True

# ====================================================================================
# UTILITY FUNCTIONS
# ====================================================================================

def get_split_summary(X_train, X_test, y_train, y_test):
    """Get summary statistics for train/test split"""
    summary = {
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'train_ratio': len(X_train) / (len(X_train) + len(X_test)),
        'n_features': X_train.shape[1],
        'y_train_mean': y_train.mean(),
        'y_train_std': y_train.std(),
        'y_test_mean': y_test.mean(),
        'y_test_std': y_test.std(),
        'y_train_min': y_train.min(),
        'y_train_max': y_train.max(),
        'y_test_min': y_test.min(),
        'y_test_max': y_test.max()
    }
    
    return summary
