$ErrorActionPreference = "Stop"

$anonKey  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl  = "https://llqphjlpypnyvknpfdyn.supabase.co"
$medicoId   = "c767fe1e-05fb-4d92-88c2-e9c6ae3e232c"
$pacienteId = "873083bc-7652-4c68-9949-b598b8141ff0"

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

# PASSO 2: POST - Inserir atendimento
Write-Host ""
Write-Host "[2/4] POST - Inserindo atendimento medico..."

$bodyPost = [ordered]@{
    paciente_id             = $pacienteId
    medico_id               = $medicoId
    queixa_principal        = "Dor de cabeca intensa"
    historia_molestia_atual = "Paciente relata cefaleia ha 3 dias com nauseas."
    exame_fisico            = "PA 120x80 mmHg. FC 72 bpm."
    hipotese_diagnostica    = "Enxaqueca sem aura"
    conduta_medica          = "Prescrito Dipirona 500mg e repouso por 48h."
    status                  = "concluido"
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/atendimentos_medicos" -Method Post -Headers $h -Body ($bodyPost | ConvertTo-Json)
$atendimentoId = $inserted.id
Write-Host ">> Atendimento inserido! ID: $atendimentoId"
Write-Host ($inserted | ConvertTo-Json -Depth 3)

# PASSO 3: GET - Ler o atendimento inserido (sem JOIN para evitar problemas)
Write-Host ""
Write-Host "[3/4] GET - Lendo atendimento inserido..."
$getUrl = "$baseUrl/rest/v1/atendimentos_medicos?id=eq.$atendimentoId"
$result = Invoke-RestMethod -Uri $getUrl -Method Get -Headers $h
Write-Host ">> Leitura com sucesso:"
Write-Host ($result | ConvertTo-Json -Depth 4)

# PASSO 4: PATCH - Atualizar observacoes
Write-Host ""
Write-Host "[4/4] PATCH - Atualizando observacoes..."
$bodyPatch = '{"observacoes":"Paciente solicitou atestado medico de 2 dias."}'
$patchUrl  = "$baseUrl/rest/v1/atendimentos_medicos?id=eq.$atendimentoId"
$patched = Invoke-RestMethod -Uri $patchUrl -Method Patch -Headers $h -Body $bodyPatch
Write-Host ">> PATCH executado com sucesso!"
Write-Host ($patched | ConvertTo-Json -Depth 3)

Write-Host ""
Write-Host "========================================"
Write-Host "   TODOS OS TESTES PASSARAM COM SUCESSO!"
Write-Host "   Tabela atendimentos_medicos: VALIDADA"
Write-Host "========================================"
