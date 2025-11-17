#!/usr/bin/env python3
"""
YTLive CLI - Command line interface for headless server
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from auth_headless import HeadlessAuth
from youtube_service import YouTubeService
from excel_parser import parse_excel_file

def cmd_auth_new(args):
    """Perform new authentication"""
    print("=== YouTube Live - New Authentication ===\n")
    
    auth = HeadlessAuth()
    
    try:
        auth.authenticate_new(args.client_secret)
        print("\n✓ Authentication successful!")
        print("✓ Credentials saved")
        print("\nYou can now use the CLI or start the daemon")
    except Exception as e:
        print(f"\n✗ Authentication failed: {e}")
        return 1
    
    return 0

def cmd_auth_status(args):
    """Check authentication status"""
    print("=== Authentication Status ===\n")
    
    auth = HeadlessAuth()
    
    if auth.load_saved_credentials():
        print(f"✓ Authenticated")
        print(f"Account: {auth.current_account_email}")
        print(f"Channels: {len(auth.all_channels)}")
        
        if args.verbose:
            print("\nChannels:")
            for ch in auth.all_channels:
                print(f"  - {ch['title']} ({ch['id']})")
                print(f"    Subscribers: {ch['subscribers']}")
        
        return 0
    else:
        print("✗ Not authenticated")
        print("Run: ytlive-cli.py auth --new")
        return 1

def cmd_create_batch(args):
    """Create batch broadcasts from Excel"""
    print("=== Create Batch Broadcasts ===\n")
    
    # Load auth
    auth = HeadlessAuth()
    if not auth.load_saved_credentials():
        print("✗ Not authenticated. Run: ytlive-cli.py auth --new")
        return 1
    
    # Parse Excel
    print(f"Parsing Excel file: {args.excel}")
    success, result = parse_excel_file(args.excel)
    
    if not success:
        print(f"✗ Failed to parse Excel: {result}")
        return 1
    
    broadcasts = result
    print(f"✓ Parsed {len(broadcasts)} broadcasts\n")
    
    # Preview
    if args.preview:
        for i, broadcast in enumerate(broadcasts[:5], 1):
            print(f"{i}. {broadcast['title']}")
            print(f"   Scheduled: {broadcast['scheduledStartTime']}")
            print(f"   Privacy: {broadcast['privacyStatus']}")
        
        if len(broadcasts) > 5:
            print(f"   ... and {len(broadcasts) - 5} more")
        
        response = input("\nProceed with creation? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled")
            return 0
    
    # Create broadcasts
    youtube = auth.get_youtube_client()
    youtube_service = YouTubeService(youtube, auth)
    
    print("\nCreating broadcasts...")
    results = []
    
    for i, broadcast in enumerate(broadcasts, 1):
        print(f"[{i}/{len(broadcasts)}] {broadcast['title']}...", end=' ')
        
        success, result = youtube_service.process_broadcast(broadcast)
        
        if success:
            print(f"✓ {result}")
            results.append({'success': True, 'id': result})
        else:
            print(f"✗ {result}")
            results.append({'success': False, 'error': result})
    
    # Summary
    success_count = sum(1 for r in results if r['success'])
    print(f"\n=== Summary ===")
    print(f"Total: {len(results)}")
    print(f"Success: {success_count}")
    print(f"Failed: {len(results) - success_count}")
    
    return 0

def cmd_schedule_batch(args):
    """Schedule batch creation"""
    print("=== Schedule Batch Creation ===\n")
    
    # Parse Excel
    print(f"Parsing Excel file: {args.excel}")
    success, result = parse_excel_file(args.excel)
    
    if not success:
        print(f"✗ Failed to parse Excel: {result}")
        return 1
    
    broadcasts = result
    print(f"✓ Parsed {len(broadcasts)} broadcasts\n")
    
    # Parse scheduled time
    try:
        if args.time:
            scheduled_time = datetime.fromisoformat(args.time)
        else:
            # Default to 1 hour from now
            scheduled_time = datetime.now() + timedelta(hours=1)
    except Exception as e:
        print(f"✗ Invalid time format: {e}")
        print("Use format: YYYY-MM-DDTHH:MM:SS")
        return 1
    
    # Load existing schedules
    if config.SCHEDULED_BATCHES_FILE.exists():
        with open(config.SCHEDULED_BATCHES_FILE, 'r') as f:
            scheduled_batches = json.load(f)
    else:
        scheduled_batches = []
    
    # Add new batch
    batch = {
        'id': f'batch_{int(datetime.now().timestamp())}',
        'name': args.name or f'Batch {len(scheduled_batches) + 1}',
        'broadcasts': broadcasts,
        'scheduledTime': scheduled_time.isoformat(),
        'status': 'pending',
        'createdAt': datetime.now().isoformat()
    }
    
    scheduled_batches.append(batch)
    
    # Save
    with open(config.SCHEDULED_BATCHES_FILE, 'w') as f:
        json.dump(scheduled_batches, f, indent=2)
    
    print(f"✓ Batch scheduled")
    print(f"Name: {batch['name']}")
    print(f"Broadcasts: {len(broadcasts)}")
    print(f"Scheduled time: {scheduled_time}")
    print(f"\nThe daemon will process this at the scheduled time")
    
    return 0

def cmd_list_scheduled(args):
    """List scheduled tasks"""
    print("=== Scheduled Tasks ===\n")
    
    # Load batches
    if config.SCHEDULED_BATCHES_FILE.exists():
        with open(config.SCHEDULED_BATCHES_FILE, 'r') as f:
            batches = json.load(f)
        
        if batches:
            print("Scheduled Batches:")
            for batch in batches:
                status_icon = {
                    'pending': '⏳',
                    'processing': '🔄',
                    'completed': '✓',
                    'failed': '✗'
                }.get(batch['status'], '?')
                
                print(f"\n{status_icon} {batch['name']}")
                print(f"  ID: {batch['id']}")
                print(f"  Status: {batch['status']}")
                print(f"  Broadcasts: {len(batch['broadcasts'])}")
                print(f"  Scheduled: {batch['scheduledTime']}")
                
                if batch['status'] == 'completed' and 'results' in batch:
                    success_count = sum(1 for r in batch['results'] if r['success'])
                    print(f"  Results: {success_count}/{len(batch['results'])} successful")
        else:
            print("No scheduled batches")
    else:
        print("No scheduled batches")
    
    print()
    
    # Load uploads
    if config.SCHEDULED_UPLOADS_FILE.exists():
        with open(config.SCHEDULED_UPLOADS_FILE, 'r') as f:
            uploads = json.load(f)
        
        if uploads:
            print("Scheduled Uploads:")
            for upload in uploads:
                status_icon = {
                    'pending': '⏳',
                    'processing': '🔄',
                    'completed': '✓',
                    'failed': '✗'
                }.get(upload['status'], '?')
                
                print(f"\n{status_icon} {upload['videoData']['title']}")
                print(f"  Status: {upload['status']}")
                print(f"  Scheduled: {upload['scheduledTime']}")
                
                if upload['status'] == 'completed':
                    print(f"  Video ID: {upload.get('videoId')}")
                elif upload['status'] == 'failed':
                    print(f"  Error: {upload.get('error')}")
        else:
            print("No scheduled uploads")
    else:
        print("No scheduled uploads")
    
    return 0

def cmd_daemon_status(args):
    """Check daemon status"""
    print("=== Daemon Status ===\n")
    
    if config.PID_FILE.exists():
        with open(config.PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        
        # Check if process is running
        try:
            import os
            os.kill(pid, 0)
            print(f"✓ Daemon is running (PID: {pid})")
            return 0
        except OSError:
            print(f"✗ Daemon is not running (stale PID file)")
            config.PID_FILE.unlink()
            return 1
    else:
        print("✗ Daemon is not running")
        return 1

def main():
    parser = argparse.ArgumentParser(
        description='YTLive CLI - Command line interface for headless YouTube Live management'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Auth command
    auth_parser = subparsers.add_parser('auth', help='Authentication management')
    auth_parser.add_argument('--new', action='store_true', help='Perform new authentication')
    auth_parser.add_argument('--status', action='store_true', help='Check authentication status')
    auth_parser.add_argument('--client-secret', default=None, help='Path to client_secret.json')
    auth_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    # Create batch command
    create_parser = subparsers.add_parser('create', help='Create batch broadcasts')
    create_parser.add_argument('excel', help='Path to Excel file')
    create_parser.add_argument('--preview', action='store_true', help='Preview before creating')
    
    # Schedule batch command
    schedule_parser = subparsers.add_parser('schedule', help='Schedule batch creation')
    schedule_parser.add_argument('excel', help='Path to Excel file')
    schedule_parser.add_argument('--time', help='Scheduled time (YYYY-MM-DDTHH:MM:SS)')
    schedule_parser.add_argument('--name', help='Batch name')
    
    # List scheduled command
    list_parser = subparsers.add_parser('list', help='List scheduled tasks')
    
    # Daemon status command
    daemon_parser = subparsers.add_parser('daemon', help='Daemon status')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Route to command handlers
    if args.command == 'auth':
        if args.new:
            return cmd_auth_new(args)
        elif args.status:
            return cmd_auth_status(args)
        else:
            print("Use --new or --status")
            return 1
    elif args.command == 'create':
        return cmd_create_batch(args)
    elif args.command == 'schedule':
        return cmd_schedule_batch(args)
    elif args.command == 'list':
        return cmd_list_scheduled(args)
    elif args.command == 'daemon':
        return cmd_daemon_status(args)
    else:
        parser.print_help()
        return 1

if __name__ == '__main__':
    sys.exit(main())
