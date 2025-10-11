#!/usr/bin/env python3
"""
Training Results Summary Script
Shows results from all completed model checkpoints
Can run anytime to check progress - no need to wait for all models
"""

import os
import sys
import joblib
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def format_duration(hours):
    """Convert hours to readable format"""
    if hours < 1:
        return f"{hours*60:.0f}m"
    elif hours < 24:
        return f"{hours:.1f}h"
    else:
        days = int(hours / 24)
        remaining_hours = hours % 24
        return f"{days}d {remaining_hours:.1f}h"

def load_checkpoint_info(checkpoint_path):
    """Load checkpoint and extract key metrics"""
    try:
        checkpoint = joblib.load(checkpoint_path)
        return {
            'r2': checkpoint.get('r2_score', 0.0),
            'mae': checkpoint.get('mae', 0.0),
            'rmse': checkpoint.get('rmse', 0.0),
            'time': checkpoint.get('training_time_hours', 0.0),
            'timestamp': checkpoint.get('timestamp', 'Unknown'),
            'params': checkpoint.get('params', {})
        }
    except Exception as e:
        print(f"⚠️  Failed to load {checkpoint_path.name}: {e}")
        return None

def main():
    print("\n" + "="*80)
    print("📊 TRAINING RESULTS SUMMARY")
    print("="*80)

    checkpoint_dir = project_root / "models" / "checkpoints"

    if not checkpoint_dir.exists():
        print("❌ No checkpoint directory found!")
        print(f"   Expected: {checkpoint_dir}")
        return 1

    # Model checkpoint files
    model_files = {
        'XGBoost': 'xgboost_checkpoint.pkl',
        'LightGBM': 'lightgbm_checkpoint.pkl',
        'CatBoost': 'catboost_checkpoint.pkl',
        'RandomForest': 'random_forest_checkpoint.pkl'
    }

    results = {}
    completed_count = 0

    # Load all available checkpoints
    print("\n🔍 Scanning for completed models...\n")

    for model_name, filename in model_files.items():
        filepath = checkpoint_dir / filename
        if filepath.exists():
            info = load_checkpoint_info(filepath)
            if info:
                results[model_name] = info
                completed_count += 1

                # Parse timestamp
                try:
                    ts = datetime.fromisoformat(info['timestamp'])
                    time_str = ts.strftime("%Y-%m-%d %H:%M")
                except:
                    time_str = "Unknown"

                print(f"✅ {model_name:15s} | R²={info['r2']:.4f} | "
                      f"MAE={info['mae']:.2f} | Time={format_duration(info['time'])} | "
                      f"Completed: {time_str}")
        else:
            print(f"⏳ {model_name:15s} | Not trained yet")

    if completed_count == 0:
        print("\n⚠️  No trained models found!")
        print("   Train models first using commands from PAPERSPACE_TRAINING_COMMANDS.md")
        return 1

    # Summary table
    print("\n" + "="*80)
    print("📈 PERFORMANCE COMPARISON")
    print("="*80)
    print(f"{'Model':<15} | {'R² Score':>10} | {'MAE':>8} | {'RMSE':>8} | {'Time':>8}")
    print("-"*80)

    # Sort by R² score (descending)
    sorted_results = sorted(results.items(), key=lambda x: x[1]['r2'], reverse=True)

    for model_name, info in sorted_results:
        print(f"{model_name:<15} | {info['r2']:>10.4f} | {info['mae']:>8.2f} | "
              f"{info['rmse']:>8.2f} | {format_duration(info['time']):>8}")

    # Best model
    if sorted_results:
        best_model, best_info = sorted_results[0]
        print("\n" + "="*80)
        print(f"🏆 BEST MODEL: {best_model}")
        print("="*80)
        print(f"   R² Score:  {best_info['r2']:.4f}")
        print(f"   MAE:       {best_info['mae']:.2f}")
        print(f"   RMSE:      {best_info['rmse']:.2f}")
        print(f"   Time:      {format_duration(best_info['time'])}")

    # Progress tracking
    total_models = len(model_files)
    progress_pct = (completed_count / total_models) * 100

    print("\n" + "="*80)
    print(f"📊 PROGRESS: {completed_count}/{total_models} models completed ({progress_pct:.0f}%)")
    print("="*80)

    if completed_count < total_models:
        print("\n⏳ Remaining models:")
        for model_name, filename in model_files.items():
            filepath = checkpoint_dir / filename
            if not filepath.exists():
                print(f"   - {model_name}")

    # Next steps
    if completed_count == total_models:
        print("\n✅ All models trained! Next step:")
        print("   python training/modular/train_ensemble_only.py")
    else:
        print("\n💡 Continue training remaining models one by one")
        print("   See: PAPERSPACE_TRAINING_COMMANDS.md")

    print("\n" + "="*80)

    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
