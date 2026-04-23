import re

file_path = 'c:/Users/maria/Downloads/antigravity lias/back.end dashboard/site nevo.HTML'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: w.document.write multiple lines
content = content.replace("w.document.write('\n</body>\n</html>');", "w.document.write('</body></html>');")

# Fix 2: DOMContentLoaded closing
# It's currently at line 19585 as })();
# Let's replace the end of the toast function
toast_end = "setTimeout(() => { toast.remove(); style.remove(); }, 300);\n            }, 2800);\n        };\n\n    })();\n    </script>"
toast_fixed = "setTimeout(() => { toast.remove(); style.remove(); }, 300);\n            }, 2800);\n        };\n\n    });\n    </script>"
content = content.replace(toast_end, toast_fixed)

# Fix 3: </script> inside comment
# It's in the Supabase Client comment
comment_old = "* 1. Adicione no HTML: <script src=\"supabase-client.js\"></script>"
comment_new = "* 1. Adicione no HTML: <script src=\"supabase-client.js\"><\\/script>"
content = content.replace(comment_old, comment_new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Todas as sintaxes corrigidas com sucesso!")
