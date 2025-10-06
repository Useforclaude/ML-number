#!/usr/bin/env python3
"""
Create Kaggle package with proper directory structure
"""
import zipfile
from pathlib import Path

# Package configuration
PACKAGE_NAME = "packages/kaggle/number-ML-kaggle-SESSION-011F-20251007.zip"

# Files to include with their paths
files_to_include = {
    # Source files (in src/ folder)
    'src/__init__.py': 'src/__init__.py',
    'src/checkpoint_manager.py': 'src/checkpoint_manager.py',
    'src/config.py': 'src/config.py',
    'src/data_handler.py': 'src/data_handler.py',
    'src/data_loader.py': 'src/data_loader.py',
    'src/data_splitter.py': 'src/data_splitter.py',
    'src/environment.py': 'src/environment.py',
    'src/evaluate.py': 'src/evaluate.py',
    'src/features.py': 'src/features.py',
    'src/gpu_monitor.py': 'src/gpu_monitor.py',
    'src/model_utils.py': 'src/model_utils.py',
    'src/tier_models.py': 'src/tier_models.py',
    'src/train.py': 'src/train.py',
    'src/train_colab.py': 'src/train_colab.py',
    'src/train_production.py': 'src/train_production.py',
    'src/training_callbacks.py': 'src/training_callbacks.py',
    'src/visualize.py': 'src/visualize.py',

    # Notebook (in notebooks/ folder)
    'notebooks/Kaggle_ML_Training_AutoResume.ipynb': 'notebooks/Kaggle_ML_Training_AutoResume.ipynb',

    # Data file (in data/raw/ folder)
    'data/raw/numberdata.csv': 'data/raw/numberdata.csv',

    # Root files
    'requirements.txt': 'requirements.txt',
    'README.md': 'README.md'
}

print(f"Creating Kaggle package: {PACKAGE_NAME}")
print(f"Files to include: {len(files_to_include)}")

with zipfile.ZipFile(PACKAGE_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for source_path, archive_path in files_to_include.items():
        source = Path(source_path)
        if source.exists():
            print(f"  ✅ Adding: {archive_path}")
            zipf.write(source, archive_path)
        else:
            print(f"  ❌ Missing: {source_path}")

print(f"\n✅ Package created: {PACKAGE_NAME}")

# Verify contents
print(f"\n🔍 Verifying package contents:")
with zipfile.ZipFile(PACKAGE_NAME, 'r') as zipf:
    namelist = zipf.namelist()
    print(f"  Total files: {len(namelist)}")

    # Check directories
    has_src = any(name.startswith('src/') for name in namelist)
    has_data = any(name.startswith('data/') for name in namelist)
    has_notebooks = any(name.startswith('notebooks/') for name in namelist)

    print(f"  src/ folder: {'✅' if has_src else '❌'}")
    print(f"  data/ folder: {'✅' if has_data else '❌'}")
    print(f"  notebooks/ folder: {'✅' if has_notebooks else '❌'}")

    # Show structure
    print(f"\n📂 Package structure:")
    dirs = set()
    for name in namelist:
        parts = name.split('/')
        if len(parts) > 1:
            dirs.add(parts[0])

    for d in sorted(dirs):
        count = sum(1 for name in namelist if name.startswith(f"{d}/"))
        print(f"  {d}/ ({count} files)")

    # Root files
    root_files = [name for name in namelist if '/' not in name]
    if root_files:
        print(f"  / ({len(root_files)} files)")

print("\n✅ Done!")
