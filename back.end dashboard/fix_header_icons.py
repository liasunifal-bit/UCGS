import os
import re

def fix_header_icons(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix Bell icon in button
    content = re.sub(
        r'(<button class="notification-btn".*?>).*?(<span class="notification-badge")',
        r'\1\n                    <i data-lucide="bell"></i>\n                    \2',
        content,
        flags=re.DOTALL
    )

    # Fix Moon icon in dropdown
    content = re.sub(
        r'<span class="dropdown-theme-label">.*?Tema Noturno</span>',
        r'<span class="dropdown-theme-label"><i data-lucide="moon" style="width:16px;height:16px;display:inline-block;vertical-align:middle;margin-right:8px;"></i> Tema Noturno</span>',
        content
    )

    # Fix Bell in panel header
    content = re.sub(
        r'<h2>.*?Notifica.*?<span',
        r'<h2><i data-lucide="bell" style="vertical-align:middle;margin-right:8px;"></i> Notificações <span',
        content
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Header icons fixed in {file_path}")

if __name__ == "__main__":
    target = r'c:\Users\maria\Downloads\antigravity lias\back.end dashboard\site nevo.HTML'
    fix_header_icons(target)
