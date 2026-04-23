$ErrorActionPreference = "Stop"

$anonKey      = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl      = "https://llqphjlpypnyvknpfdyn.supabase.co"
$pacienteId   = "873083bc-7652-4c68-9949-b598b8141ff0"
$nutricionistaId = "c767fe1e-05fb-4d92-88c2-e9c6ae3e232c" 

Write-Host "[1/4] Autenticando com medico2@ucgs.com..."
$login = Invoke-RestMethod -Uri "$baseUrl/auth/v1/token?grant_type=password" -Method Post `
    -Headers @{ "apikey" = $anonKey; "Content-Type" = "application/json" } `
    -Body '{"email":"medico2@ucgs.com","password":"123456"}'
$jwt = $login.access_token

$h = @{
    "apikey"        = $anonKey
    "Authorization" = "Bearer $jwt"
    "Content-Type"  = "application/json"
    "Prefer"        = "return=representation"
}

# POST - Registrar avaliacao
Write-Host "[2/4] POST - Registrando avaliacao nutricional..."
$bodyPost = [ordered]@{
    paciente_id              = $pacienteId
    nutricionista_id         = $nutricionistaId
    peso_kg                  = 75.5
    altura_cm                = 175.0
    imc                      = 24.65
    classificacao_imc        = "Eutrofia"
    meta_calorica_kcal       = 2100.00
    observacoes_recordatorio = "Paciente relata pular o café da manhã com frequência."
}

$inserted = Invoke-RestMethod -Uri "$baseUrl/rest/v1/avaliacoes_nutricionais" -Method Post -Headers $h -Body ($bodyPost | ConvertTo-Json)
$avaliacaoId = $inserted.id
Write-Host "ID gerado: $avaliacaoId"

# GET - Listar
Write-Host "[3/4] GET - Listando avaliacoes..."
$result = Invoke-RestMethod -Uri "$baseUrl/rest/v1/avaliacoes_nutricionais?paciente_id=eq.$pacienteId" -Method Get -Headers $h

# PATCH - Atualizar
Write-Host "[4/4] PATCH - Atualizando..."
$patched = Invoke-RestMethod -Uri "$baseUrl/rest/v1/avaliacoes_nutricionais?id=eq.$avaliacaoId" -Method Patch -Headers $h `
    -Body '{"observacoes_recordatorio":"Paciente relata pular o café da manhã. Adicionado foco em reeducação alimentar matinal. TESTE REAL"}'

Write-Host "SCRIPT CONCLUIDO SEM DELETAR O REGISTRO."
