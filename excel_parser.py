import pandas as pd
from datetime import datetime, timezone, timedelta
import config

class ExcelParser:
    def __init__(self):
        self.df = None
        self.file_path = None
    
    def load_excel(self, file_path):
        try:
            self.df = pd.read_excel(file_path)
            self.file_path = file_path
            
            missing_cols = [col for col in config.EXCEL_REQUIRED_COLUMNS if col not in self.df.columns]
            if missing_cols:
                return False, f"Missing required columns: {', '.join(missing_cols)}"
            
            for col, default_val in config.EXCEL_OPTIONAL_COLUMNS.items():
                if col not in self.df.columns:
                    self.df[col] = default_val
            
            return True, f"Loaded {len(self.df)} rows successfully"
        except Exception as e:
            return False, f"Error loading Excel: {str(e)}"
    
    def get_preview(self, rows=10):
        if self.df is None:
            return None
        return self.df.head(rows)
    
    def get_all_rows(self):
        if self.df is None:
            return []
        
        rows = []
        for idx, row in self.df.iterrows():
            try:
                broadcast_data = self._parse_row(row, idx)
                rows.append(broadcast_data)
            except Exception as e:
                rows.append({"error": f"Row {idx+1}: {str(e)}", "row_index": idx})
        
        return rows
    
    def _parse_row(self, row, idx):
        tags_list = [tag.strip() for tag in str(row['tags']).split(',') if tag.strip()]
        
        scheduled_start_time = None
        
        # Try to parse from single column 'scheduledStartTime' (ISO format)
        if pd.notna(row.get('scheduledStartTime')):
            sst_str = str(row['scheduledStartTime']).strip()
            if sst_str and sst_str.lower() != 'nan':
                try:
                    # Try ISO format: 2025-11-20T20:00:00 or 2025-11-20T20:00:00Z
                    if 'T' in sst_str:
                        if not sst_str.endswith('Z'):
                            # Parse as local time and convert to UTC
                            dt = datetime.fromisoformat(sst_str.replace('Z', ''))
                            # Convert local time to UTC
                            utc_offset_seconds = datetime.now().astimezone().utcoffset().total_seconds()
                            dt_utc = dt - timedelta(seconds=utc_offset_seconds)
                            scheduled_start_time = dt_utc.isoformat() + 'Z'
                        else:
                            scheduled_start_time = sst_str
                    else:
                        # Try parsing as datetime and convert to ISO
                        dt = datetime.strptime(sst_str, "%Y-%m-%d %H:%M:%S")
                        # Convert local time to UTC
                        utc_offset_seconds = datetime.now().astimezone().utcoffset().total_seconds()
                        dt_utc = dt - timedelta(seconds=utc_offset_seconds)
                        scheduled_start_time = dt_utc.isoformat() + 'Z'
                except:
                    pass
        
        # Fallback: Try to parse from two columns (legacy format)
        if not scheduled_start_time and pd.notna(row.get('scheduledStartDate')) and pd.notna(row.get('scheduledStartTime_old')):
            scheduled_date = str(row['scheduledStartDate'])
            scheduled_time = str(row['scheduledStartTime_old'])
            
            if scheduled_date and scheduled_date.lower() != 'nan' and scheduled_time and scheduled_time.lower() != 'nan':
                try:
                    dt = datetime.strptime(f"{scheduled_date} {scheduled_time}", "%Y-%m-%d %H:%M")
                    # Convert local time to UTC
                    utc_offset_seconds = datetime.now().astimezone().utcoffset().total_seconds()
                    dt_utc = dt - timedelta(seconds=utc_offset_seconds)
                    scheduled_start_time = dt_utc.isoformat() + 'Z'
                except:
                    try:
                        if isinstance(row['scheduledStartDate'], datetime):
                            dt = row['scheduledStartDate']
                        else:
                            dt = datetime.strptime(scheduled_date, "%Y-%m-%d")
                        time_parts = scheduled_time.split(':')
                        dt = dt.replace(hour=int(time_parts[0]), minute=int(time_parts[1]))
                        # Convert local time to UTC
                        utc_offset_seconds = datetime.now().astimezone().utcoffset().total_seconds()
                        dt_utc = dt - timedelta(seconds=utc_offset_seconds)
                        scheduled_start_time = dt_utc.isoformat() + 'Z'
                    except:
                        try:
                            dt = datetime.strptime(f"{scheduled_date} {scheduled_time}", "%d/%m/%Y %H:%M")
                            # Convert local time to UTC
                            utc_offset_seconds = datetime.now().astimezone().utcoffset().total_seconds()
                            dt_utc = dt - timedelta(seconds=utc_offset_seconds)
                            scheduled_start_time = dt_utc.isoformat() + 'Z'
                        except:
                            scheduled_start_time = None
        
        thumbnail_path = None
        if pd.notna(row.get('thumbnailPath')) and str(row['thumbnailPath']).strip():
            thumb_str = str(row['thumbnailPath']).strip()
            if thumb_str and thumb_str.lower() != 'nan':
                thumbnail_path = thumb_str
        
        stream_id = None
        if pd.notna(row.get('streamId')) and str(row['streamId']).strip():
            sid_str = str(row['streamId']).strip()
            if sid_str and sid_str.lower() != 'nan':
                stream_id = sid_str
        
        stream_key = None
        if pd.notna(row.get('streamKey')) and str(row['streamKey']).strip():
            skey_str = str(row['streamKey']).strip()
            if skey_str and skey_str.lower() != 'nan':
                stream_key = skey_str
        
        category_id = "22"
        if pd.notna(row.get('categoryId')):
            try:
                if isinstance(row['categoryId'], (int, float)):
                    category_id = str(int(row['categoryId']))
                else:
                    category_id = str(int(float(row['categoryId'])))
            except (ValueError, TypeError):
                category_id = "22"
        
        return {
            "row_index": idx,
            "title": str(row['title']),
            "description": str(row['description']),
            "tags": tags_list,
            "categoryId": category_id,
            "privacyStatus": str(row['privacyStatus']),
            "scheduledStartTime": scheduled_start_time,
            "thumbnailPath": thumbnail_path,
            "streamId": stream_id,
            "streamKey": stream_key,
            "latency": str(row.get('latency', 'normal')),
            "enableDvr": self._parse_bool(row.get('enableDvr', True)),
            "enableEmbed": self._parse_bool(row.get('enableEmbed', True)),
            "recordFromStart": self._parse_bool(row.get('recordFromStart', True)),
            "madeForKids": self._parse_bool(row.get('madeForKids', False)),
            "containsSyntheticMedia": self._parse_bool(row.get('containsSyntheticMedia', False)),
            "enableMonetization": self._parse_bool(row.get('enableMonetization', False))
        }
    
    def _parse_bool(self, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.upper() in ['TRUE', '1', 'YES']
        return bool(value)
