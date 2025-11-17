import pandas as pd
from datetime import datetime, timedelta

def parse_excel_file(file_path, default_date=None, default_time=None):
    """Parse Excel file for broadcast data"""
    try:
        df = pd.read_excel(file_path)
        
        broadcasts = []
        
        for index, row in df.iterrows():
            # Parse tags
            tags = []
            if pd.notna(row.get('tags')):
                tags = [tag.strip() for tag in str(row['tags']).split(',')]
            
            # Parse scheduled time
            scheduled_time = parse_scheduled_time(
                row.get('scheduledStartDate'),
                row.get('scheduledStartTime'),
                default_date,
                default_time
            )
            
            broadcast = {
                'title': row.get('title', f'Untitled Broadcast {index + 1}'),
                'description': row.get('description', ''),
                'tags': tags,
                'categoryId': str(row.get('categoryId', '20')),
                'privacyStatus': row.get('privacyStatus', 'public'),
                'scheduledStartTime': scheduled_time,
                'thumbnailPath': row.get('thumbnailPath', ''),
                'streamId': row.get('streamId', ''),
                'streamKey': row.get('streamKey', ''),
                'latency': row.get('latency', 'normal'),
                'enableDvr': bool(row.get('enableDvr', True)),
                'enableEmbed': bool(row.get('enableEmbed', True)),
                'recordFromStart': bool(row.get('recordFromStart', True)),
                'madeForKids': bool(row.get('madeForKids', False)),
                'containsSyntheticMedia': bool(row.get('containsSyntheticMedia', False)),
                'enableMonetization': bool(row.get('enableMonetization', False))
            }
            
            broadcasts.append(broadcast)
        
        return True, broadcasts
    except Exception as e:
        return False, str(e)

def parse_scheduled_time(date_val, time_val, default_date=None, default_time=None):
    """Parse scheduled time from date and time values"""
    try:
        # Use defaults if not provided
        if pd.isna(date_val):
            if default_date:
                date_val = default_date
            else:
                # Default to tomorrow
                date_val = (datetime.now() + timedelta(days=1)).date()
        
        if pd.isna(time_val):
            if default_time:
                time_val = default_time
            else:
                # Default to 12:00
                time_val = "12:00"
        
        # Parse date
        if isinstance(date_val, str):
            date_obj = datetime.strptime(date_val, '%Y-%m-%d').date()
        else:
            date_obj = date_val if hasattr(date_val, 'date') else date_val
        
        # Parse time
        if isinstance(time_val, str):
            time_obj = datetime.strptime(time_val, '%H:%M').time()
        else:
            time_obj = time_val if hasattr(time_val, 'time') else time_val
        
        # Combine
        scheduled_dt = datetime.combine(date_obj, time_obj)
        
        return scheduled_dt.isoformat()
    except Exception as e:
        print(f"Error parsing scheduled time: {e}")
        # Default to 1 hour from now
        default_time = datetime.now() + timedelta(hours=1)
        return default_time.isoformat()
