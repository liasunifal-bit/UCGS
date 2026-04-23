$ErrorActionPreference = "Stop"

$anonKey       = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl       = "https://llqphjlpypnyvknpfdyn.supabase.co"

# IDs obtidos diretamente do banco
$procDiagDorId     = "ecba8f44-742b-47c4-8e29-a75dce2911bd"   # Dor Aguda (critica)
$procDiagRiscoId   = "9c32586a-20b8-471a-9930-324c52f1fc90"   # Risco de Infecção (media)
$nocControleId     = "3f605947-fa12-4379-b8d0-720b2b7a2723"   # NOC 1400 - Controle da Dor
$nicManejoId       = "556f6192-5383-4be3-b052-897845a1a229"   # NIC 1400 - Manejo da Dor
$nicReducaoAnsId   = "0bcfb1c5-73c0-4eac-b976-1adc2ca4cdf8"   # NIC 5820 - Reducao da Ansiedade

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

# POST - Planejamento para Dor Aguda
Write-Host ""
Write-Host "[2/4] POST - Criando planejamento para diagnostico: Dor Aguda (critica)..."

$nocIds = ConvertTo-Json @($nocControleId) -Compress
$nicIds = ConvertTo-Json @($nicManejoId, $nicReducaoAnsId) -Compress

$bodyPlan = [ordered]@{
    processo_diagnostico_id  = $procDiagDorId
    noc_ids                  = $nocIds
    meta_resultado           = "Reducao da EVA para menor ou igual a 3 em 24 horas"
    prazo_meta               = "24 horas"
    nic_ids                  = $nicIds
    descricao_intervencoes   = "Administrar analgesico conforme prescricao. Monitorar EVA a cada 2h. Posicionamento adequado."
    status                   = "em_andamento"
}

$plan1 = Invoke-RestMethod -Uri "$baseUrl/rest/v1/processo_planejamento_diagnostico" -Method Post -Headers $h -Body ($bodyPlan | ConvertTo-Json)
$planId = $plan1.id
Write-Host ">> Planejamento criado! ID: $planId"
Write-Host "   NOC: $($plan1.noc_ids) | NIC: $($plan1.nic_ids)"

# GET - Ler o planejamento
Write-Host ""
Write-Host "[3/4] GET - Lendo planejamento criado..."
$result = Invoke-RestMethod -Uri "$baseUrl/rest/v1/processo_planejamento_diagnostico?id=eq.$planId" -Method Get -Headers $h
Write-Host ">> Planejamento lido com sucesso!"
Write-Host "   Meta: $($result.meta_resultado)"
Write-Host "   Prazo: $($result.prazo_meta)"
Write-Host "   Status: $($result.status)"

# PATCH - Registrar avaliacao do planejamento
Write-Host ""
Write-Host "[4/4] PATCH - Registrando avaliacao do planejamento..."
$bodyAvalia = '{"avaliacao":"EVA reduzida para 4/10 apos 12h. Mantendo intervencoes.","data_avaliacao":"2026-04-21","status":"em_andamento"}'
$patched = Invoke-RestMethod -Uri "$baseUrl/rest/v1/processo_planejamento_diagnostico?id=eq.$planId" -Method Patch -Headers $h -Body $bodyAvalia
Write-Host ">> Avaliacao registrada! Status: $($patched.status)"
Write-Host "   Avaliacao: $($patched.avaliacao)"

Write-Host ""
Write-Host "============================================"
Write-Host "   TODOS OS TESTES PASSARAM COM SUCESSO!"
Write-Host "   processo_planejamento_diagnostico: OK  "
Write-Host "============================================"
