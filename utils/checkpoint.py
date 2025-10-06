#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Auto-Checkpoint System
Saves project state every 15 minutes to prevent data loss

Usage:
    from utils.checkpoint import CheckpointManager

    checkpoint = CheckpointManager()
    checkpoint.start()  # Start auto-save

    # Your work here...

    checkpoint.stop()   # Stop auto-save

By Alex - World-Class AI Expert
"""
import os
import json
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class CheckpointManager:
    """
    Automatic checkpoint system that saves project state periodically
    """

    def __init__(self, interval_minutes: int = 15, checkpoint_dir: str = None):
        """
        Initialize checkpoint manager

        Parameters:
        -----------
        interval_minutes : int
            Checkpoint interval in minutes (default: 15)
        checkpoint_dir : str
            Directory to save checkpoints (default: project_root/checkpoints)
        """
        self.interval_seconds = interval_minutes * 60
        self.checkpoint_dir = checkpoint_dir or self._get_default_checkpoint_dir()
        self.running = False
        self.thread = None
        self.checkpoint_count = 0
        self.last_checkpoint_time = None

        # Create checkpoint directory
        os.makedirs(self.checkpoint_dir, exist_ok=True)

        logger.info(f"Checkpoint manager initialized (interval: {interval_minutes} min)")

    def _get_default_checkpoint_dir(self) -> str:
        """Get default checkpoint directory"""
        project_root = Path(__file__).parent.parent
        return str(project_root / 'checkpoints')

    def start(self):
        """Start automatic checkpoint system"""
        if self.running:
            logger.warning("Checkpoint system already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._checkpoint_loop, daemon=True)
        self.thread.start()

        logger.info(f"✅ Auto-checkpoint started (every {self.interval_seconds // 60} minutes)")
        print(f"✅ Auto-checkpoint started - saves every {self.interval_seconds // 60} minutes to {self.checkpoint_dir}")

    def stop(self):
        """Stop automatic checkpoint system"""
        if not self.running:
            logger.warning("Checkpoint system not running")
            return

        self.running = False
        if self.thread:
            self.thread.join(timeout=5)

        # Save final checkpoint
        self.save_checkpoint()

        logger.info("Checkpoint system stopped")
        print(f"✅ Auto-checkpoint stopped (saved {self.checkpoint_count} checkpoints)")

    def _checkpoint_loop(self):
        """Main checkpoint loop (runs in background thread)"""
        while self.running:
            time.sleep(self.interval_seconds)
            if self.running:  # Check again after sleep
                self.save_checkpoint()

    def save_checkpoint(self, custom_data: Optional[Dict[str, Any]] = None):
        """
        Save checkpoint to disk

        Parameters:
        -----------
        custom_data : dict, optional
            Additional data to save in checkpoint
        """
        try:
            timestamp = datetime.now()
            checkpoint_data = {
                'timestamp': timestamp.isoformat(),
                'checkpoint_number': self.checkpoint_count + 1,
                'project_state': self._get_project_state(),
                'environment_info': self._get_environment_info(),
                'custom_data': custom_data or {}
            }

            # Save checkpoint file
            filename = f"checkpoint_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.checkpoint_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)

            self.checkpoint_count += 1
            self.last_checkpoint_time = timestamp

            logger.info(f"Checkpoint saved: {filename}")
            print(f"💾 Checkpoint #{self.checkpoint_count} saved at {timestamp.strftime('%H:%M:%S')}")

            # Also update latest checkpoint (always same filename)
            latest_path = os.path.join(self.checkpoint_dir, 'checkpoint_latest.json')
            with open(latest_path, 'w', encoding='utf-8') as f:
                json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)

            # Cleanup old checkpoints (keep last 10)
            self._cleanup_old_checkpoints(keep_last=10)

        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")
            print(f"❌ Checkpoint save failed: {e}")

    def _get_project_state(self) -> Dict[str, Any]:
        """Get current project state"""
        from src.config import BASE_PATH, ENV_TYPE

        state = {
            'base_path': BASE_PATH,
            'environment': ENV_TYPE,
            'files_modified_today': self._get_modified_files_today()
        }

        # Check if project state file exists
        project_state_path = os.path.join(BASE_PATH, '.project_state.json')
        if os.path.exists(project_state_path):
            try:
                with open(project_state_path, 'r') as f:
                    state['project_tracking'] = json.load(f)
            except:
                pass

        return state

    def _get_environment_info(self) -> Dict[str, Any]:
        """Get environment information"""
        import sys
        import platform

        return {
            'python_version': sys.version,
            'platform': platform.platform(),
            'cwd': os.getcwd()
        }

    def _get_modified_files_today(self) -> list:
        """Get list of files modified today"""
        from src.config import BASE_PATH

        today = datetime.now().date()
        modified_files = []

        try:
            for root, dirs, files in os.walk(BASE_PATH):
                # Skip venv and cache directories
                dirs[:] = [d for d in dirs if d not in ['.venv', '__pycache__', '.git', 'node_modules']]

                for file in files:
                    if file.endswith(('.py', '.json', '.md', '.txt')):
                        filepath = os.path.join(root, file)
                        try:
                            mtime = datetime.fromtimestamp(os.path.getmtime(filepath)).date()
                            if mtime == today:
                                rel_path = os.path.relpath(filepath, BASE_PATH)
                                modified_files.append(rel_path)
                        except:
                            pass
        except:
            pass

        return modified_files[:50]  # Limit to 50 files

    def _cleanup_old_checkpoints(self, keep_last: int = 10):
        """Delete old checkpoint files, keeping only the most recent ones"""
        try:
            checkpoint_files = [
                f for f in os.listdir(self.checkpoint_dir)
                if f.startswith('checkpoint_') and f.endswith('.json') and f != 'checkpoint_latest.json'
            ]

            if len(checkpoint_files) > keep_last:
                # Sort by filename (timestamp in filename)
                checkpoint_files.sort()

                # Delete oldest files
                for old_file in checkpoint_files[:-keep_last]:
                    try:
                        os.remove(os.path.join(self.checkpoint_dir, old_file))
                    except:
                        pass
        except:
            pass

    def load_latest_checkpoint(self) -> Optional[Dict[str, Any]]:
        """
        Load the most recent checkpoint

        Returns:
        --------
        checkpoint_data : dict or None
            Latest checkpoint data, or None if not found
        """
        latest_path = os.path.join(self.checkpoint_dir, 'checkpoint_latest.json')

        if not os.path.exists(latest_path):
            logger.warning("No checkpoint found")
            return None

        try:
            with open(latest_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            logger.info(f"Loaded checkpoint from {data['timestamp']}")
            return data
        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}")
            return None

    def list_checkpoints(self) -> list:
        """
        List all available checkpoints

        Returns:
        --------
        checkpoints : list
            List of checkpoint files with timestamps
        """
        try:
            checkpoint_files = [
                f for f in os.listdir(self.checkpoint_dir)
                if f.startswith('checkpoint_') and f.endswith('.json') and f != 'checkpoint_latest.json'
            ]

            checkpoint_files.sort(reverse=True)
            return checkpoint_files
        except:
            return []

    def __enter__(self):
        """Context manager support"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager support"""
        self.stop()


# ====================================================================================
# CONVENIENCE FUNCTIONS
# ====================================================================================

def start_autosave(interval_minutes: int = 15):
    """
    Start auto-checkpoint system (convenience function)

    Parameters:
    -----------
    interval_minutes : int
        Checkpoint interval in minutes

    Returns:
    --------
    manager : CheckpointManager
        Checkpoint manager instance
    """
    manager = CheckpointManager(interval_minutes=interval_minutes)
    manager.start()
    return manager


def manual_checkpoint(custom_data: Optional[Dict[str, Any]] = None):
    """
    Save manual checkpoint (convenience function)

    Parameters:
    -----------
    custom_data : dict, optional
        Custom data to include in checkpoint
    """
    manager = CheckpointManager()
    manager.save_checkpoint(custom_data=custom_data)


# ====================================================================================
# EXAMPLE USAGE
# ====================================================================================

if __name__ == "__main__":
    print("Testing Checkpoint System...")

    # Test 1: Manual checkpoint
    print("\n1. Creating manual checkpoint...")
    manual_checkpoint({'test': 'manual checkpoint', 'value': 123})

    # Test 2: Auto-checkpoint with context manager
    print("\n2. Testing auto-checkpoint (will run for 35 seconds)...")
    with CheckpointManager(interval_minutes=0.5) as checkpoint:  # 30 seconds for testing
        print("   Working...")
        time.sleep(35)
        print("   Done!")

    # Test 3: List checkpoints
    print("\n3. Listing checkpoints...")
    manager = CheckpointManager()
    checkpoints = manager.list_checkpoints()
    for cp in checkpoints[:5]:
        print(f"   - {cp}")

    # Test 4: Load latest
    print("\n4. Loading latest checkpoint...")
    latest = manager.load_latest_checkpoint()
    if latest:
        print(f"   Timestamp: {latest['timestamp']}")
        print(f"   Checkpoint #: {latest['checkpoint_number']}")

    print("\n✅ Checkpoint system test complete!")
