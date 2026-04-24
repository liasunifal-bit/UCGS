
import sys

def find_mojibake(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if 'ðŸ' in line:
                    print(f"Line {i}: {line.strip()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_mojibake(r"c:\Users\maria\Downloads\antigravity lias\dashboard\index.html")
