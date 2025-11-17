"""
Patch untuk video_uploader.py
Menambahkan method cancel_upload dan update clear_completed_uploads
"""

# TAMBAHKAN METHOD INI KE CLASS VideoUploader (setelah remove_scheduled_upload):

def cancel_upload(self, index: int) -> bool:
    """
    Cancel a scheduled upload by index
    
    Args:
        index: Index of upload to cancel
        
    Returns:
        True if cancelled successfully, False otherwise
    """
    try:
        if 0 <= index < len(self.scheduled_uploads):
            upload_item = self.scheduled_uploads[index]
            
            # Only cancel if status is pending
            if upload_item['status'] == 'pending':
                upload_item['status'] = 'cancelled'
                upload_item['cancelled_at'] = datetime.now().isoformat()
                self.save_scheduled_uploads()
                return True
        return False
    except Exception as e:
        print(f"Error cancelling upload: {e}")
        return False

def cancel_multiple_uploads(self, indices: list) -> int:
    """
    Cancel multiple scheduled uploads
    
    Args:
        indices: List of indices to cancel
        
    Returns:
        Number of successfully cancelled uploads
    """
    cancelled_count = 0
    
    # Sort indices in reverse to maintain index validity
    for index in sorted(indices, reverse=True):
        if self.cancel_upload(index):
            cancelled_count += 1
    
    return cancelled_count


# UPDATE METHOD clear_completed_uploads() - Ganti dengan versi ini:

def clear_completed_uploads(self):
    """
    Remove completed, failed, and cancelled uploads from schedule
    """
    try:
        self.scheduled_uploads = [
            item for item in self.scheduled_uploads 
            if item['status'] not in ['completed', 'failed', 'cancelled']
        ]
        self.save_scheduled_uploads()
        return True
    except Exception as e:
        print(f"Error clearing uploads: {e}")
        return False


# TAMBAHKAN METHOD BARU untuk statistik:

def get_upload_statistics(self) -> dict:
    """
    Get statistics about scheduled uploads
    
    Returns:
        Dictionary with upload statistics
    """
    stats = {
        'total': len(self.scheduled_uploads),
        'pending': 0,
        'processing': 0,
        'completed': 0,
        'failed': 0,
        'cancelled': 0
    }
    
    for upload in self.scheduled_uploads:
        status = upload.get('status', 'unknown')
        if status in stats:
            stats[status] += 1
    
    return stats


# UPDATE _scheduler_loop untuk lebih robust:

def _scheduler_loop(self, log_callback=None):
    """
    Main scheduler loop - checks for due uploads with better error handling
    """
    def log(msg):
        if log_callback:
            try:
                log_callback(msg)
            except Exception as e:
                print(f"Log callback error: {e}")
    
    log("[VIDEO SCHEDULER] Started - checking every 30 seconds")
    
    error_count = 0
    max_errors = 5
    
    while self.is_running:
        try:
            now = datetime.now()
            
            # Process scheduled uploads
            for upload_item in self.scheduled_uploads:
                # Skip if not pending
                if upload_item['status'] != 'pending':
                    continue
                
                # Check if due
                try:
                    scheduled_time = datetime.fromisoformat(upload_item['scheduled_time'])
                    
                    if now >= scheduled_time:
                        log(f"[VIDEO UPLOAD] Starting scheduled upload: {upload_item['video_data']['title']}")
                        
                        # Update status
                        upload_item['status'] = 'processing'
                        upload_item['started_at'] = now.isoformat()
                        self.save_scheduled_uploads()
                        
                        # Perform upload
                        try:
                            success, result = self.upload_video_immediate(
                                upload_item['video_data'],
                                log_callback=log_callback
                            )
                            
                            if success:
                                upload_item['status'] = 'completed'
                                upload_item['video_id'] = result
                                upload_item['completed_at'] = datetime.now().isoformat()
                                log(f"[VIDEO UPLOAD] ✓ Upload completed: {result}")
                            else:
                                upload_item['status'] = 'failed'
                                upload_item['error'] = str(result)
                                upload_item['failed_at'] = datetime.now().isoformat()
                                log(f"[VIDEO UPLOAD] ✗ Upload failed: {result}")
                            
                            self.save_scheduled_uploads()
                            
                        except Exception as e:
                            upload_item['status'] = 'failed'
                            upload_item['error'] = str(e)
                            upload_item['failed_at'] = datetime.now().isoformat()
                            self.save_scheduled_uploads()
                            log(f"[VIDEO UPLOAD] ✗ Exception: {e}")
                
                except Exception as e:
                    log(f"[VIDEO SCHEDULER] Error processing upload: {e}")
            
            # Reset error count on successful iteration
            error_count = 0
            
            # Wait before next check
            time.sleep(30)  # Check every 30 seconds
            
        except Exception as e:
            error_count += 1
            log(f"[VIDEO SCHEDULER] Loop error ({error_count}/{max_errors}): {e}")
            
            if error_count >= max_errors:
                log(f"[VIDEO SCHEDULER] Too many errors, stopping scheduler")
                self.is_running = False
                break
            
            time.sleep(60)  # Wait longer on error
    
    log("[VIDEO SCHEDULER] Stopped")
