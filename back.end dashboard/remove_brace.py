import re

file_path = 'c:/Users/maria/Downloads/antigravity lias/back.end dashboard/site nevo.HTML'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the extra brace
toast_end = "setTimeout(() => { toast.remove(); style.remove(); }, 300);\n            }, 2800);\n        };\n\n    });\n    </script>"
toast_fixed = "setTimeout(() => { toast.remove(); style.remove(); }, 300);\n            }, 2800);\n        };\n    </script>"

content = content.replace(toast_end, toast_fixed)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Brace extra removida com sucesso!")
