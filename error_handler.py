"""
Enhanced Error Handler for Long-Running Operations
Provides robust error handling, resource cleanup, and retry logic
"""

import functools
import threading
import time
import traceback
from typing import Callable, Optional, Any
from datetime import datetime

class ErrorHandler:
    """Centralized error handling and resource management"""
    
    @staticmethod
    def safe_thread_execute(func: Callable, log_callback: Optional[Callable] = None,
                           error_callback: Optional[Callable] = None,
                           finally_callback: Optional[Callable] = None,
                           max_retries: int = 0, retry_delay: float = 1.0) -> threading.Thread:
        """
        Execute a function in a thread with comprehensive error handling
        
        Args:
            func: Function to execute
            log_callback: Logging function
            error_callback: Called on error with exception
            finally_callback: Called after execution (success or failure)
            max_retries: Number of retry attempts on failure
            retry_delay: Delay between retries in seconds
            
        Returns:
            Thread object
        """
        
        def wrapped():
            attempts = 0
            last_error = None
            
            while attempts <= max_retries:
                try:
                    if log_callback and attempts > 0:
                        log_callback(f"[RETRY] Attempt {attempts + 1}/{max_retries + 1}")
                    
                    func()
                    
                    if log_callback and attempts > 0:
                        log_callback(f"[SUCCESS] Succeeded after {attempts + 1} attempt(s)")
                    
                    break  # Success, exit loop
                    
                except Exception as e:
                    last_error = e
                    attempts += 1
                    
                    error_msg = f"[ERROR] {type(e).__name__}: {str(e)}"
                    
                    if log_callback:
                        log_callback(error_msg)
                        if attempts <= max_retries:
                            log_callback(f"[RETRY] Retrying in {retry_delay}s...")
                    
                    if error_callback:
                        try:
                            error_callback(e)
                        except Exception as callback_error:
                            if log_callback:
                                log_callback(f"[ERROR] Error callback failed: {callback_error}")
                    
                    if attempts <= max_retries:
                        time.sleep(retry_delay)
                    else:
                        if log_callback:
                            log_callback(f"[FAILED] All {max_retries + 1} attempts failed")
                            log_callback(traceback.format_exc())
                
                finally:
                    if attempts > max_retries:
                        # Final cleanup after all retries exhausted
                        if finally_callback:
                            try:
                                finally_callback()
                            except Exception as cleanup_error:
                                if log_callback:
                                    log_callback(f"[ERROR] Cleanup failed: {cleanup_error}")
        
        thread = threading.Thread(target=wrapped, daemon=True)
        thread.start()
        return thread
    
    @staticmethod
    def safe_execute(func: Callable, default_return: Any = None,
                    log_callback: Optional[Callable] = None) -> Any:
        """
        Execute a function with try-catch and return default on error
        
        Args:
            func: Function to execute
            default_return: Value to return on error
            log_callback: Optional logging function
            
        Returns:
            Function result or default_return on error
        """
        try:
            return func()
        except Exception as e:
            if log_callback:
                log_callback(f"[ERROR] {type(e).__name__}: {str(e)}")
            return default_return
    
    @staticmethod
    def watchdog_wrapper(func: Callable, timeout: float = 300.0,
                        log_callback: Optional[Callable] = None) -> Callable:
        """
        Wrap a function with a watchdog timer
        
        Args:
            func: Function to wrap
            timeout: Timeout in seconds
            log_callback: Optional logging function
            
        Returns:
            Wrapped function
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=target, daemon=True)
            thread.start()
            thread.join(timeout)
            
            if thread.is_alive():
                if log_callback:
                    log_callback(f"[TIMEOUT] Function exceeded {timeout}s timeout")
                raise TimeoutError(f"Operation timed out after {timeout}s")
            
            if exception[0]:
                raise exception[0]
            
            return result[0]
        
        return wrapper


class ResourceMonitor:
    """Monitor resources and prevent memory leaks"""
    
    def __init__(self, log_callback: Optional[Callable] = None):
        self.log_callback = log_callback
        self.threads = []
        self.cleanup_callbacks = []
    
    def register_thread(self, thread: threading.Thread):
        """Register a thread for monitoring"""
        self.threads.append({
            'thread': thread,
            'created_at': datetime.now(),
            'name': getattr(thread, 'name', 'unnamed')
        })
    
    def register_cleanup(self, callback: Callable):
        """Register a cleanup callback"""
        self.cleanup_callbacks.append(callback)
    
    def cleanup_dead_threads(self):
        """Remove references to dead threads"""
        self.threads = [t for t in self.threads if t['thread'].is_alive()]
    
    def get_active_thread_count(self) -> int:
        """Get count of active monitored threads"""
        self.cleanup_dead_threads()
        return len(self.threads)
    
    def force_cleanup(self):
        """Force cleanup of all registered resources"""
        if self.log_callback:
            self.log_callback("[CLEANUP] Starting resource cleanup...")
        
        # Call all cleanup callbacks
        for callback in self.cleanup_callbacks:
            try:
                callback()
            except Exception as e:
                if self.log_callback:
                    self.log_callback(f"[CLEANUP ERROR] {e}")
        
        # Log thread status
        self.cleanup_dead_threads()
        if self.log_callback and self.threads:
            self.log_callback(f"[CLEANUP] {len(self.threads)} thread(s) still active")
    
    def get_status(self) -> dict:
        """Get resource status"""
        self.cleanup_dead_threads()
        return {
            'active_threads': len(self.threads),
            'cleanup_callbacks': len(self.cleanup_callbacks),
            'threads': [
                {
                    'name': t['name'],
                    'alive': t['thread'].is_alive(),
                    'age_seconds': (datetime.now() - t['created_at']).total_seconds()
                }
                for t in self.threads
            ]
        }
