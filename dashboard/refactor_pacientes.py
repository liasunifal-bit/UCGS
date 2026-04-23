import re

def refactor_pacientes():
    path = r"c:\Users\maria\Downloads\antigravity lias\dashboard\js\modules\pacientes-ui.js"
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Replace pacLoadState and pacSaveState
    content = re.sub(
        r"function pacLoadState\(\) \{[\s\S]*?\} catch\(e\) \{ return \[\]; \}\n\s*\}",
        "window.pacStateArray = [];\n        function pacLoadState() {\n            return window.pacStateArray || [];\n        }",
        content
    )
    
    content = re.sub(
        r"function pacSaveState\(list\) \{[\s\S]*?\}",
        "function pacSaveState(list) {\n            window.pacStateArray = list;\n        }",
        content
    )

    # 2. Add pacFetchSupabase and rewrite pacInitDemo
    new_init = """async function pacFetchSupabase() {
            if (window.PacientesService) {
                try {
                    window.pacStateArray = await window.PacientesService.getPacientes();
                } catch (e) { console.error('Erro Supabase', e); }
            }
            return window.pacStateArray;
        }

        async function pacInitDemo() {
            await pacFetchSupabase();
            pacRenderTable();
        }"""
    
    content = re.sub(
        r"function pacInitDemo\(\) \{[\s\S]*?return demo;\n\s*\}",
        new_init,
        content
    )

    # 3. Refactor window.pacSave to be async and call Supabase
    save_func_pattern = r"window\.pacSave = function\(\) \{([\s\S]*?)(pacRenderTable\(\);\n\s*\};)"
    
    def replacer_save(match):
        body = match.group(1)
        tail = match.group(2)
        
        # Replace the update branch
        body = re.sub(
            r"(list\[idx\] = patient;\n\s*\})([\s\S]*?)(pacSaveState\(list\);)",
            r"\1\n                if(window.PacientesService) { await window.PacientesService.updatePaciente(patient.id, patient); await pacFetchSupabase(); }\n                else { pacSaveState(list); }",
            body
        )
        # Replace the insert branch
        body = re.sub(
            r"(list\.push\(patient\);\n\s*)(pacSaveState\(list\);)",
            r"\1if(window.PacientesService) { await window.PacientesService.insertPaciente(patient); await pacFetchSupabase(); }\n                else { pacSaveState(list); }",
            body
        )
        return f"window.pacSave = async function() {{{body}{tail}"
    
    content = re.sub(save_func_pattern, replacer_save, content)

    # 4. Refactor window.pacToggleStatus to be async
    toggle_pattern = r"window\.pacToggleStatus = function\(id\) \{([\s\S]*?)(pacSaveState\(list\);)([\s\S]*?\};)"
    
    def replacer_toggle(match):
        body = match.group(1)
        tail = match.group(3)
        return f"window.pacToggleStatus = async function(id) {{{body}if(window.PacientesService) {{ await window.PacientesService.updatePaciente(p.id, {{ status: p.status }}); await pacFetchSupabase(); }} else {{ pacSaveState(list); }}{tail}"
        
    content = re.sub(toggle_pattern, replacer_toggle, content)

    # 5. Fix initialization calls at the bottom of the Pacientes module
    content = re.sub(
        r"pacInitDemo\(\);\n\s*pacRenderTable\(\);",
        "pacInitDemo();",
        content
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Refatoração do módulo pacientes-ui.js concluída!")

if __name__ == "__main__":
    refactor_pacientes()
