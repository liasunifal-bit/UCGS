import re
import os

def extract_modules():
    path = r"c:\Users\maria\Downloads\antigravity lias\dashboard\index.html"
    modules_dir = r"c:\Users\maria\Downloads\antigravity lias\dashboard\js\modules"
    
    os.makedirs(modules_dir, exist_ok=True)
    
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Find all script tags
    # Using a robust regex to find <script> ... </script> taking care of attributes
    # The non-greedy .*? works but we might need to handle newlines
    script_pattern = re.compile(r'(<script[^>]*>)(.*?)(</script>)', re.DOTALL | re.IGNORECASE)
    
    def replacer(match):
        open_tag = match.group(1)
        content = match.group(2)
        close_tag = match.group(3)
        
        # Don't extract scripts that already have a src attribute
        if 'src=' in open_tag.lower():
            return match.group(0)
            
        # Determine module name based on content
        module_name = None
        
        # Checking for common headers or function names to identify modules
        if 'HISTÓRICO DE EVENTOS' in content or 'histRenderTimeline' in content:
            module_name = 'historico-eventos.js'
        elif 'UTILITÁRIOS DE SEGURANÇA' in content or 'renderNotifications' in content:
            module_name = 'utilitarios-seguranca.js'
        elif 'ATENDIMENTO MÉDICO' in content or 'amInit' in content:
            module_name = 'atendimento-medico.js'
        elif 'pacLoadState' in content or 'pacRenderTable' in content:
            module_name = 'pacientes-ui.js'
        elif 'prtRenderTimeline' in content or 'prtSaveForm' in content:
            module_name = 'prontuario-ui.js'
        elif 'FISIOTERAPIA' in content or 'fisioRenderTable' in content:
            module_name = 'fisioterapia-ui.js'
        elif 'ODONTOLOGIA' in content or 'odontoRenderTable' in content:
            module_name = 'odontologia-ui.js'
        elif 'Chart.js' in content or 'var chartMap' in content:
            module_name = 'dashboard-charts.js'
            
        # If the script is large and we identified a module name
        if module_name and len(content.strip()) > 500:
            module_path = os.path.join(modules_dir, module_name)
            
            # Write the content to the new file
            with open(module_path, 'w', encoding='utf-8') as mf:
                mf.write(content.strip())
                
            print(f"Extracted: {module_name} ({len(content)} bytes)")
            
            # Replace the script block with a src reference
            # Note: preserving the original attributes (like type="module" if present)
            # but removing inner content.
            # We add a trailing comment to help with debugging
            new_script = f'{open_tag}</script>\n<!-- Extracted to js/modules/{module_name} -->'
            # Insert src attribute before the closing bracket of open_tag
            # E.g. <script type="module"> -> <script type="module" src="js/modules/module_name">
            if open_tag.endswith('/>'):
                new_open = open_tag[:-2] + f' src="js/modules/{module_name}" />'
            else:
                new_open = open_tag[:-1] + f' src="js/modules/{module_name}">'
                
            return f'{new_open}</script>'
            
        return match.group(0)

    # Perform substitution
    new_html = script_pattern.sub(replacer, html)
    
    # Save the updated HTML
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)
        
    print("Extraction and cleanup completed.")

if __name__ == "__main__":
    extract_modules()
