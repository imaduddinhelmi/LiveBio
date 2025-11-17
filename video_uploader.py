import os
import threading
import time
from datetime import datetime, timedelta
from queue import Queue, Empty
import json
from pathlib import Path

class VideoUploader:
    def __init__(self, youtube_service):
        self.youtube_service = youtube_service
        self.upload_queue = Queue()
        self.scheduled_uploads = []
        self.is_running = False
        self.scheduler_thread = None
        self.config_file = Path.home() / ".ytlive" / "scheduled_uploads.json"
        self.load_scheduled_uploads()
    
    def add_to_queue(self, video_data):
        """Add video to upload queue"""
        self.upload_queue.put(video_data)
    
    def schedule_upload(self, video_data, scheduled_time):
        """Schedule a video upload for a specific time"""
        upload_item = {
            "video_data": video_data,
            "scheduled_time": scheduled_time,
            "status": "pending",
            "added_at": datetime.now().isoformat()
        }
        self.scheduled_uploads.append(upload_item)
        self.save_scheduled_uploads()
        return len(self.scheduled_uploads) - 1
    
    def remove_scheduled_upload(self, index):
        """Remove a scheduled upload by index"""
        if 0 <= index < len(self.scheduled_uploads):
            removed = self.scheduled_uploads.pop(index)
            self.save_scheduled_uploads()
            return True, removed
        return False, "Invalid index"
    
    def get_scheduled_uploads(self):
        """Get all scheduled uploads"""
        return self.scheduled_uploads.copy()
    
    def cancel_upload(self, index: int) -> bool:
        """Cancel a scheduled upload by index"""
        try:
            if 0 <= index < len(self.scheduled_uploads):
                upload_item = self.scheduled_uploads[index]
                
                if upload_item['status'] == 'pending':
                    upload_item['status'] = 'cancelled'
                    upload_item['cancelled_at'] = datetime.now().isoformat()
                    self.save_scheduled_uploads()
                    return True
            return False
        except Exception as e:
            print(f"Error cancelling upload: {e}")
            return False
    
    def clear_completed_uploads(self):
        """Remove completed/failed/cancelled uploads from schedule"""
        self.scheduled_uploads = [
            item for item in self.scheduled_uploads 
            if item["status"] not in ['completed', 'failed', 'cancelled']
        ]
        self.save_scheduled_uploads()
    
    def save_scheduled_uploads(self):
        """Save scheduled uploads to file"""
        try:
            os.makedirs(self.config_file.parent, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.scheduled_uploads, f, indent=2)
        except Exception as e:
            print(f"Error saving scheduled uploads: {e}")
    
    def load_scheduled_uploads(self):
        """Load scheduled uploads from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.scheduled_uploads = json.load(f)
        except Exception as e:
            print(f"Error loading scheduled uploads: {e}")
            self.scheduled_uploads = []
    
    def start_scheduler(self, log_callback=None):
        """Start the scheduler thread"""
        if self.is_running:
            return False, "Scheduler already running"
        
        self.is_running = True
        self.scheduler_thread = threading.Thread(
            target=self._scheduler_loop,
            args=(log_callback,),
            daemon=True
        )
        self.scheduler_thread.start()
        return True, "Scheduler started"
    
    def stop_scheduler(self):
        """Stop the scheduler thread"""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        return True, "Scheduler stopped"
    
    def _scheduler_loop(self, log_callback=None):
        """Main scheduler loop - checks for due uploads"""
        def log(msg):
            if log_callback:
                log_callback(msg)
        
        log("[SCHEDULER] Started - checking every 30 seconds")
        
        while self.is_running:
            try:
                now = datetime.now()
                
                for item in self.scheduled_uploads:
                    if item["status"] != "pending":
                        continue
                    
                    scheduled_time = datetime.fromisoformat(item["scheduled_time"])
                    
                    if now >= scheduled_time:
                        log(f"[SCHEDULER] Processing scheduled upload: {item['video_data']['title']}")
                        item["status"] = "processing"
                        self.save_scheduled_uploads()
                        
                        success, result = self.upload_video(
                            item["video_data"],
                            log_callback=log
                        )
                        
                        if success:
                            item["status"] = "completed"
                            item["video_id"] = result
                            item["completed_at"] = datetime.now().isoformat()
                            log(f"[SCHEDULER] ✓ Upload completed: {result}")
                        else:
                            item["status"] = "failed"
                            item["error"] = str(result)
                            item["failed_at"] = datetime.now().isoformat()
                            log(f"[SCHEDULER] ✗ Upload failed: {result}")
                        
                        self.save_scheduled_uploads()
                
                time.sleep(30)
                
            except Exception as e:
                log(f"[SCHEDULER] Error: {str(e)}")
                time.sleep(30)
        
        log("[SCHEDULER] Stopped")
    
    def upload_video(self, video_data, log_callback=None):
        """Upload a video to YouTube"""
        def log(msg):
            if log_callback:
                log_callback(msg)
        
        try:
            video_path = video_data["videoPath"]
            
            if not os.path.exists(video_path):
                return False, f"Video file not found: {video_path}"
            
            log(f"[UPLOAD] Starting upload: {video_data['title']}")
            log(f"[UPLOAD] File: {video_path}")
            log(f"[UPLOAD] Size: {os.path.getsize(video_path) / (1024*1024):.2f} MB")
            
            success, result = self.youtube_service.upload_video_file(video_data)
            
            if success:
                video_id = result
                log(f"[UPLOAD] ✓ Video uploaded successfully! ID: {video_id}")
                
                if video_data.get("thumbnailPath"):
                    log(f"[UPLOAD] Uploading thumbnail...")
                    thumb_success, thumb_result = self.youtube_service.upload_thumbnail(
                        video_id, 
                        video_data["thumbnailPath"]
                    )
                    if thumb_success:
                        log(f"[UPLOAD] ✓ Thumbnail uploaded")
                    else:
                        log(f"[UPLOAD] ⚠ Thumbnail upload failed: {thumb_result}")
                
                return True, video_id
            else:
                log(f"[UPLOAD] ✗ Upload failed: {result}")
                return False, result
                
        except Exception as e:
            error_msg = f"Upload error: {str(e)}"
            log(f"[UPLOAD] ✗ {error_msg}")
            return False, error_msg
    
    def upload_video_immediate(self, video_data, log_callback=None):
        """Upload video immediately (not scheduled)"""
        return self.upload_video(video_data, log_callback)
