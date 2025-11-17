const fs = require('fs').promises;

class YouTubeService {
  constructor(authService) {
    this.authService = authService;
  }

  getYouTube() {
    return this.authService.getYouTubeClient();
  }

  async createBroadcast(broadcastData) {
    try {
      const youtube = this.getYouTube();
      
      const body = {
        snippet: {
          title: broadcastData.title,
          description: broadcastData.description,
          scheduledStartTime: broadcastData.scheduledStartTime,
          tags: broadcastData.tags || [],
          categoryId: broadcastData.categoryId || '20'
        },
        status: {
          privacyStatus: broadcastData.privacyStatus || 'public',
          selfDeclaredMadeForKids: broadcastData.madeForKids || false
        },
        contentDetails: {
          enableDvr: broadcastData.enableDvr !== false,
          enableEmbed: broadcastData.enableEmbed !== false,
          recordFromStart: broadcastData.recordFromStart !== false,
          enableAutoStart: true,
          enableAutoStop: true
        }
      };

      const selectedChannelId = this.authService.getSelectedChannelId();
      if (selectedChannelId) {
        body.snippet.channelId = selectedChannelId;
      }

      const response = await youtube.liveBroadcasts.insert({
        part: 'snippet,status,contentDetails',
        requestBody: body
      });

      const broadcastId = response.data.id;

      if (broadcastData.containsSyntheticMedia) {
        await this.updateVideoSyntheticMedia(broadcastId, true);
      }

      if (broadcastData.enableMonetization) {
        await this.updateVideoMonetization(broadcastId, true);
      }

      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error creating broadcast:', error);
      return { success: false, error: error.message };
    }
  }

  async updateVideoSyntheticMedia(videoId, containsSynthetic) {
    try {
      const youtube = this.getYouTube();
      
      const response = await youtube.videos.update({
        part: 'status',
        requestBody: {
          id: videoId,
          status: {
            containsSyntheticMedia: containsSynthetic
          }
        }
      });

      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error updating synthetic media:', error);
      return { success: false, error: error.message };
    }
  }

  async updateVideoMonetization(videoId, enableMonetization) {
    try {
      const youtube = this.getYouTube();
      
      const getResponse = await youtube.videos.list({
        part: 'status',
        id: videoId
      });

      if (!getResponse.data.items || getResponse.data.items.length === 0) {
        throw new Error(`Video ID not found: ${videoId}`);
      }

      const currentStatus = getResponse.data.items[0].status;

      const updateBody = {
        id: videoId,
        status: {
          privacyStatus: currentStatus.privacyStatus || 'public',
          madeForKids: false,
          selfDeclaredMadeForKids: false
        }
      };

      if (currentStatus.embeddable !== undefined) {
        updateBody.status.embeddable = currentStatus.embeddable;
      }
      if (currentStatus.license !== undefined) {
        updateBody.status.license = currentStatus.license;
      }
      if (currentStatus.publicStatsViewable !== undefined) {
        updateBody.status.publicStatsViewable = currentStatus.publicStatsViewable;
      }

      const response = await youtube.videos.update({
        part: 'status',
        requestBody: updateBody
      });

      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error updating monetization:', error);
      return { success: false, error: error.message };
    }
  }

  async createStream(title, latency = 'normal') {
    try {
      const youtube = this.getYouTube();
      const streamTitle = `Stream: ${title}`;

      const response = await youtube.liveStreams.insert({
        part: 'snippet,cdn,contentDetails',
        requestBody: {
          snippet: {
            title: streamTitle
          },
          cdn: {
            frameRate: 'variable',
            ingestionType: 'rtmp',
            resolution: 'variable'
          },
          contentDetails: {
            isReusable: false
          }
        }
      });

      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error creating stream:', error);
      return { success: false, error: error.message };
    }
  }

  async getStreamInfo(streamId) {
    try {
      const youtube = this.getYouTube();

      const response = await youtube.liveStreams.list({
        part: 'snippet,cdn,status',
        id: streamId
      });

      if (response.data.items && response.data.items.length > 0) {
        return { success: true, data: response.data.items[0] };
      } else {
        return { success: false, error: `Stream ID not found: ${streamId}` };
      }
    } catch (error) {
      console.error('Error getting stream info:', error);
      return { success: false, error: error.message };
    }
  }

  async findStreamByKey(streamKey) {
    try {
      const youtube = this.getYouTube();

      const response = await youtube.liveStreams.list({
        part: 'snippet,cdn,status',
        mine: true,
        maxResults: 50
      });

      for (const stream of response.data.items || []) {
        if (stream.cdn?.ingestionInfo?.streamName === streamKey) {
          return { success: true, data: stream };
        }
      }

      return { success: false, error: `No stream found with key: ${streamKey}` };
    } catch (error) {
      console.error('Error finding stream by key:', error);
      return { success: false, error: error.message };
    }
  }

  async bindBroadcastToStream(broadcastId, streamId) {
    try {
      const youtube = this.getYouTube();

      const response = await youtube.liveBroadcasts.bind({
        part: 'id,contentDetails',
        id: broadcastId,
        streamId: streamId
      });

      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error binding broadcast to stream:', error);
      return { success: false, error: error.message };
    }
  }

  async uploadThumbnail(broadcastId, thumbnailPath) {
    try {
      const youtube = this.getYouTube();
      
      const fileContent = await fs.readFile(thumbnailPath);

      const response = await youtube.thumbnails.set({
        videoId: broadcastId,
        media: {
          body: fileContent
        }
      });

      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error uploading thumbnail:', error);
      return { success: false, error: error.message };
    }
  }

  async processBroadcast(broadcastData, logCallback = null) {
    const log = (msg) => {
      console.log(msg);
      if (logCallback) logCallback(msg);
    };

    const title = broadcastData.title;
    log(`Processing: ${title}`);

    try {
      const createResult = await this.createBroadcast(broadcastData);
      if (!createResult.success) {
        log(`[X] Failed to create broadcast: ${createResult.error}`);
        return { success: false, error: createResult.error };
      }

      const broadcastId = createResult.data.id;
      log(`[OK] Created broadcast: ${broadcastId}`);

      if (broadcastData.containsSyntheticMedia) {
        log(`[INFO] Setting synthetic media flag...`);
      }

      if (broadcastData.enableMonetization) {
        log(`[INFO] Setting video as eligible for monetization...`);
      }

      let streamId;
      if (broadcastData.streamId) {
        streamId = broadcastData.streamId;
        log(`[INFO] Using existing stream ID: ${streamId}`);

        const streamInfo = await this.getStreamInfo(streamId);
        if (!streamInfo.success) {
          log(`[X] Stream ID verification failed: ${streamInfo.error}`);
          return { success: false, error: streamInfo.error };
        }
        log(`[OK] Stream verified: ${streamId}`);
      } else if (broadcastData.streamKey) {
        const streamKey = broadcastData.streamKey;
        log(`[INFO] Looking up stream with key: ${streamKey}`);

        const findResult = await this.findStreamByKey(streamKey);
        if (!findResult.success) {
          log(`[X] Stream lookup failed: ${findResult.error}`);
          return { success: false, error: findResult.error };
        }

        streamId = findResult.data.id;
        log(`[OK] Found stream: ${streamId}`);
      } else {
        const createStreamResult = await this.createStream(
          title,
          broadcastData.latency || 'normal'
        );
        if (!createStreamResult.success) {
          log(`[X] Failed to create stream: ${createStreamResult.error}`);
          return { success: false, error: createStreamResult.error };
        }

        streamId = createStreamResult.data.id;
        log(`[OK] Created stream: ${streamId}`);
      }

      const bindResult = await this.bindBroadcastToStream(broadcastId, streamId);
      if (!bindResult.success) {
        log(`[X] Failed to bind: ${bindResult.error}`);
        return { success: false, error: bindResult.error };
      }

      log(`[OK] Bound broadcast to stream`);

      if (broadcastData.thumbnailPath) {
        const uploadResult = await this.uploadThumbnail(broadcastId, broadcastData.thumbnailPath);
        if (uploadResult.success) {
          log(`[OK] Uploaded thumbnail`);
        } else {
          log(`[WARN] Thumbnail upload failed: ${uploadResult.error}`);
        }
      }

      log(`[OK] Completed: ${title}\n`);
      return { success: true, broadcastId };
    } catch (error) {
      log(`[X] Unexpected error: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  async getUpcomingBroadcasts() {
    try {
      const youtube = this.getYouTube();

      const response = await youtube.liveBroadcasts.list({
        part: 'snippet,status,contentDetails',
        broadcastStatus: 'upcoming',
        maxResults: 50
      });

      return { success: true, data: response.data.items || [] };
    } catch (error) {
      console.error('Error getting upcoming broadcasts:', error);
      return { success: false, error: error.message };
    }
  }

  async uploadVideoFile(videoData, onProgress = null) {
    try {
      const youtube = this.getYouTube();
      const videoPath = videoData.videoPath;

      const body = {
        snippet: {
          title: videoData.title,
          description: videoData.description,
          tags: videoData.tags || [],
          categoryId: videoData.categoryId || '20'
        },
        status: {
          privacyStatus: videoData.privacyStatus || 'public',
          selfDeclaredMadeForKids: videoData.madeForKids || false
        }
      };

      if (videoData.publishAt) {
        body.status.publishAt = videoData.publishAt;
      }

      const selectedChannelId = this.authService.getSelectedChannelId();
      if (selectedChannelId) {
        body.snippet.channelId = selectedChannelId;
      }

      const fileSize = (await fs.stat(videoPath)).size;
      const fileStream = require('fs').createReadStream(videoPath);

      const response = await youtube.videos.insert({
        part: 'snippet,status',
        requestBody: body,
        media: {
          body: fileStream
        }
      }, {
        onUploadProgress: (evt) => {
          const progress = (evt.bytesRead / fileSize) * 100;
          if (onProgress) {
            onProgress(Math.round(progress));
          }
        }
      });

      const videoId = response.data.id;

      if (videoData.containsSyntheticMedia) {
        await this.updateVideoSyntheticMedia(videoId, true);
      }

      if (videoData.enableMonetization) {
        await this.updateVideoMonetization(videoId, true);
      }

      return { success: true, videoId };
    } catch (error) {
      console.error('Error uploading video:', error);
      return { success: false, error: error.message };
    }
  }
}

module.exports = YouTubeService;
