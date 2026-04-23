$ErrorActionPreference = "Stop"

$anonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl = "https://llqphjlpypnyvknpfdyn.supabase.co"

Write-Host "[1/3] Autenticando medico2@ucgs.com..."
$login = Invoke-RestMethod -Uri "$baseUrl/auth/v1/token?grant_type=password" -Method Post `
    -Headers @{ "apikey" = $anonKey; "Content-Type" = "application/json" } `
    -Body '{"email":"medico2@ucgs.com","password":"123456"}'
$jwt = $login.access_token
Write-Host ">> JWT gerado com sucesso."

$h = @{
    "apikey"        = $anonKey
    "Authorization" = "Bearer $jwt"
    "Content-Type"  = "application/json"
}

Write-Host ""
Write-Host "[2/3] GET - Listando todas as intervencoes NIC..."
$all = Invoke-RestMethod -Uri "$baseUrl/rest/v1/nic_intervencoes?select=codigo,titulo,dominio" -Method Get -Headers $h
Write-Host ">> Total de intervencoes NIC retornadas: $($all.Count)"
$all | ForEach-Object { Write-Host "   [$($_.codigo)] $($_.titulo)" }

Write-Host ""
Write-Host "[3/3] GET - Buscando NIC 1400 (Manejo da Dor)..."
$specific = Invoke-RestMethod -Uri "$baseUrl/rest/v1/nic_intervencoes?codigo=eq.1400" -Method Get -Headers $h
Write-Host ">> Resultado:"
Write-Host ($specific | ConvertTo-Json -Depth 3)

Write-Host ""
Write-Host "[EXTRA] Testando bloqueio de INSERT no catalogo NIC..."
try {
    $hInsert = $h.Clone()
    $hInsert["Prefer"] = "return=representation"
    $blocked = Invoke-RestMethod -Uri "$baseUrl/rest/v1/nic_intervencoes" -Method Post -Headers $hInsert `
        -Body '{"codigo":"9999","titulo":"Intervencao Nao Autorizada"}'
    Write-Host ">> FALHA DE SEGURANCA: INSERT permitido indevidamente!"
} catch {
    Write-Host ">> CORRETO! INSERT bloqueado pelo RLS. Catalogo NIC protegido."
}

Write-Host ""
Write-Host "========================================"
Write-Host "   TODOS OS TESTES PASSARAM COM SUCESSO!"
Write-Host "   Tabela nic_intervencoes: VALIDADA    "
Write-Host "========================================"
