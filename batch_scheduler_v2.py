"""
Enhanced Batch Scheduler with Multiple Schedules Support
Supports multiple scheduled batch processes with individual management
"""

import schedule
import time
import threading
import json
from pathlib import Path
from datetime import datetime
from typing import Callable, Optional, List, Dict
import uuid

class BatchSchedulerV2:
    def __init__(self, log_callback: Optional[Callable] = None):
        self.schedule_file = Path.home() / ".ytlive" / "schedules.json"
        self.schedule_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.log_callback = log_callback or print
        self.is_running = False
        self.scheduler_thread = None
        
        # List of schedules: [{id, time, excel_path, enabled, name}]
        self.schedules: List[Dict] = []
        
        self.load_schedules()
    
    def log(self, message: str):
        """Log message with timestamp and error handling"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.log_callback(f"[{timestamp}] {message}")
        except (UnicodeEncodeError, Exception) as e:
            # Fallback for encoding issues
            try:
                safe_message = str(message).encode('ascii', 'replace').decode('ascii')
                self.log_callback(f"[{timestamp}] {safe_message}")
            except:
                print(f"[{timestamp}] [LOG ERROR] {e}")
    
    def load_schedules(self) -> bool:
        """Load all schedules from file"""
        try:
            if self.schedule_file.exists():
                with open(self.schedule_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.schedules = data.get('schedules', [])
                    return True
        except Exception as e:
            self.log(f"Error loading schedules: {str(e)}")
        return False
    
    def save_schedules(self) -> bool:
        """Save all schedules to file"""
        try:
            data = {
                'schedules': self.schedules,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.schedule_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            self.log(f"Error saving schedules: {str(e)}")
            return False
    
    def add_schedule(self, time_str: str, excel_path: str, name: str = "", enabled: bool = True) -> Optional[str]:
        """Add a new schedule
        
        Args:
            time_str: Time in HH:MM format (24-hour)
            excel_path: Path to Excel file
            name: Optional name for the schedule
            enabled: Whether scheduling is enabled
            
        Returns:
            Schedule ID if successful, None otherwise
        """
        try:
            # Validate time format
            datetime.strptime(time_str, "%H:%M")
            
            schedule_id = str(uuid.uuid4())
            
            if not name:
                name = f"Schedule {len(self.schedules) + 1}"
            
            schedule_item = {
                'id': schedule_id,
                'name': name,
                'time': time_str,
                'excel_path': excel_path,
                'enabled': enabled,
                'created_at': datetime.now().isoformat(),
                'last_run': None
            }
            
            self.schedules.append(schedule_item)
            
            if self.save_schedules():
                self.log(f"[OK] Schedule added: {name} at {time_str}")
                return schedule_id
            return None
        except ValueError:
            self.log("[ERROR] Invalid time format. Use HH:MM (e.g., 09:00)")
            return None
        except Exception as e:
            self.log(f"[ERROR] Failed to add schedule: {str(e)}")
            return None
    
    def update_schedule(self, schedule_id: str, time_str: Optional[str] = None, 
                       excel_path: Optional[str] = None, name: Optional[str] = None,
                       enabled: Optional[bool] = None) -> bool:
        """Update an existing schedule"""
        try:
            for schedule in self.schedules:
                if schedule['id'] == schedule_id:
                    if time_str:
                        datetime.strptime(time_str, "%H:%M")  # Validate
                        schedule['time'] = time_str
                    if excel_path:
                        schedule['excel_path'] = excel_path
                    if name:
                        schedule['name'] = name
                    if enabled is not None:
                        schedule['enabled'] = enabled
                    
                    return self.save_schedules()
            return False
        except Exception as e:
            self.log(f"[ERROR] Failed to update schedule: {str(e)}")
            return False
    
    def remove_schedule(self, schedule_id: str) -> bool:
        """Remove a schedule"""
        try:
            self.schedules = [s for s in self.schedules if s['id'] != schedule_id]
            return self.save_schedules()
        except Exception as e:
            self.log(f"[ERROR] Failed to remove schedule: {str(e)}")
            return False
    
    def get_schedule(self, schedule_id: str) -> Optional[Dict]:
        """Get a specific schedule by ID"""
        for schedule in self.schedules:
            if schedule['id'] == schedule_id:
                return schedule.copy()
        return None
    
    def get_all_schedules(self) -> List[Dict]:
        """Get all schedules"""
        return [s.copy() for s in self.schedules]
    
    def get_enabled_schedules(self) -> List[Dict]:
        """Get only enabled schedules"""
        return [s.copy() for s in self.schedules if s.get('enabled', False)]
    
    def start_scheduler(self, process_callback: Callable):
        """Start the scheduler thread
        
        Args:
            process_callback: Function to call when scheduled time arrives
                             Should accept (excel_path, schedule_name) as parameters
        """
        if self.is_running:
            self.log("[WARNING] Scheduler already running")
            return False
        
        enabled_schedules = self.get_enabled_schedules()
        if not enabled_schedules:
            self.log("[WARNING] No enabled schedules")
            return False
        
        # Clear any existing schedules
        schedule.clear()
        
        # Schedule all enabled jobs
        for sched in enabled_schedules:
            schedule.every().day.at(sched['time']).do(
                self._run_scheduled_job,
                process_callback,
                sched['id'],
                sched['excel_path'],
                sched['name']
            ).tag(sched['id'])
        
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        
        self.log(f"[OK] Scheduler started - {len(enabled_schedules)} schedule(s) active")
        return True
    
    def _run_scheduled_job(self, process_callback: Callable, schedule_id: str, 
                          excel_path: str, schedule_name: str):
        """Internal method to run a scheduled job"""
        self.log(f"\n{'='*60}")
        self.log(f"[SCHEDULER] BATCH STARTED: {schedule_name}")
        self.log(f"{'='*60}")
        self.log(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"Excel File: {excel_path}")
        self.log(f"{'='*60}\n")
        
        try:
            # Update last_run time
            for sched in self.schedules:
                if sched['id'] == schedule_id:
                    sched['last_run'] = datetime.now().isoformat()
            self.save_schedules()
            
            # Execute the callback
            process_callback(excel_path, schedule_name)
            
            self.log(f"\n[OK] Scheduled batch completed: {schedule_name}\n")
        except Exception as e:
            self.log(f"\n[ERROR] Scheduled batch failed: {str(e)}\n")
            import traceback
            self.log(traceback.format_exc())
    
    def _scheduler_loop(self):
        """Internal scheduler loop with better error handling"""
        self.log("Scheduler loop started")
        error_count = 0
        max_errors = 10
        
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds
                error_count = 0  # Reset error count on success
            except Exception as e:
                error_count += 1
                self.log(f"Scheduler loop error ({error_count}/{max_errors}): {str(e)}")
                
                if error_count >= max_errors:
                    self.log("[CRITICAL] Too many scheduler errors, stopping scheduler")
                    self.is_running = False
                    break
                
                time.sleep(60)  # Wait longer on error
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        if not self.is_running:
            return False
        
        try:
            self.is_running = False
            schedule.clear()
            
            if self.scheduler_thread:
                self.scheduler_thread.join(timeout=5)
            
            self.log("[OK] Scheduler stopped")
            return True
        except Exception as e:
            self.log(f"[ERROR] Error stopping scheduler: {str(e)}")
            return False
    
    def restart_scheduler(self, process_callback: Callable):
        """Restart the scheduler with current schedules"""
        self.stop_scheduler()
        time.sleep(1)
        return self.start_scheduler(process_callback)
    
    def get_next_run_times(self) -> Dict[str, Optional[str]]:
        """Get next run time for all schedules"""
        result = {}
        
        for job in schedule.jobs:
            schedule_id = job.tags.pop() if job.tags else None
            if schedule_id:
                try:
                    next_run = job.next_run
                    if next_run:
                        result[schedule_id] = next_run.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    result[schedule_id] = None
        
        return result
    
    def get_status(self) -> dict:
        """Get current scheduler status"""
        return {
            'running': self.is_running,
            'total_schedules': len(self.schedules),
            'enabled_schedules': len(self.get_enabled_schedules()),
            'schedules': self.get_all_schedules(),
            'next_runs': self.get_next_run_times() if self.is_running else {}
        }
