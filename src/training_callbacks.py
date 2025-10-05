"""
Training Callbacks for Real-time Monitoring
- Verbose checkpoint logging
- GPU monitoring during training
- Progress tracking every N epochs
"""

import time
import subprocess
from datetime import datetime
from optuna.study import StudyDirection
from optuna import Study, Trial


class VerboseCheckpointCallback:
    """
    Callback สำหรับแสดง checkpoint logs แบบ verbose
    """
    def __init__(self, checkpoint_manager, save_every=10):
        """
        Parameters:
        -----------
        checkpoint_manager : CheckpointManager
            Checkpoint manager instance
        save_every : int
            Save checkpoint ทุกกี่ trials (default: 10)
        """
        self.checkpoint_manager = checkpoint_manager
        self.save_every = save_every
        self.last_save_time = time.time()

    def __call__(self, study: Study, trial: Trial):
        """Optuna callback - เรียกทุก trial"""
        trial_number = trial.number + 1

        # Save checkpoint ทุก N trials
        if trial_number % self.save_every == 0:
            elapsed = time.time() - self.last_save_time

            print(f"\n{'='*80}")
            print(f"💾 CHECKPOINT SAVE - Trial {trial_number}")
            print(f"{'='*80}")
            print(f"⏱️  Time since last save: {elapsed:.1f} seconds")
            print(f"🎯 Best value so far: {study.best_value:.6f}")
            print(f"📊 Trials completed: {trial_number}/{len(study.trials) if hasattr(study, 'trials') else '?'}")

            # Save checkpoint
            save_start = time.time()
            self.checkpoint_manager.save_checkpoint(
                trial_number=trial_number,
                best_value=study.best_value,
                best_params=study.best_params
            )
            save_time = time.time() - save_start

            print(f"✅ Checkpoint saved in {save_time:.2f} seconds")
            print(f"📁 Location: {self.checkpoint_manager.checkpoint_dir}")
            print(f"{'='*80}\n")

            self.last_save_time = time.time()


class GPUMonitorCallback:
    """
    Callback สำหรับ monitor GPU แบบ real-time ระหว่าง training
    """
    def __init__(self, check_every=5, verbose=True):
        """
        Parameters:
        -----------
        check_every : int
            Check GPU ทุกกี่ trials (default: 5)
        verbose : bool
            แสดง GPU stats หรือไม่ (default: True)
        """
        self.check_every = check_every
        self.verbose = verbose
        self.gpu_available = self._check_gpu_available()

    def _check_gpu_available(self):
        """Check if nvidia-smi is available"""
        try:
            subprocess.check_output(['nvidia-smi'])
            return True
        except:
            return False

    def _get_gpu_stats(self):
        """Get current GPU stats"""
        if not self.gpu_available:
            return None

        try:
            # Get GPU utilization
            gpu_util = subprocess.check_output([
                'nvidia-smi',
                '--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw',
                '--format=csv,noheader,nounits'
            ]).decode('utf-8').strip().split(',')

            return {
                'utilization': int(gpu_util[0]),
                'memory_used': int(gpu_util[1]),
                'memory_total': int(gpu_util[2]),
                'temperature': int(gpu_util[3]),
                'power': float(gpu_util[4])
            }
        except:
            return None

    def __call__(self, study: Study, trial: Trial):
        """Optuna callback - เรียกทุก trial"""
        trial_number = trial.number + 1

        # Check GPU ทุก N trials
        if trial_number % self.check_every == 0 and self.verbose:
            stats = self._get_gpu_stats()

            if stats:
                timestamp = datetime.now().strftime("%H:%M:%S")
                status = "ACTIVE" if stats['utilization'] > 10 else "IDLE"
                icon = "🔥" if stats['utilization'] > 50 else "⚪"

                print(f"\n[{timestamp}] {icon} GPU: {stats['utilization']:3d}% | "
                      f"Mem: {stats['memory_used']:5d}/{stats['memory_total']:5d} MiB | "
                      f"Temp: {stats['temperature']:2d}°C | "
                      f"Power: {stats['power']:5.1f} W | "
                      f"Status: {status}")


class ProgressCallback:
    """
    Callback สำหรับแสดง progress ระหว่าง Optuna trials
    """
    def __init__(self, n_trials, show_every=10):
        """
        Parameters:
        -----------
        n_trials : int
            จำนวน trials ทั้งหมด
        show_every : int
            แสดง progress ทุกกี่ trials
        """
        self.n_trials = n_trials
        self.show_every = show_every
        self.start_time = time.time()

    def __call__(self, study: Study, trial: Trial):
        """Optuna callback"""
        trial_number = trial.number + 1

        if trial_number % self.show_every == 0:
            elapsed = time.time() - self.start_time
            progress = (trial_number / self.n_trials) * 100
            avg_time_per_trial = elapsed / trial_number
            remaining_trials = self.n_trials - trial_number
            eta = remaining_trials * avg_time_per_trial

            print(f"\n📈 Progress: {trial_number}/{self.n_trials} ({progress:.1f}%)")
            print(f"⏱️  Elapsed: {self._format_time(elapsed)} | "
                  f"ETA: {self._format_time(eta)}")
            print(f"🎯 Best R² so far: {study.best_value:.6f}")

    def _format_time(self, seconds):
        """Format seconds to HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"


class EpochLoggingCallback:
    """
    Callback สำหรับแสดง epoch logs สำหรับ XGBoost, LightGBM, CatBoost
    (ใช้กับ model.fit() เท่านั้น, ไม่ใช่ cross_val_score)
    """
    def __init__(self, log_every=10):
        """
        Parameters:
        -----------
        log_every : int
            แสดง log ทุกกี่ epochs
        """
        self.log_every = log_every

    def xgboost_callback(self, env):
        """XGBoost callback function"""
        if env.iteration % self.log_every == 0:
            print(f"[Epoch {env.iteration}] Train R²: {env.evaluation_result_list[0][1]:.6f}")

    def lightgbm_callback(self, env):
        """LightGBM callback function"""
        if env.iteration % self.log_every == 0:
            print(f"[Epoch {env.iteration}] Train R²: {env.evaluation_result_list[0][2]:.6f}")


def create_training_callbacks(checkpoint_manager=None, n_trials=100, use_gpu=True):
    """
    สร้าง callbacks สำหรับ training pipeline

    Parameters:
    -----------
    checkpoint_manager : CheckpointManager, optional
        Checkpoint manager instance
    n_trials : int
        จำนวน Optuna trials
    use_gpu : bool
        ใช้ GPU หรือไม่

    Returns:
    --------
    callbacks : list
        List of Optuna callbacks
    """
    callbacks = []

    # Progress callback
    callbacks.append(ProgressCallback(n_trials=n_trials, show_every=10))

    # GPU monitor callback (ถ้าใช้ GPU)
    if use_gpu:
        callbacks.append(GPUMonitorCallback(check_every=5, verbose=True))

    # Checkpoint callback (ถ้ามี checkpoint manager)
    if checkpoint_manager:
        callbacks.append(VerboseCheckpointCallback(
            checkpoint_manager=checkpoint_manager,
            save_every=10
        ))

    return callbacks


def print_training_header(model_name, n_trials, use_gpu):
    """
    แสดง header สำหรับ training แต่ละ model

    Parameters:
    -----------
    model_name : str
        ชื่อ model (e.g., "XGBoost")
    n_trials : int
        จำนวน trials
    use_gpu : bool
        ใช้ GPU หรือไม่
    """
    gpu_icon = "🔥" if use_gpu else "⚪"
    gpu_text = "GPU" if use_gpu else "CPU"

    print(f"\n{'='*80}")
    print(f"{gpu_icon} Training {model_name} ({gpu_text})")
    print(f"{'='*80}")
    print(f"🎯 Target: Find best hyperparameters")
    print(f"🔬 Trials: {n_trials}")
    print(f"📊 Method: Optuna TPE Sampler + 10-Fold CV")
    print(f"⏱️  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")


def print_training_footer(model_name, best_score, elapsed_time):
    """
    แสดง footer หลัง training เสร็จ

    Parameters:
    -----------
    model_name : str
        ชื่อ model
    best_score : float
        Best R² score
    elapsed_time : float
        เวลาที่ใช้ (วินาที)
    """
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)

    print(f"\n{'='*80}")
    print(f"✅ {model_name} Training Complete!")
    print(f"{'='*80}")
    print(f"🎯 Best R² Score: {best_score:.6f}")
    print(f"⏱️  Time Elapsed: {hours:02d}:{minutes:02d}:{seconds:02d}")
    print(f"🏁 Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")
