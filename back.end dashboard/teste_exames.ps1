$ErrorActionPreference = "Stop"

$anonKey       = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl       = "https://llqphjlpypnyvknpfdyn.supabase.co"
$atendimentoId = "3bcc0bbd-1c2f-4954-b0ac-ab2b8f6ac8e1"

# PASSO 1: Login
Write-Host "[1/4] Autenticando medico2@ucgs.com..."
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

# PASSO 2: POST - Inserir exame solicitado
Write-Host ""
Write-Host "[2/4] POST - Inserindo exame solicitado..."

$bodyPost = [ordered]@{
    atendimento_id    = $atendimentoId
    nome_exame        = "Hemograma Completo"
    tipo              = "Laboratorial"
    indicacao_clinica = "Investigacao de anemia e infeccao"
    status            = "solicitado"
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/atendimento_exames" -Method Post -Headers $h -Body ($bodyPost | ConvertTo-Json)
$exameId = $inserted.id
Write-Host ">> Exame inserido! ID: $exameId"
Write-Host ($inserted | ConvertTo-Json -Depth 3)

# PASSO 3: GET - Ler exames do atendimento
Write-Host ""
Write-Host "[3/4] GET - Lendo exames do atendimento..."
$result = Invoke-RestMethod -Uri "$baseUrl/rest/v1/atendimento_exames?atendimento_id=eq.$atendimentoId" -Method Get -Headers $h
Write-Host ">> Leitura com sucesso:"
Write-Host ($result | ConvertTo-Json -Depth 4)

# PASSO 4: PATCH - Registrar resultado do exame
Write-Host ""
Write-Host "[4/4] PATCH - Registrando resultado do exame..."
$bodyPatch = '{"status":"concluido","resultado":"Hb 12.5 g/dL. Leucocitos 8.500. Plaquetas 220.000.","data_resultado":"2026-04-21"}'
$patched = Invoke-RestMethod -Uri "$baseUrl/rest/v1/atendimento_exames?id=eq.$exameId" -Method Patch -Headers $h -Body $bodyPatch
Write-Host ">> PATCH executado com sucesso!"
Write-Host ($patched | ConvertTo-Json -Depth 3)

Write-Host ""
Write-Host "========================================"
Write-Host "   TODOS OS TESTES PASSARAM COM SUCESSO!"
Write-Host "   Tabela atendimento_exames: VALIDADA  "
Write-Host "========================================"
