import os
from googleapiclient.http import MediaFileUpload

class YouTubeService:
    def __init__(self, youtube_client, auth=None):
        self.youtube = youtube_client
        self.auth = auth
    
    def create_broadcast(self, broadcast_data):
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
            
            if self.auth and self.auth.get_selected_channel_id():
                body["snippet"]["channelId"] = self.auth.get_selected_channel_id()
            
            request = self.youtube.liveBroadcasts().insert(
                part="snippet,status,contentDetails",
                body=body
            )
            response = request.execute()
            
            broadcast_id = response["id"]
            
            if broadcast_data.get("containsSyntheticMedia", False):
                success, result = self.update_video_synthetic_media(broadcast_id, True)
                if not success:
                    return True, response
            
            if broadcast_data.get("enableMonetization", False):
                success, result = self.update_video_monetization(broadcast_id, True)
                if not success:
                    # Don't fail the whole broadcast creation if monetization fails
                    # Just log the warning and continue
                    print(f"[WARN] Monetization eligibility update failed: {result}")
                    # Still return success for broadcast creation
                else:
                    print(f"[OK] Video set as eligible for monetization")
            
            return True, response
        except Exception as e:
            return False, str(e)
    
    def update_video_synthetic_media(self, video_id, contains_synthetic):
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
        """
        Set video as eligible for monetization by ensuring it's not marked as Made for Kids.
        Note: Actual monetization is controlled at channel level (YPP settings).
        This method only ensures the video is eligible (not marked as kids content).
        """
        try:
            # First, get current video status to preserve other settings
            get_request = self.youtube.videos().list(
                part="status",
                id=video_id
            )
            get_response = get_request.execute()
            
            if not get_response.get("items"):
                return False, f"Video ID not found: {video_id}"
            
            current_status = get_response["items"][0]["status"]
            
            # Update status to make video eligible for monetization
            # Key: Set madeForKids to False and ensure it's not self-declared for kids
            update_body = {
                "id": video_id,
                "status": {
                    "privacyStatus": current_status.get("privacyStatus", "public"),
                    "madeForKids": False,
                    "selfDeclaredMadeForKids": False,
                }
            }
            
            # Preserve other status fields if they exist
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
        def log(msg):
            if log_callback:
                log_callback(msg)
        
        title = broadcast_data["title"]
        log(f"Processing: {title}")
        
        try:
            success, result = self.create_broadcast(broadcast_data)
            if not success:
                log(f"[X] Failed to create broadcast: {result}")
                return False, result
            
            broadcast_id = result["id"]
            log(f"[OK] Created broadcast: {broadcast_id}")
            
            if broadcast_data.get("containsSyntheticMedia", False):
                log(f"[INFO] Setting synthetic media flag...")
            
            if broadcast_data.get("enableMonetization", False):
                log(f"[INFO] Setting video as eligible for monetization (madeForKids=False)...")
                log(f"[INFO] Note: Actual monetization is controlled by channel YPP settings")
            
            # Check if streamId is provided (reuse existing stream)
            if broadcast_data.get("streamId"):
                stream_id = broadcast_data["streamId"]
                log(f"[INFO] Using existing stream ID: {stream_id}")
                
                # Verify stream exists
                success, result = self.get_stream_info(stream_id)
                if not success:
                    log(f"[X] Stream ID verification failed: {result}")
                    return False, result
                log(f"[OK] Stream verified: {stream_id}")
            elif broadcast_data.get("streamKey"):
                # Find existing stream by stream key
                stream_key = broadcast_data["streamKey"]
                log(f"[INFO] Looking up stream with key: {stream_key}")
                
                success, result = self.find_stream_by_key(stream_key)
                if not success:
                    log(f"[X] Stream lookup failed: {result}")
                    return False, result
                
                stream_id = result["id"]
                log(f"[OK] Found stream: {stream_id}")
            else:
                # Create new stream
                success, result = self.create_stream(
                    title, 
                    broadcast_data.get("latency", "normal")
                )
                if not success:
                    log(f"[X] Failed to create stream: {result}")
                    return False, result
                
                stream_id = result["id"]
                log(f"[OK] Created stream: {stream_id}")
            
            success, result = self.bind_broadcast_to_stream(broadcast_id, stream_id)
            if not success:
                log(f"[X] Failed to bind: {result}")
                return False, result
            
            log(f"[OK] Bound broadcast to stream")
            
            thumbnail_path = broadcast_data.get("thumbnailPath")
            if thumbnail_path and thumbnail_path.strip():
                success, result = self.upload_thumbnail(broadcast_id, thumbnail_path)
                if success:
                    log(f"[OK] Uploaded thumbnail")
                else:
                    log(f"[WARN] Thumbnail upload failed: {result}")
            
            log(f"[OK] Completed: {title}\n")
            return True, broadcast_id
        except Exception as e:
            log(f"[X] Unexpected error: {str(e)}")
            return False, str(e)
    
    def get_upcoming_broadcasts(self):
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
    
    def upload_video_file(self, video_data):
        """Upload a video file to YouTube"""
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
            
            if self.auth and self.auth.get_selected_channel_id():
                body["snippet"]["channelId"] = self.auth.get_selected_channel_id()
            
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
                    print(f"[UPLOAD] Progress: {progress}%")
            
            video_id = response["id"]
            
            if video_data.get("containsSyntheticMedia", False):
                success, result = self.update_video_synthetic_media(video_id, True)
            
            if video_data.get("enableMonetization", False):
                success, result = self.update_video_monetization(video_id, True)
                if success:
                    print(f"[OK] Video set as eligible for monetization")
            
            return True, video_id
        except Exception as e:
            return False, str(e)
