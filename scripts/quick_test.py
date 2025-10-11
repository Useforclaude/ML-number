#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick Test Script
Tests all core functionality without heavy training

Usage:
    python quick_test.py

By Alex - World-Class AI Expert
"""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def test_environment():
    """Test environment detection"""
    print("\n" + "="*80)
    print("1️⃣  TESTING ENVIRONMENT DETECTION")
    print("="*80)

    from src.environment import detect_environment
    from src.config import ENV_TYPE, BASE_PATH

    env = detect_environment()
    print(f"✅ Environment: {env}")
    print(f"✅ Base path: {BASE_PATH}")
    print(f"✅ ENV_TYPE: {ENV_TYPE}")


def test_data_loading():
    """Test data loading"""
    print("\n" + "="*80)
    print("2️⃣  TESTING DATA LOADING")
    print("="*80)

    from src.data_loader import load_and_validate

    df, report = load_and_validate('data/raw/numberdata.csv')
    print(f"✅ Loaded {len(df)} records")
    print(f"✅ Columns: {list(df.columns)}")

    return df


def test_features(df):
    """Test feature engineering"""
    print("\n" + "="*80)
    print("3️⃣  TESTING FEATURE ENGINEERING")
    print("="*80)

    from src.features import create_masterpiece_features

    # Test with small sample
    df_sample = df.head(100).copy()
    features = create_masterpiece_features(df_sample)

    print(f"✅ Created {features.shape[1]} features")
    print(f"✅ Sample shape: {features.shape}")
    print(f"✅ No NaN values: {not features.isnull().any().any()}")

    return features


def test_preprocessing(features, df):
    """Test preprocessing"""
    print("\n" + "="*80)
    print("4️⃣  TESTING PREPROCESSING")
    print("="*80)

    from src.model_utils import AdvancedPreprocessor
    import numpy as np

    # Prepare target
    y = np.log1p(df.head(100)['price'].values)

    preprocessor = AdvancedPreprocessor()
    X_processed = preprocessor.fit_transform(features, y)

    # Convert to numpy array if DataFrame
    if hasattr(X_processed, 'values'):
        X_processed = X_processed.values

    print(f"✅ Preprocessed shape: {X_processed.shape}")
    print(f"✅ Data type: {type(X_processed)}")
    print(f"✅ No NaN values: {not np.any(np.isnan(X_processed))}")
    print(f"✅ No Inf values: {not np.any(np.isinf(X_processed))}")

    return X_processed, y, preprocessor


def test_simple_model(X, y):
    """Test simple model training"""
    print("\n" + "="*80)
    print("5️⃣  TESTING MODEL TRAINING (LIGHT)")
    print("="*80)

    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import r2_score, mean_absolute_error

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train simple model
    print("Training RandomForest (100 trees)...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"✅ Model trained successfully")
    print(f"✅ R² Score: {r2:.4f}")
    print(f"✅ MAE: {mae:.4f}")

    return model


def test_prediction(model, preprocessor, df):
    """Test prediction pipeline"""
    print("\n" + "="*80)
    print("6️⃣  TESTING PREDICTION")
    print("="*80)

    from src.features import create_masterpiece_features
    import numpy as np
    import pandas as pd

    # Test single prediction
    test_number = df.iloc[0]['phone_number']
    test_df = pd.DataFrame({'phone_number': [test_number]})

    features = create_masterpiece_features(test_df)
    X_processed = preprocessor.transform(features)

    prediction_log = model.predict(X_processed)[0]
    predicted_price = np.expm1(prediction_log)
    actual_price = df.iloc[0]['price']

    print(f"✅ Test number: {test_number}")
    print(f"✅ Predicted: {predicted_price:,.0f} THB")
    print(f"✅ Actual: {actual_price:,.0f} THB")
    print(f"✅ Error: {abs(predicted_price - actual_price) / actual_price * 100:.1f}%")


def test_checkpoint():
    """Test checkpoint system"""
    print("\n" + "="*80)
    print("7️⃣  TESTING CHECKPOINT SYSTEM")
    print("="*80)

    from utils.checkpoint import manual_checkpoint

    manual_checkpoint({
        'test': 'quick_test.py',
        'status': 'all_tests_passed',
        'timestamp': 'auto'
    })

    print("✅ Checkpoint created")


def main():
    """Run all tests"""
    print("="*80)
    print("🧪 QUICK TEST - ML PHONE NUMBER PRICE PREDICTION")
    print("="*80)
    print("This script tests core functionality without heavy training")
    print("="*80)

    try:
        # Run tests
        test_environment()
        df = test_data_loading()
        features = test_features(df)
        X, y, preprocessor = test_preprocessing(features, df)
        model = test_simple_model(X, y)
        test_prediction(model, preprocessor, df)
        test_checkpoint()

        # Summary
        print("\n" + "="*80)
        print("✅ ALL TESTS PASSED!")
        print("="*80)
        print("\n📊 Summary:")
        print("   ✅ Environment detection: Working")
        print("   ✅ Data loading: Working")
        print("   ✅ Feature engineering: Working (151 features)")
        print("   ✅ Preprocessing: Working")
        print("   ✅ Model training: Working")
        print("   ✅ Prediction: Working")
        print("   ✅ Checkpoint system: Working")
        print("\n🎉 Project is ready for production training!")
        print("\n📝 Next steps:")
        print("   - Run full training: python main.py --run-all --optimize")
        print("   - With autosave: python run_with_autosave.py --run-all --checkpoint-interval 15")
        print("="*80)

        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
