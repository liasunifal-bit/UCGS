$ErrorActionPreference = "Stop"

$anonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$baseUrl = "https://llqphjlpypnyvknpfdyn.supabase.co"

Write-Host "--- TESTE DE API: restricoes_alimentares_paciente ---"

# 1. Login
Write-Host "[1/6] Autenticando com medico2@ucgs.com..."
$login = Invoke-RestMethod -Uri "$baseUrl/auth/v1/token?grant_type=password" -Method Post `
    -Headers @{ "apikey" = $anonKey; "Content-Type" = "application/json" } `
    -Body '{"email":"medico2@ucgs.com","password":"123456"}'
$jwt = $login.access_token
$userId = $login.user.id
Write-Host ">> Sucesso! User ID: $userId"

$h = @{
    "apikey"        = $anonKey
    "Authorization" = "Bearer $jwt"
    "Content-Type"  = "application/json"
    "Prefer"        = "return=representation"
}

# 2. Obter um Paciente Aleatório
Write-Host "[2/6] Buscando um paciente no banco..."
$pacientes = Invoke-RestMethod -Uri "$baseUrl/rest/v1/pacientes?limit=1" -Method Get -Headers $h
$pacienteId = $pacientes[0].id
Write-Host ">> Paciente selecionado: $pacienteId"

# 3. POST (Inserir)
Write-Host "[3/6] POST - Inserindo alergia a frutos do mar..."
$bodyPost = @{
    paciente_id = $pacienteId
    tipo        = "alergia"
    descricao   = "Alergia grave a camarão"
    severidade  = "grave"
    criado_por  = $userId
}
$postRes = Invoke-RestMethod -Uri "$baseUrl/rest/v1/restricoes_alimentares_paciente" -Method Post -Headers $h -Body ($bodyPost | ConvertTo-Json)
$registroId = $postRes[0].id
Write-Host ">> Inserido com sucesso! ID gerado: $registroId"

# 4. GET (Ler)
Write-Host "[4/6] GET - Listando restrições do paciente..."
$getRes = Invoke-RestMethod -Uri "$baseUrl/rest/v1/restricoes_alimentares_paciente?paciente_id=eq.$pacienteId" -Method Get -Headers $h
Write-Host ">> Total de restrições do paciente: $($getRes.Count)"
Write-Host "   Restrição: $($getRes[0].descricao) (Severidade: $($getRes[0].severidade))"

# 5. PATCH (Atualizar)
Write-Host "[5/6] PATCH - Atualizando severidade para moderada..."
$bodyPatch = @{ severidade = "moderada" }
$patchRes = Invoke-RestMethod -Uri "$baseUrl/rest/v1/restricoes_alimentares_paciente?id=eq.$registroId" -Method Patch -Headers $h -Body ($bodyPatch | ConvertTo-Json)
Write-Host ">> Atualizado com sucesso! Nova severidade: $($patchRes[0].severidade)"

# 6. DELETE (Excluir)
Write-Host "[6/6] DELETE - Excluindo o registro de teste..."
Invoke-RestMethod -Uri "$baseUrl/rest/v1/restricoes_alimentares_paciente?id=eq.$registroId" -Method Delete -Headers $h
Write-Host ">> Registro excluído com sucesso!"

Write-Host "--- TODOS OS TESTES PASSARAM! ---"
