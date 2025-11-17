import pandas as pd
from datetime import datetime
import os

class VideoExcelParser:
    """Parser for Excel file containing video upload data"""
    
    REQUIRED_COLUMNS = [
        "videoPath",
        "title",
        "description",
        "tags",
        "categoryId",
        "privacyStatus"
    ]
    
    OPTIONAL_COLUMNS = {
        "scheduledDate": None,
        "scheduledTime": None,
        "thumbnailPath": None,
        "madeForKids": False,
        "containsSyntheticMedia": False,
        "enableMonetization": True
    }
    
    def __init__(self):
        self.df = None
        self.file_path = None
    
    def load_excel(self, file_path):
        """Load and validate Excel file"""
        try:
            self.df = pd.read_excel(file_path)
            self.file_path = file_path
            
            # Check required columns
            missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in self.df.columns]
            if missing_cols:
                return False, f"Missing required columns: {', '.join(missing_cols)}"
            
            # Add optional columns with defaults
            for col, default_val in self.OPTIONAL_COLUMNS.items():
                if col not in self.df.columns:
                    self.df[col] = default_val
            
            return True, f"Loaded {len(self.df)} video(s) successfully"
        except Exception as e:
            return False, f"Error loading Excel: {str(e)}"
    
    def get_preview(self, rows=10):
        """Get preview of first N rows"""
        if self.df is None:
            return None
        return self.df.head(rows)
    
    def get_all_videos(self):
        """Parse all videos from Excel"""
        if self.df is None:
            return []
        
        videos = []
        for idx, row in self.df.iterrows():
            try:
                video_data = self._parse_row(row, idx)
                videos.append(video_data)
            except Exception as e:
                videos.append({
                    "error": f"Row {idx+1}: {str(e)}", 
                    "row_index": idx
                })
        
        return videos
    
    def _parse_row(self, row, idx):
        """Parse single row into video data"""
        # Video path - REQUIRED
        video_path = str(row['videoPath']).strip()
        if not video_path or video_path.lower() == 'nan':
            raise ValueError(f"Video path is required")
        
        if not os.path.exists(video_path):
            raise ValueError(f"Video file not found: {video_path}")
        
        # Title - REQUIRED
        title = str(row['title']).strip()
        if not title or title.lower() == 'nan':
            raise ValueError(f"Title is required")
        
        # Tags
        tags_list = []
        if pd.notna(row['tags']):
            tags_str = str(row['tags'])
            if tags_str and tags_str.lower() != 'nan':
                tags_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        
        # Category ID
        category_id = "22"
        if pd.notna(row.get('categoryId')):
            try:
                if isinstance(row['categoryId'], (int, float)):
                    category_id = str(int(row['categoryId']))
                else:
                    category_id = str(int(float(row['categoryId'])))
            except (ValueError, TypeError):
                category_id = "22"
        
        # Scheduled time
        scheduled_time = None
        if pd.notna(row.get('scheduledDate')) and pd.notna(row.get('scheduledTime')):
            scheduled_date = str(row['scheduledDate'])
            scheduled_time_str = str(row['scheduledTime'])
            
            if scheduled_date and scheduled_date.lower() != 'nan' and scheduled_time_str and scheduled_time_str.lower() != 'nan':
                try:
                    dt = datetime.strptime(f"{scheduled_date} {scheduled_time_str}", "%Y-%m-%d %H:%M")
                    scheduled_time = dt.isoformat()
                except:
                    try:
                        if isinstance(row['scheduledDate'], datetime):
                            dt = row['scheduledDate']
                        else:
                            dt = datetime.strptime(scheduled_date, "%Y-%m-%d")
                        time_parts = scheduled_time_str.split(':')
                        dt = dt.replace(hour=int(time_parts[0]), minute=int(time_parts[1]))
                        scheduled_time = dt.isoformat()
                    except:
                        scheduled_time = None
        
        # Thumbnail path
        thumbnail_path = None
        if pd.notna(row.get('thumbnailPath')):
            thumb_str = str(row['thumbnailPath']).strip()
            if thumb_str and thumb_str.lower() != 'nan':
                if os.path.exists(thumb_str):
                    thumbnail_path = thumb_str
        
        return {
            "row_index": idx,
            "videoPath": video_path,
            "title": title,
            "description": str(row['description']),
            "tags": tags_list,
            "categoryId": category_id,
            "privacyStatus": str(row['privacyStatus']),
            "scheduledTime": scheduled_time,
            "thumbnailPath": thumbnail_path,
            "madeForKids": self._parse_bool(row.get('madeForKids', False)),
            "containsSyntheticMedia": self._parse_bool(row.get('containsSyntheticMedia', False)),
            "enableMonetization": self._parse_bool(row.get('enableMonetization', True))
        }
    
    def _parse_bool(self, value):
        """Parse boolean value from Excel"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.upper() in ['TRUE', '1', 'YES']
        if pd.isna(value):
            return False
        return bool(value)
