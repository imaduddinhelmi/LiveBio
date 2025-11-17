import pandas as pd

data = {
    'videoPath': [
        'D:\\Videos\\video1.mp4',
        'D:\\Videos\\video2.mp4', 
        'D:\\Videos\\video3.mp4'
    ],
    'title': [
        'My First Video',
        'My Second Video',
        'Gaming Tutorial'
    ],
    'description': [
        'This is my first video description',
        'This is my second video description',
        'Learn how to play this game'
    ],
    'tags': [
        'tutorial,gaming,youtube',
        'vlog,daily,life',
        'gaming,tutorial,howto'
    ],
    'categoryId': [22, 22, 20],
    'privacyStatus': ['unlisted', 'unlisted', 'public'],
    'scheduledDate': ['2024-12-25', '2024-12-25', '2024-12-25'],
    'scheduledTime': ['10:00', '11:00', '14:00'],
    'thumbnailPath': ['', 'D:\\Thumbnails\\thumb2.jpg', 'D:\\Thumbnails\\thumb3.jpg'],
    'madeForKids': [False, False, False],
    'containsSyntheticMedia': [False, False, False],
    'enableMonetization': [True, True, True]
}

df = pd.DataFrame(data)
df.to_excel('sample_videos.xlsx', index=False, engine='openpyxl')
print('Sample videos.xlsx created successfully!')
