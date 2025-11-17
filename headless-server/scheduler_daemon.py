#!/usr/bin/env python3
"""
Headless Scheduler Daemon
Runs in background and processes scheduled tasks
"""

import os
import sys
import time
import json
import signal
import logging
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from auth_headless import HeadlessAuth
from youtube_service import YouTubeService
from excel_parser import parse_excel_file

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('SchedulerDaemon')

class SchedulerDaemon:
    """Daemon for processing scheduled tasks"""
    
    def __init__(self):
        self.running = False
        self.auth = None
        self.youtube_service = None
        self.scheduled_batches = []
        self.scheduled_uploads = []
    
    def setup(self):
        """Setup authentication and services"""
        logger.info("Setting up scheduler daemon...")
        
        # Load authentication
        self.auth = HeadlessAuth()
        if not self.auth.load_saved_credentials():
            logger.error("Failed to load credentials. Please authenticate first.")
            return False
        
        # Create YouTube service
        youtube_client = self.auth.get_youtube_client()
        self.youtube_service = YouTubeService(youtube_client, self.auth)
        
        logger.info("Scheduler daemon setup complete")
        return True
    
    def load_scheduled_tasks(self):
        """Load scheduled tasks from files"""
        # Load scheduled batches
        if config.SCHEDULED_BATCHES_FILE.exists():
            try:
                with open(config.SCHEDULED_BATCHES_FILE, 'r') as f:
                    self.scheduled_batches = json.load(f)
                logger.info(f"Loaded {len(self.scheduled_batches)} scheduled batches")
            except Exception as e:
                logger.error(f"Error loading scheduled batches: {e}")
                self.scheduled_batches = []
        
        # Load scheduled uploads
        if config.SCHEDULED_UPLOADS_FILE.exists():
            try:
                with open(config.SCHEDULED_UPLOADS_FILE, 'r') as f:
                    self.scheduled_uploads = json.load(f)
                logger.info(f"Loaded {len(self.scheduled_uploads)} scheduled uploads")
            except Exception as e:
                logger.error(f"Error loading scheduled uploads: {e}")
                self.scheduled_uploads = []
    
    def save_scheduled_tasks(self):
        """Save scheduled tasks to files"""
        try:
            with open(config.SCHEDULED_BATCHES_FILE, 'w') as f:
                json.dump(self.scheduled_batches, f, indent=2)
            
            with open(config.SCHEDULED_UPLOADS_FILE, 'w') as f:
                json.dump(self.scheduled_uploads, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving scheduled tasks: {e}")
    
    def process_scheduled_batches(self):
        """Process scheduled batch broadcasts"""
        now = datetime.now()
        
        for batch in self.scheduled_batches:
            if batch['status'] != 'pending':
                continue
            
            scheduled_time = datetime.fromisoformat(batch['scheduledTime'])
            
            if now >= scheduled_time:
                logger.info(f"Processing scheduled batch: {batch['name']}")
                batch['status'] = 'processing'
                batch['startedAt'] = now.isoformat()
                self.save_scheduled_tasks()
                
                results = []
                for broadcast_data in batch['broadcasts']:
                    success, result = self.youtube_service.process_broadcast(broadcast_data)
                    results.append({
                        'title': broadcast_data['title'],
                        'success': success,
                        'broadcastId': result if success else None,
                        'error': result if not success else None
                    })
                
                batch['status'] = 'completed'
                batch['completedAt'] = datetime.now().isoformat()
                batch['results'] = results
                self.save_scheduled_tasks()
                
                success_count = sum(1 for r in results if r['success'])
                logger.info(f"Batch completed: {success_count}/{len(results)} successful")
    
    def process_scheduled_uploads(self):
        """Process scheduled video uploads"""
        now = datetime.now()
        
        for upload in self.scheduled_uploads:
            if upload['status'] != 'pending':
                continue
            
            scheduled_time = datetime.fromisoformat(upload['scheduledTime'])
            
            if now >= scheduled_time:
                logger.info(f"Processing scheduled upload: {upload['videoData']['title']}")
                upload['status'] = 'processing'
                self.save_scheduled_tasks()
                
                success, result = self.youtube_service.upload_video_file(upload['videoData'])
                
                if success:
                    upload['status'] = 'completed'
                    upload['videoId'] = result
                    upload['completedAt'] = datetime.now().isoformat()
                    logger.info(f"Upload completed: {result}")
                else:
                    upload['status'] = 'failed'
                    upload['error'] = result
                    upload['failedAt'] = datetime.now().isoformat()
                    logger.error(f"Upload failed: {result}")
                
                self.save_scheduled_tasks()
    
    def run_cycle(self):
        """Run one processing cycle"""
        try:
            self.load_scheduled_tasks()
            self.process_scheduled_batches()
            self.process_scheduled_uploads()
        except Exception as e:
            logger.error(f"Error in processing cycle: {e}")
    
    def start(self):
        """Start the daemon"""
        if not self.setup():
            return False
        
        self.running = True
        logger.info("Scheduler daemon started")
        
        # Write PID file
        with open(config.PID_FILE, 'w') as f:
            f.write(str(os.getpid()))
        
        try:
            while self.running:
                self.run_cycle()
                time.sleep(config.SCHEDULER_INTERVAL)
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        finally:
            self.stop()
        
        return True
    
    def stop(self):
        """Stop the daemon"""
        logger.info("Stopping scheduler daemon...")
        self.running = False
        
        # Remove PID file
        if config.PID_FILE.exists():
            config.PID_FILE.unlink()
        
        logger.info("Scheduler daemon stopped")

def signal_handler(signum, frame):
    """Handle signals"""
    logger.info(f"Received signal {signum}")
    sys.exit(0)

def main():
    """Main entry point"""
    # Setup signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    daemon = SchedulerDaemon()
    daemon.start()

if __name__ == '__main__':
    main()
