import re

def main():
    path = r'c:\Users\maria\Downloads\antigravity lias\dashboard\index.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the submitBtn block and append the registerBtn
    register_btn = '\n                    <button type="button" class="form-submit" id="registerBtn" style="background: var(--brand-blue); margin-top: 10px;">\n                        <span class="form-submit-label">Registrar Nova Conta</span>\n                    </button>'

    if 'id="registerBtn"' not in html:
        # Use DOTALL so .*? matches newlines inside the button tag
        html = re.sub(
            r'(<button type="submit" class="form-submit" id="submitBtn">.*?</button>)',
            r'\1' + register_btn,
            html,
            flags=re.DOTALL
        )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print('Fixed index.html with registerBtn')

if __name__ == '__main__':
    main()
