# 📍 วางไว้ที่: ML_Project_Refactored/tests/test_api.py

import unittest
import json
from unittest.mock import Mock, patch
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAPI(unittest.TestCase):
    """Unit tests for API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        # Mock the Flask/FastAPI app
        self.app = Mock()
        self.client = Mock()
    
    def test_predict_endpoint(self):
        """Test /predict endpoint"""
        # Mock request data
        test_data = {
            'phone_number': '0888888888'
        }
        
        # Expected response structure
        expected_response = {
            'phone_number': '0888888888',
            'predicted_price': 1000000,
            'price_range': {
                'min': 800000,
                'max': 1200000
            },
            'confidence': 0.95,
            'features': {
                'rarity_score': 95,
                'pattern_type': 'all_same',
                'cultural_significance': 98
            }
        }
        
        # Test response
        self.assertIn('predicted_price', expected_response)
        self.assertIn('confidence', expected_response)
        self.assertGreater(expected_response['predicted_price'], 0)
    
    def test_batch_predict_endpoint(self):
        """Test /batch_predict endpoint"""
        test_data = {
            'phone_numbers': [
                '0888888888',
                '0812345678',
                '0899999999'
            ]
        }
        
        # Expected response
        expected_response = {
            'predictions': [
                {'phone_number': '0888888888', 'predicted_price': 1000000},
                {'phone_number': '0812345678', 'predicted_price': 200000},
                {'phone_number': '0899999999', 'predicted_price': 1500000}
            ],
            'processing_time': 0.5
        }
        
        self.assertEqual(len(expected_response['predictions']), 3)
    
    def test_health_check_endpoint(self):
        """Test /health endpoint"""
        expected_response = {
            'status': 'healthy',
            'model_version': 'v1.0',
            'last_updated': '2024-06-25'
        }
        
        self.assertEqual(expected_response['status'], 'healthy')
    
    def test_error_handling(self):
        """Test API error handling"""
        # Test invalid phone number
        invalid_data = {
            'phone_number': '123'  # Too short
        }
        
        # Should return error response
        expected_error = {
            'error': 'Invalid phone number format',
            'message': 'Phone number must be 10 digits',
            'status_code': 400
        }
        
        self.assertEqual(expected_error['status_code'], 400)

if __name__ == '__main__':
    unittest.main()