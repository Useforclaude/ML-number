"""
Paperspace Pre-Flight Validation Script
Run this BEFORE training to catch all errors early

Usage:
    python validate_paperspace.py

Or in Jupyter:
    !python /storage/number-ML/validate_paperspace.py
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"{text}")
    print("="*80)


def validate_paperspace_environment():
    """Validate Paperspace setup - catch errors before training"""

    print_header("🔍 PAPERSPACE PRE-FLIGHT VALIDATION")

    errors = []
    warnings = []

    # 1. Check Python path
    print("\n1️⃣  Checking Python path...")
    project_path = '/storage/number-ML'
    if project_path not in sys.path:
        errors.append("Project path not in sys.path")
        print(f"   ❌ {project_path} not in sys.path")
        print(f"      Fix: sys.path.insert(0, '{project_path}')")
    else:
        print(f"   ✅ Python path configured correctly")

    # 2. Check data file exists
    print("\n2️⃣  Checking data file...")
    data_file = '/storage/number-ML/data/raw/numberdata.csv'
    if not os.path.exists(data_file):
        errors.append(f"Data file not found: {data_file}")
        print(f"   ❌ Data file missing: {data_file}")
    else:
        size_mb = os.path.getsize(data_file) / (1024**2)
        print(f"   ✅ Data file found ({size_mb:.1f} MB)")

    # 3. Check GPU availability
    print("\n3️⃣  Checking GPU...")
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print(f"   ✅ GPU: {gpu_name} ({gpu_mem:.1f} GB)")

            # Detect tier
            if 'M4000' in gpu_name:
                print(f"      ℹ️  Tier: Paperspace Free (M4000)")
            elif 'P5000' in gpu_name or 'P4000' in gpu_name:
                print(f"      ℹ️  Tier: Paperspace Pro ($8/month)")
            elif 'RTX' in gpu_name:
                print(f"      ℹ️  Tier: Paperspace Growth")
        else:
            warnings.append("GPU not available - training will be slower on CPU")
            print(f"   ⚠️  GPU not available (will use CPU)")
            print(f"      Check: Notebook Settings → Instance Type → Free-GPU or Pro")
    except ImportError:
        errors.append("PyTorch not installed")
        print(f"   ❌ PyTorch not installed")
        print(f"      Fix: !pip install torch")

    # 4. Check storage space
    print("\n4️⃣  Checking storage...")
    try:
        result = subprocess.run(
            ['df', '-h', '/storage'],
            capture_output=True,
            text=True,
            check=True
        )
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            used = parts[2]
            avail = parts[3]
            percent = parts[4]
            usage_pct = int(percent.rstrip('%'))

            print(f"   Used: {used}, Available: {avail}, Usage: {percent}")

            if usage_pct > 80:
                warnings.append(f"Storage > 80% full ({percent})")
                print(f"   ⚠️  Storage > 80% full - clean up files recommended")
            else:
                print(f"   ✅ Storage OK ({100-usage_pct}% free)")
    except Exception as e:
        warnings.append(f"Could not check storage: {e}")
        print(f"   ⚠️  Could not check storage")

    # 5. Check imports
    print("\n5️⃣  Checking ML libraries...")
    required_libs = {
        'xgboost': 'XGBoost',
        'lightgbm': 'LightGBM',
        'catboost': 'CatBoost',
        'optuna': 'Optuna',
        'sklearn': 'scikit-learn',
        'pandas': 'Pandas',
        'numpy': 'NumPy'
    }
    missing_libs = []

    for lib, name in required_libs.items():
        try:
            __import__(lib)
            print(f"   ✅ {name}")
        except ImportError:
            missing_libs.append(name)
            print(f"   ❌ {name} (not installed)")

    if missing_libs:
        errors.append(f"Missing libraries: {', '.join(missing_libs)}")
        print(f"\n   Fix: !pip install -r /storage/number-ML/requirements.txt")

    # 6. Check directories exist
    print("\n6️⃣  Checking directories...")
    required_dirs = [
        '/storage/number-ML/src',
        '/storage/number-ML/data/raw',
        '/storage/number-ML/checkpoints',
        '/storage/number-ML/models/deployed',
        '/storage/number-ML/results'
    ]

    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
            print(f"   ⚠️  {dir_path} (missing - will create)")
            try:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
                print(f"      ✅ Created: {dir_path}")
            except Exception as e:
                errors.append(f"Could not create {dir_path}: {e}")
        else:
            print(f"   ✅ {dir_path}")

    # 7. Check critical files
    print("\n7️⃣  Checking critical files...")
    critical_files = [
        '/storage/number-ML/src/config.py',
        '/storage/number-ML/src/data_handler.py',
        '/storage/number-ML/src/features.py',
        '/storage/number-ML/src/model_utils.py',
        '/storage/number-ML/src/train_production.py',
    ]

    missing_files = []
    for file_path in critical_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
            print(f"   ❌ {os.path.basename(file_path)} (missing)")
        else:
            print(f"   ✅ {os.path.basename(file_path)}")

    if missing_files:
        errors.append(f"Missing files: {len(missing_files)}")
        print(f"\n   Fix: Re-upload project or run setup_paperspace.py")

    # 8. Check SMARTFIX is included
    print("\n8️⃣  Checking SMARTFIX auto-fallback...")
    model_utils_path = '/storage/number-ML/src/model_utils.py'
    if os.path.exists(model_utils_path):
        with open(model_utils_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'actual_use_gpu' in content and 'Testing LightGBM GPU' in content:
                print(f"   ✅ SMARTFIX auto-fallback mechanism found")
            else:
                warnings.append("SMARTFIX mechanism not found in model_utils.py")
                print(f"   ⚠️  SMARTFIX not found - LightGBM may hang on GPU")
    else:
        errors.append("model_utils.py not found")

    # Summary
    print_header("📋 VALIDATION SUMMARY")

    print(f"\nTotal checks: 8")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if errors:
        print(f"\n❌ ERRORS FOUND ({len(errors)}):")
        for i, error in enumerate(errors, 1):
            print(f"   {i}. {error}")
        print("\n⚠️  FIX ERRORS BEFORE TRAINING!")
        print("\nCommon fixes:")
        print("  1. Run: python /storage/number-ML/setup_paperspace.py")
        print("  2. Install deps: !pip install -r /storage/number-ML/requirements.txt")
        print("  3. Add to Cell 1: sys.path.insert(0, '/storage/number-ML')")
        return False

    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"   {i}. {warning}")
        print("\nℹ️  Warnings can be ignored, but recommended to fix")

    if not errors:
        print("\n✅ ALL CHECKS PASSED - READY TO TRAIN!")
        print("\n🚀 Next steps:")
        print("   1. Run training notebook")
        print("   2. Monitor GPU usage (should be 70-90%)")
        print("   3. Check checkpoints saving every 10 trials")
        print("   4. Expected time: 7-8 hours (Pro) or 10-12 hours (Free)")
        return True


def main():
    """Main entry point"""
    print("\n" + "🖥️ "*30)
    print("PAPERSPACE VALIDATION SCRIPT")
    print("🖥️ "*30)

    # Add project to path (in case not added yet)
    project_path = '/storage/number-ML'
    if project_path not in sys.path:
        sys.path.insert(0, project_path)
        print(f"\n✅ Added {project_path} to Python path")

    # Run validation
    success = validate_paperspace_environment()

    # Exit code
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
