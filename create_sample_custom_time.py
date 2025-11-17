"""
Create sample Excel files with custom scheduled times
"""

import pandas as pd
from datetime import datetime, timedelta

def create_custom_time_broadcast_excel():
    """Create sample broadcast Excel with custom times"""
    
    # Start from tomorrow at 20:00
    base_date = datetime.now() + timedelta(days=1)
    base_date = base_date.replace(hour=20, minute=0, second=0, microsecond=0)
    
    data = [
        {
            'title': 'Live Gaming Night #1',
            'description': 'Evening gaming session with chat',
            'tags': 'gaming,live,multiplayer',
            'categoryId': 20,
            'privacyStatus': 'public',
            'scheduledStartTime': base_date.strftime('%Y-%m-%dT20:00:00'),
            'madeForKids': False,
            'containsSyntheticMedia': False,
            'enableDvr': True,
            'enableMonetization': True,
            'latency': 'normal'
        },
        {
            'title': 'Live Gaming Night #2',
            'description': 'Evening gaming session with chat',
            'tags': 'gaming,live,multiplayer',
            'categoryId': 20,
            'privacyStatus': 'public',
            'scheduledStartTime': (base_date + timedelta(hours=2, minutes=30)).strftime('%Y-%m-%dT22:30:00'),
            'madeForKids': False,
            'containsSyntheticMedia': False,
            'enableDvr': True,
            'enableMonetization': True,
            'latency': 'normal'
        },
        {
            'title': 'Morning Talk Show',
            'description': 'Morning discussion and Q&A',
            'tags': 'talk,discussion,live',
            'categoryId': 22,
            'privacyStatus': 'public',
            'scheduledStartTime': (base_date + timedelta(days=1, hours=-10)).strftime('%Y-%m-%dT10:00:00'),
            'madeForKids': False,
            'containsSyntheticMedia': False,
            'enableDvr': True,
            'enableMonetization': True,
            'latency': 'normal'
        },
        {
            'title': 'Afternoon Workshop',
            'description': 'Tutorial and learning session',
            'tags': 'tutorial,workshop,education',
            'categoryId': 27,
            'privacyStatus': 'public',
            'scheduledStartTime': (base_date + timedelta(days=1, hours=-6)).strftime('%Y-%m-%dT14:00:00'),
            'madeForKids': False,
            'containsSyntheticMedia': False,
            'enableDvr': True,
            'enableMonetization': True,
            'latency': 'normal'
        },
        {
            'title': 'Weekend Special Stream',
            'description': 'Special weekend live session',
            'tags': 'special,weekend,live',
            'categoryId': 20,
            'privacyStatus': 'public',
            'scheduledStartTime': (base_date + timedelta(days=2, hours=1)).strftime('%Y-%m-%dT21:00:00'),
            'madeForKids': False,
            'containsSyntheticMedia': False,
            'enableDvr': True,
            'enableMonetization': True,
            'latency': 'normal'
        }
    ]
    
    df = pd.DataFrame(data)
    filename = 'sample_broadcasts_custom_time.xlsx'
    df.to_excel(filename, index=False, engine='openpyxl')
    
    print(f"[OK] Created: {filename}")
    print(f"  - {len(data)} broadcasts with custom times")
    print(f"\nScheduled Times:")
    for idx, item in enumerate(data, 1):
        print(f"  {idx}. {item['title']}")
        print(f"     Time: {item['scheduledStartTime']}")


def create_event_schedule_excel():
    """Create sample event schedule with multiple sessions per day"""
    
    # 3-day event starting tomorrow
    day1 = datetime.now() + timedelta(days=1)
    day1 = day1.replace(hour=9, minute=0, second=0, microsecond=0)
    
    data = [
        # Day 1
        {
            'title': 'Event Opening Ceremony',
            'description': 'Welcome and opening remarks',
            'tags': 'event,opening,ceremony',
            'categoryId': 22,
            'privacyStatus': 'public',
            'scheduledStartTime': day1.strftime('%Y-%m-%dT09:00:00'),
            'enableMonetization': True
        },
        {
            'title': 'Keynote Session',
            'description': 'Main keynote presentation',
            'tags': 'event,keynote,presentation',
            'categoryId': 27,
            'privacyStatus': 'public',
            'scheduledStartTime': (day1 + timedelta(hours=1)).strftime('%Y-%m-%dT10:00:00'),
            'enableMonetization': True
        },
        {
            'title': 'Workshop Session 1',
            'description': 'Interactive workshop',
            'tags': 'event,workshop,interactive',
            'categoryId': 27,
            'privacyStatus': 'public',
            'scheduledStartTime': (day1 + timedelta(hours=3)).strftime('%Y-%m-%dT12:00:00'),
            'enableMonetization': True
        },
        {
            'title': 'Panel Discussion',
            'description': 'Expert panel discussion',
            'tags': 'event,panel,discussion',
            'categoryId': 22,
            'privacyStatus': 'public',
            'scheduledStartTime': (day1 + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%dT14:30:00'),
            'enableMonetization': True
        },
        {
            'title': 'Day 1 Closing',
            'description': 'Day 1 wrap-up and summary',
            'tags': 'event,closing,summary',
            'categoryId': 22,
            'privacyStatus': 'public',
            'scheduledStartTime': (day1 + timedelta(hours=8)).strftime('%Y-%m-%dT17:00:00'),
            'enableMonetization': True
        },
        
        # Day 2
        {
            'title': 'Day 2 Opening',
            'description': 'Day 2 kickoff',
            'tags': 'event,day2,opening',
            'categoryId': 22,
            'privacyStatus': 'public',
            'scheduledStartTime': (day1 + timedelta(days=1, hours=0, minutes=30)).strftime('%Y-%m-%dT09:30:00'),
            'enableMonetization': True
        },
        {
            'title': 'Technical Deep Dive',
            'description': 'In-depth technical session',
            'tags': 'event,technical,deepdive',
            'categoryId': 28,
            'privacyStatus': 'public',
            'scheduledStartTime': (day1 + timedelta(days=1, hours=2)).strftime('%Y-%m-%dT11:00:00'),
            'enableMonetization': True
        },
        {
            'title': 'Networking Session',
            'description': 'Community networking',
            'tags': 'event,networking,community',
            'categoryId': 22,
            'privacyStatus': 'public',
            'scheduledStartTime': (day1 + timedelta(days=1, hours=5)).strftime('%Y-%m-%dT14:00:00'),
            'enableMonetization': True
        },
        
        # Day 3
        {
            'title': 'Final Day Opening',
            'description': 'Final day kickoff',
            'tags': 'event,final,opening',
            'categoryId': 22,
            'privacyStatus': 'public',
            'scheduledStartTime': (day1 + timedelta(days=2, hours=0)).strftime('%Y-%m-%dT09:00:00'),
            'enableMonetization': True
        },
        {
            'title': 'Grand Finale & Awards',
            'description': 'Event conclusion and awards ceremony',
            'tags': 'event,finale,awards',
            'categoryId': 22,
            'privacyStatus': 'public',
            'scheduledStartTime': (day1 + timedelta(days=2, hours=9)).strftime('%Y-%m-%dT18:00:00'),
            'enableMonetization': True
        }
    ]
    
    # Add default values for missing columns
    for item in data:
        item.setdefault('madeForKids', False)
        item.setdefault('containsSyntheticMedia', False)
        item.setdefault('enableDvr', True)
        item.setdefault('latency', 'normal')
    
    df = pd.DataFrame(data)
    filename = 'sample_event_schedule.xlsx'
    df.to_excel(filename, index=False, engine='openpyxl')
    
    print(f"\n[OK] Created: {filename}")
    print(f"  - {len(data)} sessions across 3 days")
    print(f"\nEvent Schedule:")
    current_day = None
    for idx, item in enumerate(data, 1):
        time_str = item['scheduledStartTime']
        day = time_str.split('T')[0]
        time_part = time_str.split('T')[1]
        
        if day != current_day:
            current_day = day
            print(f"\n  Day {day}:")
        
        print(f"    {time_part} - {item['title']}")


def create_weekly_schedule_excel():
    """Create sample weekly schedule (Tue/Thu pattern)"""
    
    # Find next Tuesday
    today = datetime.now()
    days_ahead = (1 - today.weekday()) % 7  # Tuesday is 1
    if days_ahead == 0:
        days_ahead = 7
    
    next_tuesday = today + timedelta(days=days_ahead)
    next_tuesday = next_tuesday.replace(hour=20, minute=0, second=0, microsecond=0)
    
    data = []
    
    # 4 weeks schedule
    for week in range(4):
        # Tuesday
        tuesday = next_tuesday + timedelta(weeks=week)
        data.append({
            'title': f'Tuesday Live Stream - Week {week + 1}',
            'description': 'Weekly Tuesday gaming session',
            'tags': 'weekly,tuesday,gaming',
            'categoryId': 20,
            'privacyStatus': 'public',
            'scheduledStartTime': tuesday.strftime('%Y-%m-%dT20:00:00'),
            'enableMonetization': True,
            'madeForKids': False,
            'containsSyntheticMedia': False,
            'enableDvr': True,
            'latency': 'normal'
        })
        
        # Thursday (2 days after Tuesday)
        thursday = tuesday + timedelta(days=2)
        thursday = thursday.replace(hour=21, minute=30)
        data.append({
            'title': f'Thursday Late Night - Week {week + 1}',
            'description': 'Weekly Thursday late night stream',
            'tags': 'weekly,thursday,latenight',
            'categoryId': 20,
            'privacyStatus': 'public',
            'scheduledStartTime': thursday.strftime('%Y-%m-%dT21:30:00'),
            'enableMonetization': True,
            'madeForKids': False,
            'containsSyntheticMedia': False,
            'enableDvr': True,
            'latency': 'normal'
        })
    
    df = pd.DataFrame(data)
    filename = 'sample_weekly_schedule.xlsx'
    df.to_excel(filename, index=False, engine='openpyxl')
    
    print(f"\n[OK] Created: {filename}")
    print(f"  - {len(data)} streams (4 weeks, Tue/Thu pattern)")
    print(f"\nWeekly Schedule:")
    for idx, item in enumerate(data, 1):
        time_str = item['scheduledStartTime']
        print(f"  {idx}. {item['title']}")
        print(f"     Time: {time_str}")


if __name__ == "__main__":
    print("Creating sample Excel files with custom scheduled times...\n")
    print("=" * 60)
    
    try:
        create_custom_time_broadcast_excel()
        create_event_schedule_excel()
        create_weekly_schedule_excel()
        
        print("\n" + "=" * 60)
        print("\n[SUCCESS] All sample files created successfully!")
        print("\nFiles created:")
        print("  1. sample_broadcasts_custom_time.xlsx - Mixed schedule")
        print("  2. sample_event_schedule.xlsx - 3-day event")
        print("  3. sample_weekly_schedule.xlsx - 4-week Tue/Thu pattern")
        print("\nYou can now:")
        print("  1. Open these files in Excel")
        print("  2. Modify the times as needed")
        print("  3. Load in AutoLiveBio (Tab: Import & Run)")
        print("  4. Click 'Process Batch'")
        print("\nHappy scheduling!")
        
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
