#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test All Imports
Verify that all imports work correctly across the project

Run: python tests/test_imports.py
"""
import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_imports():
    """Test all critical imports"""
    print("="*80)
    print("🧪 TESTING ALL IMPORTS")
    print("="*80)

    errors = []

    # Test 1: Environment
    print("\n1. Testing environment module...")
    try:
        from src.environment import EnvironmentDetector, setup_environment, detect_environment
        print("   ✅ src.environment")
    except Exception as e:
        errors.append(f"src.environment: {str(e)}")
        print(f"   ❌ src.environment: {str(e)}")

    # Test 2: Config
    print("\n2. Testing config module...")
    try:
        from src.config import (
            CONFIG, MODEL_CONFIG, DATA_CONFIG, BATCH_CONFIG,
            API_CONFIG, LOGGING_CONFIG, BASE_PATH, DATA_PATH,
            MODEL_PATH, RESULTS_PATH, ENV_TYPE
        )
        print("   ✅ src.config (all configs)")
        print(f"      ENV_TYPE: {ENV_TYPE}")
        print(f"      BASE_PATH: {BASE_PATH}")
    except Exception as e:
        errors.append(f"src.config: {str(e)}")
        print(f"   ❌ src.config: {str(e)}")

    # Test 3: Data Handler
    print("\n3. Testing data_handler module...")
    try:
        from src.data_handler import (
            load_and_clean_data, find_phone_column, find_price_column,
            clean_phone_number
        )
        print("   ✅ src.data_handler")
    except Exception as e:
        errors.append(f"src.data_handler: {str(e)}")
        print(f"   ❌ src.data_handler: {str(e)}")

    # Test 4: Data Loader
    print("\n4. Testing data_loader module...")
    try:
        from src.data_loader import (
            load_data_multi_format, validate_data,
            auto_detect_phone_column, auto_detect_price_column,
            load_and_validate
        )
        print("   ✅ src.data_loader")
    except Exception as e:
        errors.append(f"src.data_loader: {str(e)}")
        print(f"   ❌ src.data_loader: {str(e)}")

    # Test 5: Features
    print("\n5. Testing features module...")
    try:
        from src.features import create_masterpiece_features, create_all_features
        print("   ✅ src.features")
    except Exception as e:
        errors.append(f"src.features: {str(e)}")
        print(f"   ❌ src.features: {str(e)}")

    # Test 6: Data Splitter
    print("\n6. Testing data_splitter module...")
    try:
        from src.data_splitter import split_data_stratified
        print("   ✅ src.data_splitter")
    except Exception as e:
        errors.append(f"src.data_splitter: {str(e)}")
        print(f"   ❌ src.data_splitter: {str(e)}")

    # Test 7: Model Utils
    print("\n7. Testing model_utils module...")
    try:
        from src.model_utils import (
            AdvancedPreprocessor, enhanced_feature_selection,
            create_polynomial_features, create_interaction_features
        )
        print("   ✅ src.model_utils")
    except Exception as e:
        errors.append(f"src.model_utils: {str(e)}")
        print(f"   ❌ src.model_utils: {str(e)}")

    # Test 8: Train
    print("\n8. Testing train module...")
    try:
        from src.train import train_all_models, create_ensemble_models
        print("   ✅ src.train")
    except Exception as e:
        errors.append(f"src.train: {str(e)}")
        print(f"   ❌ src.train: {str(e)}")

    # Test 9: Tier Models
    print("\n9. Testing tier_models module...")
    try:
        from src.tier_models import TierSpecificPricePredictor
        print("   ✅ src.tier_models")
    except Exception as e:
        errors.append(f"src.tier_models: {str(e)}")
        print(f"   ❌ src.tier_models: {str(e)}")

    # Test 10: Evaluate
    print("\n10. Testing evaluate module...")
    try:
        from src.evaluate import (
            evaluate_ensemble_predictions, analyze_predictions,
            generate_evaluation_report
        )
        print("   ✅ src.evaluate")
    except Exception as e:
        errors.append(f"src.evaluate: {str(e)}")
        print(f"   ❌ src.evaluate: {str(e)}")

    # Test 11: Visualize
    print("\n11. Testing visualize module...")
    try:
        from src.visualize import (
            plot_model_comparison, plot_feature_importance,
            plot_error_distribution, create_dashboard
        )
        print("   ✅ src.visualize")
    except Exception as e:
        errors.append(f"src.visualize: {str(e)}")
        print(f"   ❌ src.visualize: {str(e)}")

    # Test 12: API
    print("\n12. Testing api modules...")
    try:
        from api.prediction import PredictionPipeline
        print("   ✅ api.prediction")
    except Exception as e:
        errors.append(f"api.prediction: {str(e)}")
        print(f"   ❌ api.prediction: {str(e)}")

    try:
        from api.app import create_app
        print("   ✅ api.app")
    except Exception as e:
        errors.append(f"api.app: {str(e)}")
        print(f"   ❌ api.app: {str(e)}")

    # Test 13: Utils
    print("\n13. Testing utils modules...")
    try:
        from utils.helpers import setup_logging, timer, memory_usage
        print("   ✅ utils.helpers")
    except Exception as e:
        errors.append(f"utils.helpers: {str(e)}")
        print(f"   ❌ utils.helpers: {str(e)}")

    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)

    if errors:
        print(f"\n❌ {len(errors)} import(s) FAILED:")
        for error in errors:
            print(f"   - {error}")
        print("\n⚠️  CRITICAL: Fix these imports before proceeding!")
        return False
    else:
        print("\n✅ ALL IMPORTS PASSED!")
        print("\n🎉 Project structure is correct and ready to use!")
        return True


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
