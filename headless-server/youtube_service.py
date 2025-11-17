import os
from googleapiclient.http import MediaFileUpload

class YouTubeService:
    """YouTube service for headless server operation"""
    
    def __init__(self, youtube_client, auth=None):
        self.youtube = youtube_client
        self.auth = auth
    
    def create_broadcast(self, broadcast_data):
        """Create YouTube live broadcast"""
        try:
            body = {
                "snippet": {
                    "title": broadcast_data["title"],
                    "description": broadcast_data["description"],
                    "scheduledStartTime": broadcast_data["scheduledStartTime"],
                    "tags": broadcast_data["tags"],
                    "categoryId": broadcast_data["categoryId"]
                },
                "status": {
                    "privacyStatus": broadcast_data["privacyStatus"],
                    "selfDeclaredMadeForKids": broadcast_data.get("madeForKids", False)
                },
                "contentDetails": {
                    "enableDvr": broadcast_data.get("enableDvr", True),
                    "enableEmbed": broadcast_data.get("enableEmbed", True),
                    "recordFromStart": broadcast_data.get("recordFromStart", True),
                    "enableAutoStart": True,
                    "enableAutoStop": True
                }
            }
            
            if self.auth and self.auth.selected_channel_id:
                body["snippet"]["channelId"] = self.auth.selected_channel_id
            
            request = self.youtube.liveBroadcasts().insert(
                part="snippet,status,contentDetails",
                body=body
            )
            response = request.execute()
            
            broadcast_id = response["id"]
            
            if broadcast_data.get("containsSyntheticMedia", False):
                self.update_video_synthetic_media(broadcast_id, True)
            
            if broadcast_data.get("enableMonetization", False):
                self.update_video_monetization(broadcast_id, True)
            
            return True, response
        except Exception as e:
            return False, str(e)
    
    def update_video_synthetic_media(self, video_id, contains_synthetic):
        """Update synthetic media flag"""
        try:
            request = self.youtube.videos().update(
                part="status",
                body={
                    "id": video_id,
                    "status": {
                        "containsSyntheticMedia": contains_synthetic
                    }
                }
            )
            response = request.execute()
            return True, response
        except Exception as e:
            return False, str(e)
    
    def update_video_monetization(self, video_id, enable_monetization):
        """Set video as eligible for monetization"""
        try:
            get_request = self.youtube.videos().list(
                part="status",
                id=video_id
            )
            get_response = get_request.execute()
            
            if not get_response.get("items"):
                return False, f"Video ID not found: {video_id}"
            
            current_status = get_response["items"][0]["status"]
            
            update_body = {
                "id": video_id,
                "status": {
                    "privacyStatus": current_status.get("privacyStatus", "public"),
                    "madeForKids": False,
                    "selfDeclaredMadeForKids": False,
                }
            }
            
            if "embeddable" in current_status:
                update_body["status"]["embeddable"] = current_status["embeddable"]
            if "license" in current_status:
                update_body["status"]["license"] = current_status["license"]
            if "publicStatsViewable" in current_status:
                update_body["status"]["publicStatsViewable"] = current_status["publicStatsViewable"]
            
            request = self.youtube.videos().update(
                part="status",
                body=update_body
            )
            response = request.execute()
            return True, response
        except Exception as e:
            return False, str(e)
    
    def create_stream(self, title, latency="normal"):
        """Create live stream"""
        try:
            stream_title = f"Stream: {title}"
            
            request = self.youtube.liveStreams().insert(
                part="snippet,cdn,contentDetails",
                body={
                    "snippet": {
                        "title": stream_title
                    },
                    "cdn": {
                        "frameRate": "variable",
                        "ingestionType": "rtmp",
                        "resolution": "variable"
                    },
                    "contentDetails": {
                        "isReusable": False
                    }
                }
            )
            response = request.execute()
            return True, response
        except Exception as e:
            return False, str(e)
    
    def get_stream_info(self, stream_id):
        """Get stream information"""
        try:
            request = self.youtube.liveStreams().list(
                part="snippet,cdn,status",
                id=stream_id
            )
            response = request.execute()
            if response.get("items"):
                return True, response["items"][0]
            else:
                return False, f"Stream ID not found: {stream_id}"
        except Exception as e:
            return False, str(e)
    
    def find_stream_by_key(self, stream_key):
        """Find stream by key"""
        try:
            request = self.youtube.liveStreams().list(
                part="snippet,cdn,status",
                mine=True,
                maxResults=50
            )
            response = request.execute()
            
            for stream in response.get("items", []):
                if stream.get("cdn", {}).get("ingestionInfo", {}).get("streamName") == stream_key:
                    return True, stream
            
            return False, f"No stream found with key: {stream_key}"
        except Exception as e:
            return False, str(e)
    
    def bind_broadcast_to_stream(self, broadcast_id, stream_id):
        """Bind broadcast to stream"""
        try:
            request = self.youtube.liveBroadcasts().bind(
                part="id,contentDetails",
                id=broadcast_id,
                streamId=stream_id
            )
            response = request.execute()
            return True, response
        except Exception as e:
            return False, str(e)
    
    def upload_thumbnail(self, broadcast_id, thumbnail_path):
        """Upload thumbnail"""
        if not os.path.exists(thumbnail_path):
            return False, f"Thumbnail file not found: {thumbnail_path}"
        
        try:
            request = self.youtube.thumbnails().set(
                videoId=broadcast_id,
                media_body=MediaFileUpload(thumbnail_path, chunksize=-1, resumable=True)
            )
            response = request.execute()
            return True, response
        except Exception as e:
            return False, str(e)
    
    def process_broadcast(self, broadcast_data, log_callback=None):
        """Process complete broadcast creation"""
        def log(msg):
            if log_callback:
                log_callback(msg)
            print(msg)
        
        title = broadcast_data["title"]
        log(f"[BROADCAST] Processing: {title}")
        
        try:
            success, result = self.create_broadcast(broadcast_data)
            if not success:
                log(f"[BROADCAST] ✗ Failed to create: {result}")
                return False, result
            
            broadcast_id = result["id"]
            log(f"[BROADCAST] ✓ Created: {broadcast_id}")
            
            if broadcast_data.get("containsSyntheticMedia", False):
                log(f"[BROADCAST] Setting synthetic media flag...")
            
            if broadcast_data.get("enableMonetization", False):
                log(f"[BROADCAST] Setting monetization eligibility...")
            
            # Handle stream
            if broadcast_data.get("streamId"):
                stream_id = broadcast_data["streamId"]
                log(f"[BROADCAST] Using existing stream: {stream_id}")
                
                success, result = self.get_stream_info(stream_id)
                if not success:
                    log(f"[BROADCAST] ✗ Stream verification failed: {result}")
                    return False, result
                log(f"[BROADCAST] ✓ Stream verified")
            elif broadcast_data.get("streamKey"):
                stream_key = broadcast_data["streamKey"]
                log(f"[BROADCAST] Looking up stream key: {stream_key}")
                
                success, result = self.find_stream_by_key(stream_key)
                if not success:
                    log(f"[BROADCAST] ✗ Stream lookup failed: {result}")
                    return False, result
                
                stream_id = result["id"]
                log(f"[BROADCAST] ✓ Found stream: {stream_id}")
            else:
                success, result = self.create_stream(
                    title, 
                    broadcast_data.get("latency", "normal")
                )
                if not success:
                    log(f"[BROADCAST] ✗ Failed to create stream: {result}")
                    return False, result
                
                stream_id = result["id"]
                log(f"[BROADCAST] ✓ Created stream: {stream_id}")
            
            success, result = self.bind_broadcast_to_stream(broadcast_id, stream_id)
            if not success:
                log(f"[BROADCAST] ✗ Failed to bind: {result}")
                return False, result
            
            log(f"[BROADCAST] ✓ Bound to stream")
            
            thumbnail_path = broadcast_data.get("thumbnailPath")
            if thumbnail_path and thumbnail_path.strip():
                success, result = self.upload_thumbnail(broadcast_id, thumbnail_path)
                if success:
                    log(f"[BROADCAST] ✓ Uploaded thumbnail")
                else:
                    log(f"[BROADCAST] ⚠ Thumbnail upload failed: {result}")
            
            log(f"[BROADCAST] ✓ Completed: {title}\n")
            return True, broadcast_id
        except Exception as e:
            log(f"[BROADCAST] ✗ Unexpected error: {str(e)}")
            return False, str(e)
    
    def get_upcoming_broadcasts(self):
        """Get upcoming broadcasts"""
        try:
            request = self.youtube.liveBroadcasts().list(
                part="snippet,status,contentDetails",
                broadcastStatus="upcoming",
                maxResults=50
            )
            response = request.execute()
            return True, response.get("items", [])
        except Exception as e:
            return False, str(e)
    
    def upload_video_file(self, video_data, progress_callback=None):
        """Upload video file"""
        try:
            video_path = video_data["videoPath"]
            
            body = {
                "snippet": {
                    "title": video_data["title"],
                    "description": video_data["description"],
                    "tags": video_data["tags"],
                    "categoryId": video_data["categoryId"]
                },
                "status": {
                    "privacyStatus": video_data["privacyStatus"],
                    "selfDeclaredMadeForKids": video_data.get("madeForKids", False)
                }
            }
            
            if video_data.get("publishAt"):
                body["status"]["publishAt"] = video_data["publishAt"]
            
            if self.auth and self.auth.selected_channel_id:
                body["snippet"]["channelId"] = self.auth.selected_channel_id
            
            media = MediaFileUpload(
                video_path,
                chunksize=1024*1024*5,
                resumable=True
            )
            
            request = self.youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    if progress_callback:
                        progress_callback(progress)
                    print(f"[UPLOAD] Progress: {progress}%")
            
            video_id = response["id"]
            
            if video_data.get("containsSyntheticMedia", False):
                self.update_video_synthetic_media(video_id, True)
            
            if video_data.get("enableMonetization", False):
                self.update_video_monetization(video_id, True)
            
            return True, video_id
        except Exception as e:
            return False, str(e)
