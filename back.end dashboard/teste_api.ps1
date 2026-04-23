$ErrorActionPreference = "Stop"

$anonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow"
$urlLogin = "https://llqphjlpypnyvknpfdyn.supabase.co/auth/v1/token?grant_type=password"

$bodyLogin = @{
    email = "medico2@ucgs.com"
    password = "123456"
} | ConvertTo-Json

$headersLogin = @{
    "apikey" = $anonKey
    "Content-Type" = "application/json"
}

Write-Output "[1/2] Autenticando com medico2@ucgs.com..."
try {
    $responseLogin = Invoke-RestMethod -Uri $urlLogin -Method Post -Headers $headersLogin -Body $bodyLogin
    $jwt = $responseLogin.access_token
    Write-Output ">> Sucesso! JWT gerado."
} catch {
    Write-Error "Falha no login: $_"
    exit
}

Write-Output "`n[2/2] Inserindo paciente com o JWT (Testando RLS)..."
$urlInsert = "https://llqphjlpypnyvknpfdyn.supabase.co/rest/v1/pacientes"
$headersInsert = @{
    "apikey" = $anonKey
    "Authorization" = "Bearer $jwt"
    "Content-Type" = "application/json"
    "Prefer" = "return=representation"
}

# Gerando um CPF aleatório para evitar erro de UNIQUE caso seja rodado mais de uma vez
$randomCpf = "{0:D3}.{1:D3}.{2:D3}-99" -f (Get-Random -Maximum 999), (Get-Random -Maximum 999), (Get-Random -Maximum 999)

$bodyInsert = @{
    nome = "Paciente Teste via Powershell"
    cpf = $randomCpf
    nascimento = "1990-01-01"
    sexo = "F"
    cidade = "São Paulo"
} | ConvertTo-Json

try {
    $responseInsert = Invoke-RestMethod -Uri $urlInsert -Method Post -Headers $headersInsert -Body $bodyInsert
    Write-Output ">> SUCESSO ABSOLUTO! O RLS permitiu a inserção. Retorno do banco:"
    $responseInsert | ConvertTo-Json -Depth 3
} catch {
    Write-Error "Falha na inserção. O RLS ou a formatação barrou: $_"
}
