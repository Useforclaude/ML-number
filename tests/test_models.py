# 📍 วางไว้ที่: ML_Project_Refactored/tests/test_models.py

import unittest
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.model_utils import (
    create_base_models,
    enhanced_feature_selection,
    HybridFeatureSelector,
    optimize_xgboost,
    optimize_lightgbm,
    AdvancedStackingEnsemble,
    WeightedEnsemble
)

class TestModelTraining(unittest.TestCase):
    """Unit tests for model training components"""
    
    def setUp(self):
        """Set up test data"""
        np.random.seed(42)
        n_samples = 1000
        n_features = 50
        
        # Create synthetic data
        X = pd.DataFrame(
            np.random.randn(n_samples, n_features),
            columns=[f'feature_{i}' for i in range(n_features)]
        )
        # Add some correlation with target
        y = X['feature_0'] * 2 + X['feature_1'] * 1.5 + np.random.randn(n_samples) * 0.1
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
    
    def test_create_base_models(self):
        """Test base model creation"""
        models = create_base_models(best_xgb_params={}, best_lgb_params={}, 
                                  best_cat_params={}, best_rf_params={})
        
        # Check model count
        self.assertGreater(len(models), 5, "Should have at least 5 base models")
        
        # Check model names
        model_names = [name for name, _ in models]
        expected_models = ['XGBoost_Opt', 'LightGBM_Opt', 'CatBoost_Opt', 
                          'RandomForest_Opt', 'ExtraTrees_Opt']
        for expected in expected_models:
            self.assertIn(expected, model_names, f"Missing model: {expected}")
    
    def test_feature_selection(self):
        """Test feature selection methods"""
        # Test enhanced feature selection
        selected_features, scores = enhanced_feature_selection(
            self.X_train, self.y_train, n_features=20
        )
        
        self.assertEqual(len(selected_features), 20)
        self.assertIsInstance(scores, pd.DataFrame)
        self.assertIn('combined_score', scores.columns)
        
        # Test HybridFeatureSelector
        selector = HybridFeatureSelector(n_features=15)
        X_selected = selector.fit_transform(self.X_train, self.y_train)
        
        self.assertEqual(X_selected.shape[1], 15)
        self.assertEqual(X_selected.shape[0], self.X_train.shape[0])
    
    def test_model_optimization(self):
        """Test hyperparameter optimization (with fewer trials)"""
        # Test XGBoost optimization with minimal trials
        best_params = optimize_xgboost(self.X_train, self.y_train, n_trials=2)
        
        required_params = ['n_estimators', 'max_depth', 'learning_rate']
        for param in required_params:
            self.assertIn(param, best_params, f"Missing parameter: {param}")
    
    def test_ensemble_models(self):
        """Test ensemble model creation"""
        # Create dummy predictions
        n_samples = len(self.y_test)
        test_predictions = {
            'Model1': np.random.randn(n_samples),
            'Model2': np.random.randn(n_samples),
            'Model3': np.random.randn(n_samples)
        }
        
        # Test WeightedEnsemble
        ensemble = WeightedEnsemble()
        weights = ensemble.optimize_weights(test_predictions, self.y_test)
        
        self.assertEqual(len(weights), 3)
        self.assertAlmostEqual(sum(weights.values()), 1.0, places=5)
        
        # Test predictions
        ensemble_pred = ensemble.predict(test_predictions)
        self.assertEqual(len(ensemble_pred), n_samples)
    
    def test_stacking_ensemble(self):
        """Test advanced stacking ensemble"""
        # Create simple base models
        from sklearn.linear_model import LinearRegression
        from sklearn.tree import DecisionTreeRegressor
        
        base_models = [
            ('lr', LinearRegression()),
            ('dt', DecisionTreeRegressor(max_depth=3, random_state=42))
        ]
        
        stacking = AdvancedStackingEnsemble(
            base_models=base_models,
            meta_model='ridge',
            use_probas=False,
            n_folds=3
        )
        
        # Fit and predict
        stacking.fit(self.X_train, self.y_train)
        predictions = stacking.predict(self.X_test)
        
        self.assertEqual(len(predictions), len(self.X_test))
        self.assertFalse(np.isnan(predictions).any())

if __name__ == '__main__':
    unittest.main()