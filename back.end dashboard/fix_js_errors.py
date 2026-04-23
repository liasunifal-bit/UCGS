#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

DEST = "site nevo.HTML"

with open(DEST, "r", encoding="utf-8") as f:
    content = f.read()

# ── 1. Fix 'submit is not defined' ─────────────────────────────────
# Vamos criar uma variável segura 'loginSubmitBtn' e substituir 'submit.'
# O botão no HTML provavelmente tem id="submit" ou id="loginSubmit" ou a classe '.ucgs-login-submit'
# Para garantir, vou usar '.ucgs-login-submit'
content = content.replace(
    "submit.addEventListener('click', (e) => {",
    "const loginSubmitBtn = document.querySelector('.ucgs-login-submit');\n    if(loginSubmitBtn) loginSubmitBtn.addEventListener('click', (e) => {"
)
# Substitui submit.disabled e submit.classList onde ocorrem (nas views que vimos antes)
content = re.sub(r'\bsubmit\.disabled\b', "if(document.querySelector('.ucgs-login-submit')) document.querySelector('.ucgs-login-submit').disabled", content)
content = re.sub(r'\bsubmit\.classList\b', "if(document.querySelector('.ucgs-login-submit')) document.querySelector('.ucgs-login-submit').classList", content)

# ── 2. Fix Google Sign-in 403 e Client ID not found ────────────────
# Comenta o script e a inicialização para evitar os erros 403 e warning no console
# Remove a tag <script src="https://accounts.google.com/gsi/client" async defer></script>
content = content.replace(
    '<script src="https://accounts.google.com/gsi/client" async defer></script>',
    '<!-- <script src="https://accounts.google.com/gsi/client" async defer></script> -->'
)

# Adiciona condição para não tentar inicializar o google sign-in se o ID for o dummy
gsi_init_str = "google.accounts.id.initialize({"
gsi_init_fix = "if (GOOGLE_CONFIG.CLIENT_ID.includes('000000000000')) { console.log('[UCGS] Google Sign-In desativado (Client ID padrao)'); return false; }\n    google.accounts.id.initialize({"
if gsi_init_str in content:
    content = content.replace(gsi_init_str, gsi_init_fix)

# ── 3. Salvar ──────────────────────────────────────────────────────
with open(DEST, "w", encoding="utf-8") as f:
    f.write(content)

print(f"[OK] Arquivo salvo ({len(content):,} chars)")
