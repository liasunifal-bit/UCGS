$ErrorActionPreference = "Stop"

$anonKey       = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl       = "https://llqphjlpypnyvknpfdyn.supabase.co"
$atendimentoId = "3bcc0bbd-1c2f-4954-b0ac-ab2b8f6ac8e1"

# PASSO 1: Login
Write-Host "[1/4] Autenticando medico2@ucgs.com..."
$loginBody = '{"email":"medico2@ucgs.com","password":"123456"}'
$loginHeaders = @{ "apikey" = $anonKey; "Content-Type" = "application/json" }
$login = Invoke-RestMethod -Uri "$baseUrl/auth/v1/token?grant_type=password" -Method Post -Headers $loginHeaders -Body $loginBody
$jwt = $login.access_token
Write-Host ">> JWT gerado com sucesso."

$h = @{
    "apikey"        = $anonKey
    "Authorization" = "Bearer $jwt"
    "Content-Type"  = "application/json"
    "Prefer"        = "return=representation"
}

# PASSO 2: POST - Inserir medicamento
Write-Host ""
Write-Host "[2/4] POST - Inserindo medicamento prescrito..."

$bodyPost = [ordered]@{
    atendimento_id = $atendimentoId
    medicamento    = "Dipirona Sodica"
    dosagem        = "500mg"
    via            = "Oral"
    frequencia     = "8 em 8 horas"
    duracao        = "5 dias"
    observacoes    = "Tomar apos as refeicoes"
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/atendimento_medicamentos" -Method Post -Headers $h -Body ($bodyPost | ConvertTo-Json)
$medId = $inserted.id
Write-Host ">> Medicamento inserido! ID: $medId"
Write-Host ($inserted | ConvertTo-Json -Depth 3)

# PASSO 3: GET - Ler os medicamentos do atendimento
Write-Host ""
Write-Host "[3/4] GET - Lendo medicamentos do atendimento..."
$getUrl = "$baseUrl/rest/v1/atendimento_medicamentos?atendimento_id=eq.$atendimentoId"
$result = Invoke-RestMethod -Uri $getUrl -Method Get -Headers $h
Write-Host ">> Leitura com sucesso:"
Write-Host ($result | ConvertTo-Json -Depth 4)

# PASSO 4: PATCH - Atualizar dosagem
Write-Host ""
Write-Host "[4/4] PATCH - Atualizando dosagem do medicamento..."
$bodyPatch = '{"dosagem":"1g","observacoes":"Dose aumentada por orientacao medica."}'
$patchUrl  = "$baseUrl/rest/v1/atendimento_medicamentos?id=eq.$medId"
$patched = Invoke-RestMethod -Uri $patchUrl -Method Patch -Headers $h -Body $bodyPatch
Write-Host ">> PATCH executado com sucesso!"
Write-Host ($patched | ConvertTo-Json -Depth 3)

Write-Host ""
Write-Host "========================================"
Write-Host "   TODOS OS TESTES PASSARAM COM SUCESSO!"
Write-Host "   Tabela atendimento_medicamentos: OK  "
Write-Host "========================================"
