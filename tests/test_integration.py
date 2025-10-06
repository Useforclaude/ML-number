# 📍 วางไว้ที่: ML_Project_Refactored/tests/test_integration.py

import unittest
import pandas as pd
import numpy as np
import os
import sys
import tempfile
import joblib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestIntegrationPipeline(unittest.TestCase):
    """Integration tests for the complete ML pipeline"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for test outputs
        self.temp_dir = tempfile.mkdtemp()
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'phone_number': [
                '0888888888', '0812345678', '0823456789', '0834567890',
                '0845678901', '0856789012', '0867890123', '0878901234',
                '0889012345', '0890123456', '0811111111', '0822222222',
                '0833333333', '0844444444', '0855555555', '0866666666',
                '0877777777', '0899999999', '0800000000', '0812121212'
            ],
            'price': [
                1000000, 500000, 100000, 50000,
                30000, 25000, 20000, 15000,
                12000, 10000, 300000, 250000,
                200000, 80000, 150000, 180000,
                220000, 2000000, 400000, 160000
            ]
        })
        
        # Save sample data
        self.data_path = os.path.join(self.temp_dir, 'test_data.csv')
        self.sample_data.to_csv(self.data_path, index=False)
    
    def test_complete_pipeline(self):
        """Test the complete pipeline from data loading to prediction"""
        try:
            # Import required modules
            from src.data_handler import load_and_clean_data
            from src.features import create_masterpiece_features
            from src.model_utils import (
                enhanced_feature_selection, AdvancedPreprocessor,
                create_base_models
            )
            
            # Step 1: Load and clean data
            df_cleaned = load_and_clean_data(self.data_path)
            self.assertIsNotNone(df_cleaned)
            self.assertGreater(len(df_cleaned), 0)
            
            # Step 2: Feature engineering
            df_featured = create_masterpiece_features(df_cleaned)
            feature_count = len(df_featured.columns) - 3  # Exclude phone, price, weight
            self.assertGreater(feature_count, 100)
            
            # Step 3: Prepare for training
            X = df_featured.drop(columns=['phone_number', 'price', 'sample_weight'])
            y = np.log1p(df_featured['price'])
            
            # Check for NaN values
            self.assertFalse(X.isnull().any().any())
            self.assertFalse(y.isnull().any())
            
            # Step 4: Feature selection
            selected_features, scores = enhanced_feature_selection(X, y, n_features=50)
            self.assertEqual(len(selected_features), 50)
            
            # Step 5: Preprocessing
            preprocessor = AdvancedPreprocessor(method='hybrid')
            X_processed = preprocessor.fit_transform(X[selected_features], y)
            self.assertEqual(X_processed.shape[0], len(X))
            
        except Exception as e:
            self.fail(f"Pipeline failed with error: {str(e)}")
    
    def test_model_save_load(self):
        """Test model saving and loading"""
        try:
            from sklearn.ensemble import RandomForestRegressor
            
            # Create and train a simple model
            model = RandomForestRegressor(n_estimators=10, random_state=42)
            X = np.random.randn(100, 10)
            y = np.random.randn(100)
            model.fit(X, y)
            
            # Save model
            model_path = os.path.join(self.temp_dir, 'test_model.pkl')
            model_data = {
                'model': model,
                'feature_names': [f'feature_{i}' for i in range(10)],
                'model_name': 'test_rf',
                'r2_score': 0.85,
                'config': {'test': True}
            }
            joblib.dump(model_data, model_path)
            
            # Load model
            loaded_data = joblib.load(model_path)
            self.assertIsNotNone(loaded_data['model'])
            self.assertEqual(loaded_data['model_name'], 'test_rf')
            self.assertEqual(len(loaded_data['feature_names']), 10)
            
            # Test prediction
            predictions = loaded_data['model'].predict(X[:5])
            self.assertEqual(len(predictions), 5)
            
        except Exception as e:
            self.fail(f"Model save/load failed: {str(e)}")
    
    def test_prediction_pipeline(self):
        """Test end-to-end prediction for new phone numbers"""
        try:
            # Create mock trained model and preprocessor
            from sklearn.ensemble import RandomForestRegressor
            from src.features import create_masterpiece_features
            
            # Train a simple model
            df_featured = create_masterpiece_features(self.sample_data)
            X = df_featured.drop(columns=['phone_number', 'price', 'sample_weight'])
            y = np.log1p(df_featured['price'])
            
            # Select top features (simplified)
            feature_cols = X.columns[:20].tolist()
            
            model = RandomForestRegressor(n_estimators=10, random_state=42)
            model.fit(X[feature_cols], y)
            
            # Test prediction on new numbers
            new_phones = pd.DataFrame({
                'phone_number': ['0888888888', '0812345678', '0899999999'],
                'price': [0, 0, 0]  # Dummy prices
            })
            
            # Create features for new phones
            new_features = create_masterpiece_features(new_phones)
            X_new = new_features[feature_cols]
            
            # Make predictions
            predictions_log = model.predict(X_new)
            predictions = np.expm1(predictions_log)
            
            # Validate predictions
            self.assertEqual(len(predictions), 3)
            self.assertTrue(all(p > 0 for p in predictions))
            
            # Premium numbers should have higher predictions
            self.assertGreater(predictions[0], predictions[1])  # 0888888888 > 0812345678
            self.assertGreater(predictions[2], predictions[1])  # 0899999999 > 0812345678
            
        except Exception as e:
            self.fail(f"Prediction pipeline failed: {str(e)}")
    
    def test_error_handling(self):
        """Test error handling in the pipeline"""
        # Test with invalid data
        invalid_data = pd.DataFrame({
            'wrong_column': ['abc', 'def'],
            'another_wrong': [1, 2]
        })
        
        invalid_path = os.path.join(self.temp_dir, 'invalid.csv')
        invalid_data.to_csv(invalid_path, index=False)
        
        try:
            from src.data_handler import load_and_clean_data
            # Should handle missing columns gracefully
            result = load_and_clean_data(invalid_path)
            # Depending on implementation, might return None or raise specific exception
        except Exception as e:
            # Should raise a meaningful exception
            self.assertIsInstance(e, (KeyError, ValueError))
    
    def tearDown(self):
        """Clean up temporary files"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    unittest.main()