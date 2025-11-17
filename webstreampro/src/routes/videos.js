const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs').promises;
const config = require('../utils/config');
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
  limits: { fileSize: config.UPLOAD_LIMITS.FILE_SIZE }
});

module.exports = (videoUploader) => {
  router.post('/upload', requireAuth, upload.fields([
    { name: 'video', maxCount: 1 },
    { name: 'thumbnail', maxCount: 1 }
  ]), async (req, res) => {
    try {
      if (!req.files || !req.files.video) {
        return res.status(400).json({ success: false, error: 'No video file uploaded' });
      }

      const videoData = {
        title: req.body.title || 'Untitled Video',
        description: req.body.description || '',
        tags: req.body.tags ? req.body.tags.split(',').map(t => t.trim()) : [],
        categoryId: req.body.categoryId || '20',
        privacyStatus: req.body.privacyStatus || 'public',
        videoPath: req.files.video[0].path,
        thumbnailPath: req.files.thumbnail ? req.files.thumbnail[0].path : null,
        madeForKids: req.body.madeForKids === 'true',
        containsSyntheticMedia: req.body.containsSyntheticMedia === 'true',
        enableMonetization: req.body.enableMonetization === 'true'
      };

      if (req.body.publishAt) {
        videoData.publishAt = new Date(req.body.publishAt).toISOString();
      }

      const result = await videoUploader.uploadVideoImmediate(videoData);

      await fs.unlink(req.files.video[0].path).catch(() => {});
      if (req.files.thumbnail) {
        await fs.unlink(req.files.thumbnail[0].path).catch(() => {});
      }

      res.json(result);
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.post('/schedule-upload', requireAuth, upload.fields([
    { name: 'video', maxCount: 1 },
    { name: 'thumbnail', maxCount: 1 }
  ]), async (req, res) => {
    try {
      if (!req.files || !req.files.video) {
        return res.status(400).json({ success: false, error: 'No video file uploaded' });
      }

      if (!req.body.scheduledTime) {
        return res.status(400).json({ success: false, error: 'Scheduled time required' });
      }

      const videoData = {
        title: req.body.title || 'Untitled Video',
        description: req.body.description || '',
        tags: req.body.tags ? req.body.tags.split(',').map(t => t.trim()) : [],
        categoryId: req.body.categoryId || '20',
        privacyStatus: req.body.privacyStatus || 'public',
        videoPath: req.files.video[0].path,
        thumbnailPath: req.files.thumbnail ? req.files.thumbnail[0].path : null,
        madeForKids: req.body.madeForKids === 'true',
        containsSyntheticMedia: req.body.containsSyntheticMedia === 'true',
        enableMonetization: req.body.enableMonetization === 'true'
      };

      const uploadId = await videoUploader.scheduleUpload(
        videoData,
        new Date(req.body.scheduledTime)
      );

      res.json({ success: true, uploadId });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.get('/scheduled-uploads', requireAuth, (req, res) => {
    try {
      const uploads = videoUploader.getScheduledUploads();
      res.json({ success: true, uploads });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.post('/cancel-upload/:index', requireAuth, async (req, res) => {
    try {
      const index = parseInt(req.params.index);
      const result = await videoUploader.cancelUpload(index);
      res.json({ success: result });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.delete('/clear-completed-uploads', requireAuth, async (req, res) => {
    try {
      await videoUploader.clearCompletedUploads();
      res.json({ success: true });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.post('/start-scheduler', requireAuth, (req, res) => {
    try {
      const result = videoUploader.startScheduler();
      res.json(result);
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.post('/stop-scheduler', requireAuth, (req, res) => {
    try {
      const result = videoUploader.stopScheduler();
      res.json(result);
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  return router;
};
