import pandas as pd
from datetime import datetime, timedelta

base_date = datetime.now() + timedelta(days=1)

data = {
    'title': [
        'Live Test A - Gaming Stream',
        'Live Test B - Tutorial',
        'Live Test C - Q&A Session'
    ],
    'description': [
        'Testing YouTube Live API integration for gaming content',
        'Tutorial on Python automation with YouTube API',
        'Live Q&A session with viewers'
    ],
    'tags': [
        'gaming,live,test,automation',
        'tutorial,python,youtube,api',
        'qa,live,interactive'
    ],
    'categoryId': [20, 27, 22],
    'privacyStatus': ['unlisted', 'public', 'unlisted'],
    'scheduledStartDate': [
        (base_date + timedelta(hours=1)).strftime('%Y-%m-%d'),
        (base_date + timedelta(hours=3)).strftime('%Y-%m-%d'),
        (base_date + timedelta(hours=5)).strftime('%Y-%m-%d')
    ],
    'scheduledStartTime': [
        (base_date + timedelta(hours=1)).strftime('%H:%M'),
        (base_date + timedelta(hours=3)).strftime('%H:%M'),
        (base_date + timedelta(hours=5)).strftime('%H:%M')
    ],
    'thumbnailPath': ['', '', ''],
    'streamId': ['', '', ''],
    'streamKey': ['', '', ''],
    'latency': ['normal', 'low', 'normal'],
    'enableDvr': [True, True, True],
    'enableEmbed': [True, True, True],
    'recordFromStart': [True, True, True],
    'madeForKids': [False, False, False],
    'containsSyntheticMedia': [False, False, True]
}

df = pd.DataFrame(data)

import sys
output_file = sys.argv[1] if len(sys.argv) > 1 else 'sample_broadcasts_new.xlsx'

df.to_excel(output_file, index=False)
print(f"Created {output_file}")
print(f"\nNote: Date/time columns are now included in the Excel file")
print(f"Scheduled times start from: {base_date.strftime('%Y-%m-%d %H:%M')}")
print(f"\n{df.to_string()}")
