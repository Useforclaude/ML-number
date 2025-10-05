"""
GPU Monitoring Utility for Real-time GPU Usage Tracking
Shows GPU utilization every N seconds during training
"""

import subprocess
import threading
import time
from datetime import datetime


class GPUMonitor:
    """
    Real-time GPU monitoring that runs in background thread

    Usage:
        monitor = GPUMonitor(interval=30)  # Check every 30 seconds
        monitor.start()

        # Your training code here...

        monitor.stop()
    """

    def __init__(self, interval=30, verbose=True):
        """
        Initialize GPU monitor

        Parameters:
        -----------
        interval : int
            Seconds between GPU checks (default: 30)
        verbose : bool
            Print detailed info (default: True)
        """
        self.interval = interval
        self.verbose = verbose
        self.running = False
        self.thread = None
        self.gpu_available = self._check_gpu()

    def _check_gpu(self):
        """Check if GPU is available"""
        try:
            subprocess.check_output(
                ['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'],
                stderr=subprocess.DEVNULL
            )
            return True
        except:
            return False

    def _get_gpu_info(self):
        """Get current GPU statistics"""
        if not self.gpu_available:
            return None

        try:
            # Get GPU name
            gpu_name = subprocess.check_output(
                ['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            # Get GPU utilization
            gpu_util = subprocess.check_output(
                ['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            # Get GPU memory
            gpu_mem_used = subprocess.check_output(
                ['nvidia-smi', '--query-gpu=memory.used', '--format=csv,noheader'],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            gpu_mem_total = subprocess.check_output(
                ['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader'],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            # Get temperature
            gpu_temp = subprocess.check_output(
                ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            # Get power usage
            gpu_power = subprocess.check_output(
                ['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader'],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            return {
                'name': gpu_name,
                'utilization': int(gpu_util),
                'memory_used': gpu_mem_used,
                'memory_total': gpu_mem_total,
                'temperature': int(gpu_temp),
                'power': gpu_power
            }
        except Exception as e:
            if self.verbose:
                print(f"⚠️  GPU info error: {e}")
            return None

    def _monitor_loop(self):
        """Background monitoring loop"""
        print(f"\n{'='*80}")
        print(f"🎮 GPU MONITORING STARTED (checking every {self.interval} seconds)")
        print(f"{'='*80}\n")

        check_count = 0

        while self.running:
            info = self._get_gpu_info()

            if info:
                check_count += 1
                timestamp = datetime.now().strftime('%H:%M:%S')

                # Determine status emoji based on utilization
                if info['utilization'] >= 70:
                    status = "🔥"
                    status_text = "ACTIVE"
                elif info['utilization'] >= 30:
                    status = "⚡"
                    status_text = "WORKING"
                elif info['utilization'] > 0:
                    status = "💤"
                    status_text = "IDLE"
                else:
                    status = "⚪"
                    status_text = "UNUSED"

                # Print compact format
                print(f"[{timestamp}] {status} GPU: {info['utilization']:3d}% | "
                      f"Mem: {info['memory_used']:>10s} / {info['memory_total']} | "
                      f"Temp: {info['temperature']:2d}°C | "
                      f"Power: {info['power']:>7s} | "
                      f"Status: {status_text}")

                # Print detailed warning if GPU is idle during training
                if check_count > 2 and info['utilization'] == 0:
                    print(f"    ⚠️  GPU utilization is 0% - may be using CPU instead!")
                    print(f"    💡 This is normal during data loading or CPU-only models (RandomForest)")

            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  GPU not available")

            # Sleep for interval
            time.sleep(self.interval)

    def start(self):
        """Start GPU monitoring in background thread"""
        if not self.gpu_available:
            print("⚠️  No GPU detected - monitoring disabled")
            return False

        if self.running:
            print("⚠️  GPU monitoring already running")
            return False

        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        return True

    def stop(self):
        """Stop GPU monitoring"""
        if not self.running:
            return

        self.running = False
        if self.thread:
            self.thread.join(timeout=2)

        print(f"\n{'='*80}")
        print(f"🎮 GPU MONITORING STOPPED")
        print(f"{'='*80}\n")

    def get_current_usage(self):
        """Get current GPU usage (synchronous)"""
        return self._get_gpu_info()


def print_gpu_summary():
    """Print a one-time GPU summary"""
    monitor = GPUMonitor(verbose=False)
    info = monitor.get_current_usage()

    if info:
        print(f"\n{'='*80}")
        print(f"🎮 GPU SUMMARY")
        print(f"{'='*80}")
        print(f"GPU Model:       {info['name']}")
        print(f"Utilization:     {info['utilization']}%")
        print(f"Memory Used:     {info['memory_used']} / {info['memory_total']}")
        print(f"Temperature:     {info['temperature']}°C")
        print(f"Power Draw:      {info['power']}")
        print(f"{'='*80}\n")
        return True
    else:
        print("\n⚠️  No GPU available\n")
        return False


if __name__ == "__main__":
    # Test GPU monitoring
    print("Testing GPU Monitor for 60 seconds...")
    monitor = GPUMonitor(interval=10)

    if monitor.start():
        try:
            time.sleep(60)
        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            monitor.stop()
    else:
        print("GPU monitoring failed to start")
