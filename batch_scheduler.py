import schedule
import time
import threading
import json
from pathlib import Path
from datetime import datetime
from typing import Callable, Optional

class BatchScheduler:
    def __init__(self, log_callback: Optional[Callable] = None):
        self.schedule_file = Path.home() / ".ytlive" / "schedule.json"
        self.schedule_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.log_callback = log_callback or print
        self.is_running = False
        self.scheduler_thread = None
        
        self.scheduled_time = "09:00"
        self.excel_file_path = None
        self.enabled = False
        
        self.load_schedule()
    
    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.log_callback(f"[{timestamp}] {message}")
        except UnicodeEncodeError:
            # Fallback for Windows console encoding issues
            safe_message = message.encode('ascii', 'replace').decode('ascii')
            self.log_callback(f"[{timestamp}] {safe_message}")
    
    def load_schedule(self) -> bool:
        """Load schedule configuration from file"""
        try:
            if self.schedule_file.exists():
                with open(self.schedule_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.scheduled_time = data.get('scheduled_time', '09:00')
                    self.excel_file_path = data.get('excel_file_path')
                    self.enabled = data.get('enabled', False)
                    return True
        except Exception as e:
            self.log(f"Error loading schedule: {str(e)}")
        return False
    
    def save_schedule(self) -> bool:
        """Save schedule configuration to file"""
        try:
            data = {
                'scheduled_time': self.scheduled_time,
                'excel_file_path': self.excel_file_path,
                'enabled': self.enabled,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.schedule_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            self.log(f"Error saving schedule: {str(e)}")
            return False
    
    def set_schedule(self, time_str: str, excel_path: str, enabled: bool = True):
        """Configure the schedule
        
        Args:
            time_str: Time in HH:MM format (24-hour)
            excel_path: Path to Excel file
            enabled: Whether scheduling is enabled
        """
        try:
            # Validate time format
            datetime.strptime(time_str, "%H:%M")
            
            self.scheduled_time = time_str
            self.excel_file_path = excel_path
            self.enabled = enabled
            
            if self.save_schedule():
                self.log(f"[OK] Schedule configured: Daily at {time_str}")
                return True
            return False
        except ValueError:
            self.log("[ERROR] Invalid time format. Use HH:MM (e.g., 09:00)")
            return False
    
    def start_scheduler(self, process_callback: Callable):
        """Start the scheduler thread
        
        Args:
            process_callback: Function to call when scheduled time arrives
        """
        if self.is_running:
            self.log("[WARNING] Scheduler already running")
            return False
        
        if not self.enabled:
            self.log("[WARNING] Scheduler is disabled")
            return False
        
        if not self.excel_file_path:
            self.log("[ERROR] No Excel file configured")
            return False
        
        # Clear any existing schedules
        schedule.clear()
        
        # Schedule the job
        schedule.every().day.at(self.scheduled_time).do(
            self._run_scheduled_job, 
            process_callback
        )
        
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        
        self.log(f"[OK] Scheduler started - Daily batch at {self.scheduled_time}")
        return True
    
    def _run_scheduled_job(self, process_callback: Callable):
        """Internal method to run the scheduled job"""
        self.log(f"\n{'='*60}")
        self.log(f"[SCHEDULER] BATCH STARTED")
        self.log(f"{'='*60}")
        self.log(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"Excel File: {self.excel_file_path}")
        self.log(f"{'='*60}\n")
        
        try:
            process_callback()
            self.log(f"\n[OK] Scheduled batch completed successfully\n")
        except Exception as e:
            self.log(f"\n[ERROR] Scheduled batch failed: {str(e)}\n")
            import traceback
            self.log(traceback.format_exc())
    
    def _scheduler_loop(self):
        """Internal scheduler loop"""
        self.log("Scheduler loop started")
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                self.log(f"Scheduler error: {str(e)}")
                time.sleep(60)
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        if not self.is_running:
            return False
        
        self.is_running = False
        schedule.clear()
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=2)
        
        self.log("[OK] Scheduler stopped")
        return True
    
    def get_next_run_time(self) -> Optional[str]:
        """Get the next scheduled run time"""
        if not self.enabled or not schedule.jobs:
            return None
        
        try:
            next_run = schedule.next_run()
            if next_run:
                return next_run.strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass
        return None
    
    def get_status(self) -> dict:
        """Get current scheduler status"""
        return {
            'enabled': self.enabled,
            'running': self.is_running,
            'scheduled_time': self.scheduled_time,
            'excel_file': self.excel_file_path,
            'next_run': self.get_next_run_time()
        }
