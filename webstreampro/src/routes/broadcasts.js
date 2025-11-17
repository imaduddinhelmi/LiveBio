const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs').promises;
const config = require('../utils/config');
const { parseExcelFile } = require('../utils/excelParser');
const { requireAuth } = require('../middleware/auth');

const storage = multer.diskStorage({
  destination: async (req, file, cb) => {
    await fs.mkdir(config.PATHS.UPLOADS_DIR, { recursive: true });
    cb(null, config.PATHS.UPLOADS_DIR);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({ 
  storage,
  limits: { fileSize: config.UPLOAD_LIMITS.EXCEL_SIZE }
});

module.exports = (youtubeService, batchScheduler) => {
  router.post('/parse-excel', requireAuth, upload.single('excelFile'), async (req, res) => {
    try {
      if (!req.file) {
        return res.status(400).json({ success: false, error: 'No file uploaded' });
      }

      const result = parseExcelFile(req.file.path);
      
      await fs.unlink(req.file.path);

      if (result.success) {
        res.json({ success: true, broadcasts: result.broadcasts });
      } else {
        res.status(400).json({ success: false, error: result.error });
      }
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.post('/create', requireAuth, async (req, res) => {
    try {
      const { broadcastData } = req.body;
      
      const result = await youtubeService.processBroadcast(broadcastData);
      
      if (result.success) {
        res.json({ success: true, broadcastId: result.broadcastId });
      } else {
        res.status(400).json({ success: false, error: result.error });
      }
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.post('/create-batch', requireAuth, async (req, res) => {
    try {
      const { broadcasts } = req.body;
      const results = [];

      for (const broadcast of broadcasts) {
        const result = await youtubeService.processBroadcast(broadcast);
        results.push({
          title: broadcast.title,
          success: result.success,
          broadcastId: result.broadcastId,
          error: result.error
        });
      }

      const successCount = results.filter(r => r.success).length;
      res.json({ 
        success: true, 
        results,
        summary: `${successCount}/${results.length} broadcasts created successfully`
      });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.post('/schedule-batch', requireAuth, async (req, res) => {
    try {
      const { broadcasts, scheduledTime, batchName } = req.body;
      
      const result = await batchScheduler.scheduleBatch(
        broadcasts,
        new Date(scheduledTime),
        batchName
      );

      res.json(result);
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.get('/scheduled-batches', requireAuth, (req, res) => {
    try {
      const batches = batchScheduler.getScheduledBatches();
      res.json({ success: true, batches });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.post('/cancel-batch/:batchId', requireAuth, async (req, res) => {
    try {
      const { batchId } = req.params;
      const result = await batchScheduler.cancelBatch(batchId);
      res.json(result);
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.delete('/clear-completed-batches', requireAuth, async (req, res) => {
    try {
      await batchScheduler.clearCompletedBatches();
      res.json({ success: true });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.get('/upcoming', requireAuth, async (req, res) => {
    try {
      const result = await youtubeService.getUpcomingBroadcasts();
      
      if (result.success) {
        res.json({ success: true, broadcasts: result.data });
      } else {
        res.status(400).json({ success: false, error: result.error });
      }
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  return router;
};
