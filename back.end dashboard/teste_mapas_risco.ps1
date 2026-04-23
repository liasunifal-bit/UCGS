$ErrorActionPreference = "Stop"

$anonKey      = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl      = "https://llqphjlpypnyvknpfdyn.supabase.co"
$registradoPor = "c767fe1e-05fb-4d92-88c2-e9c6ae3e232c"

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
Write-Host "[2/4] POST - Registrando risco ocupacional..."
# =============================================
$bodyPost = [ordered]@{
    registrado_por   = $registradoPor
    setor            = "Laboratorio de Analises Clinicas"
    data_avaliacao   = "2026-04-22"
    tipo_risco       = "biologico"
    descricao_risco  = "Exposicao a agentes biologicos patogenicos durante coleta e manipulacao de amostras biologicas"
    agente           = "Virus, bacterias, fungos presentes em amostras de sangue, urina e secrecoes"
    nivel_risco      = "alto"
    medidas_controle = "EPI obrigatorio (luvas, mascara, avental). Cabine de seguranca biologica. Protocolo de descarte de perfurocortantes."
    status           = "ativo"
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/mapas_risco_ocupacional" -Method Post `
    -Headers $h -Body ($bodyPost | ConvertTo-Json -Depth 5)
$riscoId = $inserted.id
Write-Host ">> Risco registrado! ID: $riscoId"
Write-Host "   Setor: $($inserted.setor)"
Write-Host "   Tipo: $($inserted.tipo_risco) | Nivel: $($inserted.nivel_risco)"
Write-Host "   Status: $($inserted.status)"

# =============================================
Write-Host ""
Write-Host "[3/4] GET - Listando riscos por nivel critico/alto..."
# =============================================
$result = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/mapas_risco_ocupacional?nivel_risco=eq.alto&order=data_avaliacao.desc" `
    -Method Get -Headers $h
Write-Host ">> Total de riscos ALTO encontrados: $($result.Count)"
Write-Host "   Setor: $($result[0].setor)"
Write-Host "   Agente: $($result[0].agente.Substring(0,[Math]::Min(55,$result[0].agente.Length)))..."

# =============================================
Write-Host ""
Write-Host "[4/4] PATCH - Atualizando medidas de controle..."
# =============================================
$patched = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/mapas_risco_ocupacional?id=eq.$riscoId" `
    -Method Patch -Headers $h `
    -Body '{"medidas_controle":"EPI obrigatorio. Cabine de seguranca biologica. Protocolo de perfurocortantes. Vacinacao obrigatoria (HBV). Treinamento semestral."}'
Write-Host ">> PATCH executado!"
Write-Host "   Medidas atualizadas: $($patched.medidas_controle)"

Write-Host ""
Write-Host "========================================"
Write-Host " TODOS OS TESTES PASSARAM COM SUCESSO!  "
Write-Host " MODULO SEG. TRABALHO: mapas_risco [1/2]"
Write-Host "========================================"
