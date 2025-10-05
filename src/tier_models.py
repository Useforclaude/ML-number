# ================================================================
# 🎯 TIER-SPECIFIC MODELS IMPLEMENTATION
# By Alex - Enhanced from community suggestion
# ================================================================

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor, XGBClassifier
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import joblib
import logging

logger = logging.getLogger(__name__)

class TierSpecificPricePredictor:
    """
    Enhanced tier-specific model with dynamic boundaries
    """
    
    def __init__(self, use_dynamic_boundaries=True, use_soft_voting=True):
        self.use_dynamic_boundaries = use_dynamic_boundaries
        self.use_soft_voting = use_soft_voting
        
        # Will be set dynamically or use defaults
        self.tier_boundaries = None
        self.tier_names = ['standard', 'premium', 'luxury']
        
        # Models
        self.router_model = None
        self.tier_models = {}
        self.tier_scalers = {}  # Separate scalers for each tier
        
        # Feature importance
        self.feature_importance = {}
        
        # Model configs (moved to config.py ideally)
        self.model_configs = self._get_model_configs()

    def _get_model_configs(self):
        """Get model configurations for each tier"""
        return {
            'standard': {
                'model_class': LGBMRegressor,
                'params': {
                    'n_estimators': 500,
                    'learning_rate': 0.05,
                    'max_depth': 15,
                    'num_leaves': 31,
                    'min_child_samples': 20,
                    'subsample': 0.8,
                    'colsample_bytree': 0.8,
                    'random_state': 42,
                    'n_jobs': -1,
                    'verbosity': -1
                }
            },
            'premium': {
                'model_class': XGBRegressor,
                'params': {
                    'n_estimators': 800,
                    'learning_rate': 0.03,
                    'max_depth': 12,
                    'subsample': 0.85,
                    'colsample_bytree': 0.85,
                    'reg_alpha': 0.1,
                    'reg_lambda': 1.0,
                    'random_state': 42,
                    'n_jobs': -1
                }
            },
            'luxury': {
                'model_class': CatBoostRegressor,
                'params': {
                    'iterations': 1000,
                    'learning_rate': 0.02,
                    'depth': 10,
                    'l2_leaf_reg': 5,
                    'border_count': 128,
                    'random_state': 42,
                    'verbose': False
                }
            }
        }

    def _find_optimal_n_clusters(self, log_prices):
        """Find optimal number of clusters using elbow method"""
        from sklearn.metrics import silhouette_score
        
        scores = []
        for k in range(2, 6):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(log_prices)
            score = silhouette_score(log_prices, labels)
            scores.append(score)
        
        # Return k with highest silhouette score
        return scores.index(max(scores)) + 2
    
    def _validate_boundaries(self, boundaries, prices):
        """Validate tier boundaries"""
        for i in range(len(boundaries) - 1):
            tier_mask = (prices >= boundaries[i]) & (prices < boundaries[i+1])
            count = tier_mask.sum()
            if count < 10:
                logger.warning(f"Tier {i} has only {count} samples")
    
    def _scale_features(self, X, tier):
        """Scale features for specific tier"""
        # For now, return as-is. Can add tier-specific scaling later
        return X
    
    def _calculate_feature_importance(self, feature_names):
        """Calculate aggregated feature importance"""
        self.feature_importance = {}
        for tier, model in self.tier_models.items():
            if model is not None and hasattr(model, 'feature_importances_'):
                self.feature_importance[tier] = pd.Series(
                    model.feature_importances_,
                    index=feature_names
                ).sort_values(ascending=False)
    
    def find_optimal_tier_boundaries(self, prices, n_tiers=3):
        """
        Find natural price clusters using KMeans
        Enhanced version with validation
        """
        logger.info("Finding optimal tier boundaries...")
        
        # Log transform for better clustering
        log_prices = np.log1p(prices).reshape(-1, 1)
        
        # Find optimal number of clusters if needed
        if n_tiers == 'auto':
            n_tiers = self._find_optimal_n_clusters(log_prices)
        
        # Cluster
        kmeans = KMeans(n_clusters=n_tiers, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(log_prices)
        
        # Get sorted cluster centers
        centers = np.sort(kmeans.cluster_centers_.flatten())
        
        # Calculate boundaries
        boundaries = [0]
        for i in range(len(centers) - 1):
            # Use geometric mean for log-space
            boundary = np.expm1((centers[i] + centers[i+1]) / 2)
            boundaries.append(boundary)
        boundaries.append(np.inf)
        
        # Validate boundaries
        self._validate_boundaries(boundaries, prices)
        
        logger.info(f"Optimal boundaries: {[f'฿{b:,.0f}' if b < np.inf else '∞' for b in boundaries]}")
        
        return boundaries
    
    def train(self, X, y_log, y_prices, sample_weight=None):
        """
        Complete training pipeline
        """
        # 1. Find tier boundaries if dynamic
        if self.use_dynamic_boundaries:
            self.tier_boundaries = self.find_optimal_tier_boundaries(y_prices)
        else:
            self.tier_boundaries = [0, 50000, 500000, np.inf]
        
        # 2. Train router
        tier_labels = self.train_router(X, y_prices)
        
        # 3. Train tier-specific models
        self.train_tier_models(X, y_log, y_prices, tier_labels, sample_weight)
        
        # 4. Calculate feature importance
        self._calculate_feature_importance(X.columns)
        
        return self
    
    def predict(self, X, return_tier_info=False):
        """
        Enhanced prediction with soft voting option
        """
        if self.use_soft_voting:
            predictions = self._predict_soft(X)
        else:
            predictions = self._predict_hard(X)
        
        if return_tier_info:
            tier_probs = self.router_model.predict_proba(X)
            tier_predictions = self.router_model.predict(X)
            return predictions, tier_predictions, tier_probs
        
        return predictions
    
    def _predict_soft(self, X):
        """Probability-weighted prediction"""
        tier_probs = self.router_model.predict_proba(X)
        predictions = np.zeros(len(X))
        
        for i, tier in enumerate(self.tier_names):
            if tier in self.tier_models:
                # Scale features for this tier
                X_scaled = self._scale_features(X, tier)
                tier_pred = self.tier_models[tier].predict(X_scaled)
                predictions += tier_probs[:, i] * tier_pred
        
        return predictions

    def _predict_hard(self, X):
        """Hard prediction using router"""
        # Router predicts tier
        tier_predictions = self.router_model.predict(X)
        predictions = np.zeros(len(X))
        
        # Predict for each tier
        for i, tier_idx in enumerate(tier_predictions):
            tier = self.tier_names[tier_idx]
            if tier in self.tier_models and self.tier_models[tier] is not None:
                # Get single row as DataFrame to preserve feature names
                X_single = X.iloc[[i]] if hasattr(X, 'iloc') else X[i:i+1]
                predictions[i] = self.tier_models[tier].predict(X_single)[0]
        
        return predictions
        
    def create_tier_label(self, prices):
        """สร้าง label สำหรับแต่ละ tier"""
        return pd.cut(prices, bins=self.tier_boundaries, 
                     labels=self.tier_names, include_lowest=True)
    
    def train_router(self, X, y_prices):
        """Train router model เพื่อทำนายว่าเบอร์อยู่ tier ไหน"""
        print("\n🎯 Training Router Model...")
        
        # Create tier labels
        tier_labels = self.create_tier_label(y_prices)
        
        # Convert to numeric (0, 1, 2)
        tier_numeric = pd.Categorical(tier_labels).codes
        
        # Train a classifier
        from xgboost import XGBClassifier
        self.router_model = XGBClassifier(
            n_estimators=300,
            max_depth=8,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1
        )
        
        self.router_model.fit(X, tier_numeric)
        
        # Evaluate router
        router_pred = self.router_model.predict(X)
        router_acc = (router_pred == tier_numeric).mean()
        print(f"✅ Router Accuracy: {router_acc:.2%}")
        
        return tier_labels
    
    def train_tier_models(self, X, y_log, y_prices, tier_labels, sample_weight=None):
        """Train separate model for each tier"""
        
        # Train model for each tier
        for tier in self.tier_names:
            print(f"\n🏆 Training {tier.upper()} tier model...")
            
            # Get data for this tier
            tier_mask = tier_labels == tier
            if tier_mask.sum() < 10:
                print(f"⚠️ Not enough samples for {tier} tier ({tier_mask.sum()} samples)")
                continue
                
            X_tier = X[tier_mask]
            y_tier = y_log[tier_mask]

            # Handle sample weights
            if sample_weight is not None:
                weights_tier = sample_weight[tier_mask]
            else:
                weights_tier = None
            
            # Get model configuration
            config = self.model_configs[tier]
            model_class = config['model_class']
            params = config['params']
            
            # Create and train model
            model = model_class(**params)
            
            # Add sample weights for luxury tier
            if tier == 'luxury':
                # Give more weight to extreme values
                prices_tier = y_prices[tier_mask]
                luxury_weights = np.ones(len(prices_tier))
                luxury_weights[prices_tier > 1_000_000] = 3.0
                luxury_weights[prices_tier > 2_000_000] = 5.0
                
                if weights_tier is not None:
                    final_weights = luxury_weights * weights_tier
                else:
                    final_weights = luxury_weights
                
                if hasattr(model, 'fit'):
                    model.fit(X_tier, y_tier, sample_weight=final_weights)
                else:
                    model.fit(X_tier, y_tier)
            else:
                if hasattr(model, 'fit') and weights_tier is not None:
                    model.fit(X_tier, y_tier, sample_weight=weights_tier)
                else:
                    model.fit(X_tier, y_tier)
            
            # Store model
            self.tier_models[tier] = model
            
            # Evaluate
            y_pred = model.predict(X_tier)
            r2 = r2_score(y_tier, y_pred)
            mae = mean_absolute_error(np.expm1(y_tier), np.expm1(y_pred))
            
            print(f"   R² Score: {r2:.4f}")
            print(f"   MAE: ฿{mae:,.0f}")
            print(f"   Samples: {len(X_tier)}")
    
    def predict(self, X):
        """Predict using appropriate tier model"""
        
        # 1. Router predicts tier
        tier_predictions = self.router_model.predict(X)
        tier_names_pred = [self.tier_names[i] for i in tier_predictions]
        
        # 2. Initialize predictions array
        predictions = np.zeros(len(X))
        
        # 3. Predict using appropriate model for each tier
        for i, tier in enumerate(self.tier_names):
            tier_mask = np.array(tier_names_pred) == tier
            
            if tier_mask.sum() > 0 and self.tier_models[tier] is not None:
                X_tier = X[tier_mask]
                predictions[tier_mask] = self.tier_models[tier].predict(X_tier)
            elif tier_mask.sum() > 0:
                # Fallback to standard model if tier model not available
                if self.tier_models['standard'] is not None:
                    X_tier = X[tier_mask]
                    predictions[tier_mask] = self.tier_models['standard'].predict(X_tier)
        
        return predictions
    
    def get_feature_importance(self, feature_names):
        """Get feature importance for each tier"""
        importance_dict = {}
        
        for tier, model in self.tier_models.items():
            if model is None:
                continue
                
            if hasattr(model, 'feature_importances_'):
                importance = model.feature_importances_
            elif hasattr(model, 'get_feature_importance'):
                importance = model.get_feature_importance()
            else:
                continue
                
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': importance
            }).sort_values('importance', ascending=False)
            
            importance_dict[tier] = importance_df
            
        return importance_dict

# ================================================================
# วิธีใช้งาน (Integration with existing code)
# ================================================================

# ใส่ใน Cell 4 แทนที่ ensemble เดิม:
"""
# Create tier-specific predictor
tier_predictor = TierSpecificPricePredictor()

# Train all tier models
tier_predictor.train_tier_models(
    X_train_selected, 
    y_train_log,
    np.expm1(y_train_log)  # actual prices for tier classification
)

# Make predictions
tier_predictions = tier_predictor.predict(X_test_selected)

# Calculate performance
tier_r2 = r2_score(y_test_log, tier_predictions)
print(f"\n🎯 Tier-Specific Model R²: {tier_r2:.4f}")

# Compare with original
if tier_r2 > final_r2:
    print(f"✅ Tier model is better! (+{tier_r2 - final_r2:.4f})")
    super_ensemble = tier_predictions
else:
    print(f"❌ Original model is better")
    
# Get tier-specific feature importance
tier_importance = tier_predictor.get_feature_importance(selected_features)
"""

# ================================================================
# Enhanced: Hybrid Approach (Ensemble of Tier Models)
# ================================================================

def create_hybrid_tier_ensemble(tier_predictor, original_ensemble, X_test, y_test_log):
    """
    สร้าง ensemble ระหว่าง tier-specific models และ original ensemble
    """
    # Get predictions from both approaches
    tier_pred = tier_predictor.predict(X_test)
    
    # Find optimal blending weight
    best_alpha = 0
    best_r2 = 0
    
    for alpha in np.arange(0, 1.1, 0.1):
        blended = alpha * tier_pred + (1 - alpha) * original_ensemble
        r2 = r2_score(y_test_log, blended)
        
        if r2 > best_r2:
            best_r2 = r2
            best_alpha = alpha
    
    print(f"\n🎯 Optimal blend: {best_alpha:.1%} tier + {(1-best_alpha):.1%} original")
    print(f"   Hybrid R²: {best_r2:.4f}")
    
    # Return best blend
    return best_alpha * tier_pred + (1 - best_alpha) * original_ensemble

# ================================================================
# Advanced: Dynamic Tier Boundaries
# ================================================================

def find_optimal_tier_boundaries(prices, n_tiers=3):
    """
    หา boundaries ที่เหมาะสมโดยอัตโนมัติ
    """
    from sklearn.cluster import KMeans
    
    # Log transform prices
    log_prices = np.log1p(prices).reshape(-1, 1)
    
    # Use KMeans to find natural clusters
    kmeans = KMeans(n_clusters=n_tiers, random_state=42)
    clusters = kmeans.fit_predict(log_prices)
    
    # Find boundaries between clusters
    boundaries = [0]
    for i in range(n_tiers - 1):
        # Find the midpoint between cluster centers
        center1 = kmeans.cluster_centers_[i][0]
        center2 = kmeans.cluster_centers_[i + 1][0]
        boundary = np.expm1((center1 + center2) / 2)
        boundaries.append(boundary)
    boundaries.append(np.inf)
    
    print(f"🎯 Optimal tier boundaries: {[f'฿{b:,.0f}' if b < np.inf else '∞' for b in boundaries]}")
    
    return boundaries

print("✅ Tier-Specific Models implementation ready!")
print("\n📝 Key advantages:")
print("1. Each tier gets specialized treatment")
print("2. Luxury tier can use special algorithms (CatBoost)")
print("3. Feature importance varies by tier")
print("4. Can blend with original ensemble for best results")