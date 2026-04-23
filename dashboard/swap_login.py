import re

def swap_login():
    new_model_path = r"c:\Users\maria\Downloads\antigravity lias\back.end dashboard\login modelo novo.HTML"
    index_path = r"c:\Users\maria\Downloads\antigravity lias\dashboard\index.html"
    
    with open(new_model_path, "r", encoding="utf-8") as f:
        new_html = f.read()
        
    with open(index_path, "r", encoding="utf-8") as f:
        index_html = f.read()

    # Extract new style
    style_match = re.search(r'<style[^>]*>(.*?)</style>', new_html, re.DOTALL | re.IGNORECASE)
    if not style_match:
        print("Style not found in new model")
        return
    new_style = style_match.group(0)

    # Add overlay properties to the new style's .login-shell rule so it covers the dashboard
    # We replace .login-shell { with .login-shell { position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 9999;
    new_style = re.sub(r'\.login-shell\s*\{', '.login-shell { position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 9999;', new_style)

    # Extract new main
    main_match = re.search(r'<main[^>]*login-shell[^>]*>.*?</main>', new_html, re.DOTALL | re.IGNORECASE)
    if not main_match:
        print("Main not found in new model")
        return
    new_main = main_match.group(0)
    
    # Add id="authOverlay" to the new main tag so JS can hide it
    new_main = re.sub(r'<main', '<main id="authOverlay"', new_main, count=1)
    
    # Ensure the Google SSO button has the onclick event
    # Find the button with id="ssoBtn" or similar and add onclick="AuthService.signInWithOAuth('google')"
    new_main = re.sub(
        r'<button type="button" class="form-sso" id="ssoBtn">',
        '<button type="button" class="form-sso" id="ssoBtn" onclick="AuthService.signInWithOAuth(\'google\')">',
        new_main
    )

    # Replace the FIRST style block in index.html (which is the login style)
    # We find all style blocks and replace the first one
    style_blocks = list(re.finditer(r'<style[^>]*>.*?</style>', index_html, re.DOTALL | re.IGNORECASE))
    if style_blocks:
        first_style_span = style_blocks[0].span()
        index_html = index_html[:first_style_span[0]] + new_style + index_html[first_style_span[1]:]
    
    # Replace the old <main id="authOverlay" ... > with new_main
    old_main_match = re.search(r'<main[^>]*id="authOverlay"[^>]*>.*?</main>', index_html, re.DOTALL | re.IGNORECASE)
    if old_main_match:
        span = old_main_match.span()
        index_html = index_html[:span[0]] + new_main + index_html[span[1]:]
    else:
        # Fallback if id was lost, look for login-shell
        old_main_match2 = re.search(r'<main[^>]*login-shell[^>]*>.*?</main>', index_html, re.DOTALL | re.IGNORECASE)
        if old_main_match2:
            span = old_main_match2.span()
            index_html = index_html[:span[0]] + new_main + index_html[span[1]:]
        else:
            print("Old main not found in index.html")
            return

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
        
    print("Login model swapped successfully!")

if __name__ == "__main__":
    swap_login()
