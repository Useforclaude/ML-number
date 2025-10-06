# 📍 วางไว้ที่: ML_Project_Refactored/tests/test_data_splitter.py

import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_splitter import (
    PremiumPhoneDataSplitter,
    StratifiedPhoneSplitter,
    TimeSeriesPhoneSplitter,
    AdvancedCrossValidator,
    validate_split,
    get_split_summary
)

class TestDataSplitter(unittest.TestCase):
    """Unit tests for data splitting functionality"""
    
    def setUp(self):
        """Set up test data"""
        np.random.seed(42)
        
        # Create sample data with different price tiers
        self.test_data = pd.DataFrame({
            'phone_number': [f'08{str(i).zfill(8)}' for i in range(1000)],
            'price': np.concatenate([
                np.random.uniform(5000, 50000, 700),      # Standard
                np.random.uniform(50000, 200000, 200),    # Premium  
                np.random.uniform(200000, 2000000, 100)   # Ultra-premium
            ])
        })
        
        # Add time-based data
        self.test_data['date'] = pd.date_range('2023-01-01', periods=1000, freq='D')
        
        # Create features
        self.X = self.test_data[['phone_number']].copy()
        self.y = self.test_data['price'].copy()
    
    def test_premium_phone_splitter(self):
        """Test PremiumPhoneDataSplitter"""
        splitter = PremiumPhoneDataSplitter(
            test_size=0.2,
            premium_threshold=100000,
            ensure_premium_in_test=True
        )
        
        X_train, X_test, y_train, y_test = splitter.split(self.X, self.y)
        
        # Check split proportions
        self.assertAlmostEqual(len(X_test) / len(self.X), 0.2, delta=0.05)
        
        # Check premium phones in test set
        premium_in_test = (y_test > 100000).sum()
        self.assertGreater(premium_in_test, 0, "Should have premium phones in test set")
        
        # Check no overlap
        train_indices = set(X_train.index)
        test_indices = set(X_test.index)
        self.assertEqual(len(train_indices.intersection(test_indices)), 0)
    
    def test_stratified_splitter(self):
        """Test StratifiedPhoneSplitter"""
        splitter = StratifiedPhoneSplitter(
            test_size=0.2,
            n_strata=5,
            min_samples_per_stratum=2
        )
        
        X_train, X_test, y_train, y_test = splitter.split(self.X, self.y)
        
        # Check that price distribution is similar
        train_mean = y_train.mean()
        test_mean = y_test.mean()
        relative_diff = abs(train_mean - test_mean) / train_mean
        self.assertLess(relative_diff, 0.1, "Price distributions should be similar")
        
        # Check stratification
        train_quantiles = np.percentile(y_train, [25, 50, 75])
        test_quantiles = np.percentile(y_test, [25, 50, 75])
        
        for tq, teq in zip(train_quantiles, test_quantiles):
            self.assertAlmostEqual(tq, teq, delta=teq * 0.2)
    
    def test_time_series_splitter(self):
        """Test TimeSeriesPhoneSplitter"""
        splitter = TimeSeriesPhoneSplitter(
            test_size=0.2,
            gap_days=7,
            ensure_price_coverage=True
        )
        
        # Add temporal data
        X_with_time = self.X.copy()
        X_with_time['date'] = self.test_data['date']
        
        splits = splitter.split(X_with_time, self.y, time_col='date')
        X_train, X_test, y_train, y_test = splits
        
        # Check temporal ordering
        max_train_date = X_train['date'].max()
        min_test_date = X_test['date'].min()
        gap = (min_test_date - max_train_date).days
        
        self.assertGreaterEqual(gap, 7, "Should have gap between train and test")
        
        # Check price coverage
        train_price_range = (y_train.min(), y_train.max())
        test_price_range = (y_test.min(), y_test.max())
        
        # Test should have reasonable price coverage
        self.assertGreater(test_price_range[1], train_price_range[0] * 0.5)
    
    def test_advanced_cross_validator(self):
        """Test AdvancedCrossValidator"""
        cv = AdvancedCrossValidator(
            n_splits=5,
            validation_strategy='stratified'
        )
        
        splits = list(cv.split(self.X, self.y))
        
        # Check number of splits
        self.assertEqual(len(splits), 5)
        
        # Check no overlap between train and validation
        for train_idx, val_idx in splits:
            overlap = set(train_idx).intersection(set(val_idx))
            self.assertEqual(len(overlap), 0)
        
        # Check all indices are used
        all_indices = set()
        for train_idx, val_idx in splits:
            all_indices.update(train_idx)
            all_indices.update(val_idx)
        self.assertEqual(len(all_indices), len(self.X))
    
    def test_validate_split_function(self):
        """Test split validation function"""
        X_train, X_test, y_train, y_test = self.X[:800], self.X[800:], self.y[:800], self.y[800:]
        
        # Should pass validation
        result = validate_split(X_train, X_test, y_train, y_test)
        self.assertTrue(result)
        
        # Test with mismatched lengths
        with self.assertRaises(AssertionError):
            validate_split(X_train[:-10], X_test, y_train, y_test)
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        # Test with very small dataset
        small_X = self.X[:10]
        small_y = self.y[:10]
        
        splitter = PremiumPhoneDataSplitter(test_size=0.2)
        X_train, X_test, y_train, y_test = splitter.split(small_X, small_y)
        
        self.assertGreater(len(X_train), 0)
        self.assertGreater(len(X_test), 0)
        
        # Test with all same prices
        same_price_y = pd.Series([50000] * 100)
        X_train, X_test, y_train, y_test = splitter.split(self.X[:100], same_price_y)
        
        self.assertEqual(len(X_train) + len(X_test), 100)

if __name__ == '__main__':
    unittest.main()