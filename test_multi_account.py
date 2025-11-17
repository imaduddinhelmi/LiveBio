"""
Debug script to test multi-account functionality
"""

from multi_account_manager import MultiAccountManager

def test_account_manager():
    print("Testing Multi-Account Manager...")
    print("=" * 50)
    
    manager = MultiAccountManager()
    
    # Check current accounts
    accounts = manager.get_all_accounts()
    print(f"\nTotal accounts: {len(accounts)}")
    
    if accounts:
        print("\nSaved Accounts:")
        for i, acc in enumerate(accounts, 1):
            print(f"\n{i}. Account ID: {acc['id']}")
            print(f"   Name: {acc['name']}")
            print(f"   Email: {acc['email']}")
            print(f"   Channels: {len(acc.get('channels', []))}")
            print(f"   Added: {acc.get('added_date', 'N/A')[:10]}")
            print(f"   Last used: {acc.get('last_used', 'N/A')[:10]}")
            
            # Check if token file exists
            token_path = manager.get_token_path(acc['id'])
            token_exists = token_path.exists()
            print(f"   Token file: {'✓ Exists' if token_exists else '✗ Missing'}")
            
            if acc.get('channels'):
                print(f"   Channels:")
                for ch in acc['channels'][:3]:  # Show first 3 channels
                    print(f"      - {ch.get('title', 'Unknown')}")
    else:
        print("\nNo accounts saved yet.")
    
    # Check active account
    print("\n" + "=" * 50)
    active = manager.get_active_account()
    if active:
        print(f"\nActive Account: {active['name']}")
    else:
        print("\nNo active account set")
    
    print("\n" + "=" * 50)
    print(f"Accounts file: {manager.accounts_file}")
    print(f"Tokens directory: {manager.tokens_dir}")
    print("\nTest complete!")

if __name__ == "__main__":
    test_account_manager()
