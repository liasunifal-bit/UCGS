$ErrorActionPreference = "Stop"

$anonKey         = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl         = "https://llqphjlpypnyvknpfdyn.supabase.co"
$pacienteId      = "873083bc-7652-4c68-9949-b598b8141ff0"
$nutricionistaId = "c767fe1e-05fb-4d92-88c2-e9c6ae3e232c"

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
Write-Host "[2/4] POST - Criando plano alimentar..."
# =============================================
$refeicoes = @(
    @{
        tipo    = "cafe_da_manha"
        horario = "07:00"
        itens   = @(
            @{ alimento = "Pao integral"; quantidade = "2 fatias"; kcal = 140 },
            @{ alimento = "Ovo mexido";   quantidade = "2 unidades"; kcal = 155 }
        )
    },
    @{
        tipo    = "almoco"
        horario = "12:00"
        itens   = @(
            @{ alimento = "Arroz integral"; quantidade = "4 colheres"; kcal = 220 },
            @{ alimento = "Feijao carioca"; quantidade = "2 colheres"; kcal = 180 },
            @{ alimento = "Frango grelhado"; quantidade = "150g"; kcal = 240 }
        )
    }
)

$bodyPost = [ordered]@{
    paciente_id        = $pacienteId
    nutricionista_id   = $nutricionistaId
    nome_plano         = "Plano Reeducacao Alimentar - Fase 1"
    data_inicio        = "2026-04-22"
    data_fim           = "2026-05-22"
    meta_calorica_kcal = 2100
    meta_proteina_g    = 150
    meta_carboidrato_g = 250
    meta_gordura_g     = 70
    refeicoes          = $refeicoes
    observacoes        = "Evitar frituras e alimentos ultraprocessados."
    ativo              = $true
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/planos_alimentares" -Method Post `
    -Headers $h -Body ($bodyPost | ConvertTo-Json -Depth 10)
$planoId = $inserted.id
Write-Host ">> Plano criado! ID: $planoId"
Write-Host "   Nome: $($inserted.nome_plano)"
Write-Host "   Vigencia: $($inserted.data_inicio) ate $($inserted.data_fim)"
Write-Host "   Meta calorica: $($inserted.meta_calorica_kcal) kcal"

# =============================================
Write-Host ""
Write-Host "[3/4] GET - Listando planos ativos do paciente..."
# =============================================
$result = Invoke-RestMethod -Uri "$baseUrl/rest/v1/planos_alimentares?paciente_id=eq.$pacienteId&ativo=eq.true" `
    -Method Get -Headers $h
Write-Host ">> Total de planos ativos: $($result.Count)"
Write-Host "   Plano: $($result[0].nome_plano)"
$qtdRefeicoes = $result[0].refeicoes.Count
Write-Host "   Refeicoes cadastradas no JSONB: $qtdRefeicoes"

# =============================================
Write-Host ""
Write-Host "[4/4] PATCH - Adicionando observacao ao plano..."
# =============================================
$patched = Invoke-RestMethod -Uri "$baseUrl/rest/v1/planos_alimentares?id=eq.$planoId" `
    -Method Patch -Headers $h `
    -Body '{"observacoes":"Evitar frituras. Incluir hidratacao minima de 2L de agua por dia."}'
Write-Host ">> PATCH executado! Observacao: $($patched.observacoes)"

Write-Host ""
Write-Host "========================================"
Write-Host " TODOS OS TESTES PASSARAM COM SUCESSO!  "
Write-Host " CAMADA NUTRICIONAL: planos_alimentares  "
Write-Host "========================================"
