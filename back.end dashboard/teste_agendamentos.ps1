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

# PASSO 2: POST - Inserir agendamento de retorno
Write-Host ""
Write-Host "[2/4] POST - Inserindo agendamento de retorno..."

$bodyPost = [ordered]@{
    atendimento_id  = $atendimentoId
    tipo            = "retorno"
    especialidade   = "Clinica Geral"
    data_agendamento= "2026-05-05T09:00:00+00:00"
    motivo          = "Retorno para avaliacao pos-tratamento de cefaleia"
    status          = "pendente"
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/atendimento_agendamentos" -Method Post -Headers $h -Body ($bodyPost | ConvertTo-Json)
$agendId = $inserted.id
Write-Host ">> Agendamento inserido! ID: $agendId"
Write-Host ($inserted | ConvertTo-Json -Depth 3)

# PASSO 3: GET - Ler agendamentos do atendimento
Write-Host ""
Write-Host "[3/4] GET - Lendo agendamentos do atendimento..."
$result = Invoke-RestMethod -Uri "$baseUrl/rest/v1/atendimento_agendamentos?atendimento_id=eq.$atendimentoId" -Method Get -Headers $h
Write-Host ">> Leitura com sucesso:"
Write-Host ($result | ConvertTo-Json -Depth 4)

# PASSO 4: PATCH - Confirmar o agendamento
Write-Host ""
Write-Host "[4/4] PATCH - Confirmando agendamento..."
$bodyPatch = '{"status":"confirmado","observacoes":"Paciente confirmou presenca por telefone."}'
$patched = Invoke-RestMethod -Uri "$baseUrl/rest/v1/atendimento_agendamentos?id=eq.$agendId" -Method Patch -Headers $h -Body $bodyPatch
Write-Host ">> PATCH executado com sucesso!"
Write-Host ($patched | ConvertTo-Json -Depth 3)

Write-Host ""
Write-Host "========================================"
Write-Host "   TODOS OS TESTES PASSARAM COM SUCESSO!"
Write-Host "   Tabela atendimento_agendamentos: OK  "
Write-Host "========================================"
