#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Single Phone Number Prediction Script
Quick price prediction for a single phone number

Usage:
    python scripts/predict_single.py 0812345678
    python scripts/predict_single.py 0899999999 --model models/deployed/best_model.pkl
    python scripts/predict_single.py 0856565656 --explain

By Alex - World-Class AI Expert
"""
import os
import sys
import argparse
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import MODEL_PATH
from src.features import create_masterpiece_features


# ====================================================================================
# SINGLE PREDICTION FUNCTION
# ====================================================================================

def predict_single(
    phone_number: str,
    model_path: str,
    explain: bool = False,
    verbose: bool = True
) -> dict:
    """
    Predict price for a single phone number

    Parameters:
    -----------
    phone_number : str
        10-digit phone number
    model_path : str
        Path to trained model
    explain : bool
        Show feature explanations
    verbose : bool
        Print detailed output

    Returns:
    --------
    result : dict
        Prediction result with price, confidence, and features
    """
    # Validate phone number
    phone_clean = str(phone_number).strip().replace('-', '').replace(' ', '')

    if not (len(phone_clean) == 10 and phone_clean.isdigit()):
        raise ValueError(f"Invalid phone number: {phone_number}. Must be 10 digits.")

    # Load model
    if verbose:
        print(f"📱 Phone Number: {phone_clean}")
        print(f"📦 Loading model...")

    model_data = joblib.load(model_path)

    if isinstance(model_data, dict):
        model = model_data.get('model')
        feature_names = model_data.get('feature_names', [])
        preprocessor = model_data.get('preprocessor')
        model_info = {
            'name': model_data.get('model_name', 'Unknown'),
            'r2_score': model_data.get('r2_score', 0)
        }
    else:
        model = model_data
        feature_names = []
        preprocessor = None
        model_info = {'name': 'Model'}

    if verbose:
        print(f"✅ Model loaded: {model_info['name']}")

    # Create features
    if verbose:
        print(f"🔧 Creating features...")

    df = pd.DataFrame({'phone_number': [phone_clean]})
    features_df = create_masterpiece_features(df)

    # Select features
    if feature_names:
        available_features = [f for f in feature_names if f in features_df.columns]
        X = features_df[available_features]

        # Add missing features as zeros
        for f in feature_names:
            if f not in available_features:
                X[f] = 0
    else:
        X = features_df

    # Preprocess
    if preprocessor:
        X = preprocessor.transform(X)

    # Predict
    prediction_log = model.predict(X)[0]
    prediction = np.expm1(prediction_log)

    # Calculate confidence interval (±20%)
    price_low = prediction * 0.8
    price_high = prediction * 1.2

    # Create result
    result = {
        'phone_number': phone_clean,
        'predicted_price': round(prediction, 0),
        'price_low': round(price_low, 0),
        'price_high': round(price_high, 0),
        'model_name': model_info['name'],
        'model_r2': model_info.get('r2_score', 0)
    }

    # Add feature explanations
    if explain and feature_names:
        # Get top 10 features by value
        feature_values = {}
        for i, fname in enumerate(feature_names[:50]):  # Top 50 features
            if fname in features_df.columns:
                feature_values[fname] = features_df[fname].iloc[0]

        # Sort by absolute value
        sorted_features = sorted(
            feature_values.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:10]

        result['top_features'] = sorted_features

    # Print result
    if verbose:
        print("\n" + "=" * 80)
        print("💰 PRICE PREDICTION")
        print("=" * 80)
        print(f"Phone Number:    {phone_clean}")
        print(f"Predicted Price: {result['predicted_price']:>12,.0f} ฿")
        print(f"Price Range:     {result['price_low']:>12,.0f} - {result['price_high']:>12,.0f} ฿")
        print(f"Model:           {result['model_name']}")
        if 'model_r2' in result and result['model_r2'] > 0:
            print(f"Model R² Score:  {result['model_r2']:>12.4f}")
        print("=" * 80)

        if explain and 'top_features' in result:
            print("\n📊 TOP CONTRIBUTING FEATURES:")
            print("-" * 80)
            for i, (feat, val) in enumerate(result['top_features'], 1):
                print(f"{i:2d}. {feat:40s}: {val:>10.2f}")
            print("-" * 80)

    return result


# ====================================================================================
# COMMAND LINE INTERFACE
# ====================================================================================

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Predict price for a single phone number",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python scripts/predict_single.py 0812345678

  # With specific model
  python scripts/predict_single.py 0899999999 --model models/deployed/best_model.pkl

  # With feature explanation
  python scripts/predict_single.py 0856565656 --explain

  # Quiet mode (JSON output only)
  python scripts/predict_single.py 0812345678 --quiet --json
        """
    )

    parser.add_argument(
        'phone_number',
        help='10-digit phone number'
    )

    parser.add_argument(
        '-m', '--model',
        default=None,
        help='Model file path (default: models/deployed/best_model.pkl)'
    )

    parser.add_argument(
        '-e', '--explain',
        action='store_true',
        help='Show feature explanations'
    )

    parser.add_argument(
        '-j', '--json',
        action='store_true',
        help='Output as JSON'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Quiet mode (no verbose output)'
    )

    args = parser.parse_args()

    # Set default model path
    if args.model is None:
        args.model = str(Path(MODEL_PATH) / 'deployed' / 'best_model.pkl')

    if not Path(args.model).exists():
        print(f"❌ Model not found: {args.model}", file=sys.stderr)
        print(f"   Please train a model first or specify a valid model path", file=sys.stderr)
        sys.exit(1)

    # Run prediction
    try:
        result = predict_single(
            phone_number=args.phone_number,
            model_path=args.model,
            explain=args.explain,
            verbose=not args.quiet
        )

        # Output JSON if requested
        if args.json:
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))

        sys.exit(0)

    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        if not args.quiet:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
