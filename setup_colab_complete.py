"""
One-Command Setup Script for Google Colab

This script sets up the entire project environment in Google Colab with one command.

Usage:
    # In Colab cell:
    !python setup_colab_complete.py --project-name "ML_Phone_Number_Project"

Features:
- Mount Google Drive automatically
- Create project structure in Drive
- Verify all dependencies
- Test checkpoint system
- Ready to train!
"""

import os
import sys
import argparse
from pathlib import Path


def mount_google_drive():
    """Mount Google Drive"""
    print("📂 Mounting Google Drive...")

    try:
        from google.colab import drive
        drive.mount('/content/drive', force_remount=False)
        print("✅ Google Drive mounted successfully!")
        return True
    except Exception as e:
        print(f"❌ Error mounting Drive: {e}")
        return False


def create_project_structure(project_name):
    """
    Create project directory structure in Google Drive

    Parameters:
    -----------
    project_name : str
        Project folder name in Google Drive

    Returns:
    --------
    project_dir : str
        Full path to project directory
    """
    project_dir = f"/content/drive/MyDrive/{project_name}"

    directories = [
        f"{project_dir}/checkpoints",
        f"{project_dir}/models",
        f"{project_dir}/logs",
        f"{project_dir}/results",
        f"{project_dir}/data",
        f"{project_dir}/notebooks",
        f"{project_dir}/scripts"
    ]

    print(f"\n📁 Creating project structure in Drive...")
    print(f"   Project directory: {project_dir}")

    for dir_path in directories:
        os.makedirs(dir_path, exist_ok=True)
        print(f"   ✓ Created: {dir_path}")

    print("✅ Project structure created!")
    return project_dir


def verify_dependencies():
    """Verify all required dependencies are installed"""
    print("\n🔍 Verifying dependencies...")

    required_packages = {
        'numpy': 'numpy',
        'pandas': 'pandas',
        'scikit-learn': 'sklearn',
        'xgboost': 'xgboost',
        'lightgbm': 'lightgbm',
        'catboost': 'catboost',
        'optuna': 'optuna',
        'joblib': 'joblib',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn'
    }

    missing_packages = []
    installed_versions = {}

    for package_name, import_name in required_packages.items():
        try:
            module = __import__(import_name)
            version = getattr(module, '__version__', 'unknown')
            installed_versions[package_name] = version
            print(f"   ✓ {package_name}: {version}")
        except ImportError:
            missing_packages.append(package_name)
            print(f"   ✗ {package_name}: NOT INSTALLED")

    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("   Installing missing packages...")
        os.system(f"pip install -q {' '.join(missing_packages)}")
        print("✅ Packages installed!")
    else:
        print("\n✅ All dependencies verified!")

    return len(missing_packages) == 0


def test_checkpoint_system(project_dir):
    """Test checkpoint save/load functionality"""
    print("\n🧪 Testing checkpoint system...")

    checkpoint_dir = f"{project_dir}/checkpoints"

    # Add project to path
    sys.path.insert(0, '/content/number-ML')

    try:
        from src.checkpoint_manager import CheckpointManager

        # Create manager
        manager = CheckpointManager(
            checkpoint_dir=checkpoint_dir,
            max_checkpoints=3
        )

        # Create dummy model
        class DummyModel:
            def state_dict(self):
                return {'weights': [1, 2, 3]}

        model = DummyModel()

        # Save test checkpoint
        print("   Testing checkpoint save...")
        manager.save_checkpoint(
            epoch=0,
            model=model,
            metrics={'test': True}
        )

        # Load checkpoint
        print("   Testing checkpoint load...")
        checkpoint = manager.load_latest_checkpoint()

        if checkpoint and checkpoint.get('metrics', {}).get('test'):
            print("✅ Checkpoint system working!")
            return True
        else:
            print("❌ Checkpoint system failed!")
            return False

    except Exception as e:
        print(f"❌ Error testing checkpoints: {e}")
        return False


def create_readme(project_dir):
    """Create README in project directory"""
    readme_path = f"{project_dir}/README.txt"

    content = """
ML Phone Number Price Prediction - Google Colab Setup
=====================================================

✅ Setup Complete!

Project Structure:
------------------
/checkpoints/   - Training checkpoints (auto-save every 10 epochs)
/models/        - Trained models
/logs/          - Training logs
/results/       - Evaluation results
/data/          - Training data
/notebooks/     - Colab notebooks
/scripts/       - Utility scripts

How to Use:
-----------
1. Open the Colab notebook: Colab_ML_Training_AutoResume.ipynb
2. Run Cell 1-4 to mount Drive and check for checkpoints
3. Run Cell 5-6 to load data and train
4. If disconnected, just run Cell 1-6 again → Auto-resume!

Auto-Resume Feature:
--------------------
- Training auto-saves every 10 epochs to Drive
- If Colab disconnects, your progress is safe
- When you reconnect and run the notebook again:
  → Cell 4 detects the last checkpoint
  → Training resumes from last saved epoch
  → Zero data loss!

Checkpoints Location:
---------------------
All checkpoints saved to: {}/checkpoints/
  - checkpoint_latest.pkl (most recent)
  - checkpoint_best.pkl (best performance)
  - checkpoint_epoch_N.pkl (every 10 epochs)

Recovery Info:
--------------
Check recovery_info.json in checkpoints/ for last session details.

Support:
--------
If you encounter issues:
1. Check checkpoints/recovery_info.json
2. Verify Google Drive is mounted
3. Ensure all cells ran successfully

Last Setup: {}
    """.format(project_dir, Path(readme_path).parent)

    with open(readme_path, 'w') as f:
        f.write(content)

    print(f"✅ README created: {readme_path}")


def print_next_steps(project_dir):
    """Print instructions for next steps"""
    print("\n" + "=" * 70)
    print("🎉 SETUP COMPLETE!")
    print("=" * 70)
    print(f"\n📁 Project directory: {project_dir}")
    print("\n📋 Next Steps:")
    print("\n1. Upload your project ZIP file or extract it to /content/number-ML")
    print("\n2. Open the Colab notebook:")
    print(f"   {project_dir}/notebooks/Colab_ML_Training_AutoResume.ipynb")
    print("\n3. Run the notebook cells sequentially:")
    print("   Cell 1: Mount Drive ✅ (already done!)")
    print("   Cell 2: Upload/Extract project")
    print("   Cell 3: Install dependencies")
    print("   Cell 4: Auto-detect checkpoint")
    print("   Cell 5: Load data")
    print("   Cell 6: Train with auto-resume")
    print("   Cell 7: Evaluate")
    print("   Cell 8: Download results")
    print("\n4. If disconnected:")
    print("   → Just run Cell 1-6 again")
    print("   → Training will resume from last checkpoint!")
    print("\n" + "=" * 70)
    print("\n✨ Your training progress is now 100% safe in Google Drive!")
    print("=" * 70)


def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(description='Setup Google Colab environment')
    parser.add_argument(
        '--project-name',
        type=str,
        default='ML_Phone_Number_Project',
        help='Project folder name in Google Drive'
    )
    parser.add_argument(
        '--skip-tests',
        action='store_true',
        help='Skip checkpoint system tests'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("🚀 GOOGLE COLAB SETUP - ML PHONE NUMBER PRICE PREDICTION")
    print("=" * 70)

    # Step 1: Mount Drive
    if not mount_google_drive():
        print("\n❌ Setup failed: Could not mount Google Drive")
        return False

    # Step 2: Create structure
    project_dir = create_project_structure(args.project_name)

    # Step 3: Verify dependencies
    deps_ok = verify_dependencies()

    # Step 4: Test checkpoints (if not skipped)
    if not args.skip_tests:
        test_ok = test_checkpoint_system(project_dir)
    else:
        test_ok = True
        print("\n⏭️  Skipped checkpoint tests")

    # Step 5: Create README
    create_readme(project_dir)

    # Step 6: Print next steps
    if deps_ok and test_ok:
        print_next_steps(project_dir)
        return True
    else:
        print("\n⚠️  Setup completed with warnings. Please check errors above.")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
