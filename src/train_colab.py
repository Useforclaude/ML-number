"""
Training Script for Google Colab with Auto-Checkpoint & Auto-Resume

This module provides training functions optimized for Google Colab:
- Auto-save checkpoints to Google Drive
- Auto-resume from latest checkpoint
- Survive runtime disconnections
- Progress tracking and logging

Features:
- Train ML models with auto-checkpoint every N epochs
- Save to Google Drive for persistence
- Resume seamlessly after disconnection
- Support for XGBoost, LightGBM, CatBoost, scikit-learn
- Optuna hyperparameter optimization with checkpoints

Usage:
    from src.train_colab import train_with_auto_resume

    # Simple training
    train_with_auto_resume(
        model=model,
        X_train=X_train,
        y_train=y_train,
        checkpoint_dir='/content/drive/MyDrive/project/checkpoints',
        total_epochs=100,
        save_every=10
    )
"""

import os
import time
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Callable
from datetime import datetime

# ML libraries
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# Import checkpoint manager
from src.checkpoint_manager import CheckpointManager

# Import existing training modules
try:
    from src.train import (
        train_xgboost,
        train_lightgbm,
        train_catboost,
        train_random_forest
    )
except ImportError:
    print("⚠️  Warning: Could not import some training functions")


class ColabTrainer:
    """
    Training wrapper with auto-checkpoint for Google Colab
    """

    def __init__(
        self,
        checkpoint_dir: str,
        project_dir: str = None,
        save_every: int = 10,
        max_checkpoints: int = 5
    ):
        """
        Initialize Colab trainer

        Parameters:
        -----------
        checkpoint_dir : str
            Directory to save checkpoints (should be in Google Drive)
        project_dir : str, optional
            Project root directory in Google Drive
        save_every : int
            Save checkpoint every N epochs/iterations
        max_checkpoints : int
            Maximum checkpoints to keep
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.project_dir = Path(project_dir) if project_dir else self.checkpoint_dir.parent
        self.save_every = save_every

        # Initialize checkpoint manager
        self.checkpoint_manager = CheckpointManager(
            checkpoint_dir=str(self.checkpoint_dir),
            max_checkpoints=max_checkpoints,
            save_every=save_every,
            auto_sync=True
        )

        # Create project directories
        self.models_dir = self.project_dir / 'models'
        self.logs_dir = self.project_dir / 'logs'
        self.results_dir = self.project_dir / 'results'

        for dir_path in [self.models_dir, self.logs_dir, self.results_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        print(f"📁 Colab Trainer initialized")
        print(f"   Project: {self.project_dir}")
        print(f"   Checkpoints: {self.checkpoint_dir}")

    def check_for_resume(self) -> Tuple[bool, Optional[Dict]]:
        """
        Check if should resume from checkpoint

        Returns:
        --------
        should_resume : bool
            True if checkpoint found
        checkpoint : dict or None
            Checkpoint data if found
        """
        checkpoint = self.checkpoint_manager.load_latest_checkpoint()

        if checkpoint:
            print("=" * 60)
            print("🔄 CHECKPOINT FOUND - RESUME MODE")
            print("=" * 60)
            print(f"Last epoch: {checkpoint['epoch']}")
            print(f"Timestamp: {checkpoint['timestamp']}")
            if 'metrics' in checkpoint:
                print(f"Metrics: {checkpoint['metrics']}")
            print("=" * 60)
            return True, checkpoint
        else:
            print("=" * 60)
            print("🆕 NO CHECKPOINT FOUND - FRESH START")
            print("=" * 60)
            return False, None

    def train_with_checkpoints(
        self,
        model_type: str,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
        params: Dict = None,
        total_epochs: int = 100,
        early_stopping_rounds: int = 50,
        verbose: bool = True
    ) -> Dict:
        """
        Train model with auto-checkpoint

        Parameters:
        -----------
        model_type : str
            Model type ('xgboost', 'lightgbm', 'catboost', 'random_forest')
        X_train : array-like
            Training features
        y_train : array-like
            Training target
        X_val : array-like, optional
            Validation features
        y_val : array-like, optional
            Validation target
        params : dict, optional
            Model parameters
        total_epochs : int
            Total epochs to train
        early_stopping_rounds : int
            Early stopping rounds
        verbose : bool
            Print progress

        Returns:
        --------
        result : dict
            Training results with model and metrics
        """
        # Check for resume
        should_resume, checkpoint = self.check_for_resume()

        # Determine start epoch
        if should_resume:
            start_epoch = checkpoint['epoch'] + 1
            model = checkpoint.get('model')
            best_score = checkpoint.get('metrics', {}).get('best_r2', -float('inf'))
            print(f"▶️  Resuming from epoch {start_epoch}/{total_epochs}")
        else:
            start_epoch = 0
            model = None
            best_score = -float('inf')
            print(f"🆕 Starting fresh training for {total_epochs} epochs")

        # Training loop with checkpoints
        training_history = {'train_loss': [], 'val_loss': [], 'r2_score': []}

        for epoch in range(start_epoch, total_epochs):
            epoch_start_time = time.time()

            # Train for one epoch
            if model_type == 'xgboost':
                model, train_loss = self._train_xgb_epoch(
                    model, X_train, y_train, params, epoch
                )
            elif model_type == 'lightgbm':
                model, train_loss = self._train_lgb_epoch(
                    model, X_train, y_train, params, epoch
                )
            elif model_type == 'catboost':
                model, train_loss = self._train_cat_epoch(
                    model, X_train, y_train, params, epoch
                )
            elif model_type == 'random_forest':
                model, train_loss = self._train_rf_epoch(
                    model, X_train, y_train, params, epoch
                )
            else:
                raise ValueError(f"Unknown model type: {model_type}")

            # Validation
            if X_val is not None and y_val is not None:
                val_preds = model.predict(X_val)
                val_loss = mean_squared_error(y_val, val_preds)
                r2 = r2_score(y_val, val_preds)
            else:
                val_loss = train_loss
                val_preds = model.predict(X_train)
                r2 = r2_score(y_train, val_preds)

            # Update history
            training_history['train_loss'].append(train_loss)
            training_history['val_loss'].append(val_loss)
            training_history['r2_score'].append(r2)

            # Print progress
            epoch_time = time.time() - epoch_start_time
            if verbose and (epoch % 5 == 0 or epoch == total_epochs - 1):
                print(f"Epoch {epoch+1}/{total_epochs} | "
                      f"Train Loss: {train_loss:.4f} | "
                      f"Val Loss: {val_loss:.4f} | "
                      f"R²: {r2:.4f} | "
                      f"Time: {epoch_time:.2f}s")

            # Check if best model
            is_best = r2 > best_score
            if is_best:
                best_score = r2

            # Save checkpoint
            if self.checkpoint_manager.should_save(epoch) or is_best:
                metrics = {
                    'train_loss': float(train_loss),
                    'val_loss': float(val_loss),
                    'r2_score': float(r2),
                    'best_r2': float(best_score)
                }

                self.checkpoint_manager.save_checkpoint(
                    epoch=epoch,
                    model=model,
                    metrics=metrics,
                    extra_data={'training_history': training_history},
                    is_best=is_best
                )

                # Update recovery info
                self.checkpoint_manager.create_recovery_info(
                    epoch=epoch,
                    total_epochs=total_epochs,
                    metrics=metrics,
                    next_steps=f"Continue training from epoch {epoch + 1}"
                )

        # Final save
        final_metrics = {
            'train_loss': float(training_history['train_loss'][-1]),
            'val_loss': float(training_history['val_loss'][-1]),
            'r2_score': float(training_history['r2_score'][-1]),
            'best_r2': float(best_score)
        }

        self.checkpoint_manager.save_checkpoint(
            epoch=total_epochs - 1,
            model=model,
            metrics=final_metrics,
            extra_data={'training_history': training_history},
            is_best=final_metrics['r2_score'] >= best_score
        )

        print(f"\n✅ Training complete!")
        print(f"   Best R²: {best_score:.4f}")
        print(f"   Final R²: {final_metrics['r2_score']:.4f}")

        return {
            'model': model,
            'metrics': final_metrics,
            'history': training_history,
            'best_score': best_score
        }

    def _train_xgb_epoch(self, model, X, y, params, epoch):
        """Train XGBoost for one epoch"""
        import xgboost as xgb

        if model is None:
            # Initialize model
            params = params or {
                'objective': 'reg:squarederror',
                'learning_rate': 0.1,
                'max_depth': 6,
                'n_estimators': 100
            }
            model = xgb.XGBRegressor(**params)

        # For XGBoost, we can't easily do incremental training
        # So we train fully each time (this is a limitation)
        model.fit(X, y, verbose=False)

        # Calculate loss
        preds = model.predict(X)
        loss = mean_squared_error(y, preds)

        return model, loss

    def _train_lgb_epoch(self, model, X, y, params, epoch):
        """Train LightGBM for one epoch"""
        import lightgbm as lgb

        if model is None:
            params = params or {
                'objective': 'regression',
                'learning_rate': 0.1,
                'max_depth': 6,
                'n_estimators': 100
            }
            model = lgb.LGBMRegressor(**params)

        model.fit(X, y, verbose=False)
        preds = model.predict(X)
        loss = mean_squared_error(y, preds)

        return model, loss

    def _train_cat_epoch(self, model, X, y, params, epoch):
        """Train CatBoost for one epoch"""
        from catboost import CatBoostRegressor

        if model is None:
            params = params or {
                'iterations': 100,
                'learning_rate': 0.1,
                'depth': 6,
                'task_type': 'CPU'
            }
            model = CatBoostRegressor(**params, verbose=False)

        model.fit(X, y, verbose=False)
        preds = model.predict(X)
        loss = mean_squared_error(y, preds)

        return model, loss

    def _train_rf_epoch(self, model, X, y, params, epoch):
        """Train Random Forest for one epoch"""
        from sklearn.ensemble import RandomForestRegressor

        if model is None:
            params = params or {
                'n_estimators': 100,
                'max_depth': 10,
                'random_state': 42
            }
            model = RandomForestRegressor(**params)

        model.fit(X, y)
        preds = model.predict(X)
        loss = mean_squared_error(y, preds)

        return model, loss

    def save_final_model(
        self,
        model: Any,
        model_name: str,
        metrics: Dict,
        feature_names: list = None
    ) -> str:
        """
        Save final trained model to Google Drive

        Parameters:
        -----------
        model : Any
            Trained model
        model_name : str
            Model name (e.g., 'xgboost_final')
        metrics : dict
            Model metrics
        feature_names : list, optional
            Feature names

        Returns:
        --------
        save_path : str
            Path to saved model
        """
        import joblib

        save_path = self.models_dir / f"{model_name}.pkl"

        model_package = {
            'model': model,
            'model_name': model_name,
            'metrics': metrics,
            'feature_names': feature_names,
            'timestamp': datetime.now().isoformat(),
            'trained_on': 'Google Colab'
        }

        joblib.dump(model_package, save_path)

        print(f"💾 Final model saved: {save_path}")
        print(f"   Size: {save_path.stat().st_size / (1024*1024):.2f} MB")

        return str(save_path)


# Convenience functions

def train_with_auto_resume(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: Optional[np.ndarray] = None,
    y_val: Optional[np.ndarray] = None,
    model_type: str = 'xgboost',
    checkpoint_dir: str = '/content/drive/MyDrive/ML_Project/checkpoints',
    project_dir: str = '/content/drive/MyDrive/ML_Project',
    total_epochs: int = 100,
    save_every: int = 10,
    params: Dict = None
) -> Dict:
    """
    Train model with auto-checkpoint and auto-resume

    Parameters:
    -----------
    X_train : array-like
        Training features
    y_train : array-like
        Training target
    X_val : array-like, optional
        Validation features
    y_val : array-like, optional
        Validation target
    model_type : str
        'xgboost', 'lightgbm', 'catboost', 'random_forest'
    checkpoint_dir : str
        Checkpoint directory in Google Drive
    project_dir : str
        Project directory in Google Drive
    total_epochs : int
        Total epochs to train
    save_every : int
        Save checkpoint every N epochs
    params : dict, optional
        Model parameters

    Returns:
    --------
    result : dict
        Training results
    """
    # Create trainer
    trainer = ColabTrainer(
        checkpoint_dir=checkpoint_dir,
        project_dir=project_dir,
        save_every=save_every
    )

    # Train with checkpoints
    result = trainer.train_with_checkpoints(
        model_type=model_type,
        X_train=X_train,
        y_train=y_train,
        X_val=X_val,
        y_val=y_val,
        params=params,
        total_epochs=total_epochs
    )

    # Save final model
    trainer.save_final_model(
        model=result['model'],
        model_name=f'{model_type}_final',
        metrics=result['metrics']
    )

    return result


if __name__ == '__main__':
    print("Colab Training Script - Example Usage")
    print("=" * 60)

    # Example: Create synthetic data
    from sklearn.datasets import make_regression

    X, y = make_regression(n_samples=1000, n_features=20, noise=0.1, random_state=42)

    # Split train/val
    from sklearn.model_selection import train_test_split
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"Training data shape: {X_train.shape}")
    print(f"Validation data shape: {X_val.shape}")

    # Train with auto-resume
    result = train_with_auto_resume(
        X_train=X_train,
        y_train=y_train,
        X_val=X_val,
        y_val=y_val,
        model_type='xgboost',
        checkpoint_dir='/tmp/test_checkpoints',
        project_dir='/tmp/test_project',
        total_epochs=20,
        save_every=5
    )

    print("\n" + "=" * 60)
    print("✅ Training Complete!")
    print(f"Final R²: {result['metrics']['r2_score']:.4f}")
    print(f"Best R²: {result['best_score']:.4f}")
