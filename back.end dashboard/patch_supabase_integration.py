# -*- coding: utf-8 -*-
"""
Patch: Integrar o formulário 'Novo Mapa de Risco' com o Supabase.
Substitui o handler 'Save' local por um que faz POST na tabela
mapas_risco_ocupacional via SupabaseClient.
"""

import os

filepath = r"c:\Users\maria\Downloads\antigravity lias\back.end dashboard\site nevo.HTML"

with open(filepath, 'rb') as f:
    data = f.read()

# Marcador de início: a linha do addEventListener do Save
old_start = b"btnSave.addEventListener('click', function() {"
# Marcador de fim: o fechamento do handler seguido por reset
old_end = b"showToast('Mapa de risco cadastrado com sucesso!', 'success');\r\n            }\r\n        });"

start_idx = data.find(old_start)
end_idx = data.find(old_end)

if start_idx == -1:
    print("ERRO: Nao encontrou o inicio do handler Save")
    exit(1)
if end_idx == -1:
    print("ERRO: Nao encontrou o fim do handler Save")
    exit(1)

end_idx += len(old_end)

print(f"Encontrado handler Save: bytes {start_idx} a {end_idx}")
print(f"Tamanho do bloco a substituir: {end_idx - start_idx} bytes")

new_handler = b"""btnSave.addEventListener('click', async function() {
            if (btnSave.disabled) return;

            const setor = inputSetor.value.trim();
            const tipo  = selectTipo.value;
            const nivel = selectNivel.value;

            // --- Mapeamento frontend -> banco de dados ---
            const tipoDbMap = {
                'Biol\\u00f3gico':'biologico','F\\u00edsico':'fisico','Qu\\u00edmico':'quimico',
                'Ergon\\u00f4mico':'ergonomico','Acidentes':'acidentes',
                'Qu\\u00edmico / Ergon\\u00f4mico':'quimico','Acidentes / F\\u00edsico':'fisico'
            };
            const nivelDbMap = {
                'Baixo':'baixo','M\\u00e9dio':'medio','Alto':'alto','Cr\\u00edtico':'critico'
            };

            // Feedback visual: loading
            const originalText = btnSave.textContent;
            btnSave.disabled = true;
            btnSave.textContent = 'Salvando...';
            btnSave.style.opacity = '0.7';

            try {
                // Obter user logado
                const user = SupabaseClient.auth.getUser();
                const userId = user ? user.id : null;

                const payload = {
                    setor: setor,
                    tipo_risco: tipoDbMap[tipo] || 'biologico',
                    nivel_risco: nivelDbMap[nivel] || 'medio',
                    agente_nocivo: tipo + ' - ' + setor,
                    fonte_geradora: 'Ambiente de trabalho - ' + setor,
                    populacao_exposta: 'Colaboradores do ' + setor,
                    medidas_controle: 'Avaliacao inicial. Medidas a serem definidas.',
                    status: 'ativo'
                };
                if (userId) payload.registrado_por = userId;

                const result = await SupabaseClient.from('mapas_risco_ocupacional').insert(payload);

                // --- Sucesso: atualizar DOM ---
                const today = new Date();
                const dateStr = today.toLocaleDateString('pt-BR');
                const nextDate = new Date(today);
                nextDate.setMonth(nextDate.getMonth() + 6);
                const nextStr = nextDate.toLocaleDateString('pt-BR');

                const nivelClass = nivel === 'Cr\\u00edtico' ? 'badge-danger' :
                                   nivel === 'Alto' ? 'badge-warning' :
                                   nivel === 'M\\u00e9dio' ? 'badge-info' : 'badge-success';

                const tbody = document.querySelector('#mapas-risco table tbody');
                const tr = document.createElement('tr');
                tr.style.animation = 'sectionFadeSlideIn 0.4s ease both';
                const dbId = Array.isArray(result) && result[0] ? result[0].id : (result.id || '');
                tr.setAttribute('data-db-id', dbId);
                tr.innerHTML =
                    '<td><strong>' + setor + '</strong></td>' +
                    '<td>' + tipo + '</td>' +
                    '<td><span class="badge ' + nivelClass + '">' + nivel + '</span></td>' +
                    '<td>' + dateStr + '</td>' +
                    '<td>' + nextStr + '</td>' +
                    '<td><span class="badge badge-success">Em Dia</span></td>' +
                    '<td>' +
                        '<div class="riskmap-action-row">' +
                            '<button class="btn-view-map btn-ripple"' +
                                ' data-sector="' + setor + '"' +
                                ' data-type="' + tipo + '"' +
                                ' data-level="' + nivel + '"' +
                                ' data-status="Em Dia"' +
                                ' data-revision="' + dateStr + '"' +
                                ' data-next="' + nextStr + '"' +
                                ' data-image=""' +
                                ' onclick="openRiskmapModal(this, \\\\'visualizar\\\\')">' +
                                '&#128506;&#65039; Visualizar' +
                            '</button>' +
                        '</div>' +
                    '</td>';

                tbody.appendChild(tr);
                closeModal();

                if (typeof showToast === 'function') {
                    showToast('Mapa de risco salvo no banco de dados!', 'success');
                }
                console.log('[SUPABASE] POST mapas_risco_ocupacional - ID:', dbId);

            } catch (error) {
                console.error('[SUPABASE] Erro ao salvar mapa de risco:', error.message);
                if (typeof showToast === 'function') {
                    showToast('Erro ao salvar: ' + error.message, 'error');
                } else {
                    alert('Erro ao salvar no banco: ' + error.message);
                }
            } finally {
                btnSave.textContent = originalText;
                btnSave.disabled = false;
                btnSave.style.opacity = '';
                validateForm();
            }
        });"""

data_new = data[:start_idx] + new_handler + data[end_idx:]

with open(filepath, 'wb') as f:
    f.write(data_new)

print(f"SUCESSO! Patch aplicado. Arquivo atualizado.")
print(f"Bytes originais: {len(data)}")
print(f"Bytes novos: {len(data_new)}")
