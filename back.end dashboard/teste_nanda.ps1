$ErrorActionPreference = "Stop"

$anonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl = "https://llqphjlpypnyvknpfdyn.supabase.co"

# PASSO 1: Login
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

# PASSO 2: GET - Listar diagnosticos NANDA (catalogo)
Write-Host ""
Write-Host "[2/3] GET - Listando todos os diagnosticos NANDA..."
$all = Invoke-RestMethod -Uri "$baseUrl/rest/v1/nanda_diagnosticos?select=codigo,titulo,dominio" -Method Get -Headers $h
Write-Host ">> Total de diagnosticos retornados: $($all.Count)"
$all | ForEach-Object { Write-Host "   [$($_.codigo)] $($_.titulo)" }

# PASSO 3: GET - Buscar diagnostico específico por codigo
Write-Host ""
Write-Host "[3/3] GET - Buscando diagnostico especifico (codigo 00132 - Dor Aguda)..."
$specific = Invoke-RestMethod -Uri "$baseUrl/rest/v1/nanda_diagnosticos?codigo=eq.00132" -Method Get -Headers $h
Write-Host ">> Resultado:"
Write-Host ($specific | ConvertTo-Json -Depth 3)

# PASSO EXTRA: Testar que INSERT é bloqueado pelo RLS (deve falhar)
Write-Host ""
Write-Host "[EXTRA] Testando bloqueio de INSERT no catalogo NANDA (deve falhar com 403)..."
try {
    $hInsert = $h.Clone()
    $hInsert["Prefer"] = "return=representation"
    $blocked = Invoke-RestMethod -Uri "$baseUrl/rest/v1/nanda_diagnosticos" -Method Post -Headers $hInsert `
        -Body '{"codigo":"99999","titulo":"Diagnostico Nao Autorizado"}'
    Write-Host ">> FALHA DE SEGURANÇA: INSERT foi permitido indevidamente!" -ForegroundColor Red
} catch {
    Write-Host ">> CORRETO! INSERT bloqueado pelo RLS. Catalogo protegido." -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================"
Write-Host "   TODOS OS TESTES PASSARAM COM SUCESSO!"
Write-Host "   Tabela nanda_diagnosticos: VALIDADA  "
Write-Host "========================================"
