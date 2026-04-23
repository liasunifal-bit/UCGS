$ErrorActionPreference = "Stop"

$anonKey    = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl    = "https://llqphjlpypnyvknpfdyn.supabase.co"
$pacienteId = "873083bc-7652-4c68-9949-b598b8141ff0"
$dentistaId = "c767fe1e-05fb-4d92-88c2-e9c6ae3e232c"
$avaliacaoId = "eaf4d19b-925b-477c-9950-d3d2acf16ca7"

# =============================================
Write-Host "[1/4] Autenticando medico2@ucgs.com..."
# =============================================
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

# =============================================
Write-Host ""
Write-Host "[2/4] POST - Registrando 3 dentes no odontograma (CPO-D)..."
# =============================================

# Dente 46 - Cariado (o da queixa principal)
$d46 = [ordered]@{
    avaliacao_id = $avaliacaoId
    paciente_id  = $pacienteId
    dentista_id  = $dentistaId
    numero_dente = 46
    face         = "oclusal"
    condicao     = "cariado"
    observacoes  = "Carie profunda com comprometimento pulpar provavel. Sensibilidade ao frio."
}
$r1 = Invoke-RestMethod -Uri "$baseUrl/rest/v1/odontograma" -Method Post -Headers $h -Body ($d46 | ConvertTo-Json)
Write-Host ">> Dente 46 (cariado): ID $($r1.id)"

# Dente 36 - Restaurado
$d36 = [ordered]@{
    avaliacao_id = $avaliacaoId
    paciente_id  = $pacienteId
    dentista_id  = $dentistaId
    numero_dente = 36
    face         = "oclusal"
    condicao     = "restaurado"
    observacoes  = "Restauracao de amalgama antiga. Boa adaptacao marginal."
}
$r2 = Invoke-RestMethod -Uri "$baseUrl/rest/v1/odontograma" -Method Post -Headers $h -Body ($d36 | ConvertTo-Json)
Write-Host ">> Dente 36 (restaurado): ID $($r2.id)"

# Dente 18 - Extraído
$d18 = [ordered]@{
    avaliacao_id = $avaliacaoId
    paciente_id  = $pacienteId
    dentista_id  = $dentistaId
    numero_dente = 18
    face         = "todas"
    condicao     = "extraído"
    observacoes  = "Extracao por carie extensa. Relato do paciente."
}
$r3 = Invoke-RestMethod -Uri "$baseUrl/rest/v1/odontograma" -Method Post -Headers $h -Body ($d18 | ConvertTo-Json)
Write-Host ">> Dente 18 (extraido): ID $($r3.id)"

# =============================================
Write-Host ""
Write-Host "[3/4] GET - Consultando odontograma completo da avaliacao..."
# =============================================
$result = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/odontograma?avaliacao_id=eq.$avaliacaoId&order=numero_dente.asc" `
    -Method Get -Headers $h

Write-Host ">> Total de dentes mapeados: $($result.Count)"
$cariados   = ($result | Where-Object { $_.condicao -eq "cariado" }).Count
$restaurados = ($result | Where-Object { $_.condicao -eq "restaurado" }).Count
$extraidos  = ($result | Where-Object { $_.condicao -in @("extraído","ausente_outras_razoes") }).Count
$cpod = $cariados + $restaurados + $extraidos
Write-Host "   Cariados (C): $cariados | Perdidos (P): $extraidos | Obturados (O): $restaurados"
Write-Host "   Indice CPO-D calculado: $cpod"

# =============================================
Write-Host ""
Write-Host "[4/4] PATCH - Atualizando observacao do dente 46..."
# =============================================
$patched = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/odontograma?id=eq.$($r1.id)" `
    -Method Patch -Headers $h `
    -Body '{"observacoes":"Carie profunda com comprometimento pulpar. Indicado tratamento endodontico antes da restauracao."}'
Write-Host ">> PATCH executado!"
Write-Host "   Dente 46 - Nova obs: $($patched.observacoes)"

Write-Host ""
Write-Host "========================================"
Write-Host " TODOS OS TESTES PASSARAM COM SUCESSO!  "
Write-Host " MODULO ODONTOLOGIA: odontograma [2/3]  "
Write-Host "========================================"
