"""
Prediction Pipeline for Deployment
By Alex - World-Class AI Expert
"""
import os
import sys
import numpy as np
import pandas as pd
import joblib
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import features module
from src.features import create_masterpiece_features

# ====================================================================================
# PREDICTION PIPELINE CLASS
# ====================================================================================

class PredictionPipeline:
    """
    Production-ready prediction pipeline for phone number price prediction
    """
    
    def __init__(self, model_path=None, config_path=None):
        """
        Initialize prediction pipeline
        
        Parameters:
        -----------
        model_path : str
            Path to saved model file
        config_path : str
            Path to configuration file
        """
        self.model = None
        self.feature_names = None
        self.preprocessor = None
        self.model_info = {}
        
        # Load model if path provided
        if model_path:
            self.load_model(model_path)
        
        # Load config if path provided
        if config_path:
            self.load_config(config_path)
    
    def load_model(self, model_path):
        """Load model from file"""
        try:
            print(f"📦 Loading model from: {model_path}")
            
            # Load model data
            model_data = joblib.load(model_path)
            
            # Extract components based on structure
            if isinstance(model_data, dict):
                # New format with metadata
                self.model = model_data.get('model')
                self.feature_names = model_data.get('feature_names', [])
                self.model_info = {
                    'model_name': model_data.get('model_name', 'Unknown'),
                    'r2_score': model_data.get('r2_score', 0),
                    'timestamp': model_data.get('timestamp', 'Unknown')
                }
            else:
                # Old format - just the model
                self.model = model_data
                self.feature_names = []
                self.model_info = {'model_name': 'Legacy Model'}
            
            print(f"✅ Model loaded successfully: {self.model_info.get('model_name')}")
            
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            raise
    
    def load_config(self, config_path):
        """Load configuration from file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            self.config = config
            print("✅ Configuration loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading config: {str(e)}")
            self.config = {}
    
    def validate_phone_number(self, phone_number):
        """
        Validate phone number format
        
        Parameters:
        -----------
        phone_number : str
            Phone number to validate
        
        Returns:
        --------
        is_valid : bool
            Whether phone number is valid
        cleaned_number : str
            Cleaned phone number
        """
        # Clean phone number
        phone_str = str(phone_number).strip().replace(' ', '').replace('-', '')
        
        # Handle different formats
        if phone_str.startswith('+66'):
            phone_str = '0' + phone_str[3:]
        elif phone_str.startswith('66') and len(phone_str) == 11:
            phone_str = '0' + phone_str[2:]
        elif len(phone_str) == 9 and not phone_str.startswith('0'):
            phone_str = '0' + phone_str
        
        # Validate
        is_valid = (
            len(phone_str) == 10 and 
            phone_str.isdigit() and 
            phone_str[0] == '0'
        )
        
        return is_valid, phone_str if is_valid else None
    
    def predict_single(self, phone_number):
        """
        Predict price for a single phone number
        
        Parameters:
        -----------
        phone_number : str
            Phone number to predict
        
        Returns:
        --------
        result : dict
            Prediction result with metadata
        """
        # Validate phone number
        is_valid, cleaned_number = self.validate_phone_number(phone_number)
        
        if not is_valid:
            return {
                'success': False,
                'error': 'Invalid phone number format',
                'phone_number': phone_number
            }
        
        try:
            # Create dataframe
            df = pd.DataFrame([{
                'phone_number': cleaned_number,
                'price': 0  # Dummy price for feature creation
            }])
            
            # Create features
            features_df = create_masterpiece_features(df)
            
            # Select features if feature names are available
            if self.feature_names:
                # Ensure all required features exist
                missing_features = set(self.feature_names) - set(features_df.columns)
                if missing_features:
                    # Add missing features with default values
                    for feat in missing_features:
                        features_df[feat] = 0
                
                # Select features in correct order
                features_df = features_df[self.feature_names]
            
            # Make prediction (log scale)
            prediction_log = self.model.predict(features_df)[0]
            
            # Convert to price
            predicted_price = np.expm1(prediction_log)
            
            # Get confidence interval (if model supports it)
            confidence_low = predicted_price * 0.8  # Default 80%
            confidence_high = predicted_price * 1.2  # Default 120%
            
            # Determine price tier
            if predicted_price >= 100000:
                tier = 'Ultra Premium'
            elif predicted_price >= 50000:
                tier = 'Premium'
            elif predicted_price >= 20000:
                tier = 'High'
            elif predicted_price >= 5000:
                tier = 'Medium'
            else:
                tier = 'Standard'
            
            # Create result
            result = {
                'success': True,
                'phone_number': cleaned_number,
                'predicted_price': float(predicted_price),
                'price_range': {
                    'low': float(confidence_low),
                    'high': float(confidence_high)
                },
                'tier': tier,
                'model_info': self.model_info,
                'features': {
                    'ending_score': float(features_df.get('ending_score', [0])[0]),
                    'power_sum': float(features_df.get('power_sum', [0])[0]),
                    'special_lucky_score': float(features_df.get('special_lucky_score', [0])[0]),
                    'rarity_score': float(features_df.get('rarity_score', [0])[0])
                },
                'timestamp': datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Prediction error: {str(e)}',
                'phone_number': cleaned_number
            }
    
    def predict_batch(self, phone_numbers):
        """
        Predict prices for multiple phone numbers
        
        Parameters:
        -----------
        phone_numbers : list
            List of phone numbers
        
        Returns:
        --------
        results : list
            List of prediction results
        """
        results = []
        
        # Process each phone number
        for phone in phone_numbers:
            result = self.predict_single(phone)
            results.append(result)
        
        # Summary statistics
        successful = [r for r in results if r['success']]
        
        summary = {
            'total': len(phone_numbers),
            'successful': len(successful),
            'failed': len(results) - len(successful),
            'results': results
        }
        
        if successful:
            prices = [r['predicted_price'] for r in successful]
            summary['statistics'] = {
                'mean_price': np.mean(prices),
                'median_price': np.median(prices),
                'min_price': np.min(prices),
                'max_price': np.max(prices)
            }
        
        return summary
    
    def explain_prediction(self, phone_number):
        """
        Explain prediction for a phone number
        
        Parameters:
        -----------
        phone_number : str
            Phone number to explain
        
        Returns:
        --------
        explanation : dict
            Detailed explanation of prediction
        """
        # First get prediction
        prediction = self.predict_single(phone_number)
        
        if not prediction['success']:
            return prediction
        
        # Validate and clean phone number
        _, cleaned_number = self.validate_phone_number(phone_number)
        
        # Create features
        df = pd.DataFrame([{'phone_number': cleaned_number, 'price': 0}])
        features_df = create_masterpiece_features(df)
        
        # Get feature values
        feature_values = features_df.iloc[0].to_dict()
        
        # Identify key drivers
        key_drivers = []
        
        # Check ending pattern
        ending = cleaned_number[-4:]
        if ending == cleaned_number[-1] * 4:
            key_drivers.append(f"เลขท้าย 4 ตัวซ้ำ ({ending}) - พรีเมี่ยมสูง")
        elif ending[-2:] == ending[-1] * 2:
            key_drivers.append(f"เลขท้ายซ้ำ ({ending[-2:]}) - มงคล")
        
        # Check sequences
        if '1234' in cleaned_number or '5678' in cleaned_number:
            key_drivers.append("มีเลขเรียงกัน - เพิ่มมูลค่า")
        
        # Check lucky numbers
        lucky_count = sum(1 for d in cleaned_number if d in '5689')
        if lucky_count >= 6:
            key_drivers.append(f"เลขมงคลมาก ({lucky_count}/10) - ราคาสูง")
        
        # Create explanation
        explanation = {
            **prediction,
            'explanation': {
                'key_drivers': key_drivers,
                'feature_analysis': {
                    'ความมงคล': {
                        'ending_score': feature_values.get('ending_score', 0),
                        'special_lucky_score': feature_values.get('special_lucky_score', 0),
                        'power_sum': feature_values.get('power_sum', 0)
                    },
                    'ความหายาก': {
                        'rarity_score': feature_values.get('rarity_score', 0),
                        'unique_digits': feature_values.get('unique_digits', 0),
                        'complexity_score': feature_values.get('complexity_score', 0)
                    },
                    'รูปแบบพิเศษ': {
                        'sequence_score': feature_values.get('sequence_score', 0),
                        'mirror_pattern': feature_values.get('mirror_pattern', 0),
                        'wave_pattern': feature_values.get('wave_pattern', 0)
                    }
                }
            }
        }
        
        return explanation

# ====================================================================================
# UTILITY FUNCTIONS
# ====================================================================================

def load_latest_model(model_dir):
    """
    Load the latest model from directory
    
    Parameters:
    -----------
    model_dir : str
        Directory containing models
    
    Returns:
    --------
    pipeline : PredictionPipeline
        Loaded prediction pipeline
    """
    # Look for best_model.pkl first
    best_model_path = os.path.join(model_dir, 'best_model.pkl')
    
    if os.path.exists(best_model_path):
        pipeline = PredictionPipeline(model_path=best_model_path)
        return pipeline
    
    # Otherwise find latest model by timestamp
    model_files = [f for f in os.listdir(model_dir) if f.endswith('.pkl')]
    
    if not model_files:
        raise ValueError(f"No model files found in {model_dir}")
    
    # Sort by modification time
    latest_model = max(model_files, key=lambda f: os.path.getmtime(os.path.join(model_dir, f)))
    
    pipeline = PredictionPipeline(model_path=os.path.join(model_dir, latest_model))
    return pipeline

def create_prediction_service(model_path, config_path=None):
    """
    Create prediction service
    
    Parameters:
    -----------
    model_path : str
        Path to model
    config_path : str, optional
        Path to config
    
    Returns:
    --------
    service : PredictionPipeline
        Prediction service
    """
    service = PredictionPipeline(model_path=model_path, config_path=config_path)
    
    print("\n✅ Prediction service created successfully!")
    print(f"   Model: {service.model_info.get('model_name', 'Unknown')}")
    print(f"   R² Score: {service.model_info.get('r2_score', 0):.4f}")
    
    return service

# ====================================================================================
# EXAMPLE USAGE
# ====================================================================================

if __name__ == "__main__":
    # Example usage
    print("🚀 Phone Number Price Prediction Service")
    print("="*60)
    
    # Load model
    model_path = "../models/deployed/best_model.pkl"
    
    try:
        # Create prediction service
        service = create_prediction_service(model_path)
        
        # Test predictions
        test_numbers = [
            '0812345678',
            '0899999999',
            '0856565656',
            '0987654321'
        ]
        
        print("\n📱 Testing predictions:")
        for number in test_numbers:
            result = service.predict_single(number)
            if result['success']:
                print(f"\n{number}: ฿{result['predicted_price']:,.0f}")
                print(f"   Tier: {result['tier']}")
                print(f"   Range: ฿{result['price_range']['low']:,.0f} - ฿{result['price_range']['high']:,.0f}")
            else:
                print(f"\n{number}: Error - {result['error']}")
        
        # Test batch prediction
        print("\n📊 Testing batch prediction:")
        batch_result = service.predict_batch(test_numbers)
        print(f"   Processed: {batch_result['total']} numbers")
        print(f"   Success: {batch_result['successful']}")
        print(f"   Failed: {batch_result['failed']}")
        
        if 'statistics' in batch_result:
            stats = batch_result['statistics']
            print(f"   Average price: ฿{stats['mean_price']:,.0f}")
            print(f"   Price range: ฿{stats['min_price']:,.0f} - ฿{stats['max_price']:,.0f}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
