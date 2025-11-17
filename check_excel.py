import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== sample_broadcasts.xlsx ===")
df1 = pd.read_excel('sample_broadcasts.xlsx')
print(f"Columns: {list(df1.columns)}")
print(f"Number of rows: {len(df1)}")

if 'scheduledStartDate' in df1.columns and 'scheduledStartTime' in df1.columns:
    print("\nDate/Time columns found:")
    print(f"scheduledStartDate: {df1['scheduledStartDate'].tolist()}")
    print(f"scheduledStartTime: {df1['scheduledStartTime'].tolist()}")
else:
    print("\nNo scheduledStartDate/scheduledStartTime columns found.")
    print("Available columns:", list(df1.columns))

print("\n" + "="*80 + "\n")

print("=== sample_broadcasts_new.xlsx ===")
df2 = pd.read_excel('sample_broadcasts_new.xlsx')
print(f"Columns: {list(df2.columns)}")
print(f"Number of rows: {len(df2)}")

if 'scheduledStartDate' in df2.columns and 'scheduledStartTime' in df2.columns:
    print("\nDate/Time columns found:")
    print(f"scheduledStartDate: {df2['scheduledStartDate'].tolist()}")
    print(f"scheduledStartTime: {df2['scheduledStartTime'].tolist()}")
else:
    print("\nNo scheduledStartDate/scheduledStartTime columns found.")
    print("Available columns:", list(df2.columns))
