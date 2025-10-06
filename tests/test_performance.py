# 📍 วางไว้ที่: ML_Project_Refactored/tests/test_performance.py

import unittest
import pandas as pd
import numpy as np
import time
import memory_profiler
import sys
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.features import create_masterpiece_features
from src.model_utils import create_base_models, AdvancedPreprocessor

class TestPerformance(unittest.TestCase):
    """Performance and stress tests for the ML system"""
    
    def setUp(self):
        """Set up test environment"""
        self.time_threshold = {
            'feature_creation': 10.0,    # seconds for 1000 samples
            'preprocessing': 5.0,        # seconds for 1000 samples  
            'prediction': 1.0,           # seconds for 1000 samples
            'batch_prediction': 5.0      # seconds for 10000 samples
        }
        
        # Memory thresholds (MB)
        self.memory_threshold = {
            'feature_creation': 500,     # MB for 10000 samples
            'model_loading': 1000,       # MB for all models
            'prediction': 200            # MB for 10000 predictions
        }
    
    def test_feature_creation_performance(self):
        """Test feature creation performance"""
        # Create test data
        n_samples = 1000
        test_data = pd.DataFrame({
            'phone_number': [f'08{str(i).zfill(8)}' for i in range(n_samples)],
            'price': np.random.uniform(10000, 1000000, n_samples)
        })
        
        # Time feature creation
        start_time = time.time()
        features = create_masterpiece_features(test_data)
        elapsed_time = time.time() - start_time
        
        print(f"\n⏱️ Feature creation for {n_samples} samples: {elapsed_time:.2f}s")
        
        # Check performance
        self.assertLess(elapsed_time, self.time_threshold['feature_creation'],
                       f"Feature creation too slow: {elapsed_time:.2f}s")
        
        # Check output
        self.assertEqual(len(features), n_samples)
        self.assertGreater(len(features.columns), 200)
    
    def test_preprocessing_performance(self):
        """Test preprocessing performance"""
        # Create synthetic data
        n_samples = 1000
        n_features = 250
        
        X = pd.DataFrame(
            np.random.randn(n_samples, n_features),
            columns=[f'feature_{i}' for i in range(n_features)]
        )
        y = np.random.randn(n_samples)
        
        # Time preprocessing
        preprocessor = AdvancedPreprocessor(method='hybrid')
        
        start_time = time.time()
        X_processed = preprocessor.fit_transform(X, y)
        elapsed_time = time.time() - start_time
        
        print(f"\n⏱️ Preprocessing {n_samples}x{n_features}: {elapsed_time:.2f}s")
        
        self.assertLess(elapsed_time, self.time_threshold['preprocessing'])
    
    def test_batch_prediction_performance(self):
        """Test batch prediction performance"""
        # Create large batch of phone numbers
        n_samples = 10000
        test_phones = pd.DataFrame({
            'phone_number': [f'08{str(i).zfill(8)}' for i in range(n_samples)],
            'price': [0] * n_samples  # Dummy prices
        })
        
        # Mock a simple model for testing
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor(n_estimators=10, n_jobs=-1)
        
        # Create features (subset for speed)
        features_subset = pd.DataFrame(
            np.random.randn(n_samples, 50),
            columns=[f'feature_{i}' for i in range(50)]
        )
        
        # Fit model
        model.fit(features_subset[:100], np.random.randn(100))
        
        # Time batch prediction
        start_time = time.time()
        predictions = model.predict(features_subset)
        elapsed_time = time.time() - start_time
        
        print(f"\n⏱️ Batch prediction for {n_samples} samples: {elapsed_time:.2f}s")
        print(f"   Throughput: {n_samples/elapsed_time:.0f} predictions/second")
        
        self.assertLess(elapsed_time, self.time_threshold['batch_prediction'])
    
    def test_concurrent_predictions(self):
        """Test concurrent prediction handling"""
        n_concurrent = 10
        n_samples_per_request = 100
        
        def make_prediction(request_id):
            """Simulate prediction request"""
            X = pd.DataFrame(
                np.random.randn(n_samples_per_request, 50),
                columns=[f'feature_{i}' for i in range(50)]
            )
            
            # Mock prediction
            predictions = np.random.randn(n_samples_per_request)
            return request_id, len(predictions)
        
        # Test thread-based concurrency
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_prediction, i) for i in range(n_concurrent)]
            results = [f.result() for f in futures]
        thread_time = time.time() - start_time
        
        print(f"\n🔄 Thread-based concurrent predictions: {thread_time:.2f}s")
        self.assertEqual(len(results), n_concurrent)
        
        # Test process-based concurrency
        start_time = time.time()
        with ProcessPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_prediction, i) for i in range(n_concurrent)]
            results = [f.result() for f in futures]
        process_time = time.time() - start_time
        
        print(f"🔄 Process-based concurrent predictions: {process_time:.2f}s")
        self.assertEqual(len(results), n_concurrent)
    
    def test_memory_usage(self):
        """Test memory usage for large datasets"""
        # Skip if memory_profiler not available
        try:
            from memory_profiler import memory_usage
        except ImportError:
            self.skipTest("memory_profiler not installed")
        
        def create_features_mem_test():
            """Function to test memory usage"""
            n_samples = 10000
            test_data = pd.DataFrame({
                'phone_number': [f'08{str(i).zfill(8)}' for i in range(n_samples)],
                'price': np.random.uniform(10000, 1000000, n_samples)
            })
            features = create_masterpiece_features(test_data)
            return features
        
        # Measure memory usage
        mem_usage = memory_usage(create_features_mem_test)
        max_memory = max(mem_usage) - min(mem_usage)
        
        print(f"\n💾 Memory usage for 10k samples: {max_memory:.1f} MB")
        
        self.assertLess(max_memory, self.memory_threshold['feature_creation'],
                       f"Memory usage too high: {max_memory:.1f} MB")
    
    def test_stress_extreme_values(self):
        """Test system with extreme values"""
        # Test with very high prices
        extreme_data = pd.DataFrame({
            'phone_number': ['0999999999', '0888888888', '0777777777'],
            'price': [1e10, 1e12, 1e15]  # Extremely high prices
        })
        
        try:
            features = create_masterpiece_features(extreme_data)
            self.assertEqual(len(features), 3)
            # Check no inf or nan values
            self.assertFalse(features.isin([np.inf, -np.inf]).any().any())
            self.assertFalse(features.isnull().any().any())
        except Exception as e:
            self.fail(f"Failed on extreme values: {str(e)}")
    
    def test_stress_malformed_data(self):
        """Test system with malformed data"""
        # Various malformed inputs
        malformed_cases = [
            # Missing values
            pd.DataFrame({
                'phone_number': ['0812345678', None, '0823456789'],
                'price': [10000, 20000, None]
            }),
            # Invalid phone numbers
            pd.DataFrame({
                'phone_number': ['123', 'abcdefghij', '0812345678'],
                'price': [10000, 20000, 30000]
            }),
            # Empty dataframe
            pd.DataFrame(columns=['phone_number', 'price']),
            # Duplicate entries
            pd.DataFrame({
                'phone_number': ['0812345678'] * 5,
                'price': [10000, 20000, 30000, 40000, 50000]
            })
        ]
        
        for i, data in enumerate(malformed_cases):
            try:
                if len(data) > 0:
                    # Should handle gracefully without crashing
                    result = create_masterpiece_features(data)
                    self.assertIsNotNone(result)
                print(f"✅ Handled malformed case {i+1}")
            except Exception as e:
                # Should raise meaningful errors
                self.assertIsInstance(e, (ValueError, KeyError, TypeError))

if __name__ == '__main__':
    unittest.main(verbosity=2)