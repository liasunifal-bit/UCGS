$ErrorActionPreference = "Stop"

$anonKey         = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl         = "https://llqphjlpypnyvknpfdyn.supabase.co"
$pacienteId      = "873083bc-7652-4c68-9949-b598b8141ff0"
$nutricionistaId = "c767fe1e-05fb-4d92-88c2-e9c6ae3e232c"
$planoId         = "3c127c28-f07a-424a-bdf8-650775dced8d"

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
Write-Host "[2/4] POST - Registrando acompanhamento de retorno..."
# =============================================
$bodyPost = [ordered]@{
    paciente_id      = $pacienteId
    nutricionista_id = $nutricionistaId
    plano_id         = $planoId
    data_consulta    = "2026-04-22"
    peso_atual_kg    = 74.2
    imc_atual        = 24.22
    classificacao_imc = "Eutrofia"
    adesao_plano     = "boa"
    queixas_paciente = "Refere dificuldade para tomar cafe da manha cedo."
    evolucao_clinica = "Perda de 1,3kg desde o inicio do plano. Boa evolucao."
    conduta          = "Manter plano atual com ajuste no horario do cafe da manha."
    ajuste_plano     = $false
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/acompanhamentos_nutricionais" -Method Post `
    -Headers $h -Body ($bodyPost | ConvertTo-Json -Depth 5)
$acompId = $inserted.id
Write-Host ">> Acompanhamento registrado! ID: $acompId"
Write-Host "   Peso atual: $($inserted.peso_atual_kg) kg | IMC: $($inserted.imc_atual)"
Write-Host "   Adesao ao plano: $($inserted.adesao_plano)"

# =============================================
Write-Host ""
Write-Host "[3/4] GET - Listando acompanhamentos do paciente..."
# =============================================
$result = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/acompanhamentos_nutricionais?paciente_id=eq.$pacienteId&order=data_consulta.desc" `
    -Method Get -Headers $h
Write-Host ">> Total de acompanhamentos encontrados: $($result.Count)"
Write-Host "   Ultima consulta: $($result[0].data_consulta)"
Write-Host "   Evolucao: $($result[0].evolucao_clinica)"

# =============================================
Write-Host ""
Write-Host "[4/4] PATCH - Registrando ajuste no plano..."
# =============================================
$patched = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/acompanhamentos_nutricionais?id=eq.$acompId" `
    -Method Patch -Headers $h `
    -Body '{"conduta":"Manter plano com ajuste no horario. Incluir lanche da manha.","ajuste_plano":true}'
Write-Host ">> PATCH executado! Ajuste no plano: $($patched.ajuste_plano)"
Write-Host "   Nova conduta: $($patched.conduta)"

Write-Host ""
Write-Host "========================================"
Write-Host " TODOS OS TESTES PASSARAM COM SUCESSO!  "
Write-Host " CAMADA NUTRICIONAL: acompanhamentos    "
Write-Host "========================================"
