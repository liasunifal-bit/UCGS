import os

backup_path = r'c:\Users\maria\Downloads\antigravity lias\back.end dashboard\site nevo_backup_encoding.HTML'

with open(backup_path, 'rb') as f:
    lines = f.readlines()
    if len(lines) >= 29067:
        print(f"Line 29067 bytes: {lines[29066]}")
    else:
        print(f"File only has {len(lines)} lines.")
