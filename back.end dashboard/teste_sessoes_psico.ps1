$ErrorActionPreference = "Stop"

$anonKey     = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl     = "https://llqphjlpypnyvknpfdyn.supabase.co"
$pacienteId  = "873083bc-7652-4c68-9949-b598b8141ff0"
$psicologoId = "c767fe1e-05fb-4d92-88c2-e9c6ae3e232c"
$avaliacaoId = "db8db045-a06d-4e5b-9086-74e14e5e3ea9"

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
Write-Host "[2/4] POST - Registrando sessao psicologica..."
# =============================================
$bodyPost = [ordered]@{
    avaliacao_id     = $avaliacaoId
    paciente_id      = $pacienteId
    psicologo_id     = $psicologoId
    data_sessao      = "2026-04-22"
    numero_sessao    = 1
    duracao_min      = 50
    abordagem        = "Terapia Cognitivo-Comportamental (TCC)"
    temas_trabalhados = "Psicoeducacao sobre ansiedade. Identificacao de pensamentos automaticos negativos."
    evolucao_clinica = "Paciente demonstrou boa compreensao do modelo cognitivo. Identificou 3 situacoes gatilho principais."
    tecnicas_usadas  = @("Psicoeducacao", "Registro de pensamentos", "Respiracao diafragmatica")
    humor_sessao     = "ansioso"
    engajamento      = "bom"
    intercorrencias  = "Nenhuma"
    plano_proxima    = "Trabalhar reestruturacao cognitiva dos pensamentos identificados. Tarefa de casa: registro diario de pensamentos."
    status           = "realizada"
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/sessoes_psicologicas" -Method Post `
    -Headers $h -Body ($bodyPost | ConvertTo-Json -Depth 5)
$sessaoId = $inserted.id
Write-Host ">> Sessao registrada! ID: $sessaoId"
Write-Host "   Sessao numero: $($inserted.numero_sessao) | Duracao: $($inserted.duracao_min) min"
Write-Host "   Humor: $($inserted.humor_sessao) | Engajamento: $($inserted.engajamento)"
Write-Host "   Status: $($inserted.status)"

# =============================================
Write-Host ""
Write-Host "[3/4] GET - Listando sessoes do paciente..."
# =============================================
$result = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/sessoes_psicologicas?avaliacao_id=eq.$avaliacaoId&order=numero_sessao.asc" `
    -Method Get -Headers $h
Write-Host ">> Total de sessoes registradas: $($result.Count)"
Write-Host "   Sessao #$($result[0].numero_sessao) | Abordagem: $($result[0].abordagem)"
Write-Host "   Evolucao: $($result[0].evolucao_clinica.Substring(0,[Math]::Min(65,$result[0].evolucao_clinica.Length)))..."

# =============================================
Write-Host ""
Write-Host "[4/4] PATCH - Atualizando plano da proxima sessao..."
# =============================================
$patched = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/sessoes_psicologicas?id=eq.$sessaoId" `
    -Method Patch -Headers $h `
    -Body '{"plano_proxima":"Reestruturacao cognitiva dos pensamentos catastróficos. Revisar tarefa de casa. Introducao ao treino de relaxamento muscular progressivo."}'
Write-Host ">> PATCH executado!"
Write-Host "   Plano proxima sessao: $($patched.plano_proxima)"

Write-Host ""
Write-Host "========================================"
Write-Host " TODOS OS TESTES PASSARAM COM SUCESSO!  "
Write-Host " MODULO PSICOLOGIA: CONCLUIDO [2/2]     "
Write-Host "========================================"
