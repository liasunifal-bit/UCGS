#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Lucide initialization: move script to end of body for synchronous execution.
"""

DEST = "site nevo.HTML"

with open(DEST, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove current Lucide script from <head> if present
old_head_script = '\n    <!-- Lucide Icons (SVG, sem dependência de fonte) -->\n    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>\n'
old_head_script2 = '\n    <!-- Lucide Icons (SVG, sem dependência de fonte) -->\n    <script src="lucide.min.js"></script>\n'
old_head_script3 = '\n    <script src="lucide.min.js"></script>\n'

for old in [old_head_script, old_head_script2, old_head_script3]:
    content = content.replace(old, "\n")

# 2. Remove old init blocks if present
old_init_block = content.find("(function() {\n        function initLucide()")
if old_init_block > 0:
    # Find the script tag wrapping it
    start = content.rfind("<script>", 0, old_init_block)
    end = content.find("</script>", old_init_block) + len("</script>")
    if start > 0 and end > 0:
        content = content[:start] + content[end:]
        print("[1] Bloco init antigo removido do head")

old_init_block2 = content.find("// Inicializa Lucide Icons ap")
if old_init_block2 > 0:
    start = content.rfind("<script>", 0, old_init_block2)
    end = content.find("</script>", old_init_block2) + len("</script>")
    if start > 0 and end > 0:
        content = content[:start] + content[end:]
        print("[1b] Bloco init antigo #2 removido")

# 3. Inject Lucide at END of body with immediate synchronous call
LUCIDE_BOTTOM = """
    <!-- Lucide Icons: carregado no fim do body para garantir DOM completo -->
    <script src="lucide.min.js"></script>
    <script>
        // Inicializa imediatamente (DOM já está pronto pois script é o último elemento)
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
            console.log('[UCGS] Lucide icons inicializados:', document.querySelectorAll('[data-lucide]').length, 'icones');
        } else {
            console.warn('[UCGS] Lucide nao carregou!');
        }
        // Expor para re-uso em SPAs / navegacao dinamica
        window._lucideRefresh = function() {
            if (typeof lucide !== 'undefined') lucide.createIcons();
        };
        // Observar novos elementos adicionados ao DOM
        if (typeof MutationObserver !== 'undefined') {
            var _lcObserver = new MutationObserver(function(muts) {
                var hasNewIcons = muts.some(function(m) {
                    return Array.from(m.addedNodes).some(function(n) {
                        return n.nodeType === 1 && (n.hasAttribute('data-lucide') || (n.querySelector && n.querySelector('[data-lucide]')));
                    });
                });
                if (hasNewIcons && typeof lucide !== 'undefined') lucide.createIcons();
            });
            _lcObserver.observe(document.body, { childList: true, subtree: true });
        }
    </script>
"""

if "lucide.min.js" not in content:
    content = content.replace("</body>", LUCIDE_BOTTOM + "</body>", 1)
    print("[2] Lucide injetado no fim do body")
else:
    print("[2] AVISO: lucide.min.js ainda presente em algum lugar no arquivo")
    # Force inject at end of body regardless
    content = content.replace("</body>", LUCIDE_BOTTOM + "</body>", 1)
    print("[2] Lucide re-injetado no fim do body (forçado)")

# 4. Save
with open(DEST, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[OK] Salvo ({len(content):,} chars)")
print("Pressione Ctrl+F5 no navegador.")
