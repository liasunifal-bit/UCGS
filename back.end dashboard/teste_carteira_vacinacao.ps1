$ErrorActionPreference = "Stop"

$anonKey      = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl      = "https://llqphjlpypnyvknpfdyn.supabase.co"
$pacienteId   = "873083bc-7652-4c68-9949-b598b8141ff0"
$registradoPor = "c767fe1e-05fb-4d92-88c2-e9c6ae3e232c"

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
Write-Host "[2/4] POST - Registrando vacina na carteira..."
# =============================================
$bodyPost = [ordered]@{
    paciente_id       = $pacienteId
    registrado_por    = $registradoPor
    nome_vacina       = "Influenza (Gripe)"
    fabricante        = "Sanofi Pasteur"
    lote              = "AH2026-043B"
    dose              = "reforco_anual"
    data_aplicacao    = "2026-04-22"
    data_proxima_dose = "2027-04-01"
    via_administracao = "intramuscular"
    local_aplicacao   = "Deltóide direito"
    aplicador         = "Enf. Silva"
    unidade_saude     = "UCGS - Ambulatorio Central"
    reacao_adversa    = $false
    observacoes       = "Aplicacao sem intercorrencias. Paciente aguardou 30 min de observacao."
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/carteira_vacinacao" -Method Post `
    -Headers $h -Body ($bodyPost | ConvertTo-Json -Depth 5)
$vacinaId = $inserted.id
Write-Host ">> Vacina registrada! ID: $vacinaId"
Write-Host "   Vacina: $($inserted.nome_vacina) | Dose: $($inserted.dose)"
Write-Host "   Lote: $($inserted.lote) | Via: $($inserted.via_administracao)"
Write-Host "   Proxima dose: $($inserted.data_proxima_dose)"

# =============================================
Write-Host ""
Write-Host "[3/4] GET - Listando carteira de vacinacao do paciente..."
# =============================================
$result = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/carteira_vacinacao?paciente_id=eq.$pacienteId&order=data_aplicacao.desc" `
    -Method Get -Headers $h
Write-Host ">> Total de vacinas registradas: $($result.Count)"
Write-Host "   Ultima vacina: $($result[0].nome_vacina) em $($result[0].data_aplicacao)"
Write-Host "   Reacao adversa: $($result[0].reacao_adversa)"

# =============================================
Write-Host ""
Write-Host "[4/4] PATCH - Registrando reacao adversa leve..."
# =============================================
$patched = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/carteira_vacinacao?id=eq.$vacinaId" `
    -Method Patch -Headers $h `
    -Body '{"reacao_adversa":true,"descricao_reacao":"Dor local e eritema no local da aplicacao por 24h. Resolveu espontaneamente."}'
Write-Host ">> PATCH executado! Reacao adversa: $($patched.reacao_adversa)"
Write-Host "   Descricao: $($patched.descricao_reacao)"

Write-Host ""
Write-Host "========================================"
Write-Host " TODOS OS TESTES PASSARAM COM SUCESSO!  "
Write-Host " MODULO VACINAS: carteira [1/1]          "
Write-Host "========================================"
