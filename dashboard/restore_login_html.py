
import re
import os

index_path = r'c:\Users\maria\Downloads\antigravity lias\dashboard\index.html'
login_path = r'c:\Users\maria\Downloads\login_UCGS (3).html'

def restore_login_content():
    if not os.path.exists(login_path):
        print(f"Login template not found: {login_path}")
        return
    
    with open(login_path, 'r', encoding='utf-8') as f:
        login_content = f.read()
    
    # Extract everything inside <main ...> </main>
    # Note: the class in template might be slightly different
    match = re.search(r'<main[^>]*class="login-shell"[^>]*>(.*?)</main>', login_content, re.DOTALL)
    if not match:
        print("Could not find login content in template")
        return
    
    inner_html = match.group(1)
    
    with open(index_path, 'r', encoding='utf-8', errors='ignore') as f:
        index_content = f.read()
    
    # Replace the empty authOverlay in index.html
    # Current index.html looks like: <main id="authOverlay" class="login-shell" role="main">\n\n        \n\n\n    \n\n\n    <!-- Supabase
    pattern = r'(<main id="authOverlay" class="login-shell" role="main">)(.*?)(<!-- Supabase SDK)'
    
    if re.search(pattern, index_content, re.DOTALL):
        new_index = re.sub(pattern, r'\1' + inner_html + r'\n\n    \3', index_content, flags=re.DOTALL)
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_index)
        print("Success! Login HTML restored inside authOverlay.")
    else:
        print("Could not find the injection point in index.html")
        # Let's try a simpler replacement if the above fails
        if '<main id="authOverlay"' in index_content:
             print("Found <main id='authOverlay'>, attempting manual slice replacement...")
             start_tag = '<main id="authOverlay" class="login-shell" role="main">'
             end_marker = '<!-- Supabase SDK'
             start_idx = index_content.find(start_tag) + len(start_tag)
             end_idx = index_content.find(end_marker)
             if start_idx != -1 and end_idx != -1:
                 new_index = index_content[:start_idx] + inner_html + "\n\n    " + index_content[end_idx:]
                 with open(index_path, 'w', encoding='utf-8') as f:
                     f.write(new_index)
                 print("Success (manual slice)!")

if __name__ == "__main__":
    restore_login_content()
