const fs = require('fs').promises;
const path = require('path');
const config = require('../utils/config');

class VideoUploader {
  constructor(youtubeService) {
    this.youtubeService = youtubeService;
    this.scheduledUploads = [];
    this.isRunning = false;
    this.schedulerInterval = null;
    this.configFile = path.join(config.PATHS.DATA_DIR, 'scheduled_uploads.json');
    this.loadScheduledUploads();
  }

  async addToQueue(videoData) {
    return await this.scheduleUpload(videoData, new Date());
  }

  async scheduleUpload(videoData, scheduledTime) {
    const uploadItem = {
      id: this.generateId(),
      videoData,
      scheduledTime: scheduledTime.toISOString(),
      status: 'pending',
      addedAt: new Date().toISOString()
    };
    
    this.scheduledUploads.push(uploadItem);
    await this.saveScheduledUploads();
    return uploadItem.id;
  }

  async removeScheduledUpload(index) {
    if (index >= 0 && index < this.scheduledUploads.length) {
      const removed = this.scheduledUploads.splice(index, 1)[0];
      await this.saveScheduledUploads();
      return { success: true, removed };
    }
    return { success: false, error: 'Invalid index' };
  }

  getScheduledUploads() {
    return [...this.scheduledUploads];
  }

  async cancelUpload(index) {
    try {
      if (index >= 0 && index < this.scheduledUploads.length) {
        const uploadItem = this.scheduledUploads[index];
        
        if (uploadItem.status === 'pending') {
          uploadItem.status = 'cancelled';
          uploadItem.cancelledAt = new Date().toISOString();
          await this.saveScheduledUploads();
          return true;
        }
      }
      return false;
    } catch (error) {
      console.error('Error cancelling upload:', error);
      return false;
    }
  }

  async clearCompletedUploads() {
    this.scheduledUploads = this.scheduledUploads.filter(
      item => !['completed', 'failed', 'cancelled'].includes(item.status)
    );
    await this.saveScheduledUploads();
  }

  async saveScheduledUploads() {
    try {
      await fs.mkdir(config.PATHS.DATA_DIR, { recursive: true });
      await fs.writeFile(
        this.configFile,
        JSON.stringify(this.scheduledUploads, null, 2)
      );
    } catch (error) {
      console.error('Error saving scheduled uploads:', error);
    }
  }

  async loadScheduledUploads() {
    try {
      const content = await fs.readFile(this.configFile, 'utf-8');
      this.scheduledUploads = JSON.parse(content);
    } catch (error) {
      this.scheduledUploads = [];
    }
  }

  startScheduler(logCallback = null) {
    if (this.isRunning) {
      return { success: false, error: 'Scheduler already running' };
    }

    this.isRunning = true;
    this.schedulerLoop(logCallback);
    return { success: true, message: 'Scheduler started' };
  }

  stopScheduler() {
    this.isRunning = false;
    if (this.schedulerInterval) {
      clearTimeout(this.schedulerInterval);
    }
    return { success: true, message: 'Scheduler stopped' };
  }

  async schedulerLoop(logCallback = null) {
    const log = (msg) => {
      console.log(msg);
      if (logCallback) logCallback(msg);
    };

    log('[SCHEDULER] Started - checking every 30 seconds');

    while (this.isRunning) {
      try {
        const now = new Date();

        for (const item of this.scheduledUploads) {
          if (item.status !== 'pending') continue;

          const scheduledTime = new Date(item.scheduledTime);

          if (now >= scheduledTime) {
            log(`[SCHEDULER] Processing scheduled upload: ${item.videoData.title}`);
            item.status = 'processing';
            await this.saveScheduledUploads();

            const result = await this.uploadVideo(item.videoData, log);

            if (result.success) {
              item.status = 'completed';
              item.videoId = result.videoId;
              item.completedAt = new Date().toISOString();
              log(`[SCHEDULER] ✓ Upload completed: ${result.videoId}`);
            } else {
              item.status = 'failed';
              item.error = result.error;
              item.failedAt = new Date().toISOString();
              log(`[SCHEDULER] ✗ Upload failed: ${result.error}`);
            }

            await this.saveScheduledUploads();
          }
        }

        await this.sleep(30000);
      } catch (error) {
        log(`[SCHEDULER] Error: ${error.message}`);
        await this.sleep(30000);
      }
    }

    log('[SCHEDULER] Stopped');
  }

  async uploadVideo(videoData, logCallback = null) {
    const log = (msg) => {
      console.log(msg);
      if (logCallback) logCallback(msg);
    };

    try {
      const videoPath = videoData.videoPath;

      const stats = await fs.stat(videoPath);
      const fileSizeMB = stats.size / (1024 * 1024);

      log(`[UPLOAD] Starting upload: ${videoData.title}`);
      log(`[UPLOAD] File: ${videoPath}`);
      log(`[UPLOAD] Size: ${fileSizeMB.toFixed(2)} MB`);

      const result = await this.youtubeService.uploadVideoFile(
        videoData,
        (progress) => {
          log(`[UPLOAD] Progress: ${progress}%`);
        }
      );

      if (result.success) {
        const videoId = result.videoId;
        log(`[UPLOAD] ✓ Video uploaded successfully! ID: ${videoId}`);

        if (videoData.thumbnailPath) {
          log(`[UPLOAD] Uploading thumbnail...`);
          const thumbResult = await this.youtubeService.uploadThumbnail(
            videoId,
            videoData.thumbnailPath
          );
          
          if (thumbResult.success) {
            log(`[UPLOAD] ✓ Thumbnail uploaded`);
          } else {
            log(`[UPLOAD] ⚠ Thumbnail upload failed: ${thumbResult.error}`);
          }
        }

        return { success: true, videoId };
      } else {
        log(`[UPLOAD] ✗ Upload failed: ${result.error}`);
        return { success: false, error: result.error };
      }
    } catch (error) {
      const errorMsg = `Upload error: ${error.message}`;
      log(`[UPLOAD] ✗ ${errorMsg}`);
      return { success: false, error: errorMsg };
    }
  }

  async uploadVideoImmediate(videoData, logCallback = null) {
    return await this.uploadVideo(videoData, logCallback);
  }

  generateId() {
    return `upload_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

module.exports = VideoUploader;
