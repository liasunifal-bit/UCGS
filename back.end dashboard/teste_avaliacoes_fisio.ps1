$ErrorActionPreference = "Stop"

$anonKey          = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl          = "https://llqphjlpypnyvknpfdyn.supabase.co"
$pacienteId       = "873083bc-7652-4c68-9949-b598b8141ff0"
$fisioterapeutaId = "c767fe1e-05fb-4d92-88c2-e9c6ae3e232c"

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
Write-Host "[2/4] POST - Registrando avaliacao fisioterapeutica..."
# =============================================
$bodyPost = [ordered]@{
    paciente_id          = $pacienteId
    fisioterapeuta_id    = $fisioterapeutaId
    data_avaliacao       = "2026-04-22"
    queixa_principal     = "Dor lombar cronica com irradiacao para membro inferior direito. EVA 7/10."
    historico_doenca     = "Paciente relata inicio ha 3 meses apos esforco fisico no trabalho."
    diagnostico_clinico  = "Lombalgia cronica com lombociatalgia direita"
    cid10                = "M54.4"
    hipotese_diagnostica = "Hernia discal L4-L5 com compressao radicular"
    membro_dominante     = "direito"
    localidade_dor       = "Regiao lombar baixa com irradiacao para gluteo e coxa direita"
    fator_melhora        = "Repouso e aplicacao de calor local"
    fator_piora          = "Flexao de tronco e posicao sentada prolongada"
    conduta_inicial      = "Termoterapia, TENS, cinesioterapia e orientacoes posturais"
    numero_sessoes_prev  = 20
    observacoes          = "Paciente com sobrepeso. Encaminhado pelo ortopedista."
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/avaliacoes_fisioterapia" -Method Post `
    -Headers $h -Body ($bodyPost | ConvertTo-Json -Depth 5)
$avaliacaoId = $inserted.id
Write-Host ">> Avaliacao registrada! ID: $avaliacaoId"
Write-Host "   Queixa: $($inserted.queixa_principal.Substring(0, [Math]::Min(60, $inserted.queixa_principal.Length)))..."
Write-Host "   CID-10: $($inserted.cid10)"
Write-Host "   Sessoes previstas: $($inserted.numero_sessoes_prev)"

# =============================================
Write-Host ""
Write-Host "[3/4] GET - Listando avaliacoes de fisioterapia do paciente..."
# =============================================
$result = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/avaliacoes_fisioterapia?paciente_id=eq.$pacienteId&order=data_avaliacao.desc" `
    -Method Get -Headers $h
Write-Host ">> Total de avaliacoes encontradas: $($result.Count)"
Write-Host "   Diagnostico: $($result[0].diagnostico_clinico)"
Write-Host "   Hipotese diagnostica: $($result[0].hipotese_diagnostica)"

# =============================================
Write-Host ""
Write-Host "[4/4] PATCH - Atualizando conduta inicial..."
# =============================================
$patched = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/avaliacoes_fisioterapia?id=eq.$avaliacaoId" `
    -Method Patch -Headers $h `
    -Body '{"conduta_inicial":"Termoterapia, TENS, cinesioterapia, RPG e orientacoes posturais. Incluir pilates terapeutico."}'
Write-Host ">> PATCH executado!"
Write-Host "   Nova conduta: $($patched.conduta_inicial)"

Write-Host ""
Write-Host "========================================"
Write-Host " TODOS OS TESTES PASSARAM COM SUCESSO!  "
Write-Host " MODULO FISIOTERAPIA: avaliacoes [1/5]  "
Write-Host "========================================"
