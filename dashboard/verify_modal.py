with open(r'c:\Users\maria\Downloads\antigravity lias\dashboard\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
modals = re.findall('id="registerModal"', html)
print('Quantidade de #registerModal:', len(modals))

new_fields = ['regNomeCompleto','regRole','regEspecialidade','regRegistro','regMatricula','regSetor','registro_profissional','nome_completo']
print('--- Novos campos ---')
for c in new_fields:
    print(c + ': ' + ('OK' if c in html else 'AUSENTE'))

old_fields = ['regCPF', 'regTelefone', 'regCategoria']
print('--- Campos antigos ---')
for c in old_fields:
    print(c + ': ' + ('AINDA PRESENTE' if c in html else 'REMOVIDO OK'))
