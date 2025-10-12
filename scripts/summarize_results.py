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
            'val_r2': checkpoint.get('r2_score', 0.0),
            'mae': checkpoint.get('mae', 0.0),
            'rmse': checkpoint.get('rmse', 0.0),
            'time': checkpoint.get('training_time_hours', 0.0),
            'timestamp': checkpoint.get('timestamp', 'Unknown'),
            'params': checkpoint.get('params', {}),
            'test_r2': checkpoint.get('test_r2'),
            'test_mae': checkpoint.get('test_mae'),
            'test_rmse': checkpoint.get('test_rmse')
        }
    except Exception as e:
        print(f"⚠️  Failed to load {checkpoint_path.name}: {e}")
        return None

def main():
    print("\n" + "="*80)
    print("📊 TRAINING RESULTS SUMMARY")
    print("="*80)

    # Candidate checkpoint directories (local + shared workspace)
    checkpoint_dirs = [
        project_root / "models" / "checkpoints",
        Path("/storage/number-ML/models/checkpoints"),
    ]
    checkpoint_dirs = [d for d in checkpoint_dirs if d.exists()]

    if not checkpoint_dirs:
        print("❌ No checkpoint directory found!")
        print("   Checked:")
        for d in set(checkpoint_dirs):
            print(f"   - {d}")
        return 1

    def find_checkpoint_path(filename):
        """Return the most recent checkpoint path among candidates"""
        candidates = [
            d / filename for d in checkpoint_dirs if (d / filename).exists()
        ]
        if not candidates:
            return None
        return max(candidates, key=lambda p: p.stat().st_mtime)

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
        filepath = find_checkpoint_path(filename)
        if filepath is not None and filepath.exists():
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

                displayed_r2 = info['test_r2'] if info['test_r2'] is not None else info['val_r2']
                print(f"✅ {model_name:15s} | "
                      f"Val R²={info['val_r2']:.4f} | "
                      f"Test R²={displayed_r2:.4f} | "
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
    print(f"{'Model':<15} | {'Val R²':>8} | {'Test R²':>8} | {'Val MAE':>9} | {'Test MAE':>9} | {'Time':>8}")
    print("-"*80)

    # Sort by best available R² score (prefer test if available)
    def score_key(info):
        return info['test_r2'] if info['test_r2'] is not None else info['val_r2']

    sorted_results = sorted(results.items(), key=lambda x: score_key(x[1]), reverse=True)

    for model_name, info in sorted_results:
        test_r2 = info['test_r2']
        test_mae = info['test_mae']
        test_r2_str = f"{test_r2:.4f}" if test_r2 is not None else "n/a"
        test_mae_str = f"{test_mae:.2f}" if test_mae is not None else "n/a"
        print(f"{model_name:<15} | {info['val_r2']:>8.4f} | {test_r2_str:>8} | "
              f"{info['mae']:>9.2f} | {test_mae_str:>9} | {format_duration(info['time']):>8}")

    # Best model
    if sorted_results:
        best_model, best_info = sorted_results[0]
        best_score = score_key(best_info)
        print("\n" + "="*80)
        print(f"🏆 BEST MODEL: {best_model}")
        print("="*80)
        print(f"   Validation R²: {best_info['val_r2']:.4f}")
        if best_info['test_r2'] is not None:
            print(f"   Test R²:       {best_info['test_r2']:.4f}")
            print(f"   Test MAE:      {best_info['test_mae']:.2f}")
            print(f"   Test RMSE:     {best_info['test_rmse']:.2f}")
        print(f"   Val MAE:       {best_info['mae']:.2f}")
        print(f"   Val RMSE:      {best_info['rmse']:.2f}")
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
            if find_checkpoint_path(filename) is None:
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
