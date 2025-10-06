# 📍 วางไว้ที่: ML_Project_Refactored/tests/test_preprocessing.py

import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_handler import (
    clean_phone_number,
    find_phone_column,
    find_price_column,
    load_and_clean_data
)
from src.model_utils import AdvancedPreprocessor

class TestDataPreprocessing(unittest.TestCase):
    """Unit tests for data preprocessing"""
    
    def setUp(self):
        """Set up test data"""
        self.test_data = pd.DataFrame({
            'เบอร์โทรศัพท์': ['081-234-5678', '66812345678', '0812345678', 
                            '812345678', '081 234 5678', '+66812345678'],
            'ราคา': [10000, 20000, 'ติดต่อ', 15000, 25000, 30000]
        })
        
        self.clean_data = pd.DataFrame({
            'phone_number': ['0812345678', '0823456789', '0834567890'],
            'price': [10000, 20000, 30000]
        })
    
    def test_clean_phone_number(self):
        """Test phone number cleaning"""
        # Test various formats
        self.assertEqual(clean_phone_number('081-234-5678'), '0812345678')
        self.assertEqual(clean_phone_number('66812345678'), '0812345678')
        self.assertEqual(clean_phone_number('812345678'), '0812345678')
        self.assertEqual(clean_phone_number('081 234 5678'), '0812345678')
        self.assertEqual(clean_phone_number('+66812345678'), '0812345678')
        
        # Test invalid numbers
        self.assertIsNone(clean_phone_number('12345'))  # Too short
        self.assertIsNone(clean_phone_number(''))  # Empty
    
    def test_find_columns(self):
        """Test column detection"""
        # Test phone column detection
        phone_col = find_phone_column(self.test_data)
        self.assertEqual(phone_col, 'เบอร์โทรศัพท์')
        
        # Test price column detection
        price_col = find_price_column(self.test_data)
        self.assertEqual(price_col, 'ราคา')
    
    def test_advanced_preprocessor(self):
        """Test AdvancedPreprocessor"""
        # Create features first
        X = pd.DataFrame({
            'power_score': [10, 20, 30, 40, 50],
            'count_digits': [5, 7, 3, 8, 6],
            'ratio_feature': [0.1, 0.5, 0.3, 0.8, 0.2],
            'score_feature': [80, 90, 70, 95, 85],
            'binary_feature': [0, 1, 0, 1, 1]
        })
        y = pd.Series([100, 200, 150, 300, 250])
        
        preprocessor = AdvancedPreprocessor(method='hybrid')
        X_transformed = preprocessor.fit_transform(X, y)
        
        # Check output shape
        self.assertEqual(X_transformed.shape[0], X.shape[0])
        
        # Check no NaN values
        self.assertFalse(pd.DataFrame(X_transformed).isnull().any().any())
        
        # Test transform on new data
        X_new = pd.DataFrame({
            'power_score': [15, 25],
            'count_digits': [4, 6],
            'ratio_feature': [0.4, 0.6],
            'score_feature': [75, 88],
            'binary_feature': [1, 0]
        })
        X_new_transformed = preprocessor.transform(X_new)
        self.assertEqual(X_new_transformed.shape[0], X_new.shape[0])
    
    def test_sample_weight_calculation(self):
        """Test sample weight calculation"""
        df = pd.DataFrame({
            'phone_number': ['0888888888', '0812345678', '0823456789'],
            'price': [1000000, 10000, 50000]
        })
        
        # Calculate weights based on price percentiles
        price_percentiles = df['price'].rank(pct=True)
        alpha = 2.5
        base_weight = 0.5
        
        sample_weights = base_weight + (1 - base_weight) * np.exp(alpha * (price_percentiles - 0.5))
        sample_weights = sample_weights / sample_weights.mean()
        
        # Check weight properties
        self.assertAlmostEqual(sample_weights.mean(), 1.0, places=2)
        self.assertGreater(sample_weights.max(), sample_weights.min())
        
        # Premium numbers should have higher weights
        premium_idx = df['price'].idxmax()
        self.assertEqual(sample_weights.idxmax(), premium_idx)

if __name__ == '__main__':
    unittest.main()