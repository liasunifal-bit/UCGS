import os, re

dashboard_dir = r'c:\Users\maria\Downloads\antigravity lias\dashboard'

# All 25 real tables from the schema
ALL_TABLES = [
    'audit_log','avaliacoes_fisio','avaliacoes_nutri','doses_vacina',
    'entradas_prontuario','evolucoes','evolucoes_sae','exames_clinicos',
    'historico_eventos','historico_manutencao','imagens_odonto',
    'mapas_risco','notificacoes','pacientes','planos_alimentares',
    'procedimentos_odonto','processos_sae','profiles','prontuarios_odonto',
    'protocolos_manutencao','restricoes_alimentares','sessoes_fisio',
    'sessoes_psicologia','snapshots_metricas','vacinas'
]

# Collect all JS and HTML file content
references = {}  # table -> list of (file, line_no, line)
for root, dirs, files in os.walk(dashboard_dir):
    for fn in files:
        if not fn.endswith(('.js', '.html', '.py')):
            continue
        fp = os.path.join(root, fn)
        rel = fp.replace(dashboard_dir + '\\', '')
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    for tbl in ALL_TABLES:
                        if tbl in line:
                            references.setdefault(tbl, []).append((rel, i, line.strip()[:80]))
        except:
            pass

print(f"{'TABELA':<30} {'REFERÊNCIAS':<6} {'ARQUIVOS'}")
print('-' * 75)

connected  = []
partial    = []
none_found = []

for tbl in sorted(ALL_TABLES):
    refs = references.get(tbl, [])
    files = sorted(set(r[0] for r in refs))
    count = len(refs)
    
    if count == 0:
        status = '[X] SEM CONEXAO'
        none_found.append(tbl)
    elif count <= 3:
        status = '[~] Parcial'
        partial.append(tbl)
    else:
        status = '[OK] Conectada'
        connected.append(tbl)
    
    file_list = ', '.join(os.path.basename(f) for f in files[:3])
    print(f"{tbl:<30} {count:<6} {status:<20} {file_list}")

print()
print(f"RESUMO: {len(connected)} conectadas | {len(partial)} parciais | {len(none_found)} sem conexão")
print()
print("SEM CONEXÃO:")
for t in none_found:
    print(f"  - {t}")
