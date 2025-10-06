"""
Model Utilities for ML Project (Part 1)
By Alex - World-Class AI Expert

Contains preprocessing, feature selection, and optimization functions
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler, PowerTransformer
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression, RFE
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.model_selection import cross_val_score, KFold
import optuna
from optuna.samplers import TPESampler
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
import warnings
warnings.filterwarnings('ignore')

# ====================================================================================
# ADVANCED PREPROCESSING
# ====================================================================================

class AdvancedPreprocessor:
    """Advanced preprocessing pipeline"""
    
    def __init__(self, numeric_features=None, categorical_features=None):
        self.numeric_features = numeric_features
        self.categorical_features = categorical_features
        self.scalers = {}
        self.transformers = {}
        self.feature_groups = {}
        
    def fit(self, X, y=None):
        """Fit preprocessor on training data"""
        print("\n🔧 Fitting Advanced Preprocessor...")
        
        # Identify feature types if not provided
        if self.numeric_features is None:
            self.numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
        if self.categorical_features is None:
            self.categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Identify feature groups
        self.feature_groups = self._identify_feature_groups(X)
        
        # Fit different scalers for different feature groups
        for group_name, features in self.feature_groups.items():
            if not features:
                continue
                
            if group_name in ['power_features', 'score_features']:
                # Use RobustScaler for features that might have outliers
                self.scalers[group_name] = RobustScaler()
                self.scalers[group_name].fit(X[features])
            elif group_name in ['count_features', 'binary_features']:
                # No scaling for count and binary features
                pass
            elif group_name == 'ratio_features':
                # Use PowerTransformer for ratio features
                self.transformers[group_name] = PowerTransformer(method='yeo-johnson')
                self.transformers[group_name].fit(X[features])
            else:
                # Use StandardScaler for other features
                self.scalers[group_name] = StandardScaler()
                self.scalers[group_name].fit(X[features])
        
        print(f"✅ Fitted preprocessor with {len(self.feature_groups)} feature groups")
        return self
    
    def transform(self, X):
        """Transform data"""
        X_transformed = X.copy()
        
        # Handle missing values first
        X_processed = self._handle_missing_values(X_transformed)
        
        # Apply transformations by group
        for group_name, features in self.feature_groups.items():
            # Filter to only include features that exist in X
            features_in_X = [f for f in features if f in X_processed.columns]
            
            # Separate numeric features from the group
            if isinstance(X_processed[features_in_X], pd.DataFrame):
                numeric_features_in_group = X_processed[features_in_X].select_dtypes(
                    include=[np.number]
                ).columns.tolist()
            else:
                numeric_features_in_group = features_in_X
            
            if not numeric_features_in_group:
                continue
            
            if group_name in self.scalers:
                try:
                    X_transformed[numeric_features_in_group] = self.scalers[group_name].transform(X_processed[numeric_features_in_group])
                except Exception as e:
                    print(f"   Warning: Could not transform {group_name}: {str(e)}")
            elif group_name in self.transformers:
                try:
                    X_transformed[numeric_features_in_group] = self.transformers[group_name].transform(X_processed[numeric_features_in_group])
                except Exception as e:
                    print(f"   Warning: Could not transform {group_name}: {str(e)}")
        
        return X_transformed
    
    def _identify_feature_groups(self, X):
        """Identify different types of features"""
        feature_groups = {
            'power_features': [],
            'count_features': [],
            'ratio_features': [],
            'score_features': [],
            'binary_features': [],
            'other_features': []
        }
        
        for col in X.columns:
            if 'power' in col or 'weight' in col:
                feature_groups['power_features'].append(col)
            elif 'count' in col or 'repeat' in col or 'num_' in col:
                feature_groups['count_features'].append(col)
            elif 'ratio' in col or '_to_' in col:
                feature_groups['ratio_features'].append(col)
            elif 'score' in col or 'index' in col:
                feature_groups['score_features'].append(col)
            elif col in self.numeric_features and X[col].nunique() <= 2:
                feature_groups['binary_features'].append(col)
            else:
                feature_groups['other_features'].append(col)
        
        return feature_groups
    
    def _handle_missing_values(self, X):
        """Handle missing values intelligently"""
        X_processed = X.copy()
        
        # 1. ระบุ categorical columns
        categorical_columns = ['complexity_class', 'estimated_tier', 'market_position',
                              'predicted_price_category']
        
        # เพิ่ม binned features จาก v5.0 (ถ้ามี)
        binned_cols = [col for col in X.columns if '_bin_' in col or '_qbin_' in col]
        categorical_columns.extend(binned_cols)
        
        # กรอง categorical columns ที่มีอยู่จริงใน X
        categorical_columns = [col for col in categorical_columns if col in X.columns]
        
        # 2. แยก numeric และ categorical columns
        numeric_columns = [col for col in X.columns if col not in categorical_columns]
        
        # 3. Fill NaN สำหรับ numeric columns ด้วย median
        if numeric_columns:
            X_processed[numeric_columns] = X_processed[numeric_columns].fillna(X_processed[numeric_columns].median())
        
        # 4. Fill NaN สำหรับ categorical columns ด้วย mode หรือค่า default
        for col in categorical_columns:
            if col in X_processed.columns:
                # ใช้ mode (ค่าที่พบบ่อยที่สุด) หรือค่า default
                if X_processed[col].notna().any():  # ถ้ามีค่าที่ไม่ใช่ NaN
                    mode_value = X_processed[col].mode()[0] if len(X_processed[col].mode()) > 0 else 0
                    X_processed[col] = X_processed[col].fillna(mode_value)
                else:  # ถ้าทั้งคอลัมน์เป็น NaN
                    X_processed[col] = X_processed[col].fillna(0)
        
        return X_processed
    
    def fit_transform(self, X, y=None):
        """Fit and transform in one step"""
        return self.fit(X, y).transform(X)

# ====================================================================================
# FEATURE SELECTION
# ====================================================================================

class HybridFeatureSelector:
    """Hybrid feature selection combining multiple methods"""
    
    def __init__(self, n_features=100, methods=['univariate', 'tree_based', 'rfe']):
        self.n_features = n_features
        self.methods = methods
        self.selected_features = None
        self.feature_scores = None
        
    def fit(self, X, y, sample_weight=None):
        """Fit feature selector"""
        print(f"\n🎯 Selecting top {self.n_features} features using hybrid approach...")
        
        all_scores = {}
        
        # 1. Univariate selection
        if 'univariate' in self.methods:
            print("   📊 Univariate selection (f_regression)...")
            selector = SelectKBest(f_regression, k=min(self.n_features * 2, X.shape[1]))
            selector.fit(X, y)
            univariate_scores = pd.Series(selector.scores_, index=X.columns)
            all_scores['univariate'] = univariate_scores / univariate_scores.max()
            
        # 2. Mutual information
        if 'mutual_info' in self.methods:
            print("   📊 Mutual information...")
            mi_scores = mutual_info_regression(X, y)
            mi_scores = pd.Series(mi_scores, index=X.columns)
            all_scores['mutual_info'] = mi_scores / mi_scores.max()
            
        # 3. Tree-based importance
        if 'tree_based' in self.methods:
            print("   🌳 Tree-based importance...")
            rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
            rf.fit(X, y, sample_weight=sample_weight)
            tree_scores = pd.Series(rf.feature_importances_, index=X.columns)
            all_scores['tree_based'] = tree_scores / tree_scores.max()
            
        # 4. Extra Trees importance
        if 'extra_trees' in self.methods:
            print("   🌳 Extra Trees importance...")
            et = ExtraTreesRegressor(n_estimators=100, random_state=42, n_jobs=-1)
            et.fit(X, y, sample_weight=sample_weight)
            et_scores = pd.Series(et.feature_importances_, index=X.columns)
            all_scores['extra_trees'] = et_scores / et_scores.max()
            
        # Combine scores
        print("   🔄 Combining scores...")
        score_df = pd.DataFrame(all_scores).fillna(0)
        self.feature_scores = score_df.mean(axis=1).sort_values(ascending=False)
        
        # Select top features
        self.selected_features = self.feature_scores.head(self.n_features).index.tolist()
        
        print(f"✅ Selected {len(self.selected_features)} features")
        return self
    
    def transform(self, X):
        """Transform to selected features"""
        return X[self.selected_features]
    
    def fit_transform(self, X, y, sample_weight=None):
        """Fit and transform"""
        return self.fit(X, y, sample_weight).transform(X)

def enhanced_feature_selection(X_train, y_train, X_test=None, n_features=150, 
                             sample_weight=None, random_state=42):
    """
    Enhanced feature selection using multiple methods
    
    Parameters:
    -----------
    X_train : pd.DataFrame
        Training features
    y_train : pd.Series
        Training target
    X_test : pd.DataFrame, optional
        Test features
    n_features : int
        Number of features to select
    sample_weight : np.array, optional
        Sample weights
    random_state : int
        Random seed
    
    Returns:
    --------
    X_train_selected, X_test_selected, selected_features, feature_selector
    """
    print(f"\n🎯 Enhanced Feature Selection - Selecting {n_features} features")
    
    # Initialize selector
    selector = HybridFeatureSelector(
        n_features=n_features,
        methods=['univariate', 'mutual_info', 'tree_based', 'extra_trees']
    )
    
    # Fit and transform
    X_train_selected = selector.fit_transform(X_train, y_train, sample_weight)
    
    # Transform test set if provided
    if X_test is not None:
        X_test_selected = selector.transform(X_test)
    else:
        X_test_selected = None
    
    # Show top features
    print("\n📊 Top 20 features by importance:")
    for i, (feat, score) in enumerate(selector.feature_scores.head(20).items()):
        print(f"   {i+1:2d}. {feat:40s} - Score: {score:.4f}")
    
    return X_train_selected, X_test_selected, selector.selected_features, selector

# ====================================================================================
# FEATURE ENGINEERING HELPERS
# ====================================================================================

def create_polynomial_features(X, degree=2, include_bias=False):
    """Create polynomial features for key variables"""
    from sklearn.preprocessing import PolynomialFeatures
    
    # Select only numeric columns with reasonable cardinality
    numeric_cols = X.select_dtypes(include=[np.number]).columns
    key_features = []
    
    for col in numeric_cols:
        if X[col].nunique() > 10:  # Skip binary/low cardinality features
            key_features.append(col)
    
    # Limit to top 10 features to avoid explosion
    key_features = key_features[:10]
    
    if key_features:
        poly = PolynomialFeatures(degree=degree, include_bias=include_bias)
        X_poly = poly.fit_transform(X[key_features])
        
        # Get feature names
        feature_names = poly.get_feature_names_out(key_features)
        
        # Create dataframe
        X_poly_df = pd.DataFrame(X_poly, columns=feature_names, index=X.index)
        
        # Remove original features (they're already in X)
        X_poly_df = X_poly_df.drop(columns=key_features, errors='ignore')
        
        # Concatenate with original features
        X_enhanced = pd.concat([X, X_poly_df], axis=1)
        
        print(f"✅ Added {X_poly_df.shape[1]} polynomial features")
        return X_enhanced
    else:
        return X

def create_interaction_features(X, top_n=20):
    """Create interaction features between top features"""
    # Get numeric columns
    numeric_cols = X.select_dtypes(include=[np.number]).columns[:top_n]
    
    interaction_features = pd.DataFrame(index=X.index)
    
    # Create interactions
    for i in range(len(numeric_cols)):
        for j in range(i+1, len(numeric_cols)):
            feat1, feat2 = numeric_cols[i], numeric_cols[j]
            
            # Multiplication interaction
            interaction_features[f'{feat1}_x_{feat2}'] = X[feat1] * X[feat2]
            
            # Division interaction (with small constant to avoid division by zero)
            interaction_features[f'{feat1}_div_{feat2}'] = X[feat1] / (X[feat2] + 1e-8)
    
    # Limit number of interaction features
    if interaction_features.shape[1] > 50:
        # Keep only top 50 by variance
        variances = interaction_features.var().sort_values(ascending=False)
        interaction_features = interaction_features[variances.head(50).index]
    
    print(f"✅ Added {interaction_features.shape[1]} interaction features")
    
    return pd.concat([X, interaction_features], axis=1)

"""
Model Utilities for ML Project (Part 2)
By Alex - World-Class AI Expert

Hyperparameter optimization functions for all models
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, make_scorer
from sklearn.ensemble import RandomForestRegressor, VotingRegressor, StackingRegressor
from sklearn.linear_model import Ridge
import optuna
from optuna.samplers import TPESampler
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
import warnings
warnings.filterwarnings('ignore')

# ====================================================================================
# HYPERPARAMETER OPTIMIZATION - XGBOOST
# ====================================================================================

def optimize_xgboost(X_train, y_train, n_trials=100, cv_folds=5, sample_weight=None, use_gpu=False, callbacks=None):
    """
    Optimize XGBoost hyperparameters using Optuna with GPU support

    Parameters:
    -----------
    X_train : array-like
        Training features
    y_train : array-like
        Training target
    n_trials : int
        Number of Optuna trials (default: 100)
    cv_folds : int
        Cross-validation folds (default: 5)
    sample_weight : array-like, optional
        Sample weights
    use_gpu : bool
        Use GPU for training (default: False)

    Returns:
    --------
    best_params : dict
        Best hyperparameters found
    """

    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 100, 2000),
            'max_depth': trial.suggest_int('max_depth', 3, 15),
            'learning_rate': trial.suggest_float('learning_rate', 0.001, 0.3, log=True),
            'subsample': trial.suggest_float('subsample', 0.5, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
            'gamma': trial.suggest_float('gamma', 0, 5),
            'reg_alpha': trial.suggest_float('reg_alpha', 0, 5),
            'reg_lambda': trial.suggest_float('reg_lambda', 0, 5),
            'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
            'random_state': 42,
            'n_jobs': -1,
            'enable_categorical': True
        }

        # ✅ GPU CONFIGURATION (XGBoost 2.0+ syntax)
        if use_gpu:
            params['device'] = 'cuda'
            params['tree_method'] = 'hist'
            if trial.number == 0:
                print(f"      🔥 XGBoost using GPU (device=cuda)")
        else:
            params['device'] = 'cpu'
            params['tree_method'] = 'hist'
            if trial.number == 0:
                print(f"      ⚪ XGBoost using CPU (device=cpu)")

        model = xgb.XGBRegressor(**params)

        # Use sample weights if provided
        if sample_weight is not None:
            scores = cross_val_score(
                model, X_train, y_train,
                cv=cv_folds,
                scoring='r2',
                params={'sample_weight': sample_weight},  # sklearn 1.7+ uses 'params' not 'fit_params'
                n_jobs=-1  # Parallel processing for faster CV
            )
        else:
            scores = cross_val_score(
                model, X_train, y_train,
                cv=cv_folds,
                scoring='r2',
                n_jobs=-1  # Parallel processing for faster CV
            )

        return scores.mean()

    # Run optimization
    study = optuna.create_study(
        direction='maximize',
        sampler=TPESampler(seed=42)
    )

    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True, callbacks=callbacks)

    best_params = study.best_params
    best_params['random_state'] = 42
    best_params['n_jobs'] = -1
    best_params['enable_categorical'] = True

    # ✅ GPU CONFIGURATION FOR BEST PARAMS (XGBoost 2.0+ syntax)
    if use_gpu:
        best_params['device'] = 'cuda'
        best_params['tree_method'] = 'hist'
    else:
        best_params['device'] = 'cpu'
        best_params['tree_method'] = 'hist'

    print(f"   Best CV R² Score: {study.best_value:.6f}")

    return best_params

# ====================================================================================
# HYPERPARAMETER OPTIMIZATION - LIGHTGBM
# ====================================================================================

def optimize_lightgbm(X_train, y_train, n_trials=100, cv_folds=5, sample_weight=None, use_gpu=False, callbacks=None):
    """
    Optimize LightGBM hyperparameters using Optuna with GPU support

    ⚡ SMART GPU FALLBACK: Tests GPU first, falls back to CPU if fails

    Parameters:
    -----------
    X_train : array-like
        Training features
    y_train : array-like
        Training target
    n_trials : int
        Number of Optuna trials (default: 100)
    cv_folds : int
        Cross-validation folds (default: 5)
    sample_weight : array-like, optional
        Sample weights
    use_gpu : bool
        Use GPU for training (default: False)

    Returns:
    --------
    best_params : dict
        Best hyperparameters found
    """

    # ⚡ SMART GPU FALLBACK - Test GPU compilation first
    actual_use_gpu = use_gpu
    if use_gpu:
        print(f"      🔬 Testing LightGBM GPU compilation...")
        try:
            import signal
            import time

            # Test GPU with minimal training
            test_params = {
                'n_estimators': 10,
                'max_depth': 3,
                'max_bin': 255,  # GPU limit
                'device': 'gpu',
                'gpu_platform_id': 0,
                'gpu_device_id': 0,
                'verbosity': -1,
                'random_state': 42
            }

            # Try to create and fit model with timeout
            test_model = lgb.LGBMRegressor(**test_params)

            # Use small subset for test
            test_size = min(100, len(X_train))
            start_time = time.time()
            test_model.fit(X_train[:test_size], y_train[:test_size])
            elapsed = time.time() - start_time

            # If successful and reasonable time (< 30 seconds)
            if elapsed < 30:
                print(f"      ✅ GPU test passed ({elapsed:.1f}s) - Using GPU for training")
                actual_use_gpu = True
            else:
                print(f"      ⚠️  GPU test slow ({elapsed:.1f}s) - Falling back to CPU")
                actual_use_gpu = False

        except Exception as e:
            print(f"      ⚠️  GPU test failed: {str(e)[:50]}...")
            print(f"      🔄 Automatically falling back to CPU for LightGBM")
            actual_use_gpu = False

    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 100, 2000),
            'max_depth': trial.suggest_int('max_depth', 3, 15),
            'learning_rate': trial.suggest_float('learning_rate', 0.001, 0.3, log=True),
            'num_leaves': trial.suggest_int('num_leaves', 20, 300),
            'subsample': trial.suggest_float('subsample', 0.5, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
            'reg_alpha': trial.suggest_float('reg_alpha', 0, 5),
            'reg_lambda': trial.suggest_float('reg_lambda', 0, 5),
            'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
            'max_bin': trial.suggest_int('max_bin', 50, 255 if actual_use_gpu else 500),  # GPU limit: 255
            'random_state': 42,
            'n_jobs': -1,
            'verbosity': -1,
            'force_col_wise': True
        }

        # ✅ GPU CONFIGURATION (uses actual_use_gpu after fallback test)
        if actual_use_gpu:
            params['device'] = 'gpu'
            params['gpu_platform_id'] = 0
            params['gpu_device_id'] = 0
            if trial.number == 0:
                print(f"      🔥 LightGBM using GPU (device=gpu)")
        else:
            params['device'] = 'cpu'
            if trial.number == 0:
                print(f"      ⚪ LightGBM using CPU (device=cpu)")

        model = lgb.LGBMRegressor(**params)

        # Use sample weights if provided
        # NOTE: Early stopping is NOT used here because cross_val_score doesn't provide eval_set
        # Early stopping will be used in final training after hyperparameter optimization
        if sample_weight is not None:
            scores = cross_val_score(
                model, X_train, y_train,
                cv=cv_folds,
                scoring='r2',
                params={'sample_weight': sample_weight},  # sklearn 1.7+ uses 'params' not 'fit_params'
                n_jobs=1  # LightGBM handles parallelism internally
            )
        else:
            scores = cross_val_score(
                model, X_train, y_train,
                cv=cv_folds,
                scoring='r2',
                n_jobs=1  # LightGBM handles parallelism internally
            )

        return scores.mean()

    # Run optimization
    study = optuna.create_study(
        direction='maximize',
        sampler=TPESampler(seed=42)
    )

    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True, callbacks=callbacks)

    best_params = study.best_params
    best_params['random_state'] = 42
    best_params['n_jobs'] = -1
    best_params['verbosity'] = -1
    best_params['force_col_wise'] = True

    # ✅ GPU CONFIGURATION FOR BEST PARAMS (uses actual_use_gpu after fallback test)
    # Note: max_bin already limited to 255 for GPU in objective function
    if actual_use_gpu:
        best_params['device'] = 'gpu'
        best_params['gpu_platform_id'] = 0
        best_params['gpu_device_id'] = 0
    else:
        best_params['device'] = 'cpu'

    print(f"   Best CV R² Score: {study.best_value:.6f}")

    # Store final GPU usage status in best_params for reference
    best_params['_gpu_used'] = actual_use_gpu

    return best_params

# ====================================================================================
# HYPERPARAMETER OPTIMIZATION - CATBOOST
# ====================================================================================

def optimize_catboost(X_train, y_train, n_trials=100, cv_folds=5, sample_weight=None, use_gpu=False, callbacks=None):
    """
    Optimize CatBoost hyperparameters using Optuna with GPU support

    Parameters:
    -----------
    X_train : array-like
        Training features
    y_train : array-like
        Training target
    n_trials : int
        Number of Optuna trials (default: 100)
    cv_folds : int
        Cross-validation folds (default: 5)
    sample_weight : array-like, optional
        Sample weights
    use_gpu : bool
        Use GPU for training (default: False)

    Returns:
    --------
    best_params : dict
        Best hyperparameters found
    """

    def objective(trial):
        params = {
            'iterations': trial.suggest_int('iterations', 100, 2000),
            'depth': trial.suggest_int('depth', 3, 12),
            'learning_rate': trial.suggest_float('learning_rate', 0.001, 0.3, log=True),
            'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1, 10),
            'border_count': trial.suggest_int('border_count', 32, 255),
            'bagging_temperature': trial.suggest_float('bagging_temperature', 0, 1),
            'random_seed': 42,
            'verbose': False,
            'allow_writing_files': False
        }

        # ✅ GPU CONFIGURATION
        if use_gpu:
            params['task_type'] = 'GPU'
            params['devices'] = '0'
            if trial.number == 0:
                print(f"      🔥 CatBoost using GPU (task_type=GPU)")
        else:
            params['task_type'] = 'CPU'
            params['thread_count'] = -1
            if trial.number == 0:
                print(f"      ⚪ CatBoost using CPU (task_type=CPU)")

        model = cb.CatBoostRegressor(**params)

        # Use sample weights if provided
        if sample_weight is not None:
            scores = cross_val_score(
                model, X_train, y_train,
                cv=cv_folds,
                scoring='r2',
                params={'sample_weight': sample_weight},  # sklearn 1.7+ uses 'params' not 'fit_params'
                n_jobs=1  # CatBoost handles parallelism internally
            )
        else:
            scores = cross_val_score(
                model, X_train, y_train,
                cv=cv_folds,
                scoring='r2',
                n_jobs=1  # CatBoost handles parallelism internally
            )

        return scores.mean()

    # Run optimization
    study = optuna.create_study(
        direction='maximize',
        sampler=TPESampler(seed=42)
    )

    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True, callbacks=callbacks)

    best_params = study.best_params
    best_params['random_seed'] = 42
    best_params['verbose'] = False
    best_params['allow_writing_files'] = False

    # ✅ GPU CONFIGURATION FOR BEST PARAMS
    if use_gpu:
        best_params['task_type'] = 'GPU'
        best_params['devices'] = '0'
    else:
        best_params['task_type'] = 'CPU'
        best_params['thread_count'] = -1

    print(f"   Best CV R² Score: {study.best_value:.6f}")

    return best_params

# ====================================================================================
# HYPERPARAMETER OPTIMIZATION - RANDOM FOREST
# ====================================================================================

def optimize_random_forest(X_train, y_train, n_trials=50, cv_folds=5, sample_weight=None, use_gpu=False, callbacks=None):
    """Optimize Random Forest hyperparameters using Optuna"""

    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 100, 500),
            'max_depth': trial.suggest_int('max_depth', 5, 30),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
            'max_features': trial.suggest_float('max_features', 0.5, 1.0),
            'bootstrap': True,
            'random_state': 42,
            'n_jobs': -1
        }

        model = RandomForestRegressor(**params)

        # Use sample weights if provided
        if sample_weight is not None:
            scores = cross_val_score(
                model, X_train, y_train,
                cv=cv_folds,
                scoring='r2',
                params={'sample_weight': sample_weight},  # sklearn 1.7+ uses 'params' not 'fit_params'
                n_jobs=1  # RF handles parallelism internally via n_jobs
            )
        else:
            scores = cross_val_score(
                model, X_train, y_train,
                cv=cv_folds,
                scoring='r2',
                n_jobs=1  # RF handles parallelism internally via n_jobs
            )

        return scores.mean()
    
    # Run optimization
    study = optuna.create_study(
        direction='maximize', 
        sampler=TPESampler(seed=42)
    )
    
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True, callbacks=callbacks)

    best_params = study.best_params
    best_params['bootstrap'] = True
    best_params['random_state'] = 42
    best_params['n_jobs'] = -1

    # Note: RandomForest doesn't support GPU acceleration
    if use_gpu:
        print(f"   ℹ️  Note: RandomForest doesn't support GPU (using CPU)")

    print(f"   Best CV R² Score: {study.best_value:.6f}")
    
    return best_params

# ====================================================================================
# ENSEMBLE METHODS
# ====================================================================================

class AdvancedStackingEnsemble:
    """Advanced stacking ensemble with multiple layers"""
    
    def __init__(self, base_models, meta_model=None, cv_folds=5, use_probas=False):
        self.base_models = base_models
        self.meta_model = meta_model or Ridge(alpha=1.0)
        self.cv_folds = cv_folds
        self.use_probas = use_probas
        self.stacking_regressor = None
        
    def fit(self, X, y, sample_weight=None):
        """Fit the stacking ensemble"""
        print("\n🏗️ Building Advanced Stacking Ensemble...")
        
        # Create stacking regressor
        self.stacking_regressor = StackingRegressor(
            estimators=self.base_models,
            final_estimator=self.meta_model,
            cv=self.cv_folds,
            n_jobs=1,  # Prevent GPU device conflict with CatBoost/XGBoost (was: -1)
            passthrough=False
        )
        
        # Fit with sample weights if provided
        if sample_weight is not None:
            self.stacking_regressor.fit(X, y, sample_weight=sample_weight)
        else:
            self.stacking_regressor.fit(X, y)
        
        print("✅ Stacking ensemble fitted successfully")
        return self
    
    def predict(self, X):
        """Make predictions"""
        return self.stacking_regressor.predict(X)
    
    def get_feature_importance(self):
        """Get feature importance from base models"""
        importances = {}
        
        for name, model in self.base_models:
            if hasattr(model, 'feature_importances_'):
                importances[name] = model.feature_importances_
            elif hasattr(model, 'coef_'):
                importances[name] = np.abs(model.coef_)
        
        return importances

class WeightedEnsemble:
    """Weighted average ensemble"""
    
    def __init__(self, models, weights=None):
        self.models = models
        self.weights = weights
        
    def fit(self, X, y, sample_weight=None):
        """Fit all models"""
        print("\n🏗️ Building Weighted Ensemble...")
        
        for name, model in self.models:
            print(f"   Training {name}...")
            if sample_weight is not None and hasattr(model, 'fit'):
                try:
                    model.fit(X, y, sample_weight=sample_weight)
                except:
                    model.fit(X, y)
            else:
                model.fit(X, y)
        
        print("✅ Weighted ensemble fitted successfully")
        return self
    
    def predict(self, X):
        """Make weighted predictions"""
        predictions = []
        
        for name, model in self.models:
            pred = model.predict(X)
            predictions.append(pred)
        
        predictions = np.array(predictions).T
        
        if self.weights is not None:
            return np.average(predictions, axis=1, weights=self.weights)
        else:
            return np.mean(predictions, axis=1)
    
    def optimize_weights(self, X, y):
        """Optimize weights using validation data"""
        from scipy.optimize import minimize
        
        predictions = []
        for name, model in self.models:
            pred = model.predict(X)
            predictions.append(pred)
        
        predictions = np.array(predictions).T
        
        def objective(weights):
            weighted_pred = np.average(predictions, axis=1, weights=weights)
            return -r2_score(y, weighted_pred)
        
        # Constraints: weights sum to 1, all weights >= 0
        constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
        bounds = [(0, 1) for _ in range(len(self.models))]
        
        # Initial weights
        initial_weights = np.ones(len(self.models)) / len(self.models)
        
        # Optimize
        result = minimize(objective, initial_weights, method='SLSQP',
                         bounds=bounds, constraints=constraints)
        
        self.weights = result.x
        print(f"\n✅ Optimized weights: {self.weights}")
        
        return self

def create_super_ensemble(models_dict, X_train, y_train, X_test, y_test, sample_weight=None):
    """Create a super ensemble combining multiple ensemble methods"""
    print("\n🚀 Creating Super Ensemble...")
    
    # 1. Voting Ensemble
    voting_models = [(name, model) for name, model in models_dict.items()]
    voting_ensemble = VotingRegressor(voting_models, n_jobs=-1)
    voting_ensemble.fit(X_train, y_train, sample_weight=sample_weight)
    
    # 2. Stacking Ensemble
    stacking_ensemble = AdvancedStackingEnsemble(
        base_models=voting_models[:5],  # Use top 5 models
        meta_model=Ridge(alpha=1.0),
        cv_folds=5
    )
    stacking_ensemble.fit(X_train, y_train, sample_weight)
    
    # 3. Weighted Ensemble
    weighted_ensemble = WeightedEnsemble(models=voting_models)
    weighted_ensemble.fit(X_train, y_train, sample_weight)
    weighted_ensemble.optimize_weights(X_test, y_test)
    
    # Combine all ensembles
    super_models = [
        ('voting', voting_ensemble),
        ('stacking', stacking_ensemble),
        ('weighted', weighted_ensemble)
    ]
    
    # Final super ensemble
    super_ensemble = WeightedEnsemble(models=super_models)
    super_ensemble.weights = [0.3, 0.4, 0.3]  # Can be optimized
    
    print("✅ Super Ensemble created successfully")
    
    return super_ensemble

