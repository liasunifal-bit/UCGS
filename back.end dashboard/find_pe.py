import sys
with open("site nevo.HTML", "r", encoding="utf-8", errors="replace") as f:
    with open("pe_outputs.txt", "w", encoding="utf-8") as out:
        for i, line in enumerate(f):
            if "id=\"pe" in line or "id='pe" in line:
                out.write(f"{i}: {line.strip()}\n")
