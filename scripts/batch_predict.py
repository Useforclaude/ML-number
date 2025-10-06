#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Batch Prediction Script
Predict prices for thousands of phone numbers at once

Usage:
    python scripts/batch_predict.py \
        --input data/numbers.csv \
        --output results/predictions.csv \
        --model models/deployed/best_model.pkl

By Alex - World-Class AI Expert
"""
import os
import sys
import argparse
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import BASE_PATH, MODEL_PATH, BATCH_CONFIG
from src.data_loader import load_data_multi_format, auto_detect_phone_column
from src.features import create_masterpiece_features


# ====================================================================================
# BATCH PREDICTION CLASS
# ====================================================================================

class BatchPredictor:
    """Batch prediction for phone number prices"""

    def __init__(self, model_path: str, verbose: bool = True):
        """
        Initialize batch predictor

        Parameters:
        -----------
        model_path : str
            Path to trained model
        verbose : bool
            Print progress messages
        """
        self.model_path = model_path
        self.verbose = verbose
        self.model = None
        self.model_info = {}
        self.feature_names = []
        self.preprocessor = None

        self._load_model()

    def _load_model(self):
        """Load trained model from file"""
        if self.verbose:
            print(f"📦 Loading model from: {self.model_path}")

        try:
            model_data = joblib.load(self.model_path)

            if isinstance(model_data, dict):
                self.model = model_data.get('model')
                self.feature_names = model_data.get('feature_names', [])
                self.preprocessor = model_data.get('preprocessor')
                self.model_info = {
                    'name': model_data.get('model_name', 'Unknown'),
                    'r2_score': model_data.get('r2_score', 0),
                    'timestamp': model_data.get('timestamp', 'Unknown')
                }
            else:
                self.model = model_data

            if self.verbose:
                print(f"✅ Model loaded: {self.model_info.get('name', 'Model')}")
                if 'r2_score' in self.model_info:
                    print(f"   R² Score: {self.model_info['r2_score']:.4f}")

        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")

    def predict_batch(
        self,
        phone_numbers: pd.Series,
        batch_size: int = None,
        show_progress: bool = True
    ) -> np.ndarray:
        """
        Predict prices for batch of phone numbers

        Parameters:
        -----------
        phone_numbers : pd.Series
            Series of phone numbers
        batch_size : int, optional
            Batch size for processing (default from config)
        show_progress : bool
            Show progress bar

        Returns:
        --------
        predictions : np.ndarray
            Predicted prices
        """
        if batch_size is None:
            batch_size = BATCH_CONFIG['batch_size']

        n_total = len(phone_numbers)
        predictions = np.zeros(n_total)

        # Process in batches
        iterator = range(0, n_total, batch_size)
        if show_progress:
            iterator = tqdm(iterator, desc="Predicting", unit="batch")

        for i in iterator:
            batch = phone_numbers.iloc[i:i + batch_size]

            # Create features for batch
            batch_df = pd.DataFrame({'phone_number': batch})
            features_df = create_masterpiece_features(batch_df)

            # Select features used by model
            if self.feature_names:
                # Get available features
                available_features = [f for f in self.feature_names if f in features_df.columns]
                X_batch = features_df[available_features]

                # Add missing features as zeros
                for f in self.feature_names:
                    if f not in available_features:
                        X_batch[f] = 0
            else:
                X_batch = features_df

            # Preprocess if preprocessor available
            if self.preprocessor:
                X_batch = self.preprocessor.transform(X_batch)

            # Predict
            batch_predictions = self.model.predict(X_batch)

            # Convert from log scale if needed
            batch_predictions = np.expm1(batch_predictions)

            predictions[i:i + len(batch)] = batch_predictions

        return predictions

    def predict_from_file(
        self,
        input_path: str,
        output_path: str,
        phone_column: str = None,
        include_confidence: bool = True,
        include_features: bool = False,
        export_format: str = None
    ):
        """
        Predict prices from input file and save to output file

        Parameters:
        -----------
        input_path : str
            Input file path (CSV, TXT, XLS, XLSX, JSON)
        output_path : str
            Output file path
        phone_column : str, optional
            Phone number column name (auto-detected if None)
        include_confidence : bool
            Include confidence intervals
        include_features : bool
            Include selected features in output
        export_format : str, optional
            Export format (auto-detected from output_path)
        """
        if self.verbose:
            print("\n" + "=" * 80)
            print("🚀 BATCH PREDICTION")
            print("=" * 80)
            print(f"Input:  {input_path}")
            print(f"Output: {output_path}")
            print("=" * 80)

        # Load data
        df = load_data_multi_format(input_path)

        if phone_column is None:
            phone_column = auto_detect_phone_column(df)

        phone_numbers = df[phone_column].astype(str)

        # Predict
        predictions = self.predict_batch(phone_numbers)

        # Create output dataframe
        df_output = df.copy()
        df_output['predicted_price'] = predictions.round(0).astype(int)

        # Add confidence intervals if requested
        if include_confidence:
            # Simple confidence interval: ±20%
            df_output['price_low'] = (predictions * 0.8).round(0).astype(int)
            df_output['price_high'] = (predictions * 1.2).round(0).astype(int)
            df_output['confidence'] = 'Medium'  # Can be improved with proper uncertainty estimation

        # Add top features if requested
        if include_features and self.feature_names:
            # Create features
            features_df = create_masterpiece_features(df)

            # Add top 5 most important features
            top_features = self.feature_names[:5] if len(self.feature_names) >= 5 else self.feature_names
            for feat in top_features:
                if feat in features_df.columns:
                    df_output[f'feat_{feat}'] = features_df[feat]

        # Determine export format
        if export_format is None:
            export_format = Path(output_path).suffix.lstrip('.').lower()
            if not export_format:
                export_format = BATCH_CONFIG['default_export_format']

        # Save output
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if export_format == 'csv':
            df_output.to_csv(output_path, index=False, encoding='utf-8-sig')
        elif export_format in ['xlsx', 'xls']:
            df_output.to_excel(output_path, index=False, engine='openpyxl')
        elif export_format == 'json':
            df_output.to_json(output_path, orient='records', indent=2, force_ascii=False)
        else:
            # Default to CSV
            df_output.to_csv(output_path, index=False, encoding='utf-8-sig')

        if self.verbose:
            print(f"\n✅ Predictions saved to: {output_path}")
            print(f"   Format: {export_format.upper()}")
            print(f"   Total predictions: {len(df_output):,}")

            # Show summary statistics
            print(f"\n📊 Price Statistics:")
            print(f"   Min:    {predictions.min():>12,.0f} ฿")
            print(f"   Median: {np.median(predictions):>12,.0f} ฿")
            print(f"   Mean:   {predictions.mean():>12,.0f} ฿")
            print(f"   Max:    {predictions.max():>12,.0f} ฿")

        return df_output


# ====================================================================================
# COMMAND LINE INTERFACE
# ====================================================================================

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Batch prediction for phone number prices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python scripts/batch_predict.py -i data/numbers.csv -o results/predictions.csv

  # Specify model and phone column
  python scripts/batch_predict.py -i data/numbers.csv -o results/predictions.csv \\
      --model models/deployed/best_model.pkl \\
      --phone-column phone_number

  # Include confidence intervals and features
  python scripts/batch_predict.py -i data/numbers.xlsx -o results/predictions.xlsx \\
      --confidence --features

  # Export to JSON
  python scripts/batch_predict.py -i data/numbers.csv -o results/predictions.json \\
      --format json
        """
    )

    # Required arguments
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Input file path (CSV, TXT, XLS, XLSX, JSON)'
    )

    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output file path'
    )

    # Optional arguments
    parser.add_argument(
        '-m', '--model',
        default=None,
        help='Model file path (default: models/deployed/best_model.pkl)'
    )

    parser.add_argument(
        '-p', '--phone-column',
        default=None,
        help='Phone number column name (auto-detected if not specified)'
    )

    parser.add_argument(
        '-b', '--batch-size',
        type=int,
        default=None,
        help=f'Batch size for processing (default: {BATCH_CONFIG["batch_size"]})'
    )

    parser.add_argument(
        '-f', '--format',
        choices=['csv', 'xlsx', 'json'],
        help='Output format (auto-detected from output path if not specified)'
    )

    parser.add_argument(
        '--confidence',
        action='store_true',
        help='Include confidence intervals'
    )

    parser.add_argument(
        '--features',
        action='store_true',
        help='Include top features in output'
    )

    parser.add_argument(
        '--no-progress',
        action='store_true',
        help='Disable progress bar'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Quiet mode (minimal output)'
    )

    args = parser.parse_args()

    # Set default model path
    if args.model is None:
        args.model = str(Path(MODEL_PATH) / 'deployed' / 'best_model.pkl')

    if not Path(args.model).exists():
        print(f"❌ Model not found: {args.model}")
        print(f"   Please train a model first or specify a valid model path")
        sys.exit(1)

    # Create batch predictor
    predictor = BatchPredictor(
        model_path=args.model,
        verbose=not args.quiet
    )

    # Run prediction
    try:
        predictor.predict_from_file(
            input_path=args.input,
            output_path=args.output,
            phone_column=args.phone_column,
            include_confidence=args.confidence,
            include_features=args.features,
            export_format=args.format
        )

        print("\n✅ Batch prediction completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
