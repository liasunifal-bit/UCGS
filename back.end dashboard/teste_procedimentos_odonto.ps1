$ErrorActionPreference = "Stop"

$anonKey     = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl     = "https://llqphjlpypnyvknpfdyn.supabase.co"
$pacienteId  = "873083bc-7652-4c68-9949-b598b8141ff0"
$dentistaId  = "c767fe1e-05fb-4d92-88c2-e9c6ae3e232c"
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
Write-Host "[2/4] POST - Registrando procedimento odontologico..."
# =============================================
$bodyPost = [ordered]@{
    avaliacao_id      = $avaliacaoId
    paciente_id       = $pacienteId
    dentista_id       = $dentistaId
    data_procedimento = "2026-04-22"
    numero_dente      = 46
    face              = "oclusal"
    tipo_procedimento = "Restauracao com resina composta"
    descricao         = "Remocao de carie com curetas e alta rotacao. Condicionamento acido. Aplicacao de sistema adesivo. Restauracao incremental com resina composta A3."
    material_usado    = "Resina composta A3, sistema adesivo Scotchbond, acido fosforico 37%"
    duracao_min       = 45
    status            = "realizado"
    observacoes       = "Paciente colaborativo. Anestesia local sem intercorrencias. Oclusao verificada e ajustada."
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/procedimentos_odontologicos" -Method Post `
    -Headers $h -Body ($bodyPost | ConvertTo-Json -Depth 5)
$procId = $inserted.id
Write-Host ">> Procedimento registrado! ID: $procId"
Write-Host "   Tipo: $($inserted.tipo_procedimento)"
Write-Host "   Dente: $($inserted.numero_dente) | Face: $($inserted.face)"
Write-Host "   Duracao: $($inserted.duracao_min) min | Status: $($inserted.status)"

# =============================================
Write-Host ""
Write-Host "[3/4] GET - Listando procedimentos da avaliacao..."
# =============================================
$result = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/procedimentos_odontologicos?avaliacao_id=eq.$avaliacaoId&order=data_procedimento.desc" `
    -Method Get -Headers $h
Write-Host ">> Total de procedimentos registrados: $($result.Count)"
Write-Host "   Ultimo: $($result[0].tipo_procedimento) - Dente $($result[0].numero_dente)"
Write-Host "   Material: $($result[0].material_usado)"

# =============================================
Write-Host ""
Write-Host "[4/4] PATCH - Atualizando status para pendente (proxima sessao)..."
# =============================================
$bodyPatch = '{"status":"realizado","observacoes":"Restauracao concluida. Retorno em 30 dias para profilaxia e verificacao de adaptacao marginal."}'
$patched = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/procedimentos_odontologicos?id=eq.$procId" `
    -Method Patch -Headers $h -Body $bodyPatch
Write-Host ">> PATCH executado! Status: $($patched.status)"
Write-Host "   Observacao final: $($patched.observacoes)"

Write-Host ""
Write-Host "========================================"
Write-Host " TODOS OS TESTES PASSARAM COM SUCESSO!  "
Write-Host " MODULO ODONTOLOGIA: CONCLUIDO [3/3]    "
Write-Host "========================================"
