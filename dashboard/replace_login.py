import re

def main():
    # Read login_UCGS (3).html
    with open(r"c:\Users\maria\Downloads\login_UCGS (3).html", "r", encoding="utf-8") as f:
        login_html = f.read()

    # Extract CSS
    css_match = re.search(r'<style>(.*?)</style>', login_html, re.DOTALL)
    if not css_match:
        print("CSS not found in login html")
        return
    css_content = css_match.group(1)

    # Extract SVG + HTML
    # Starts from <svg xmlns="http://www.w3.org/2000/svg" to </main>
    html_match = re.search(r'(<svg xmlns="http://www.w3.org/2000/svg".*?</main>)', login_html, re.DOTALL)
    if not html_match:
        print("HTML not found in login html")
        return
    html_content = html_match.group(1)
    
    # Add id="authOverlay" to the main tag to keep JS working
    html_content = html_content.replace('<main class="login-shell" role="main">', '<main id="authOverlay" class="login-shell" role="main">')

    # Read index.html
    index_path = r"c:\Users\maria\Downloads\antigravity lias\dashboard\index.html"
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()

    # Replace CSS in index.html
    # We look for the block between /* ==========================================================
    #        UCGS · TELA DE ACESSO PREMIUM (Split Layout)
    #        ========================================================== */
    # and </style>
    
    # Let's find the exact CSS block to replace
    start_css_marker = "/* ==========================================================\n           UCGS · TELA DE ACESSO PREMIUM (Split Layout)\n           ========================================================== */"
    # Actually, it's easier to find it by regex
    index_content = re.sub(r'/\* ==========================================================\n           UCGS · TELA DE ACESSO PREMIUM \(Split Layout\).*?@media \(max-width: 480px\) \{ \.auth-form-panel \{ padding: 32px 20px; \} \}\s*', css_content, index_content, flags=re.DOTALL)

    # Replace HTML in index.html
    # Look for <!-- OVERLAY DE LOGIN UCGS — SPLIT PREMIUM --> to <!-- Skip link
    index_content = re.sub(r'<div id="authOverlay">.*?</div>\n\n    <!-- Skip link', html_content + '\n\n    <!-- Skip link', index_content, flags=re.DOTALL)

    # Save back
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print("Successfully replaced login HTML and CSS in index.html")

if __name__ == "__main__":
    main()
