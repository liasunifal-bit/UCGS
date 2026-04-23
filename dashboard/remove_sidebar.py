import re

def main():
    index_path = r"c:\Users\maria\Downloads\antigravity lias\dashboard\index.html"
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Change .login-shell CSS
    html = re.sub(
        r'\.login-shell\s*\{[^}]+\}',
        ".login-shell {\n            display: flex;\n            align-items: center;\n            justify-content: center;\n            min-height: 100vh;\n            background: var(--surface-alt);\n            padding: 24px;\n        }",
        html
    )

    # Change .form-panel CSS
    html = re.sub(
        r'\.form-panel\s*\{[^}]+\}',
        ".form-panel {\n            display: flex;\n            align-items: center;\n            justify-content: center;\n            padding: 48px;\n            background: var(--surface);\n            position: relative;\n            border-radius: var(--radius-lg);\n            box-shadow: var(--shadow-elevated);\n            width: 100%;\n            max-width: 480px;\n        }",
        html
    )

    # Change .form-brand-mobile CSS
    html = re.sub(
        r'\.form-brand-mobile\s*\{[^}]+\}',
        ".form-brand-mobile {\n            display: flex;\n            flex-direction: column;\n            align-items: center;\n            gap: 12px;\n            margin-bottom: 32px;\n        }",
        html
    )

    # Remove the <aside class="brand-panel"> block
    html = re.sub(
        r'<aside class="brand-panel".*?</aside>',
        "",
        html,
        flags=re.DOTALL
    )

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    print("Sidebar removed and layout centered.")

if __name__ == "__main__":
    main()
