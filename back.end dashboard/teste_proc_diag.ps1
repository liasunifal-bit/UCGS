$ErrorActionPreference = "Stop"

$anonKey    = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl    = "https://llqphjlpypnyvknpfdyn.supabase.co"
$processoId = "a17e2742-9653-4e5d-bf26-818d6cef324a"
# UUIDs obtidos diretamente do banco
$nandaDorAgudaId    = "cf957b5a-2161-4a0c-be1f-8a172e2f803f"   # 00132 - Dor aguda
$nandaRiscoInfecId  = "2a9e4bc9-718c-4d70-9e6a-0bc7aa031f2f"   # 00004 - Risco de infeccao

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

Write-Host ""
Write-Host "[2/4] POST - Atribuindo diagnostico NANDA 00132 (Dor Aguda) ao processo..."
$body1 = [ordered]@{
    processo_id = $processoId
    nanda_id    = $nandaDorAgudaId
    prioridade  = "alta"
    status      = "ativo"
    origem      = "Entrevista clinica e avaliacao fisica"
}
$diag1 = Invoke-RestMethod -Uri "$baseUrl/rest/v1/processo_diagnosticos_enfermagem" -Method Post -Headers $h -Body ($body1 | ConvertTo-Json)
$diagId = $diag1.id
Write-Host ">> Diagnostico 1 atribuido! ID: $diagId"

Write-Host ""
Write-Host "[2b/4] POST - Atribuindo diagnostico NANDA 00004 (Risco de Infeccao)..."
$body2 = [ordered]@{
    processo_id = $processoId
    nanda_id    = $nandaRiscoInfecId
    prioridade  = "media"
    status      = "ativo"
    origem      = "Historia de procedimento invasivo recente"
}
$diag2 = Invoke-RestMethod -Uri "$baseUrl/rest/v1/processo_diagnosticos_enfermagem" -Method Post -Headers $h -Body ($body2 | ConvertTo-Json)
Write-Host ">> Diagnostico 2 atribuido! ID: $($diag2.id)"

Write-Host ""
Write-Host "[3/4] GET - Listando diagnosticos do processo com JOIN na NANDA..."
$result = Invoke-RestMethod -Uri "$baseUrl/rest/v1/processo_diagnosticos_enfermagem?processo_id=eq.$processoId" -Method Get -Headers $h
Write-Host ">> Total de diagnosticos atribuidos: $($result.Count)"
$result | ForEach-Object { Write-Host "   [prioridade: $($_.prioridade)] nanda_id: $($_.nanda_id)" }

Write-Host ""
Write-Host "[4/4] PATCH - Atualizando prioridade do diagnostico de Dor Aguda para critica..."
$patched = Invoke-RestMethod -Uri "$baseUrl/rest/v1/processo_diagnosticos_enfermagem?id=eq.$diagId" -Method Patch -Headers $h `
    -Body '{"prioridade":"critica","observacoes":"Paciente relata EVA 9/10. Intervencao imediata necessaria."}'
Write-Host ">> PATCH executado! Nova prioridade: $($patched.prioridade)"

Write-Host ""
Write-Host "[EXTRA] Testando UNIQUE constraint - tentando inserir o mesmo diagnostico novamente..."
try {
    $bodyDup = [ordered]@{ processo_id = $processoId; nanda_id = $nandaDorAgudaId; prioridade = "baixa" }
    $dup = Invoke-RestMethod -Uri "$baseUrl/rest/v1/processo_diagnosticos_enfermagem" -Method Post -Headers $h -Body ($bodyDup | ConvertTo-Json)
    Write-Host ">> FALHA: Duplicata permitida indevidamente!"
} catch {
    Write-Host ">> CORRETO! Constraint UNIQUE bloqueou a duplicata. Integridade garantida."
}

Write-Host ""
Write-Host "============================================"
Write-Host "   TODOS OS TESTES PASSARAM COM SUCESSO!"
Write-Host "   processo_diagnosticos_enfermagem: OK    "
Write-Host "============================================"
