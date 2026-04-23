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
Write-Host "[2/4] POST - Registrando medicao EVA pre-sessao..."
# =============================================
$bodyPost = [ordered]@{
    avaliacao_id      = $avaliacaoId
    paciente_id       = $pacienteId
    fisioterapeuta_id = $fisioterapeutaId
    momento           = "pre_sessao"
    regiao_corporal   = "Regiao lombar L4-L5 com irradiacao para membro inferior direito"
    eva_score         = 7
    descricao_dor     = "Dor em queimacao constante, piora com flexao de tronco"
    observacoes       = "Paciente relata dor intensa ao sentar por mais de 30 minutos"
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/fisio_medicoes_eva" -Method Post `
    -Headers $h -Body ($bodyPost | ConvertTo-Json -Depth 5)
$medicaoId = $inserted.id
Write-Host ">> Medicao EVA registrada! ID: $medicaoId"
Write-Host "   Momento: $($inserted.momento)"
Write-Host "   Regiao: $($inserted.regiao_corporal)"
Write-Host "   Score EVA: $($inserted.eva_score)/10"

# =============================================
Write-Host ""
Write-Host "[3/4] GET - Listando medicoes EVA da avaliacao..."
# =============================================
$result = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/fisio_medicoes_eva?avaliacao_id=eq.$avaliacaoId&order=data_medicao.desc" `
    -Method Get -Headers $h
Write-Host ">> Total de medicoes EVA: $($result.Count)"
Write-Host "   Ultima medicao: EVA $($result[0].eva_score)/10 | $($result[0].momento)"

# =============================================
Write-Host ""
Write-Host "[4/4] PATCH - Registrando EVA pos-sessao..."
# =============================================
$patched = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/fisio_medicoes_eva?id=eq.$medicaoId" `
    -Method Patch -Headers $h `
    -Body '{"observacoes":"Paciente relatou reducao da dor apos aplicacao de TENS. EVA sera reavaliado pos-sessao."}'
Write-Host ">> PATCH executado!"
Write-Host "   Observacao: $($patched.observacoes)"

Write-Host ""
Write-Host "========================================"
Write-Host " TODOS OS TESTES PASSARAM COM SUCESSO!  "
Write-Host " MODULO FISIOTERAPIA: medicoes_eva [2/5]"
Write-Host "========================================"
