#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Local Development Setup Script
Sets up the project for local development

Usage:
    python setup_local.py
    python setup_local.py --install-deps
    python setup_local.py --test-only

By Alex - World-Class AI Expert
"""
import os
import sys
import subprocess
from pathlib import Path
import argparse


def check_python_version():
    """Check Python version"""
    print("\n" + "="*80)
    print("🐍 CHECKING PYTHON VERSION")
    print("="*80)

    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)

    print("✅ Python version is compatible")
    return True


def check_venv():
    """Check if virtual environment is activated"""
    print("\n" + "="*80)
    print("📦 CHECKING VIRTUAL ENVIRONMENT")
    print("="*80)

    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )

    if in_venv:
        print(f"✅ Virtual environment is active: {sys.prefix}")
        return True
    else:
        print("⚠️  No virtual environment detected")
        print("   Recommended: activate venv first")
        print("   Command: source .venv/bin/activate  (Linux/Mac)")
        print("            .venv\\Scripts\\activate   (Windows)")
        return False


def install_dependencies(force=False):
    """Install project dependencies"""
    print("\n" + "="*80)
    print("📥 INSTALLING DEPENDENCIES")
    print("="*80)

    requirements_file = Path("requirements.txt")

    if not requirements_file.exists():
        print("❌ requirements.txt not found!")
        return False

    print("Installing from requirements.txt...")

    try:
        cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        if force:
            cmd.append("--force-reinstall")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes max
        )

        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Installation failed:")
            print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("❌ Installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error during installation: {str(e)}")
        return False


def create_directories():
    """Create necessary project directories"""
    print("\n" + "="*80)
    print("📁 CREATING DIRECTORIES")
    print("="*80)

    directories = [
        "data/raw",
        "data/processed",
        "data/features",
        "models/deployed",
        "models/experiments",
        "results/figures",
        "results/reports",
        "results/metrics",
        "logs",
        "checkpoints"
    ]

    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    print(f"✅ Created {len(directories)} directories")
    return True


def test_imports():
    """Test if all imports work"""
    print("\n" + "="*80)
    print("🧪 TESTING IMPORTS")
    print("="*80)

    try:
        # Run the test script
        result = subprocess.run(
            [sys.executable, "tests/test_imports.py"],
            capture_output=True,
            text=True,
            timeout=30
        )

        print(result.stdout)

        if result.returncode == 0:
            print("\n✅ All imports work correctly")
            return True
        else:
            print("\n❌ Some imports failed")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"❌ Error testing imports: {str(e)}")
        return False


def verify_data():
    """Verify data file exists"""
    print("\n" + "="*80)
    print("📊 VERIFYING DATA")
    print("="*80)

    data_file = Path("data/raw/numberdata.csv")

    if data_file.exists():
        file_size = data_file.stat().st_size
        print(f"✅ Data file found: {data_file}")
        print(f"   Size: {file_size:,} bytes")

        # Try to count lines
        try:
            with open(data_file, 'r') as f:
                lines = sum(1 for _ in f)
            print(f"   Lines: {lines:,}")
        except:
            pass

        return True
    else:
        print("⚠️  Data file not found: data/raw/numberdata.csv")
        print("   Please add your data file before training")
        return False


def run_quick_test():
    """Run a quick sanity test"""
    print("\n" + "="*80)
    print("🚀 RUNNING QUICK TEST")
    print("="*80)

    try:
        # Test environment detection
        print("\nTesting environment detection...")
        from src.environment import detect_environment
        env_type, base_path = detect_environment()
        print(f"   Environment: {env_type}")
        print(f"   Base path: {base_path}")

        # Test config loading
        print("\nTesting configuration...")
        from src.config import BASE_PATH, DATA_CONFIG, MODEL_CONFIG
        print(f"   BASE_PATH: {BASE_PATH}")
        print(f"   Supported formats: {DATA_CONFIG['supported_formats']}")
        print(f"   Target R²: {MODEL_CONFIG['target_r2']}")

        print("\n✅ Quick test passed")
        return True

    except Exception as e:
        print(f"\n❌ Quick test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def show_next_steps():
    """Show next steps to user"""
    print("\n" + "="*80)
    print("🎯 NEXT STEPS")
    print("="*80)
    print("""
1. Add your data file:
   cp your_data.csv data/raw/numberdata.csv

2. Run the complete pipeline:
   python main.py --run-all --optimize

3. Or run individual steps:
   python main.py --data                # Load and clean data
   python main.py --features            # Create features
   python main.py --train --optimize    # Train models
   python main.py --evaluate            # Evaluate models

4. Make predictions:
   # Single number
   python scripts/predict_single.py 0812345678

   # Batch prediction
   python scripts/batch_predict.py -i data/numbers.csv -o results/predictions.csv

5. Start API server:
   python main.py --deploy --api-type fastapi --port 8000

For more information, see:
- SESSION_SUMMARY.md
- docs/USAGE_GUIDE.md (coming soon)
- README.md
""")


def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(description="Setup local development environment")
    parser.add_argument("--install-deps", action="store_true", help="Install dependencies")
    parser.add_argument("--force-reinstall", action="store_true", help="Force reinstall dependencies")
    parser.add_argument("--test-only", action="store_true", help="Only run tests, skip setup")
    parser.add_argument("--skip-data-check", action="store_true", help="Skip data file verification")

    args = parser.parse_args()

    print("="*80)
    print("🚀 LOCAL DEVELOPMENT SETUP")
    print("   ML Phone Number Price Prediction")
    print("="*80)

    if args.test_only:
        # Only run tests
        check_python_version()
        test_imports()
        run_quick_test()
        return

    # Full setup
    success = True

    # Step 1: Check Python version
    if not check_python_version():
        success = False

    # Step 2: Check venv
    check_venv()

    # Step 3: Install dependencies
    if args.install_deps or args.force_reinstall:
        if not install_dependencies(force=args.force_reinstall):
            success = False
    else:
        print("\nℹ️  Skipping dependency installation (use --install-deps to install)")

    # Step 4: Create directories
    if not create_directories():
        success = False

    # Step 5: Verify data (optional)
    if not args.skip_data_check:
        verify_data()

    # Step 6: Test imports (if deps installed)
    if args.install_deps or args.force_reinstall:
        if not test_imports():
            success = False

        # Step 7: Run quick test
        if not run_quick_test():
            success = False

    # Summary
    print("\n" + "="*80)
    if success:
        print("✅ SETUP COMPLETE!")
        print("="*80)
        show_next_steps()
    else:
        print("❌ SETUP INCOMPLETE - Please fix the errors above")
        print("="*80)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
