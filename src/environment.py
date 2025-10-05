"""
Environment Detection and Configuration
Auto-detects runtime environment (Local/Colab/Kaggle) and configures paths accordingly
"""
import os
import sys
from pathlib import Path
from typing import Dict, Tuple, Optional
import json


class EnvironmentDetector:
    """Detect and configure runtime environment"""

    # Environment types
    ENV_LOCAL = "local"
    ENV_COLAB = "colab"
    ENV_KAGGLE = "kaggle"
    ENV_PAPERSPACE = "paperspace"
    ENV_UNKNOWN = "unknown"

    def __init__(self):
        self.env_type = self._detect_environment()
        self.base_path = self._get_base_path()
        self.is_notebook = self._is_notebook_environment()

    def _detect_environment(self) -> str:
        """
        Detect current runtime environment

        Returns:
        --------
        env_type : str
            Environment type (local, colab, kaggle, paperspace, unknown)
        """
        # Check for Paperspace Gradient
        # Paperspace has unique environment variables and /storage directory
        if ('PAPERSPACE_NOTEBOOK_REPO_ID' in os.environ or
            'PAPERSPACE_API_KEY' in os.environ or
            'PAPERSPACE_METRIC_WORKLOAD_ID' in os.environ or
            os.path.exists('/storage')):
            return self.ENV_PAPERSPACE

        # Check for Kaggle
        if 'KAGGLE_KERNEL_RUN_TYPE' in os.environ or os.path.exists('/kaggle'):
            return self.ENV_KAGGLE

        # Check for Google Colab
        try:
            import google.colab
            return self.ENV_COLAB
        except ImportError:
            pass

        # Check for common Colab indicators
        if 'COLAB_GPU' in os.environ or os.path.exists('/content'):
            return self.ENV_COLAB

        # Default to local
        return self.ENV_LOCAL

    def _get_base_path(self) -> Path:
        """
        Get appropriate base path for current environment

        Returns:
        --------
        base_path : Path
            Base directory path
        """
        if self.env_type == self.ENV_PAPERSPACE:
            # Paperspace: use /storage for persistent data
            # /storage is persistent across notebook restarts
            # /notebooks is temporary workspace
            storage_path = Path('/storage/number-ML')
            notebooks_path = Path('/notebooks/number-ML')

            # Prefer /storage for persistence
            if storage_path.exists():
                return storage_path
            elif notebooks_path.exists():
                return notebooks_path
            else:
                # Default to /storage (will be created)
                return storage_path

        elif self.env_type == self.ENV_KAGGLE:
            # Kaggle: use /kaggle/working
            return Path('/kaggle/working')

        elif self.env_type == self.ENV_COLAB:
            # Colab: check if Google Drive is mounted
            gdrive_path = Path('/content/drive/MyDrive/number-ML')
            if gdrive_path.exists():
                return gdrive_path
            else:
                # Use /content if Drive not mounted
                return Path('/content/number-ML')

        else:  # Local
            # Try to find project root by looking for key files
            current = Path.cwd()

            # Check if we're already in project root
            if (current / 'src' / 'config.py').exists():
                return current

            # Try parent directories
            for parent in [current] + list(current.parents):
                if (parent / 'src' / 'config.py').exists():
                    return parent

            # Fallback to current directory
            return current

    def _is_notebook_environment(self) -> bool:
        """Check if running in Jupyter/Colab notebook"""
        try:
            from IPython import get_ipython
            if get_ipython() is not None:
                return True
        except:
            pass
        return False

    def get_paths(self) -> Dict[str, Path]:
        """
        Get all project paths for current environment

        Returns:
        --------
        paths : dict
            Dictionary of project paths
        """
        base = self.base_path

        return {
            'base': base,
            'data': base / 'data',
            'data_raw': base / 'data' / 'raw',
            'data_processed': base / 'data' / 'processed',
            'data_features': base / 'data' / 'features',
            'models': base / 'models',
            'models_deployed': base / 'models' / 'deployed',
            'models_experiments': base / 'models' / 'experiments',
            'results': base / 'results',
            'results_figures': base / 'results' / 'figures',
            'results_reports': base / 'results' / 'reports',
            'results_metrics': base / 'results' / 'metrics',
            'logs': base / 'logs',
            'src': base / 'src',
            'api': base / 'api',
            'scripts': base / 'scripts',
            'notebooks': base / 'notebooks',
            'tests': base / 'tests',
            'utils': base / 'utils',
            'docs': base / 'docs'
        }

    def setup_directories(self, create: bool = True) -> Dict[str, Path]:
        """
        Get paths and optionally create directories

        Parameters:
        -----------
        create : bool, default=True
            Whether to create directories if they don't exist

        Returns:
        --------
        paths : dict
            Dictionary of project paths
        """
        paths = self.get_paths()

        if create:
            # Directories that should always exist
            essential_dirs = [
                'data', 'data_raw', 'data_processed', 'data_features',
                'models', 'models_deployed', 'models_experiments',
                'results', 'results_figures', 'results_reports', 'results_metrics',
                'logs'
            ]

            for dir_key in essential_dirs:
                if dir_key in paths:
                    paths[dir_key].mkdir(parents=True, exist_ok=True)

        return paths

    def setup_python_path(self):
        """Add project directories to Python path"""
        paths = self.get_paths()

        # Add to sys.path if not already there
        paths_to_add = [
            str(paths['base']),
            str(paths['src']),
        ]

        for path in paths_to_add:
            if path not in sys.path:
                sys.path.insert(0, path)

    def get_environment_info(self) -> Dict:
        """
        Get comprehensive environment information

        Returns:
        --------
        info : dict
            Environment information
        """
        return {
            'environment': self.env_type,
            'base_path': str(self.base_path),
            'is_notebook': self.is_notebook,
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'platform': sys.platform,
            'cwd': str(Path.cwd())
        }

    def print_environment_info(self):
        """Print environment information"""
        info = self.get_environment_info()

        print("="*80)
        print("🌍 ENVIRONMENT INFORMATION")
        print("="*80)
        print(f"Environment Type: {info['environment'].upper()}")
        print(f"Base Path: {info['base_path']}")
        print(f"Python Version: {info['python_version']}")
        print(f"Platform: {info['platform']}")
        print(f"Is Notebook: {info['is_notebook']}")
        print(f"Current Directory: {info['cwd']}")
        print("="*80)

    def save_state(self, state_file: Optional[Path] = None):
        """
        Save environment state to JSON file

        Parameters:
        -----------
        state_file : Path, optional
            Path to state file (default: .project_state.json)
        """
        if state_file is None:
            state_file = self.base_path / '.project_state.json'

        # Load existing state if it exists
        if state_file.exists():
            with open(state_file, 'r') as f:
                state = json.load(f)
        else:
            state = {}

        # Update environment section
        state['environment'] = self.get_environment_info()
        state['paths'] = {k: str(v) for k, v in self.get_paths().items()}

        # Save state
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)

        return state_file


# ====================================================================================
# CONVENIENCE FUNCTIONS
# ====================================================================================

def detect_environment() -> Tuple[str, Path]:
    """
    Quick environment detection

    Returns:
    --------
    env_type : str
        Environment type
    base_path : Path
        Base project path
    """
    detector = EnvironmentDetector()
    return detector.env_type, detector.base_path


def setup_environment(verbose: bool = True, create_dirs: bool = True) -> Dict:
    """
    Complete environment setup

    Parameters:
    -----------
    verbose : bool, default=True
        Print environment information
    create_dirs : bool, default=True
        Create necessary directories

    Returns:
    --------
    config : dict
        Environment configuration including paths
    """
    detector = EnvironmentDetector()

    # Setup directories
    paths = detector.setup_directories(create=create_dirs)

    # Setup Python path
    detector.setup_python_path()

    # Save state
    state_file = detector.save_state()

    # Print info if verbose
    if verbose:
        detector.print_environment_info()
        print(f"\n✅ Environment setup complete!")
        print(f"📝 State saved to: {state_file}")

    return {
        'detector': detector,
        'env_type': detector.env_type,
        'base_path': detector.base_path,
        'paths': paths,
        'info': detector.get_environment_info()
    }


def get_config_for_environment() -> Dict:
    """
    Get configuration dictionary for current environment

    Returns:
    --------
    config : dict
        Environment-specific configuration
    """
    detector = EnvironmentDetector()
    paths = detector.get_paths()

    return {
        'BASE_PATH': paths['base'],
        'DATA_PATH': paths['data'],
        'MODEL_PATH': paths['models'],
        'RESULTS_PATH': paths['results'],
        'LOGS_PATH': paths['logs'],
        'ENV_TYPE': detector.env_type,
        'IS_NOTEBOOK': detector.is_notebook
    }


# ====================================================================================
# MAIN (for testing)
# ====================================================================================

if __name__ == "__main__":
    # Test environment detection
    env_config = setup_environment(verbose=True, create_dirs=True)

    print("\n📂 Project Paths:")
    print("-" * 80)
    for name, path in env_config['paths'].items():
        exists = "✅" if path.exists() else "❌"
        print(f"{exists} {name:20s}: {path}")
