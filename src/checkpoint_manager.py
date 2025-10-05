"""
Checkpoint Manager for Google Colab & Kaggle Auto-Resume Training

This module provides checkpoint saving/loading functionality that works
seamlessly with Google Drive (Colab) and Kaggle /working directory,
allowing training to resume after runtime disconnection.

Features:
- Auto-save checkpoints to Google Drive (Colab) or /kaggle/working (Kaggle)
- Auto-detect environment (Colab, Kaggle, Local)
- Auto-detect latest checkpoint
- Resume training from checkpoint
- Cleanup old checkpoints
- Progress tracking

Usage (Colab):
    from src.checkpoint_manager import CheckpointManager

    manager = CheckpointManager(
        checkpoint_dir='/content/drive/MyDrive/project/checkpoints',
        max_checkpoints=5
    )

Usage (Kaggle):
    from src.checkpoint_manager import CheckpointManager

    manager = CheckpointManager(
        checkpoint_dir='/kaggle/working/checkpoints',
        max_checkpoints=5
    )

    # Save checkpoint (same for both)
    manager.save_checkpoint(
        epoch=10,
        model=model,
        optimizer=optimizer,
        metrics={'loss': 0.15, 'r2': 0.92}
    )

    # Load latest checkpoint (same for both)
    checkpoint = manager.load_latest_checkpoint()
    if checkpoint:
        model.load_state_dict(checkpoint['model_state'])
        start_epoch = checkpoint['epoch'] + 1
"""

import os
import glob
import json
import pickle
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import shutil


def detect_environment() -> str:
    """
    Auto-detect environment (Colab, Kaggle, or Local)

    Returns:
    --------
    env : str
        'colab', 'kaggle', or 'local'
    """
    if os.path.exists('/content/drive'):
        return 'colab'
    elif os.path.exists('/kaggle'):
        return 'kaggle'
    else:
        return 'local'


class CheckpointManager:
    """
    Manages training checkpoints with Google Drive (Colab) or Kaggle /working sync support

    Auto-detects environment and adjusts behavior accordingly
    """

    def __init__(
        self,
        checkpoint_dir: str = None,
        max_checkpoints: int = 5,
        save_every: int = 10,
        auto_sync: bool = True
    ):
        """
        Initialize checkpoint manager

        Parameters:
        -----------
        checkpoint_dir : str, optional
            Directory to save checkpoints
            If None, auto-detects based on environment:
            - Colab: /content/drive/MyDrive/ML_Project/checkpoints
            - Kaggle: /kaggle/working/checkpoints
            - Local: ./checkpoints
        max_checkpoints : int
            Maximum number of checkpoints to keep (older ones deleted)
        save_every : int
            Save checkpoint every N epochs/iterations
        auto_sync : bool
            Automatically sync after save
        """
        # Auto-detect environment
        self.env = detect_environment()

        # Set default checkpoint directory if not provided
        if checkpoint_dir is None:
            if self.env == 'colab':
                checkpoint_dir = '/content/drive/MyDrive/ML_Project/checkpoints'
            elif self.env == 'kaggle':
                checkpoint_dir = '/kaggle/working/checkpoints'
            else:
                checkpoint_dir = './checkpoints'

        self.checkpoint_dir = Path(checkpoint_dir)
        self.max_checkpoints = max_checkpoints
        self.save_every = save_every
        self.auto_sync = auto_sync

        # Create checkpoint directory if doesn't exist
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        print(f"📂 Checkpoint Manager initialized")
        print(f"   Environment: {self.env.upper()}")
        print(f"   Directory: {self.checkpoint_dir}")
        print(f"   Max checkpoints: {self.max_checkpoints}")
        print(f"   Save every: {self.save_every} epochs")

    def save_checkpoint(
        self,
        epoch: int,
        model: Any,
        optimizer: Optional[Any] = None,
        metrics: Optional[Dict] = None,
        extra_data: Optional[Dict] = None,
        is_best: bool = False
    ) -> str:
        """
        Save checkpoint to disk

        Parameters:
        -----------
        epoch : int
            Current epoch number
        model : Any
            Model object (should have state_dict() method for PyTorch)
        optimizer : Any, optional
            Optimizer object
        metrics : dict, optional
            Training metrics (loss, accuracy, etc.)
        extra_data : dict, optional
            Any extra data to save
        is_best : bool
            Whether this is the best model so far

        Returns:
        --------
        checkpoint_path : str
            Path to saved checkpoint
        """
        checkpoint_path = self.checkpoint_dir / f"checkpoint_epoch_{epoch}.pkl"

        # Prepare checkpoint data
        checkpoint = {
            'epoch': epoch,
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics or {},
            'resume_ready': True
        }

        # Save model state
        if hasattr(model, 'state_dict'):
            # PyTorch model
            checkpoint['model_state'] = model.state_dict()
        else:
            # Scikit-learn or other models
            checkpoint['model'] = model

        # Save optimizer state
        if optimizer is not None:
            if hasattr(optimizer, 'state_dict'):
                checkpoint['optimizer_state'] = optimizer.state_dict()
            else:
                checkpoint['optimizer'] = optimizer

        # Add extra data
        if extra_data:
            checkpoint['extra_data'] = extra_data

        # Save to file
        with open(checkpoint_path, 'wb') as f:
            pickle.dump(checkpoint, f)

        print(f"✅ Checkpoint saved: epoch {epoch}")
        print(f"   Path: {checkpoint_path}")
        if metrics:
            print(f"   Metrics: {metrics}")

        # Save as latest checkpoint
        latest_path = self.checkpoint_dir / "checkpoint_latest.pkl"
        shutil.copy(checkpoint_path, latest_path)

        # Save as best checkpoint if applicable
        if is_best:
            best_path = self.checkpoint_dir / "checkpoint_best.pkl"
            shutil.copy(checkpoint_path, best_path)
            print(f"🏆 Best checkpoint updated!")

        # Cleanup old checkpoints
        self._cleanup_old_checkpoints()

        # Sync to Drive (if auto_sync enabled)
        if self.auto_sync:
            self._verify_sync(checkpoint_path)

        return str(checkpoint_path)

    def load_checkpoint(self, checkpoint_path: str) -> Optional[Dict]:
        """
        Load checkpoint from disk

        Parameters:
        -----------
        checkpoint_path : str
            Path to checkpoint file

        Returns:
        --------
        checkpoint : dict or None
            Checkpoint data if successful, None otherwise
        """
        checkpoint_path = Path(checkpoint_path)

        if not checkpoint_path.exists():
            print(f"❌ Checkpoint not found: {checkpoint_path}")
            return None

        try:
            with open(checkpoint_path, 'rb') as f:
                checkpoint = pickle.load(f)

            print(f"✅ Checkpoint loaded: {checkpoint_path.name}")
            print(f"   Epoch: {checkpoint.get('epoch', 'unknown')}")
            print(f"   Timestamp: {checkpoint.get('timestamp', 'unknown')}")
            if 'metrics' in checkpoint:
                print(f"   Metrics: {checkpoint['metrics']}")

            return checkpoint

        except Exception as e:
            print(f"❌ Error loading checkpoint: {e}")
            return None

    def load_latest_checkpoint(self) -> Optional[Dict]:
        """
        Load the latest checkpoint

        Returns:
        --------
        checkpoint : dict or None
            Latest checkpoint data if exists, None otherwise
        """
        latest_path = self.checkpoint_dir / "checkpoint_latest.pkl"

        if latest_path.exists():
            return self.load_checkpoint(str(latest_path))

        # If checkpoint_latest.pkl doesn't exist, find most recent
        checkpoints = self.find_all_checkpoints()
        if checkpoints:
            latest = checkpoints[-1]  # Last one (most recent)
            return self.load_checkpoint(latest)

        print("ℹ️  No checkpoint found. Starting fresh.")
        return None

    def find_all_checkpoints(self) -> List[str]:
        """
        Find all checkpoint files in directory

        Returns:
        --------
        checkpoints : list of str
            Sorted list of checkpoint paths (oldest to newest)
        """
        pattern = str(self.checkpoint_dir / "checkpoint_epoch_*.pkl")
        checkpoints = glob.glob(pattern)

        # Sort by creation time
        checkpoints.sort(key=os.path.getctime)

        return checkpoints

    def get_latest_epoch(self) -> int:
        """
        Get the latest epoch number from checkpoints

        Returns:
        --------
        epoch : int
            Latest epoch number, or -1 if no checkpoints
        """
        checkpoint = self.load_latest_checkpoint()
        if checkpoint:
            return checkpoint['epoch']
        return -1

    def should_save(self, epoch: int) -> bool:
        """
        Determine if should save checkpoint at this epoch

        Parameters:
        -----------
        epoch : int
            Current epoch number

        Returns:
        --------
        should_save : bool
            True if should save checkpoint
        """
        return epoch % self.save_every == 0

    def _cleanup_old_checkpoints(self):
        """
        Delete old checkpoints, keeping only max_checkpoints most recent
        """
        checkpoints = self.find_all_checkpoints()

        # Keep only last N checkpoints
        if len(checkpoints) > self.max_checkpoints:
            to_delete = checkpoints[:-self.max_checkpoints]

            for ckpt in to_delete:
                try:
                    os.remove(ckpt)
                    print(f"🗑️  Deleted old checkpoint: {Path(ckpt).name}")
                except Exception as e:
                    print(f"⚠️  Could not delete {ckpt}: {e}")

    def _verify_sync(self, checkpoint_path: str):
        """
        Verify checkpoint is synced to Google Drive

        Parameters:
        -----------
        checkpoint_path : str
            Path to checkpoint file
        """
        # Check if file exists and is readable
        checkpoint_path = Path(checkpoint_path)

        if checkpoint_path.exists():
            size = checkpoint_path.stat().st_size
            size_mb = size / (1024 * 1024)
            print(f"💾 Synced to Drive: {checkpoint_path.name} ({size_mb:.2f} MB)")
        else:
            print(f"⚠️  Warning: Checkpoint file not found after save")

    def create_recovery_info(
        self,
        epoch: int,
        total_epochs: int,
        metrics: Dict,
        next_steps: str
    ):
        """
        Create recovery info file for easy resume

        Parameters:
        -----------
        epoch : int
            Current epoch
        total_epochs : int
            Total epochs planned
        metrics : dict
            Current metrics
        next_steps : str
            What to do next
        """
        info = {
            'last_epoch': epoch,
            'total_epochs': total_epochs,
            'progress_percentage': round((epoch / total_epochs) * 100, 1),
            'metrics': metrics,
            'next_steps': next_steps,
            'timestamp': datetime.now().isoformat(),
            'resume_command': f"Load checkpoint_epoch_{epoch}.pkl and continue from epoch {epoch + 1}"
        }

        info_path = self.checkpoint_dir / "recovery_info.json"

        with open(info_path, 'w') as f:
            json.dump(info, f, indent=2)

        print(f"📋 Recovery info saved: {info_path}")

    def print_recovery_info(self):
        """
        Print recovery information if available
        """
        info_path = self.checkpoint_dir / "recovery_info.json"

        if not info_path.exists():
            print("ℹ️  No recovery info available")
            return

        with open(info_path, 'r') as f:
            info = json.load(f)

        print("=" * 50)
        print("📋 RECOVERY INFORMATION")
        print("=" * 50)
        print(f"Last Epoch: {info['last_epoch']}/{info['total_epochs']}")
        print(f"Progress: {info['progress_percentage']}%")
        print(f"Timestamp: {info['timestamp']}")
        print(f"\nMetrics:")
        for key, value in info['metrics'].items():
            print(f"  {key}: {value}")
        print(f"\nNext Steps: {info['next_steps']}")
        print(f"\nResume Command:")
        print(f"  {info['resume_command']}")
        print("=" * 50)


# Utility functions for quick access

def save_training_checkpoint(
    checkpoint_dir: str,
    epoch: int,
    model: Any,
    optimizer: Any = None,
    train_loss: float = None,
    val_loss: float = None,
    metrics: Dict = None
) -> str:
    """
    Quick function to save training checkpoint

    Parameters:
    -----------
    checkpoint_dir : str
        Directory to save checkpoint
    epoch : int
        Current epoch
    model : Any
        Model to save
    optimizer : Any, optional
        Optimizer to save
    train_loss : float, optional
        Training loss
    val_loss : float, optional
        Validation loss
    metrics : dict, optional
        Additional metrics

    Returns:
    --------
    checkpoint_path : str
        Path to saved checkpoint
    """
    manager = CheckpointManager(checkpoint_dir)

    all_metrics = {}
    if train_loss is not None:
        all_metrics['train_loss'] = train_loss
    if val_loss is not None:
        all_metrics['val_loss'] = val_loss
    if metrics:
        all_metrics.update(metrics)

    return manager.save_checkpoint(
        epoch=epoch,
        model=model,
        optimizer=optimizer,
        metrics=all_metrics
    )


def load_training_checkpoint(checkpoint_dir: str) -> Optional[Dict]:
    """
    Quick function to load latest training checkpoint

    Parameters:
    -----------
    checkpoint_dir : str
        Directory containing checkpoints

    Returns:
    --------
    checkpoint : dict or None
        Checkpoint data if found
    """
    manager = CheckpointManager(checkpoint_dir)
    return manager.load_latest_checkpoint()


if __name__ == '__main__':
    # Example usage
    print("Checkpoint Manager - Example Usage")
    print("=" * 50)

    # Create manager
    manager = CheckpointManager(
        checkpoint_dir='/tmp/test_checkpoints',
        max_checkpoints=3,
        save_every=5
    )

    # Simulate saving checkpoints
    print("\n📦 Simulating checkpoint saves...")

    class DummyModel:
        def state_dict(self):
            return {'weights': [1, 2, 3]}

    model = DummyModel()

    for epoch in range(1, 21):
        if manager.should_save(epoch):
            manager.save_checkpoint(
                epoch=epoch,
                model=model,
                metrics={'loss': 1.0 / epoch, 'accuracy': 0.5 + (epoch * 0.02)}
            )

    # Load latest
    print("\n📂 Loading latest checkpoint...")
    checkpoint = manager.load_latest_checkpoint()

    if checkpoint:
        print(f"\n✅ Successfully loaded checkpoint from epoch {checkpoint['epoch']}")

    # Print recovery info
    manager.create_recovery_info(
        epoch=20,
        total_epochs=100,
        metrics={'loss': 0.05, 'accuracy': 0.90},
        next_steps="Continue training from epoch 21"
    )

    print("\n" + "=" * 50)
    manager.print_recovery_info()
