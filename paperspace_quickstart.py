#!/usr/bin/env python3
"""
Paperspace Quick Start Script
Run this in Jupyter Notebook/Lab terminal after cloning project
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run shell command and show output"""
    print(f"\n{'='*80}")
    print(f"🔧 {description}")
    print(f"{'='*80}")
    print(f"Command: {cmd}")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ Success!")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ Error!")
        if result.stderr:
            print(result.stderr)

    return result.returncode == 0

def main():
    print("="*80)
    print("📘 PAPERSPACE QUICK START")
    print("="*80)
    print("This script will:")
    print("  1. Fix blinker dependency conflict")
    print("  2. Install essential ML libraries")
    print("  3. Verify installation")
    print("  4. Check GPU availability")
    print("="*80)

    # Ask user confirmation
    response = input("\nContinue? (y/n): ")
    if response.lower() != 'y':
        print("Aborted.")
        return

    # Step 1: Fix blinker
    success = run_command(
        "pip install --ignore-installed blinker",
        "Fixing blinker conflict"
    )

    # Step 2: Install essential libraries
    libraries = [
        ("lightgbm==3.3.5", "LightGBM"),
        ("catboost==1.2.8", "CatBoost"),
        ("optuna==3.6.2", "Optuna")
    ]

    for lib, name in libraries:
        run_command(
            f"pip install {lib}",
            f"Installing {name}"
        )

    # Step 3: Verify installation
    print(f"\n{'='*80}")
    print("🔍 VERIFICATION")
    print(f"{'='*80}")

    test_imports = [
        ("lightgbm", "LightGBM"),
        ("catboost", "CatBoost"),
        ("optuna", "Optuna"),
        ("xgboost", "XGBoost"),
        ("sklearn", "scikit-learn"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy")
    ]

    all_ok = True
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - Not installed")
            all_ok = False

    # Step 4: Check GPU
    print(f"\n{'='*80}")
    print("🖥️  GPU CHECK")
    print(f"{'='*80}")

    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=name,memory.total,utilization.gpu",
         "--format=csv,noheader"],
        capture_output=True,
        text=True,
        timeout=5
    )

    if result.returncode == 0:
        print(f"✅ GPU Detected:")
        print(f"   {result.stdout.strip()}")
    else:
        print("⚠️  No GPU detected")
        print("   Training will use CPU (slower but works)")
        print("   To enable GPU:")
        print("     1. Stop notebook")
        print("     2. Settings → Instance Type → Free-GPU or P4000/P5000")
        print("     3. Start notebook again")

    # Step 5: Check data file
    print(f"\n{'='*80}")
    print("📊 DATA FILE CHECK")
    print(f"{'='*80}")

    data_path = Path("/storage/ML-number/data/raw/numberdata.csv")
    if data_path.exists():
        size_kb = data_path.stat().st_size / 1024
        print(f"✅ Data file found!")
        print(f"   Location: {data_path}")
        print(f"   Size: {size_kb:.1f} KB")

        # Count rows
        with open(data_path) as f:
            row_count = sum(1 for line in f)
        print(f"   Rows: {row_count} (including header)")
    else:
        print(f"❌ Data file not found!")
        print(f"   Expected location: {data_path}")
        print(f"\n   ⚠️  TO FIX:")
        print(f"     1. Create directory: mkdir -p /storage/ML-number/data/raw")
        print(f"     2. Upload numberdata.csv via Jupyter UI:")
        print(f"        - Navigate to /storage/ML-number/data/raw/")
        print(f"        - Right-click → Upload Files")
        print(f"        - Select numberdata.csv")

    # Final summary
    print(f"\n{'='*80}")
    print("📋 SUMMARY")
    print(f"{'='*80}")

    if all_ok and data_path.exists():
        print("✅ All checks passed!")
        print("\n🎯 NEXT STEPS:")
        print("   1. Open Jupyter Notebook/Lab")
        print("   2. Create new notebook: train_paperspace.ipynb")
        print("   3. Copy cells from PAPERSPACE_COMPLETE_GUIDE.md")
        print("   4. Run cells 1-4 to start training")
        print("\n📚 Documentation:")
        print("   - Complete guide: /storage/ML-number/PAPERSPACE_COMPLETE_GUIDE.md")
        print("   - Setup docs: /storage/ML-number/PAPERSPACE_SETUP.md")
    else:
        print("⚠️  Some issues found - please fix them first")
        print("\n🔧 TO FIX:")
        if not all_ok:
            print("   - Retry: pip install -r requirements.txt")
        if not data_path.exists():
            print("   - Upload numberdata.csv to /storage/ML-number/data/raw/")

    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
