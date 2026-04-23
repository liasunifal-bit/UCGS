$ErrorActionPreference = "Stop"

$anonKey     = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl     = "https://llqphjlpypnyvknpfdyn.supabase.co"
$pacienteId  = "873083bc-7652-4c68-9949-b598b8141ff0"
$psicologoId = "c767fe1e-05fb-4d92-88c2-e9c6ae3e232c"

# =============================================
Write-Host "[1/4] Autenticando medico2@ucgs.com..."
# =============================================
$login = Invoke-RestMethod -Uri "$baseUrl/auth/v1/token?grant_type=password" -Method Post `
    -Headers @{ "apikey" = $anonKey; "Content-Type" = "application/json" } `
    -Body '{"email":"medico2@ucgs.com","password":"123456"}'
$jwt = $login.access_token
Write-Host ">> JWT gerado com sucesso."

$h = @{
    "apikey"        = $anonKey
    "Authorization" = "Bearer $jwt"
    "Content-Type"  = "application/json"
    "Prefer"        = "return=representation"
}

# =============================================
Write-Host ""
Write-Host "[2/4] POST - Registrando avaliacao psicologica..."
# =============================================
$bodyPost = [ordered]@{
    paciente_id           = $pacienteId
    psicologo_id          = $psicologoId
    data_avaliacao        = "2026-04-22"
    motivo_encaminhamento = "Encaminhado pelo medico do trabalho por relato de estresse ocupacional e insonia."
    queixa_principal      = "Paciente relata ansiedade, dificuldade de concentracao e insonia ha 3 meses."
    historico_psico       = "Sem historico de tratamento psicologico anterior. Nega uso de psicofarmacos."
    historico_familiar    = "Mae com diagnostico de depressao. Pai alcoolista."
    contexto_social       = "Casado, 2 filhos. Empregado. Refere sobrecarga no trabalho."
    humor_predominante    = "ansioso"
    nivelconsciente       = "alerta"
    orientacao            = "orientado"
    instrumentos_usados   = @("Entrevista clinica", "BDI-II", "BAI", "Escala de Estresse Percebido")
    hipotese_diagnostica  = "Transtorno de Ansiedade Generalizada com sintomas depressivos secundarios"
    cid10                 = "F41.1"
    plano_terapeutico     = "TCC semanal. Psicoeducacao sobre ansiedade. Tecnicas de respiracao e mindfulness."
    numero_sessoes_prev   = 16
    "sigilo_reforçado"    = $true
    observacoes           = "Paciente receptivo ao tratamento. Boa alianca terapeutica."
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/avaliacoes_psicologicas" -Method Post `
    -Headers $h -Body ($bodyPost | ConvertTo-Json -Depth 5)
$avaliacaoId = $inserted.id
Write-Host ">> Avaliacao psicologica registrada! ID: $avaliacaoId"
Write-Host "   Humor predominante: $($inserted.humor_predominante)"
Write-Host "   Hipotese diagnostica: $($inserted.hipotese_diagnostica)"
Write-Host "   CID-10: $($inserted.cid10) | Sessoes previstas: $($inserted.numero_sessoes_prev)"

# =============================================
Write-Host ""
Write-Host "[3/4] GET - Listando avaliacoes psicologicas do paciente..."
# =============================================
$result = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/avaliacoes_psicologicas?paciente_id=eq.$pacienteId&order=data_avaliacao.desc" `
    -Method Get -Headers $h
Write-Host ">> Total de avaliacoes: $($result.Count)"
Write-Host "   Plano terapeutico: $($result[0].plano_terapeutico.Substring(0, [Math]::Min(65,$result[0].plano_terapeutico.Length)))..."

# =============================================
Write-Host ""
Write-Host "[4/4] PATCH - Atualizando plano terapeutico..."
# =============================================
$patched = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/avaliacoes_psicologicas?id=eq.$avaliacaoId" `
    -Method Patch -Headers $h `
    -Body '{"plano_terapeutico":"TCC semanal. Psicoeducacao sobre ansiedade. Tecnicas de respiracao, mindfulness e reestruturacao cognitiva. Avaliacao para psicofarmacologia em 30 dias."}'
Write-Host ">> PATCH executado!"
Write-Host "   Novo plano: $($patched.plano_terapeutico)"

Write-Host ""
Write-Host "========================================"
Write-Host " TODOS OS TESTES PASSARAM COM SUCESSO!  "
Write-Host " MODULO PSICOLOGIA: avaliacoes [1/2]    "
Write-Host "========================================"
