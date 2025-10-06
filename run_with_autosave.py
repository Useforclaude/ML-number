#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run Main Pipeline with Auto-Checkpoint
Automatically saves progress every 15 minutes to prevent data loss

Usage:
    python run_with_autosave.py --run-all --optimize
    python run_with_autosave.py --train --checkpoint-interval 10

By Alex - World-Class AI Expert
"""
import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.checkpoint import CheckpointManager


def main():
    """Main function with checkpoint support"""
    # Parse arguments
    parser = argparse.ArgumentParser(description='Run ML pipeline with auto-checkpoint')
    parser.add_argument('--checkpoint-interval', type=int, default=15,
                        help='Checkpoint interval in minutes (default: 15)')

    # Pass remaining args to main.py
    args, remaining_args = parser.parse_known_args()

    print("="*80)
    print("🚀 ML PIPELINE WITH AUTO-CHECKPOINT")
    print("="*80)
    print(f"Checkpoint interval: {args.checkpoint_interval} minutes")
    print(f"Pipeline arguments: {' '.join(remaining_args)}")
    print("="*80)

    # Start checkpoint system
    checkpoint_manager = CheckpointManager(interval_minutes=args.checkpoint_interval)
    checkpoint_manager.start()

    try:
        # Import and run main pipeline
        from main import main as run_pipeline

        # Modify sys.argv for main.py
        sys.argv = ['main.py'] + remaining_args

        # Run pipeline
        run_pipeline()

    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Pipeline error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Stop checkpoint system and save final state
        checkpoint_manager.stop()
        print("\n✅ Auto-checkpoint stopped - all progress saved!")


if __name__ == "__main__":
    main()
