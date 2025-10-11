"""
Paperspace Gradient Setup Script
Auto-setup for ML Phone Number Price Prediction Project
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"🚀 {text}")
    print("="*80 + "\n")


def print_success(text):
    """Print success message"""
    print(f"✅ {text}")


def print_error(text):
    """Print error message"""
    print(f"❌ {text}")


def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")


def check_paperspace_environment():
    """Check if running on Paperspace"""
    print_header("Checking Paperspace Environment")

    is_paperspace = False

    # Check environment variables
    paperspace_vars = [
        'PAPERSPACE_NOTEBOOK_REPO_ID',
        'PAPERSPACE_API_KEY',
        'PAPERSPACE_METRIC_WORKLOAD_ID'
    ]

    for var in paperspace_vars:
        if var in os.environ:
            print_success(f"Found Paperspace variable: {var}")
            is_paperspace = True

    # Check for /storage directory
    if os.path.exists('/storage'):
        print_success("Found /storage directory (Paperspace persistent storage)")
        is_paperspace = True

    if not is_paperspace:
        print_error("Not running on Paperspace!")
        print_info("This script is designed for Paperspace Gradient")
        return False

    print_success("Confirmed: Running on Paperspace Gradient!")
    return True


def setup_directories():
    """Create necessary project directories"""
    print_header("Setting Up Directory Structure")

    base_path = Path('/storage/number-ML')

    directories = [
        base_path,
        base_path / 'data' / 'raw',
        base_path / 'data' / 'processed',
        base_path / 'data' / 'features',
        base_path / 'models' / 'deployed',
        base_path / 'models' / 'experiments',
        base_path / 'results' / 'figures',
        base_path / 'results' / 'reports',
        base_path / 'results' / 'metrics',
        base_path / 'logs',
        base_path / 'checkpoints',  # Persistent checkpoints!
        base_path / 'src',
        base_path / 'notebooks',
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print_success(f"Created: {directory}")

    print_success(f"\nBase path: {base_path}")
    return base_path


def install_dependencies():
    """Install required Python packages"""
    print_header("Installing Dependencies")

    # Check if requirements.txt exists
    req_file = Path('requirements.txt')
    if not req_file.exists():
        print_error("requirements.txt not found!")
        return False

    print_info("Installing packages from requirements.txt...")

    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--quiet'],
            check=True
        )
        print_success("All dependencies installed!")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Installation failed: {e}")
        return False


def verify_gpu():
    """Check GPU availability, detect tier, and auto-configure optimal settings"""
    print_header("Verifying GPU Access & Auto-Configuration")

    try:
        import torch

        gpu_config = {
            'has_gpu': False,
            'gpu_name': None,
            'gpu_memory_gb': 0,
            'tier': 'CPU Only',
            'expected_time': '18-24 hours',
            'model_gpu_settings': {
                'xgboost': False,
                'lightgbm': False,
                'catboost': False,
                'randomforest': False  # RF never uses GPU (sklearn)
            }
        }

        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)

            print_success(f"GPU Available: {gpu_name}")
            print_success(f"GPU Memory: {gpu_memory:.1f} GB")

            gpu_config['has_gpu'] = True
            gpu_config['gpu_name'] = gpu_name
            gpu_config['gpu_memory_gb'] = gpu_memory

            # Auto-configure based on GPU performance
            print_info("\n🤖 Auto-configuring model GPU settings...")

            if 'M4000' in gpu_name:
                # M4000: Slow GPU (8 GB)
                # Strategy: Use GPU selectively (only for models that benefit most)
                gpu_config['tier'] = "Paperspace Free"
                gpu_config['expected_time'] = "10-12 hours"
                gpu_config['model_gpu_settings'] = {
                    'xgboost': True,      # ✅ GPU (benefits most)
                    'lightgbm': False,    # ❌ CPU (SMARTFIX fallback anyway)
                    'catboost': True,     # ✅ GPU (good GPU support)
                    'randomforest': False # ❌ CPU (sklearn doesn't support GPU)
                }
                print_info(f"Tier: {gpu_config['tier']} (M4000)")
                print_info("  - Queue: 5-30 minutes")
                print_info("  - Storage: 5 GB")
                print_info("  - Strategy: Selective GPU usage (XGB, CatBoost only)")

            elif 'P5000' in gpu_name or 'P4000' in gpu_name:
                # P5000/P4000: Fast GPU (16 GB)
                # Strategy: Use GPU for all models that support it
                gpu_config['tier'] = "Paperspace Pro ($8/month)"
                gpu_config['expected_time'] = "7-8 hours"
                gpu_config['model_gpu_settings'] = {
                    'xgboost': True,      # ✅ GPU
                    'lightgbm': True,     # ✅ GPU (with SMARTFIX fallback)
                    'catboost': True,     # ✅ GPU
                    'randomforest': False # ❌ CPU (sklearn)
                }
                print_info(f"Tier: {gpu_config['tier']} (P5000/P4000)")
                print_info("  - Queue: No queue!")
                print_info("  - Storage: 50 GB")
                print_info("  - Strategy: Full GPU acceleration")

            elif 'RTX' in gpu_name:
                # RTX series: Very fast GPU (24 GB)
                # Strategy: Use GPU for everything
                gpu_config['tier'] = "Paperspace Growth"
                gpu_config['expected_time'] = "6-7 hours"
                gpu_config['model_gpu_settings'] = {
                    'xgboost': True,      # ✅ GPU
                    'lightgbm': True,     # ✅ GPU
                    'catboost': True,     # ✅ GPU
                    'randomforest': False # ❌ CPU (sklearn)
                }
                print_info(f"Tier: {gpu_config['tier']} (RTX series)")
                print_info("  - Queue: No queue")
                print_info("  - Storage: Variable")
                print_info("  - Strategy: Maximum GPU acceleration")

            elif 'T4' in gpu_name:
                # T4: Medium GPU (16 GB)
                # Strategy: Use GPU for all except LightGBM (unreliable)
                gpu_config['tier'] = "Cloud GPU (T4)"
                gpu_config['expected_time'] = "8-9 hours"
                gpu_config['model_gpu_settings'] = {
                    'xgboost': True,      # ✅ GPU
                    'lightgbm': False,    # ❌ CPU (OpenCL issues)
                    'catboost': True,     # ✅ GPU
                    'randomforest': False # ❌ CPU (sklearn)
                }
                print_info(f"Tier: {gpu_config['tier']}")
                print_info("  - Strategy: GPU for XGBoost/CatBoost, CPU for LightGBM")

            else:
                # Unknown GPU: Conservative approach
                gpu_config['tier'] = f"Custom GPU ({gpu_name})"
                gpu_config['expected_time'] = "8-10 hours"
                gpu_config['model_gpu_settings'] = {
                    'xgboost': True,      # ✅ GPU (usually safe)
                    'lightgbm': False,    # ❌ CPU (conservative)
                    'catboost': True,     # ✅ GPU (usually safe)
                    'randomforest': False # ❌ CPU (sklearn)
                }
                print_info(f"Tier: {gpu_config['tier']}")
                print_info("  - Strategy: Conservative GPU usage")

            # Print auto-configuration
            print_info(f"  - Expected training time: ~{gpu_config['expected_time']}")
            print_info("\n📊 Auto-configured model settings:")
            for model, use_gpu in gpu_config['model_gpu_settings'].items():
                device = "GPU ✅" if use_gpu else "CPU ⚪"
                print_info(f"     - {model.capitalize():15s}: {device}")

            # Save configuration to file
            save_gpu_config(gpu_config)

            return gpu_config

        else:
            # No GPU - all CPU
            print_error("No GPU detected!")
            print_info("Make sure you selected GPU instance when creating the notebook")
            print_info("\nOptions:")
            print_info("  - Free tier: Free-GPU (M4000)")
            print_info("  - Pro tier: P4000/P5000 ($8/month)")
            print_info("\nℹ️  Training will continue on CPU (slower)")

            gpu_config['tier'] = "CPU Only"
            gpu_config['expected_time'] = "18-24 hours"
            # All models stay False (CPU)

            save_gpu_config(gpu_config)

            return gpu_config

    except ImportError:
        print_error("PyTorch not installed - cannot check GPU")
        print_info("Fix: pip install torch")
        return None


def save_gpu_config(gpu_config):
    """Save GPU configuration as RECOMMENDATION (not hardcoded)"""
    import json

    config_file = Path('/storage/number-ML/gpu_config_auto.json')

    # Add recommendation note
    gpu_config['_note'] = "This is a RECOMMENDATION based on your GPU. You can override these settings when training."
    gpu_config['_usage'] = "In notebook: Load this file and modify model_gpu_settings as needed"

    try:
        with open(config_file, 'w') as f:
            json.dump(gpu_config, f, indent=2)
        print_success(f"\n💾 GPU recommendations saved: {config_file}")
        print_info("    ℹ️  This is a recommendation - you can change settings when training")
        print_info("    ℹ️  Example: Change lightgbm from CPU to GPU if you want")
    except Exception as e:
        print_error(f"Could not save GPU config: {e}")


def copy_project_files():
    """Copy project files to /storage"""
    print_header("Copying Project Files")

    base_path = Path('/storage/number-ML')
    current_dir = Path.cwd()

    # Directories to copy
    dirs_to_copy = ['src', 'data', 'notebooks']

    for dir_name in dirs_to_copy:
        src_dir = current_dir / dir_name
        dst_dir = base_path / dir_name

        if src_dir.exists():
            # Remove destination if exists
            if dst_dir.exists():
                shutil.rmtree(dst_dir)

            # Copy directory
            shutil.copytree(src_dir, dst_dir)
            print_success(f"Copied: {dir_name}/ → {dst_dir}")
        else:
            print_info(f"Directory not found: {src_dir} (skipping)")

    # Copy individual files
    files_to_copy = [
        'requirements.txt',
        'CLAUDE.md',
        'README.md',
        'PAPERSPACE_SETUP.md'
    ]

    for file_name in files_to_copy:
        src_file = current_dir / file_name
        dst_file = base_path / file_name

        if src_file.exists():
            shutil.copy2(src_file, dst_file)
            print_success(f"Copied: {file_name}")
        else:
            print_info(f"File not found: {file_name} (skipping)")

    return base_path


def print_storage_usage():
    """Print /storage disk usage"""
    print_header("Storage Usage")

    try:
        result = subprocess.run(
            ['df', '-h', '/storage'],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        print_info("Paperspace Free tier: 5 GB persistent storage limit")
    except subprocess.CalledProcessError:
        print_error("Could not check storage usage")


def print_next_steps(gpu_config=None):
    """Print next steps for user"""
    print_header("Setup Complete! 🎉")

    print("""
Next Steps:

1. Open Jupyter Notebook:
   → Navigate to: /storage/number-ML/notebooks/
   → Open: Paperspace_ML_Training_AutoResume.ipynb

2. Run Training:
   → Cell 1: Environment detection (auto-detect Paperspace)
   → Cell 2: Load auto-configured GPU settings
   → Cell 3-6: Full training pipeline (models auto-select GPU/CPU)
""")

    if gpu_config and gpu_config.get('has_gpu'):
        print(f"   → Expected time: {gpu_config['expected_time']}")
        print(f"   → GPU: {gpu_config['gpu_name']}")
        print("\n   📊 Auto-configured model settings:")
        for model, use_gpu in gpu_config['model_gpu_settings'].items():
            device = "GPU ✅" if use_gpu else "CPU ⚪"
            print(f"      - {model.capitalize():15s}: {device}")
    else:
        print("   → Expected time: 18-24 hours (CPU only)")

    print("""
3. Monitor Progress:
   → Real-time GPU stats every 5 trials
   → Checkpoint saves every 10 trials
   → Progress tracking with ETA
   → 🤖 Models auto-select GPU/CPU based on performance

4. Download Model:
   → After training: /storage/number-ML/models/deployed/best_model.pkl
   → Right-click → Download

⚠️  Important Notes:

- 🤖 GPU auto-configuration: Models automatically use GPU or CPU based on performance
- Storage limit varies by tier (Free: 5 GB, Pro: 50 GB)
- Checkpoints are PERSISTENT in /storage/ ✅
- No timeout limit (train 24/7 if needed) ✅
- Configuration saved: /storage/number-ML/gpu_config_auto.json

📚 Documentation:
- Full guide: /storage/number-ML/PAPERSPACE_SETUP.md
- Error prevention: /storage/number-ML/PAPERSPACE_ERROR_PREVENTION.md
- Validation script: /storage/number-ML/validate_paperspace.py
- Project docs: /storage/number-ML/CLAUDE.md

🆘 Troubleshooting:
- GPU not available → Check notebook settings (GPU tier selected?)
- Queue too long (Free tier) → Try off-peak hours or upgrade to Pro ($8/month)
- Storage full → Delete old checkpoints: rm /storage/number-ML/checkpoints/*.pkl
- Errors before training → Run: python /storage/number-ML/validate_paperspace.py

    """)


def main():
    """Main setup function"""
    print("\n" + "="*80)
    print("🖥️  PAPERSPACE GRADIENT - ML PROJECT SETUP")
    print("="*80)

    # Step 1: Check environment
    if not check_paperspace_environment():
        print_error("\nSetup aborted - not running on Paperspace")
        sys.exit(1)

    # Step 2: Create directories
    base_path = setup_directories()

    # Step 3: Copy files
    copy_project_files()

    # Step 4: Install dependencies
    if not install_dependencies():
        print_error("\nWarning: Some dependencies may not be installed")

    # Step 5: Verify GPU and auto-configure
    gpu_config = verify_gpu()
    if gpu_config is None:
        print_info("\nGPU check failed - training will be slower on CPU")
    elif not gpu_config['has_gpu']:
        print_info("\nNo GPU detected - training will use CPU (slower)")
    else:
        print_success(f"\n✅ GPU configured: {gpu_config['gpu_name']}")
        print_info(f"   Tier: {gpu_config['tier']}")
        print_info(f"   Expected training time: {gpu_config['expected_time']}")

    # Step 6: Show storage usage
    print_storage_usage()

    # Step 7: Print next steps
    print_next_steps()

    print_success("\n✅ Setup completed successfully!")
    print(f"📁 Project location: {base_path}\n")

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
