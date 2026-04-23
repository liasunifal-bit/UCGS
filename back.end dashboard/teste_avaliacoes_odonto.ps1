$ErrorActionPreference = "Stop"

$anonKey    = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl    = "https://llqphjlpypnyvknpfdyn.supabase.co"
$pacienteId = "873083bc-7652-4c68-9949-b598b8141ff0"
$dentistaId = "c767fe1e-05fb-4d92-88c2-e9c6ae3e232c"

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
Write-Host "[2/4] POST - Registrando avaliacao odontologica..."
# =============================================
$bodyPost = [ordered]@{
    paciente_id          = $pacienteId
    dentista_id          = $dentistaId
    data_avaliacao       = "2026-04-22"
    queixa_principal     = "Dor em dente posterior inferior direito ao mastigar. Sensibilidade ao frio."
    historico_odonto     = "Paciente relata nunca ter feito tratamento orthodontico. Ultima consulta ha 2 anos."
    habitos_nocivos      = @("bruxismo", "onicofagia")
    higiene_oral         = "regular"
    frequencia_escovacao = "2x"
    usa_fio_dental       = $false
    plano_tratamento     = "Restauracao do elemento 46. Profilaxia completa. Orientacao de higiene oral."
    cpod_total           = 8
    observacoes          = "Paciente apresenta gengivite leve generalizada e calculo supragengival."
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/avaliacoes_odontologicas" -Method Post `
    -Headers $h -Body ($bodyPost | ConvertTo-Json -Depth 5)
$avaliacaoId = $inserted.id
Write-Host ">> Avaliacao odontologica registrada! ID: $avaliacaoId"
Write-Host "   Queixa: $($inserted.queixa_principal.Substring(0, [Math]::Min(55,$inserted.queixa_principal.Length)))..."
Write-Host "   Higiene oral: $($inserted.higiene_oral) | CPO-D total: $($inserted.cpod_total)"
Write-Host "   Usa fio dental: $($inserted.usa_fio_dental)"

# =============================================
Write-Host ""
Write-Host "[3/4] GET - Listando avaliacoes odontologicas do paciente..."
# =============================================
$result = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/avaliacoes_odontologicas?paciente_id=eq.$pacienteId&order=data_avaliacao.desc" `
    -Method Get -Headers $h
Write-Host ">> Total de avaliacoes: $($result.Count)"
Write-Host "   Plano de tratamento: $($result[0].plano_tratamento)"

# =============================================
Write-Host ""
Write-Host "[4/4] PATCH - Atualizando plano de tratamento..."
# =============================================
$patched = Invoke-RestMethod `
    -Uri "$baseUrl/rest/v1/avaliacoes_odontologicas?id=eq.$avaliacaoId" `
    -Method Patch -Headers $h `
    -Body '{"plano_tratamento":"Restauracao do elemento 46 com resina composta. Raspagem supragengival. Profilaxia. Orientacao de higiene oral e uso de fio dental."}'
Write-Host ">> PATCH executado!"
Write-Host "   Novo plano: $($patched.plano_tratamento)"

Write-Host ""
Write-Host "========================================"
Write-Host " TODOS OS TESTES PASSARAM COM SUCESSO!  "
Write-Host " MODULO ODONTOLOGIA: avaliacoes [1/3]   "
Write-Host "========================================"
