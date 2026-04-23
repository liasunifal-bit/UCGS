# ============================================================
# UCGS Backend — Teste de API: Pacientes
# ============================================================
# Testa todos os endpoints CRUD de /api/pacientes
#
# Uso: .\teste_backend_pacientes.ps1
# ============================================================

$ErrorActionPreference = "Continue"

# Configuração
$BASE_URL = "http://localhost:3001/api"
$SUPABASE_URL = "https://llqphjlpypnyvknpfdyn.supabase.co"
$ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"

# Credenciais de teste (usar um usuario existente no Supabase Auth)
$TEST_EMAIL = "medico2@ucgs.com"
$TEST_PASSWORD = "123456"

$passed = 0
$failed = 0

function Write-Result($testName, $success, $detail) {
    if ($success) {
        Write-Host "  [PASS] $testName" -ForegroundColor Green
        $script:passed++
    } else {
        Write-Host "  [FAIL] $testName - $detail" -ForegroundColor Red
        $script:failed++
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  UCGS Backend - Teste de API: Pacientes" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# PASSO 0: Health Check
# ============================================================
Write-Host "--- Health Check ---" -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$BASE_URL/health" -Method GET
    Write-Result "GET /api/health" ($health.status -eq "online") $health.status
} catch {
    Write-Result "GET /api/health" $false $_.Exception.Message
    Write-Host "`n  ERRO: Servidor nao esta rodando! Inicie com: cd server && npm start`n" -ForegroundColor Red
    exit 1
}

# ============================================================
# PASSO 1: Obter JWT via Supabase Auth
# ============================================================
Write-Host "`n--- Autenticacao ---" -ForegroundColor Yellow
$jwt = $null
try {
    $loginBody = @{
        email = $TEST_EMAIL
        password = $TEST_PASSWORD
    } | ConvertTo-Json

    $loginHeaders = @{
        "apikey" = $ANON_KEY
        "Content-Type" = "application/json"
    }

    $loginResp = Invoke-RestMethod -Uri "$SUPABASE_URL/auth/v1/token?grant_type=password" `
        -Method POST -Headers $loginHeaders -Body $loginBody

    $jwt = $loginResp.access_token
    Write-Result "Login Supabase Auth" ($jwt.Length -gt 10) ""
    Write-Host "    Token: $($jwt.Substring(0,30))..." -ForegroundColor DarkGray
} catch {
    Write-Result "Login Supabase Auth" $false $_.Exception.Message
    Write-Host "`n  ERRO: Nao foi possivel autenticar. Verifique email/senha.`n" -ForegroundColor Red
    exit 1
}

$authHeaders = @{
    "Authorization" = "Bearer $jwt"
    "Content-Type" = "application/json"
}

# ============================================================
# PASSO 2: POST sem token (deve retornar 401)
# ============================================================
Write-Host "`n--- Bloqueio sem Autenticacao ---" -ForegroundColor Yellow
try {
    $noAuthHeaders = @{ "Content-Type" = "application/json" }
    $noAuthBody = @{ nome = "Teste" } | ConvertTo-Json
    $resp = Invoke-WebRequest -Uri "$BASE_URL/pacientes" -Method POST `
        -Headers $noAuthHeaders -Body $noAuthBody -UseBasicParsing
    Write-Result "POST sem token -> 401" $false "Esperava 401, recebeu $($resp.StatusCode)"
} catch {
    $statusCode = $_.Exception.Response.StatusCode.Value__
    Write-Result "POST sem token -> 401" ($statusCode -eq 401) "Status: $statusCode"
}

# ============================================================
# PASSO 3: POST com campos faltando (deve retornar 400)
# ============================================================
Write-Host "`n--- Validacao de Campos ---" -ForegroundColor Yellow
try {
    $incompleteBody = @{ nome = "Teste Incompleto" } | ConvertTo-Json
    $resp = Invoke-WebRequest -Uri "$BASE_URL/pacientes" -Method POST `
        -Headers $authHeaders -Body $incompleteBody -UseBasicParsing
    Write-Result "POST campos faltando -> 400" $false "Esperava 400, recebeu $($resp.StatusCode)"
} catch {
    $statusCode = $_.Exception.Response.StatusCode.Value__
    Write-Result "POST campos faltando -> 400" ($statusCode -eq 400) "Status: $statusCode"
}

# ============================================================
# PASSO 4: POST com CPF invalido (deve retornar 400)
# ============================================================
try {
    $invalidCpfBody = @{
        nome = "Teste CPF"
        cpf = "123"
        nascimento = "2000-01-01"
        sexo = "masculino"
    } | ConvertTo-Json
    $resp = Invoke-WebRequest -Uri "$BASE_URL/pacientes" -Method POST `
        -Headers $authHeaders -Body $invalidCpfBody -UseBasicParsing
    Write-Result "POST CPF invalido -> 400" $false "Esperava 400, recebeu $($resp.StatusCode)"
} catch {
    $statusCode = $_.Exception.Response.StatusCode.Value__
    Write-Result "POST CPF invalido -> 400" ($statusCode -eq 400) "Status: $statusCode"
}

# ============================================================
# PASSO 5: POST valido (deve retornar 201)
# ============================================================
Write-Host "`n--- CRUD Completo ---" -ForegroundColor Yellow
$pacienteId = $null
$cpfTeste = "99988877766"
try {
    $validBody = @{
        nome = "Paciente Teste Backend"
        cpf = $cpfTeste
        nascimento = "1990-05-15"
        sexo = "feminino"
        telefone = "(35) 99999-0000"
        email = "teste.backend@ucgs.com"
        logradouro = "Rua das Flores"
        numero = "123"
        bairro = "Centro"
        cidade = "Alfenas"
        uf = "mg"
        cep = "37130-000"
    } | ConvertTo-Json

    $resp = Invoke-RestMethod -Uri "$BASE_URL/pacientes" -Method POST `
        -Headers $authHeaders -Body $validBody
    $pacienteId = $resp.dados[0].id
    Write-Result "POST paciente valido -> 201" ($resp.sucesso -eq $true) ""
    Write-Host "    ID criado: $pacienteId" -ForegroundColor DarkGray
} catch {
    $statusCode = $null
    try { $statusCode = $_.Exception.Response.StatusCode.Value__ } catch {}
    $errorBody = ""
    try {
        $stream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($stream)
        $errorBody = $reader.ReadToEnd()
    } catch {}
    Write-Result "POST paciente valido -> 201" $false "Status: $statusCode | $errorBody"
}

# ============================================================
# PASSO 6: GET listar pacientes
# ============================================================
try {
    $resp = Invoke-RestMethod -Uri "$BASE_URL/pacientes" -Method GET -Headers $authHeaders
    Write-Result "GET listar pacientes" ($resp.sucesso -eq $true -and $resp.total -gt 0) "Total: $($resp.total)"
} catch {
    Write-Result "GET listar pacientes" $false $_.Exception.Message
}

# ============================================================
# PASSO 7: GET buscar por ID
# ============================================================
if ($pacienteId) {
    try {
        $resp = Invoke-RestMethod -Uri "$BASE_URL/pacientes/$pacienteId" -Method GET -Headers $authHeaders
        Write-Result "GET paciente por ID" ($resp.sucesso -eq $true -and $resp.dados.nome -eq "Paciente Teste Backend") ""
    } catch {
        Write-Result "GET paciente por ID" $false $_.Exception.Message
    }
}

# ============================================================
# PASSO 8: GET buscar com filtro
# ============================================================
try {
    $resp = Invoke-RestMethod -Uri "$BASE_URL/pacientes?busca=Teste" -Method GET -Headers $authHeaders
    Write-Result "GET busca por nome" ($resp.sucesso -eq $true) "Resultados: $($resp.total)"
} catch {
    Write-Result "GET busca por nome" $false $_.Exception.Message
}

# ============================================================
# PASSO 9: PATCH atualizar paciente
# ============================================================
if ($pacienteId) {
    try {
        $updateBody = @{
            telefone = "(35) 98888-1111"
            observacoes = "Atualizado via teste backend"
        } | ConvertTo-Json

        $resp = Invoke-RestMethod -Uri "$BASE_URL/pacientes/$pacienteId" -Method PATCH `
            -Headers $authHeaders -Body $updateBody
        Write-Result "PATCH atualizar paciente" ($resp.sucesso -eq $true) ""
    } catch {
        Write-Result "PATCH atualizar paciente" $false $_.Exception.Message
    }
}

# ============================================================
# PASSO 10: DELETE soft-delete
# ============================================================
if ($pacienteId) {
    try {
        $resp = Invoke-RestMethod -Uri "$BASE_URL/pacientes/$pacienteId" -Method DELETE -Headers $authHeaders
        Write-Result "DELETE soft-delete" ($resp.sucesso -eq $true) ""
    } catch {
        Write-Result "DELETE soft-delete" $false $_.Exception.Message
    }
}

# ============================================================
# LIMPEZA: Remover paciente de teste via Supabase direto
# ============================================================
Write-Host "`n--- Limpeza ---" -ForegroundColor Yellow
if ($pacienteId) {
    try {
        $cleanHeaders = @{
            "apikey" = $ANON_KEY
            "Authorization" = "Bearer $jwt"
        }
        # Reativar para poder deletar em testes futuros
        $reactivateBody = @{ ativo = $true } | ConvertTo-Json
        Invoke-RestMethod -Uri "$SUPABASE_URL/rest/v1/pacientes?id=eq.$pacienteId" `
            -Method PATCH -Headers ($cleanHeaders + @{"Content-Type"="application/json"; "Prefer"="return=minimal"}) `
            -Body $reactivateBody | Out-Null
        Write-Result "Reativar paciente de teste" $true ""
    } catch {
        Write-Result "Reativar paciente de teste" $false $_.Exception.Message
    }
}

# ============================================================
# RESUMO
# ============================================================
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  RESULTADO FINAL" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Passou: $passed" -ForegroundColor Green
Write-Host "  Falhou: $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host "  Total:  $($passed + $failed)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

if ($failed -gt 0) { exit 1 } else { exit 0 }
