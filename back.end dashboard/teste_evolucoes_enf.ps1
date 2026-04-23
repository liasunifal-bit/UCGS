$ErrorActionPreference = "Stop"

$anonKey      = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl      = "https://llqphjlpypnyvknpfdyn.supabase.co"
$processoId   = "a17e2742-9653-4e5d-bf26-818d6cef324a"
$enfermeiroId = "c767fe1e-05fb-4d92-88c2-e9c6ae3e232c"
$diagDorId    = "ecba8f44-742b-47c4-8e29-a75dce2911bd"

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

# POST - Registrar evolução SOAP
Write-Host ""
Write-Host "[2/4] POST - Registrando evolucao SOAP de enfermagem..."

$diagIds = ConvertTo-Json @($diagDorId) -Compress
$tags    = ConvertTo-Json @("urgente", "monitorar-dor", "analgesia") -Compress

$bodyPost = [ordered]@{
    processo_id      = $processoId
    enfermeiro_id    = $enfermeiroId
    subjetivo        = "Paciente refere melhora parcial da dor. EVA atual 5/10. Relata dificuldade para dormir."
    objetivo         = "PA 138/88 mmHg. FC 84 bpm. SpO2 97%. Expressao de dor ao movimento."
    avaliacao        = "Dor aguda parcialmente controlada. Analgesia em curso com resposta moderada."
    plano            = "Manter analgesia prescrita. Reavaliar EVA em 2h. Orientar posicionamento antalgico."
    diagnosticos_ids = $diagIds
    tags             = $tags
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/evolucoes_enfermagem" -Method Post -Headers $h -Body ($bodyPost | ConvertTo-Json)
$evolId = $inserted.id
Write-Host ">> Evolucao registrada! ID: $evolId"
Write-Host "   Tags: $($inserted.tags)"
Write-Host "   Diagnosticos referenciados: $($inserted.diagnosticos_ids)"

# GET - Listar evoluções do processo
Write-Host ""
Write-Host "[3/4] GET - Listando evolucoes do processo..."
$result = Invoke-RestMethod -Uri "$baseUrl/rest/v1/evolucoes_enfermagem?processo_id=eq.$processoId" -Method Get -Headers $h
Write-Host ">> Total de evolucoes: $($result.Count)"
Write-Host "   Subjetivo: $($result.subjetivo.Substring(0, [Math]::Min(60, $result.subjetivo.Length)))..."

# PATCH - Adicionar observação
Write-Host ""
Write-Host "[4/4] PATCH - Adicionando observacao a evolucao..."
$patched = Invoke-RestMethod -Uri "$baseUrl/rest/v1/evolucoes_enfermagem?id=eq.$evolId" -Method Patch -Headers $h `
    -Body '{"observacoes":"Familiar presente. Orientacoes fornecidas sobre sinais de alerta."}'
Write-Host ">> PATCH executado! Observacao: $($patched.observacoes)"

Write-Host ""
Write-Host "========================================"
Write-Host " TODOS OS TESTES PASSARAM COM SUCESSO!"
Write-Host " CAMADA 2 - ENFERMAGEM SAE: CONCLUIDA  "
Write-Host "========================================"
