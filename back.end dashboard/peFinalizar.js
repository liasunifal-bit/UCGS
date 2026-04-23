window.peFinalizar = async function() {
            const confirmed = confirm('Confirmar finalização e salvamento completo do SAE?\n\nEsta ação registrará o Processo de Enfermagem no sistema.');
            if (!confirmed) return;
            const btn = event?.target;
            if (btn) { btn.disabled = true; btn.textContent = '� � Salvando...'; }
            
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