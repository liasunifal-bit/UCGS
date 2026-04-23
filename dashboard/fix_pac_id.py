import re

def fix_pac_id():
    path = r"c:\Users\maria\Downloads\antigravity lias\dashboard\js\modules\pacientes-ui.js"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # The block we need to replace is the else block of if (pacEditingId)
    # Right now it looks like:
    #            } else {
    #                // Create
    #                patient.id = pacNextId(list);
    #                patient.prontuario = document.getElementById('pacProntuarioDisplay').textContent;
    #                patient.status = 'ativo';
    #                patient.dataCadastro = new Date().toISOString();
    #                if(window.PacientesService) { await window.PacientesService.insertPaciente(patient); await pacFetchSupabase(); }
    #                else { pacSaveState(list); }
    #                pacCloseModal();
    #                pacShowToast('Paciente cadastrado com sucesso', 'success');
    #            }
    
    pattern = r"(\} else \{\s*// Create\s*)patient\.id = pacNextId\(list\);\s*(patient\.prontuario = [^\n]+;\s*patient\.status = 'ativo';\s*patient\.dataCadastro = new Date\(\)\.toISOString\(\);\s*)if\(window\.PacientesService\) \{ await window\.PacientesService\.insertPaciente\(patient\); await pacFetchSupabase\(\); \}\s*else \{ pacSaveState\(list\); \}"
    
    replacement = r"\1\2if(window.PacientesService) { await window.PacientesService.insertPaciente(patient); await pacFetchSupabase(); }\n                else { patient.id = pacNextId(list); list.push(patient); pacSaveState(list); }"
    
    new_content = re.sub(pattern, replacement, content)
    
    # Also fix the Update block just in case it's doing something similar
    pattern_update = r"(patient\.dataCadastro = list\[idx\]\.dataCadastro;\s*)if\(window\.PacientesService\) \{ await window\.PacientesService\.updatePaciente\(patient\.id, patient\); await pacFetchSupabase\(\); \}\s*else \{ pacSaveState\(list\); \}"
    replacement_update = r"\1if(window.PacientesService) { \n                    const { id, dataCadastro, ...updateData } = patient; \n                    await window.PacientesService.updatePaciente(patient.id, updateData); \n                    await pacFetchSupabase(); \n                }\n                else { list[idx] = patient; pacSaveState(list); }"
    
    new_content = re.sub(pattern_update, replacement_update, new_content)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("Correções de ID e payload para Supabase aplicadas com sucesso.")

if __name__ == "__main__":
    fix_pac_id()
