const cron = require('node-cron');
const fs = require('fs').promises;
const path = require('path');
const config = require('../utils/config');

class BatchScheduler {
  constructor(youtubeService) {
    this.youtubeService = youtubeService;
    this.scheduledBatches = [];
    this.cronJobs = new Map();
    this.configFile = path.join(config.PATHS.DATA_DIR, 'scheduled_batches.json');
    this.loadScheduledBatches();
  }

  async scheduleBatch(broadcasts, scheduledTime, batchName = 'Unnamed Batch') {
    const batchId = this.generateId();
    const batch = {
      id: batchId,
      name: batchName,
      broadcasts,
      scheduledTime: scheduledTime.toISOString(),
      status: 'pending',
      createdAt: new Date().toISOString(),
      results: []
    };

    this.scheduledBatches.push(batch);
    await this.saveScheduledBatches();

    this.setupCronJob(batch);

    return { success: true, batchId };
  }

  setupCronJob(batch) {
    const scheduledDate = new Date(batch.scheduledTime);
    
    const minute = scheduledDate.getMinutes();
    const hour = scheduledDate.getHours();
    const day = scheduledDate.getDate();
    const month = scheduledDate.getMonth() + 1;
    
    const cronExpression = `${minute} ${hour} ${day} ${month} *`;

    try {
      const job = cron.schedule(cronExpression, async () => {
        await this.processBatch(batch.id);
      }, {
        scheduled: true
      });

      this.cronJobs.set(batch.id, job);
      console.log(`[SCHEDULER] Cron job set for batch ${batch.id}: ${cronExpression}`);
    } catch (error) {
      console.error(`[SCHEDULER] Error setting up cron job: ${error.message}`);
    }
  }

  async processBatch(batchId, logCallback = null) {
    const log = (msg) => {
      console.log(msg);
      if (logCallback) logCallback(msg);
    };

    const batch = this.scheduledBatches.find(b => b.id === batchId);
    if (!batch) {
      log(`[SCHEDULER] Batch not found: ${batchId}`);
      return { success: false, error: 'Batch not found' };
    }

    if (batch.status !== 'pending') {
      log(`[SCHEDULER] Batch already processed: ${batchId}`);
      return { success: false, error: 'Batch already processed' };
    }

    log(`[SCHEDULER] Processing batch: ${batch.name}`);
    batch.status = 'processing';
    batch.startedAt = new Date().toISOString();
    await this.saveScheduledBatches();

    const results = [];

    for (const broadcast of batch.broadcasts) {
      const result = await this.youtubeService.processBroadcast(broadcast, log);
      results.push({
        title: broadcast.title,
        success: result.success,
        broadcastId: result.broadcastId,
        error: result.error
      });
    }

    batch.status = 'completed';
    batch.completedAt = new Date().toISOString();
    batch.results = results;
    await this.saveScheduledBatches();

    const job = this.cronJobs.get(batchId);
    if (job) {
      job.stop();
      this.cronJobs.delete(batchId);
    }

    const successCount = results.filter(r => r.success).length;
    log(`[SCHEDULER] Batch completed: ${successCount}/${results.length} successful`);

    return { success: true, results };
  }

  async cancelBatch(batchId) {
    const batch = this.scheduledBatches.find(b => b.id === batchId);
    if (!batch) {
      return { success: false, error: 'Batch not found' };
    }

    if (batch.status !== 'pending') {
      return { success: false, error: 'Can only cancel pending batches' };
    }

    batch.status = 'cancelled';
    batch.cancelledAt = new Date().toISOString();
    await this.saveScheduledBatches();

    const job = this.cronJobs.get(batchId);
    if (job) {
      job.stop();
      this.cronJobs.delete(batchId);
    }

    return { success: true };
  }

  getScheduledBatches() {
    return [...this.scheduledBatches];
  }

  async clearCompletedBatches() {
    const toRemove = this.scheduledBatches.filter(
      b => ['completed', 'failed', 'cancelled'].includes(b.status)
    );

    toRemove.forEach(batch => {
      const job = this.cronJobs.get(batch.id);
      if (job) {
        job.stop();
        this.cronJobs.delete(batch.id);
      }
    });

    this.scheduledBatches = this.scheduledBatches.filter(
      b => !['completed', 'failed', 'cancelled'].includes(b.status)
    );

    await this.saveScheduledBatches();
  }

  async saveScheduledBatches() {
    try {
      await fs.mkdir(config.PATHS.DATA_DIR, { recursive: true });
      await fs.writeFile(
        this.configFile,
        JSON.stringify(this.scheduledBatches, null, 2)
      );
    } catch (error) {
      console.error('Error saving scheduled batches:', error);
    }
  }

  async loadScheduledBatches() {
    try {
      const content = await fs.readFile(this.configFile, 'utf-8');
      this.scheduledBatches = JSON.parse(content);

      this.scheduledBatches.forEach(batch => {
        if (batch.status === 'pending') {
          const scheduledDate = new Date(batch.scheduledTime);
          if (scheduledDate > new Date()) {
            this.setupCronJob(batch);
          }
        }
      });
    } catch (error) {
      this.scheduledBatches = [];
    }
  }

  generateId() {
    return `batch_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  stopAllJobs() {
    this.cronJobs.forEach(job => job.stop());
    this.cronJobs.clear();
  }
}

module.exports = BatchScheduler;
