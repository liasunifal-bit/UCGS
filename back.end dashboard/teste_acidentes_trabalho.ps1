$ErrorActionPreference = "Stop"

$anonKey       = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl       = "https://llqphjlpypnyvknpfdyn.supabase.co"
$pacienteId    = "873083bc-7652-4c68-9949-b598b8141ff0"
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
Write-Host "[2/4] POST - Registrando acidente de trabalho..."
# =============================================
$bodyPost = [ordered]@{
    paciente_id          = $pacienteId
    registrado_por       = $registradoPor
    data_acidente        = "2026-04-22T09:30:00Z"
    setor                = "Laboratorio de Analises Clinicas"
    tipo_acidente        = "perfuracao"
    descricao            = "Profissional sofreu perfuracao com agulha hipondermica apos coleta de sangue de paciente com sorologias desconhecidas."
    parte_corpo_atingida = "Dedo indicador da mao esquerda"
    usou_epi             = $true
    causa_provavel       = "Reencape de agulha apos procedimento. Nao seguiu protocolo padrao."
    medidas_tomadas      = "Lavagem da area com agua e sabao. Notificacao ao SESMT. Coleta de sorologia basal. Orientacao sobre profilaxia PEP."
    cat_emitida          = $true
    afastamento          = $false
    dias_afastamento     = 0
    gravidade            = "moderado"
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/acidentes_trabalho" -Method Post `
    -Headers $h -Body ($bodyPost | ConvertTo-Json -Depth 5)
$acidenteId = $inserted.id
Write-Host ">> Acidente registrado! ID: $acidenteId"
Write-Host "   Tipo: $($inserted.tipo_acidente) | Gravidade: $($inserted.gravidade)"
Write-Host "   Setor: $($inserted.setor)"
Write-Host "   CAT emitida: $($inserted.cat_emitida) | Afastamento: $($inserted.afastamento)"

# =============================================
Write-Host ""
Write-Host "[3/4] GET - Consultando acidentes do setor..."
# =============================================
$result = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/acidentes_trabalho?setor=eq.Laboratorio de Analises Clinicas&order=data_acidente.desc" `
    -Method Get -Headers $h
Write-Host ">> Total de acidentes no setor: $($result.Count)"
Write-Host "   Ultimo: $($result[0].tipo_acidente) em $($result[0].data_acidente)"
Write-Host "   Parte atingida: $($result[0].parte_corpo_atingida)"

# =============================================
Write-Host ""
Write-Host "[4/4] PATCH - Atualizando medidas apos acompanhamento..."
# =============================================
$patched = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/acidentes_trabalho?id=eq.$acidenteId" `
    -Method Patch -Headers $h `
    -Body '{"medidas_tomadas":"Lavagem local. Notificacao SESMT. Sorologia basal coletada. PEP iniciada em 2h. Retorno para sorologias em 30, 90 e 180 dias. Treinamento de bioprevencao agendado."}'
Write-Host ">> PATCH executado!"
Write-Host "   Medidas finais: $($patched.medidas_tomadas)"

Write-Host ""
Write-Host "============================================"
Write-Host " TODOS OS TESTES PASSARAM COM SUCESSO!     "
Write-Host " MODULO SEG. TRABALHO: CONCLUIDO [2/2]     "
Write-Host " ==========================================  "
Write-Host " PROJETO UCGS - SCHEMA COMPLETO!            "
Write-Host " TODOS OS MODULOS IMPLEMENTADOS E TESTADOS  "
Write-Host "============================================"
