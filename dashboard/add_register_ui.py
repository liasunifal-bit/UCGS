import re

def main():
    path = r'c:\Users\maria\Downloads\antigravity lias\dashboard\index.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Add a Register button next to Submit
    register_btn = '<button type="button" class="form-submit" id="registerBtn" style="background: var(--brand-blue); margin-top: 10px;">Registrar Nova Conta</button>'

    # Find submitBtn
    if 'id="registerBtn"' not in html:
        html = re.sub(
            r'(<button type="submit" class="form-submit" id="submitBtn">.*?</button>)',
            r'\1\n' + register_btn,
            html
        )

    # Add login-ui.js script reference
    if 'login-ui.js' not in html:
        html = html.replace('</body>', '    <script src="js/modules/login-ui.js"></script>\n</body>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print('Updated index.html with registerBtn and login-ui.js')

if __name__ == '__main__':
    main()
