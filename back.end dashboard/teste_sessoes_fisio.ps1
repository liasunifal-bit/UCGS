$ErrorActionPreference = "Stop"

$anonKey          = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl          = "https://llqphjlpypnyvknpfdyn.supabase.co"
$pacienteId       = "873083bc-7652-4c68-9949-b598b8141ff0"
$fisioterapeutaId = "c767fe1e-05fb-4d92-88c2-e9c6ae3e232c"
$avaliacaoId      = "4423a1fb-dd60-4b44-b8e4-2bf8e8d83649"

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
Write-Host "[2/4] POST - Registrando sessao de fisioterapia..."
# =============================================
$recursos = ConvertTo-Json @("TENS", "Termoterapia", "Cinesioterapia", "Liberacao miofascial") -Compress

$bodyPost = [ordered]@{
    avaliacao_id      = $avaliacaoId
    paciente_id       = $pacienteId
    fisioterapeuta_id = $fisioterapeutaId
    data_sessao       = "2026-04-22"
    numero_sessao     = 1
    duracao_min       = 50
    recursos_usados   = @("TENS", "Termoterapia", "Cinesioterapia", "Liberacao miofascial")
    evolucao_sessao   = "Paciente tolerou bem os recursos terapeuticos. Relata alivio parcial apos TENS."
    resposta_paciente = "Boa resposta. Paciente colaborativo e engajado."
    eva_pre           = 7
    eva_pos           = 4
    intercorrencias   = "Nenhuma"
    conduta_proxima   = "Manter protocolo. Iniciar pilates terapeutico na proxima sessao."
    status            = "realizada"
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/sessoes_fisioterapia" -Method Post `
    -Headers $h -Body ($bodyPost | ConvertTo-Json -Depth 5)
$sessaoId = $inserted.id
Write-Host ">> Sessao registrada! ID: $sessaoId"
Write-Host "   Sessao numero: $($inserted.numero_sessao) | Duracao: $($inserted.duracao_min) min"
Write-Host "   EVA pre-sessao: $($inserted.eva_pre)/10 | EVA pos-sessao: $($inserted.eva_pos)/10"
Write-Host "   Status: $($inserted.status)"

# =============================================
Write-Host ""
Write-Host "[3/4] GET - Listando sessoes do paciente..."
# =============================================
$result = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/sessoes_fisioterapia?avaliacao_id=eq.$avaliacaoId&order=numero_sessao.asc" `
    -Method Get -Headers $h
Write-Host ">> Total de sessoes registradas: $($result.Count)"
Write-Host "   Ultima sessao: #$($result[0].numero_sessao) em $($result[0].data_sessao)"
Write-Host "   Evolucao EVA: $($result[0].eva_pre)/10 → $($result[0].eva_pos)/10"

# =============================================
Write-Host ""
Write-Host "[4/4] PATCH - Atualizando conduta da proxima sessao..."
# =============================================
$patched = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/sessoes_fisioterapia?id=eq.$sessaoId" `
    -Method Patch -Headers $h `
    -Body '{"conduta_proxima":"Iniciar pilates terapeutico. Progredir carga na cinesioterapia. Reavaliar EVA no inicio."}'
Write-Host ">> PATCH executado!"
Write-Host "   Proxima conduta: $($patched.conduta_proxima)"

Write-Host ""
Write-Host "========================================"
Write-Host " TODOS OS TESTES PASSARAM COM SUCESSO!  "
Write-Host " MODULO FISIOTERAPIA: CONCLUIDO [5/5]   "
Write-Host "========================================"
