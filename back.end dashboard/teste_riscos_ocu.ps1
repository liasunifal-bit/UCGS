$ErrorActionPreference = "Stop"

$anonKey   = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl   = "https://llqphjlpypnyvknpfdyn.supabase.co"
$processoId = "a17e2742-9653-4e5d-bf26-818d6cef324a"

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
Write-Host "[2/4] POST - Inserindo risco ocupacional biologico..."
$bodyPost = [ordered]@{
    processo_id     = $processoId
    tipo_risco      = "biologico"
    descricao       = "Exposicao a agentes patogenicos sem uso de EPI adequado"
    grau_risco      = "alto"
    medida_controle = "Uso obrigatorio de luvas, mascara N95 e avental"
}
$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/enfermagem_riscos_ocupacionais" -Method Post -Headers $h -Body ($bodyPost | ConvertTo-Json)
$riscoId = $inserted.id
Write-Host ">> Risco inserido! ID: $riscoId"
Write-Host ($inserted | ConvertTo-Json -Depth 3)

Write-Host ""
Write-Host "[2b/4] POST - Inserindo segundo risco (ergonomico)..."
$bodyPost2 = [ordered]@{
    processo_id     = $processoId
    tipo_risco      = "ergonomico"
    descricao       = "Postura inadequada no trabalho sedentario por mais de 6 horas"
    grau_risco      = "medio"
    medida_controle = "Pausas a cada 2 horas e ajuste da cadeira ergonomica"
}
$inserted2 = Invoke-RestMethod -Uri "$baseUrl/rest/v1/enfermagem_riscos_ocupacionais" -Method Post -Headers $h -Body ($bodyPost2 | ConvertTo-Json)
Write-Host ">> Segundo risco inserido! ID: $($inserted2.id)"

Write-Host ""
Write-Host "[3/4] GET - Listando riscos do processo..."
$result = Invoke-RestMethod -Uri "$baseUrl/rest/v1/enfermagem_riscos_ocupacionais?processo_id=eq.$processoId" -Method Get -Headers $h
Write-Host ">> Total de riscos encontrados: $($result.Count)"
$result | ForEach-Object { Write-Host "   [$($_.tipo_risco) - $($_.grau_risco)] $($_.descricao.Substring(0, [Math]::Min(50, $_.descricao.Length)))..." }

Write-Host ""
Write-Host "[4/4] PATCH - Atualizando grau de risco biologico para critico..."
$patched = Invoke-RestMethod -Uri "$baseUrl/rest/v1/enfermagem_riscos_ocupacionais?id=eq.$riscoId" -Method Patch -Headers $h `
    -Body '{"grau_risco":"critico","medida_controle":"Afastamento imediato e notificacao ao SESMT."}'
Write-Host ">> PATCH executado! Novo grau: $($patched.grau_risco)"

Write-Host ""
Write-Host "========================================"
Write-Host "   TODOS OS TESTES PASSARAM COM SUCESSO!"
Write-Host "   enfermagem_riscos_ocupacionais: OK   "
Write-Host "========================================"
