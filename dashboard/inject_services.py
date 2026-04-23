import re

def main():
    path = r"c:\Users\maria\Downloads\antigravity lias\dashboard\index.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # We inject the module imports at the top of the authentication script or before it.
    # We can inject a new script tag right before the auth script.
    injection = """
<script type="module">
    import { PacientesService } from './js/pacientes-service.js';
    import { ProntuarioService } from './js/prontuario-service.js';
    window.PacientesService = PacientesService;
    window.ProntuarioService = ProntuarioService;
</script>
"""
    if "window.PacientesService" not in html:
        html = html.replace('<!-- SCRIPT DE AUTENTICAÇÃO UCGS — JWT SUPABASE -->', injection + '\n<!-- SCRIPT DE AUTENTICAÇÃO UCGS — JWT SUPABASE -->')

    # We need to inform the user that fully refactoring a 4.5MB monolithic file 
    # to be fully asynchronous is highly complex and risky to do via regex.
    # Instead of blindly replacing, we will output the file.

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print("Dependencies injected.")

if __name__ == "__main__":
    main()
