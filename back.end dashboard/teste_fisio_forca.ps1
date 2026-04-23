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
Write-Host "[2/4] POST - Registrando teste de forca muscular (MRC)..."
# =============================================
$bodyPost = [ordered]@{
    avaliacao_id      = $avaliacaoId
    paciente_id       = $pacienteId
    fisioterapeuta_id = $fisioterapeutaId
    grupo_muscular    = "Extensores lombares (Eretor da espinha)"
    movimento         = "Extensao de tronco"
    lado              = "bilateral"
    grau_mrc          = 3
    descricao_mrc     = "Vence a gravidade sem resistencia adicional"
    observacoes       = "Paciente apresenta fadiga precoce. Espasmo muscular paravertebral bilateral."
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/fisio_medicoes_forca" -Method Post `
    -Headers $h -Body ($bodyPost | ConvertTo-Json -Depth 5)
$medicaoId = $inserted.id
Write-Host ">> Medicao de forca registrada! ID: $medicaoId"
Write-Host "   Grupo muscular: $($inserted.grupo_muscular)"
Write-Host "   Grau MRC: $($inserted.grau_mrc)/5 - $($inserted.descricao_mrc)"
Write-Host "   Lado: $($inserted.lado)"

# =============================================
Write-Host ""
Write-Host "[3/4] GET - Listando medicoes de forca da avaliacao..."
# =============================================
$result = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/fisio_medicoes_forca?avaliacao_id=eq.$avaliacaoId&order=data_medicao.desc" `
    -Method Get -Headers $h
Write-Host ">> Total de medicoes de forca: $($result.Count)"
Write-Host "   Grupo: $($result[0].grupo_muscular)"
Write-Host "   MRC: $($result[0].grau_mrc)/5 | Movimento: $($result[0].movimento)"

# =============================================
Write-Host ""
Write-Host "[4/4] PATCH - Atualizando observacao da medicao..."
# =============================================
$patched = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/fisio_medicoes_forca?id=eq.$medicaoId" `
    -Method Patch -Headers $h `
    -Body '{"observacoes":"Espasmo muscular paravertebral bilateral. Indicado trabalho de fortalecimento progressivo e liberacao miofascial."}'
Write-Host ">> PATCH executado!"
Write-Host "   Observacao: $($patched.observacoes)"

Write-Host ""
Write-Host "========================================"
Write-Host " TODOS OS TESTES PASSARAM COM SUCESSO!  "
Write-Host " MODULO FISIOTERAPIA: forca_mrc [4/5]   "
Write-Host "========================================"
