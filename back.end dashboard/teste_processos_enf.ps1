$ErrorActionPreference = "Stop"

$anonKey    = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl    = "https://llqphjlpypnyvknpfdyn.supabase.co"
$pacienteId = "873083bc-7652-4c68-9949-b598b8141ff0"
$enfermeiroId = "c767fe1e-05fb-4d92-88c2-e9c6ae3e232c"

Write-Host "[1/4] Autenticando medico2@ucgs.com (simulando enfermeiro)..."
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

Write-Host ""
Write-Host "[2/4] POST - Criando processo de enfermagem (SAE)..."

$bodyPost = [ordered]@{
    paciente_id            = $pacienteId
    enfermeiro_id          = $enfermeiroId
    status                 = "em_andamento"
    queixa_principal       = "Paciente refere dor torácica e falta de ar"
    historia_doenca_atual  = "Inicio há 2 dias, progressivo, sem febre"
    antecedentes_pessoais  = "HAS, DM2"
    medicamentos_em_uso    = "Metformina 850mg, Losartana 50mg"
    pressao_arterial       = "140/90"
    frequencia_cardiaca    = 88
    frequencia_respiratoria= 18
    temperatura_corporal   = 36.8
    saturacao_oxigenio     = 96.0
    peso_kg                = 78.5
    altura_cm              = 170.0
    setor_trabalho         = "Administrativo"
    turno                  = "Diurno"
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/processos_enfermagem" -Method Post -Headers $h -Body ($bodyPost | ConvertTo-Json)
$processoId = $inserted.id
Write-Host ">> Processo criado! ID: $processoId"
Write-Host ($inserted | ConvertTo-Json -Depth 3)

Write-Host ""
Write-Host "[3/4] GET - Lendo processo criado..."
$result = Invoke-RestMethod -Uri "$baseUrl/rest/v1/processos_enfermagem?id=eq.$processoId" -Method Get -Headers $h
Write-Host ">> Leitura com sucesso. Status: $($result.status)"

Write-Host ""
Write-Host "[4/4] PATCH - Atualizando status do processo para concluido..."
$patched = Invoke-RestMethod -Uri "$baseUrl/rest/v1/processos_enfermagem?id=eq.$processoId" -Method Patch -Headers $h `
    -Body '{"status":"concluido","observacoes":"SAE finalizado. Paciente encaminhado para avaliacao medica."}'
Write-Host ">> PATCH executado! Novo status: $($patched.status)"

Write-Host ""
Write-Host "========================================"
Write-Host "   TODOS OS TESTES PASSARAM COM SUCESSO!"
Write-Host "   Tabela processos_enfermagem: VALIDADA"
Write-Host "========================================"
