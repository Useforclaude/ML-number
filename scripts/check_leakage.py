#!/usr/bin/env python3
"""
Data Leakage Detection Script
Check if R² = 0.9999 is due to overfitting or data leakage
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import BASE_PATH

def main():
    print("\n" + "="*80)
    print("🔍 DATA LEAKAGE DETECTION")
    print("="*80)

    # Load checkpoint
    checkpoint_path = "models/checkpoints/random_forest_checkpoint.pkl"

    if not os.path.exists(checkpoint_path):
        print("❌ Checkpoint not found!")
        return 1

    print("\n📂 Loading checkpoint...")
    checkpoint = joblib.load(checkpoint_path)

    model = checkpoint['model']
    preprocessor = checkpoint.get('preprocessor')
    r2_val = checkpoint['r2_score']

    print(f"✅ Loaded model: {type(model).__name__}")
    print(f"   Validation R²: {r2_val:.6f}")

    # Check 1: Feature importance
    print("\n" + "="*80)
    print("CHECK 1: Top 10 Most Important Features")
    print("="*80)

    if hasattr(model, 'feature_importances_'):
        feature_names = checkpoint.get('feature_names',
                                      [f'feature_{i}' for i in range(len(model.feature_importances_))])

        importances = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)

        print("\nTop 10 features:")
        for i, row in importances.head(10).iterrows():
            print(f"   {row['feature']:40s} {row['importance']:.6f}")

        # Check for suspicious features
        suspicious = []
        for feat in importances.head(20)['feature']:
            feat_lower = feat.lower()
            if any(word in feat_lower for word in ['price', 'target', 'label', 'actual', 'real']):
                suspicious.append(feat)

        if suspicious:
            print(f"\n⚠️  SUSPICIOUS FEATURES FOUND:")
            for feat in suspicious:
                print(f"   - {feat}")
            print("\n   These might cause data leakage!")
        else:
            print("\n✅ No obviously suspicious feature names")

    # Check 2: Model complexity
    print("\n" + "="*80)
    print("CHECK 2: Model Complexity")
    print("="*80)

    if hasattr(model, 'n_estimators'):
        print(f"   n_estimators: {model.n_estimators}")
    if hasattr(model, 'max_depth'):
        print(f"   max_depth: {model.max_depth}")
    if hasattr(model, 'min_samples_split'):
        print(f"   min_samples_split: {model.min_samples_split}")
    if hasattr(model, 'min_samples_leaf'):
        print(f"   min_samples_leaf: {model.min_samples_leaf}")

    # Check 3: Load data and test on REAL test set
    print("\n" + "="*80)
    print("CHECK 3: Test on REAL Test Set (Never Seen Before)")
    print("="*80)

    try:
        from src.data_handler import load_and_clean_data
        from training.main import run_feature_pipeline
        from sklearn.model_selection import train_test_split

        # Load data
        df_raw, df_cleaned = load_and_clean_data(
            file_path='/notebooks/ML-number/data/raw/numberdata.csv',
            filter_outliers_param=True,
            max_price=100000
        )

        # Create same split as training
        price_bins = pd.qcut(df_cleaned['price'], q=5, labels=False, duplicates='drop')
        train_indices, test_indices = train_test_split(
            np.arange(len(df_cleaned)),
            test_size=0.2,
            stratify=price_bins,
            random_state=42
        )

        # Run feature pipeline
        X, y_log, sample_weights = run_feature_pipeline(
            df_cleaned,
            train_indices=train_indices
        )

        # Get test data
        X_test = X.iloc[test_indices]
        y_test = pd.Series(np.expm1(y_log.iloc[test_indices]))  # Actual prices

        # Preprocess test data
        X_test_processed = preprocessor.transform(X_test)

        # Clean NaN/Inf
        X_test_processed.replace([np.inf, -np.inf], np.nan, inplace=True)
        X_test_processed.fillna(X_test_processed.median(), inplace=True)

        # Predict on test set
        y_test_pred = model.predict(X_test_processed)

        # Calculate metrics
        r2_test = r2_score(y_test, y_test_pred)
        mae_test = mean_absolute_error(y_test, y_test_pred)
        rmse_test = np.sqrt(mean_squared_error(y_test, y_test_pred))

        print(f"\n📊 Test Set Results:")
        print(f"   Test samples: {len(y_test)}")
        print(f"   R² Score:  {r2_test:.6f}")
        print(f"   MAE:       {mae_test:.2f}")
        print(f"   RMSE:      {rmse_test:.2f}")

        # Analysis
        print(f"\n🔍 Analysis:")
        print(f"   Validation R²: {r2_val:.6f}")
        print(f"   Test R²:       {r2_test:.6f}")
        print(f"   Difference:    {abs(r2_val - r2_test):.6f}")

        if abs(r2_val - r2_test) > 0.10:
            print(f"\n🚨 OVERFITTING DETECTED!")
            print(f"   R² dropped by {abs(r2_val - r2_test):.2%} on test set")
            print(f"   Model memorized validation data!")
        elif r2_test > 0.95:
            print(f"\n⚠️  TEST R² TOO HIGH!")
            print(f"   Possible data leakage in features")
            print(f"   Check top 10 important features above")
        elif r2_test > 0.85:
            print(f"\n✅ GOOD PERFORMANCE!")
            print(f"   Model generalizes well to unseen data")
        else:
            print(f"\n⚠️  PERFORMANCE DROP")
            print(f"   Test R² = {r2_test:.6f} is lower than expected")

        # Check predictions distribution
        print(f"\n📈 Prediction Distribution:")
        print(f"   Actual prices:    min={y_test.min():,.0f}, max={y_test.max():,.0f}, mean={y_test.mean():,.0f}")
        print(f"   Predicted prices: min={y_test_pred.min():,.0f}, max={y_test_pred.max():,.0f}, mean={y_test_pred.mean():,.0f}")

        # Calculate errors by price range
        df_results = pd.DataFrame({
            'actual': y_test,
            'predicted': y_test_pred,
            'error': np.abs(y_test - y_test_pred)
        })

        print(f"\n📊 Errors by Price Range:")
        for lower, upper in [(0, 5000), (5000, 10000), (10000, 20000), (20000, 100000)]:
            mask = (df_results['actual'] >= lower) & (df_results['actual'] < upper)
            if mask.sum() > 0:
                mae_range = df_results[mask]['error'].mean()
                print(f"   ฿{lower:,}-{upper:,}: MAE = {mae_range:,.0f} ({mask.sum()} samples)")

    except Exception as e:
        print(f"❌ Failed to test on test set: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*80)
    print("✅ LEAKAGE CHECK COMPLETE")
    print("="*80)

    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
