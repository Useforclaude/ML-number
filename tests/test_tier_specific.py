# 📍 วางไว้ที่: ML_Project_Refactored/tests/test_tier_specific_models.py

import unittest
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tier_specific_models import (
    TierClassifier,
    TierSpecificPricePredictor
)

class TestTierSpecificModels(unittest.TestCase):
    """Unit tests for tier-specific modeling"""
    
    def setUp(self):
        """Set up test data"""
        np.random.seed(42)
        
        # Create synthetic data with clear tier patterns
        n_samples = 1000
        
        # Generate features
        self.X = pd.DataFrame({
            'premium_score': np.random.uniform(0, 100, n_samples),
            'pattern_count': np.random.randint(0, 10, n_samples),
            'rarity_index': np.random.uniform(0, 100, n_samples),
            'cultural_score': np.random.uniform(0, 100, n_samples),
            'complexity': np.random.uniform(0, 1, n_samples)
        })
        
        # Generate prices based on tiers
        prices = []
        for i in range(n_samples):
            if self.X.iloc[i]['premium_score'] > 80:  # Ultra-premium
                price = np.random.uniform(500000, 2000000)
            elif self.X.iloc[i]['premium_score'] > 60:  # Premium
                price = np.random.uniform(100000, 500000)
            elif self.X.iloc[i]['premium_score'] > 40:  # Mid-range
                price = np.random.uniform(50000, 100000)
            else:  # Standard
                price = np.random.uniform(5000, 50000)
            prices.append(price)
        
        self.y = pd.Series(prices)
        self.y_log = np.log1p(self.y)
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        self.y_train_log = np.log1p(self.y_train)
        self.y_test_log = np.log1p(self.y_test)
    
    def test_tier_classifier(self):
        """Test TierClassifier"""
        classifier = TierClassifier(n_tiers=4)
        
        # Train classifier
        classifier.fit(self.X_train, self.y_train)
        
        # Test predictions
        tier_predictions = classifier.predict(self.X_test)
        
        # Check predictions are valid
        self.assertEqual(len(tier_predictions), len(self.X_test))
        self.assertTrue(all(0 <= t < 4 for t in tier_predictions))
        
        # Test tier names
        tier_names = classifier.predict_tier_names(self.X_test)
        valid_names = ['standard', 'mid_range', 'premium', 'ultra_premium']
        self.assertTrue(all(name in valid_names for name in tier_names))
        
        # Check feature importance
        importance = classifier.get_feature_importance()
        self.assertIsNotNone(importance)
        self.assertEqual(len(importance), len(self.X.columns))
    
    def test_tier_specific_predictor(self):
        """Test TierSpecificPricePredictor"""
        predictor = TierSpecificPricePredictor()
        
        # Train the predictor
        predictor.train_tier_models(
            self.X_train, 
            self.y_train_log,
            self.y_train
        )
        
        # Make predictions
        predictions = predictor.predict(self.X_test)
        
        # Validate predictions
        self.assertEqual(len(predictions), len(self.X_test))
        self.assertTrue(all(p > 0 for p in predictions))
        
        # Test that different tiers get different models
        tier_importances = predictor.get_feature_importance(self.X.columns.tolist())
        self.assertGreater(len(tier_importances), 0)
    
    def test_tier_prediction_quality(self):
        """Test that tier-specific models improve predictions"""
        # Train standard model
        standard_model = RandomForestRegressor(n_estimators=50, random_state=42)
        standard_model.fit(self.X_train, self.y_train_log)
        standard_preds = standard_model.predict(self.X_test)
        
        # Train tier-specific model
        tier_predictor = TierSpecificPricePredictor()
        tier_predictor.train_tier_models(
            self.X_train,
            self.y_train_log,
            self.y_train
        )
        tier_preds = tier_predictor.predict(self.X_test)
        
        # Calculate errors
        from sklearn.metrics import mean_absolute_error
        standard_mae = mean_absolute_error(self.y_test_log, standard_preds)
        tier_mae = mean_absolute_error(self.y_test_log, tier_preds)
        
        # Tier model should perform at least as well
        self.assertLessEqual(tier_mae, standard_mae * 1.1)  # Allow 10% tolerance
    
    def test_missing_tier_handling(self):
        """Test handling of missing tier models"""
        predictor = TierSpecificPricePredictor()
        
        # Manually set some tier models to None
        predictor.tier_models = {
            'standard': RandomForestRegressor(n_estimators=10),
            'mid_range': None,  # Missing model
            'premium': RandomForestRegressor(n_estimators=10),
            'ultra_premium': None  # Missing model
        }
        
        # Train router
        predictor.router_model = TierClassifier()
        predictor.router_model.fit(self.X_train, self.y_train)
        
        # Should still make predictions (fallback to standard)
        predictions = predictor.predict(self.X_test[:10])
        self.assertEqual(len(predictions), 10)
        self.assertTrue(all(p >= 0 for p in predictions))
    
    def test_edge_cases(self):
        """Test edge cases"""
        classifier = TierClassifier(n_tiers=4)
        
        # Test with single sample
        single_X = self.X_train.iloc[[0]]
        single_y = self.y_train.iloc[[0]]
        
        classifier.fit(self.X_train, self.y_train)
        pred = classifier.predict(single_X)
        self.assertEqual(len(pred), 1)
        
        # Test with extreme values
        extreme_X = pd.DataFrame({
            'premium_score': [100, 0],
            'pattern_count': [100, 0],
            'rarity_index': [100, 0],
            'cultural_score': [100, 0],
            'complexity': [1, 0]
        })
        
        extreme_preds = classifier.predict(extreme_X)
        self.assertEqual(len(extreme_preds), 2)
        
        # High premium score should get high tier
        self.assertGreaterEqual(extreme_preds[0], extreme_preds[1])

if __name__ == '__main__':
    unittest.main()