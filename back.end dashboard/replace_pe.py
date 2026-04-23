import sys

with open('site nevo.HTML', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

target = """        window.peFinalizar = function() {
            const confirmed = confirm('Confirmar finalizaÃ§Ã£o e salvamento completo do SAE?\\n\\nEsta aÃ§Ã£o registrarÃ¡ o Processo de Enfermagem no sistema.');
            if (!confirmed) return;
            const btn = event?.target;
            if (btn) { btn.disabled = true; btn.textContent = 'â ³ Salvando...'; }
            setTimeout(() => {
                if (btn) { btn.disabled = false; btn.textContent = 'âœ“ Finalizar e Salvar SAE'; }
                peShowToast('ðŸŽ‰ SAE finalizado e salvo com sucesso!', 'success', 3500);
                setTimeout(() => peCloseFullscreen(), 1500);
            }, 1200);
        };"""

replacement = """        window.peFinalizar = async function() {
            const confirmed = confirm('Confirmar finalizaÃ§Ã£o e salvamento completo do SAE?\\n\\nEsta aÃ§Ã£o registrarÃ¡ o Processo de Enfermagem no sistema.');
            if (!confirmed) return;
            const btn = event?.target;
            if (btn) { btn.disabled = true; btn.textContent = 'â ³ Salvando...'; }
            
            try {
                let enfId = '00000000-0000-0000-0000-000000000000';
                if (typeof SupabaseClient !== 'undefined' && SupabaseClient.auth) {
                    const user = SupabaseClient.auth.getUser();
                    if (user && user.id) enfId = user.id;
                }
                
                let pacienteId = '00000000-0000-0000-0000-000000000000';
                if (window.UCGS_SELECTED_PATIENT && window.UCGS_SELECTED_PATIENT.id && window.UCGS_SELECTED_PATIENT.id.length > 5) {
                    pacienteId = window.UCGS_SELECTED_PATIENT.id;
                }

                const payload = {
                    paciente_id: pacienteId,
                    enfermeiro_id: enfId,
                    status: 'concluido',
                    queixa_principal: document.getElementById('peQueixa')?.value || '',
                    pressao_arterial: document.getElementById('pePA')?.value || '',
                    frequencia_cardiaca: parseInt(document.getElementById('peFC')?.value) || null,
                    frequencia_respiratoria: parseInt(document.getElementById('peFR')?.value) || null,
                    temperatura_corporal: parseFloat(document.getElementById('peTemp')?.value) || null,
                    saturacao_oxigenio: parseFloat(document.getElementById('peSpo2')?.value) || null,
                    observacoes: 'Registro salvo via frontend'
                };

                if (typeof SupabaseClient !== 'undefined') {
                    await SupabaseClient.from('processos_enfermagem').insert(payload);
                }

                if (btn) { btn.disabled = false; btn.textContent = 'âœ“ Finalizar e Salvar SAE'; }
                peShowToast('ðŸŽ‰ SAE finalizado e salvo com sucesso!', 'success', 3500);
                setTimeout(() => typeof peCloseFullscreen === 'function' ? peCloseFullscreen() : null, 1500);
            } catch (err) {
                if (btn) { btn.disabled = false; btn.textContent = 'âœ“ Finalizar e Salvar SAE'; }
                peShowToast('Erro ao salvar no banco: ' + err.message, 'error', 5000);
                console.error(err);
            }
        };"""

# Sometimes newline characters differ
import re
# normalize newlines to \n
content = content.replace('\r\n', '\n')
target = target.replace('\r\n', '\n')

if target in content:
    content = content.replace(target, replacement)
    with open('site nevo.HTML', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Success")
else:
    print("Target not found. Doing regex search.")
    # Fallback to regex if whitespace is an issue
    pattern = re.compile(r"window\.peFinalizar = function\(\) \{[\s\S]*?\}, 1200\);\n\s*\};")
    match = pattern.search(content)
    if match:
        content = content[:match.start()] + replacement + content[match.end():]
        with open('site nevo.HTML', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Success via Regex")
    else:
        print("Still not found")
