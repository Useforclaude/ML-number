# 📍 วางไว้ที่: ML_Project_Refactored/tests/test_features.py

import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.features import (
    create_masterpiece_features,
    detect_advanced_patterns_v2,
    calculate_mathematical_beauty,
    analyze_cultural_significance,
    calculate_rarity_index,
    analyze_price_tier_features,
    create_market_features
)

class TestFeatureEngineering(unittest.TestCase):
    """Unit tests for feature engineering functions"""
    
    def setUp(self):
        """Set up test data"""
        self.test_phones = pd.DataFrame({
            'phone_number': [
                '0888888888',  # All same digits - premium
                '0812345678',  # Sequential - premium
                '0856565656',  # Alternating pattern
                '0823456789',  # Almost sequential
                '0811111111',  # All same except first 2
                '0999999999',  # All 9s - ultra premium
                '0818181818',  # Perfect repetition
                '0800000000',  # All zeros after prefix
                '0812341234',  # Repeated block
                '0823232323'   # Alternating pattern
            ],
            'price': [1000000, 500000, 200000, 150000, 300000, 
                     2000000, 400000, 250000, 180000, 160000]
        })
    
    def test_pattern_detection(self):
        """Test advanced pattern detection"""
        # Test wave pattern
        patterns = detect_advanced_patterns_v2('0812121212')
        self.assertTrue(patterns['wave_pattern'])
        
        # Test pyramid pattern
        patterns = detect_advanced_patterns_v2('0812344321')
        self.assertTrue(patterns['pyramid_pattern'])
        
        # Test cascade pattern
        patterns = detect_advanced_patterns_v2('0823456789')
        self.assertTrue(patterns['cascade_pattern'])
        
        # Test sandwich pattern
        patterns = detect_advanced_patterns_v2('0812128888')
        self.assertTrue(patterns['sandwich_pattern'])
        
        # Test rhythm pattern
        patterns = detect_advanced_patterns_v2('0812341234')
        self.assertTrue(patterns['rhythm_pattern'])
    
    def test_mathematical_beauty(self):
        """Test mathematical beauty calculation"""
        # Test Fibonacci sequence
        beauty_score = calculate_mathematical_beauty('0811235813')
        self.assertGreater(beauty_score, 50)  # Should have high score
        
        # Test non-mathematical number
        beauty_score = calculate_mathematical_beauty('0812345678')
        self.assertLess(beauty_score, 30)  # Should have lower score
    
    def test_cultural_significance(self):
        """Test cultural significance scoring"""
        # Test lucky Chinese number
        score = analyze_cultural_significance('0888888888')
        self.assertGreater(score, 80)  # 8 is very lucky
        
        # Test unlucky number
        score = analyze_cultural_significance('0844444444')
        self.assertLess(score, 20)  # 4 is unlucky
        
        # Test Thai lucky number
        score = analyze_cultural_significance('0899999999')
        self.assertGreater(score, 70)  # 9 is lucky in Thai
    
    def test_rarity_index(self):
        """Test rarity index calculation"""
        # Test ultra rare number
        rarity = calculate_rarity_index('0999999999')
        self.assertTrue(rarity['is_ultra_rare'])
        self.assertGreater(rarity['rarity_score'], 90)
        
        # Test common number
        rarity = calculate_rarity_index('0812345678')
        self.assertFalse(rarity['is_ultra_rare'])
        self.assertLess(rarity['rarity_score'], 50)
    
    def test_price_tier_features(self):
        """Test price tier analysis"""
        # Test premium tier
        tier_features = analyze_price_tier_features('0888888888')
        self.assertEqual(tier_features['estimated_tier'], 'Premium')
        self.assertGreater(tier_features['price_multiplier'], 5)
        
        # Test standard tier
        tier_features = analyze_price_tier_features('0812345678')
        self.assertIn(tier_features['estimated_tier'], ['Standard', 'Mid-Range'])
        self.assertLess(tier_features['price_multiplier'], 3)
    
    def test_feature_completeness(self):
        """Test that all features are created"""
        features_df = create_masterpiece_features(self.test_phones)
        
        # Check feature count
        feature_count = len(features_df.columns) - 3  # Exclude phone_number, price, sample_weight
        self.assertGreater(feature_count, 200, "Should have at least 200 features")
        
        # Check for key features
        key_features = [
            'wave_pattern_v2', 'mathematical_beauty_score',
            'cultural_significance_score', 'rarity_index',
            'final_premium_score_v4', 'complexity_score'
        ]
        for feature in key_features:
            self.assertIn(feature, features_df.columns, f"Missing key feature: {feature}")
    
    def test_feature_values_range(self):
        """Test that feature values are in expected ranges"""
        features_df = create_masterpiece_features(self.test_phones)
        
        # Check that scores are between 0 and 100
        score_columns = [col for col in features_df.columns if 'score' in col]
        for col in score_columns:
            self.assertTrue(features_df[col].between(0, 100).all(), 
                          f"{col} values should be between 0 and 100")
        
        # Check no NaN values
        self.assertFalse(features_df.isnull().any().any(), 
                        "Features should not contain NaN values")
    
    def test_market_features(self):
        """Test market-based features"""
        # Mock market data
        global MARKET_PATTERN_PRICES, MARKET_PATTERN_POPULARITY
        MARKET_PATTERN_PRICES = {'8888': 50000, '1234': 10000, '5678': 15000}
        MARKET_PATTERN_POPULARITY = {'8888': 100, '1234': 50, '5678': 60}
        
        market_feats = create_market_features('0888888888')
        self.assertGreater(market_feats['market_avg_price'], 0)
        self.assertGreater(market_feats['market_popularity_score'], 0)

if __name__ == '__main__':
    unittest.main()