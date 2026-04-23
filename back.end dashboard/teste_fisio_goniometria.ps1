$ErrorActionPreference = "Stop"

$anonKey          = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl          = "https://llqphjlpypnyvknpfdyn.supabase.co"
$pacienteId       = "873083bc-7652-4c68-9949-b598b8141ff0"
$fisioterapeutaId = "c767fe1e-05fb-4d92-88c2-e9c6ae3e232c"
$avaliacaoId      = "4423a1fb-dd60-4b44-b8e4-2bf8e8d83649"

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
Write-Host "[2/4] POST - Registrando goniometria de flexao lombar..."
# =============================================
$bodyPost = [ordered]@{
    avaliacao_id      = $avaliacaoId
    paciente_id       = $pacienteId
    fisioterapeuta_id = $fisioterapeutaId
    articulacao       = "Coluna Lombar"
    movimento         = "Flexao de tronco"
    lado              = "bilateral"
    amplitude_ativa   = 45.0
    amplitude_passiva = 52.0
    amplitude_normal  = 90.0
    limitacao_perc    = 50.0
    observacoes       = "Paciente refere dor ao final da amplitude. Limitacao significativa por lombalgia."
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/fisio_medicoes_goniometria" -Method Post `
    -Headers $h -Body ($bodyPost | ConvertTo-Json -Depth 5)
$medicaoId = $inserted.id
Write-Host ">> Goniometria registrada! ID: $medicaoId"
Write-Host "   Articulacao: $($inserted.articulacao) | Movimento: $($inserted.movimento)"
Write-Host "   Amplitude ativa: $($inserted.amplitude_ativa)° | Normal: $($inserted.amplitude_normal)°"
Write-Host "   Limitacao: $($inserted.limitacao_perc)%"

# =============================================
Write-Host ""
Write-Host "[3/4] GET - Listando goniometrias da avaliacao..."
# =============================================
$result = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/fisio_medicoes_goniometria?avaliacao_id=eq.$avaliacaoId&order=data_medicao.desc" `
    -Method Get -Headers $h
Write-Host ">> Total de medicoes goniometricas: $($result.Count)"
Write-Host "   Articulacao: $($result[0].articulacao) | Lado: $($result[0].lado)"
Write-Host "   Ativa: $($result[0].amplitude_ativa)° | Passiva: $($result[0].amplitude_passiva)°"

# =============================================
Write-Host ""
Write-Host "[4/4] PATCH - Atualizando observacao da goniometria..."
# =============================================
$patched = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/fisio_medicoes_goniometria?id=eq.$medicaoId" `
    -Method Patch -Headers $h `
    -Body '{"observacoes":"Paciente refere dor ao final da amplitude. Limitacao de 50% por lombalgia cronica com espasmo muscular associado."}'
Write-Host ">> PATCH executado!"
Write-Host "   Observacao: $($patched.observacoes)"

Write-Host ""
Write-Host "========================================"
Write-Host " TODOS OS TESTES PASSARAM COM SUCESSO!  "
Write-Host " MODULO FISIOTERAPIA: goniometria [3/5] "
Write-Host "========================================"
