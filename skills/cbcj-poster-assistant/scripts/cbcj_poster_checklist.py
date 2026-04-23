"""
CBCJ 2026 - Checklist de Validação do Pôster Eletrônico
Congresso Brasileiro de Cirurgia do Joelho
Script: cbcj_poster_checklist.py
"""

def validar_poster():
    print("=" * 60)
    print("  CBCJ 2026 — Checklist de Pôster Eletrônico")
    print("  20º Congresso Brasileiro de Cirurgia do Joelho")
    print("=" * 60)
    print()

    criterios_obrigatorios = [
        ("FORMATO", [
            "Arquivo está em .ppt ou .pptx?",
            "Total de slides não ultrapassa 10?",
            "Idioma é português ou inglês?",
        ]),
        ("CONTEÚDO CIENTÍFICO", [
            "Título é claro e relevante?",
            "Introdução formula o problema claramente?",
            "Objetivos são específicos e adequados?",
            "Metodologia inclui: amostra, variáveis, análise estatística?",
            "Resultados são claros e coerentes com os objetivos?",
            "Conclusão é adequada aos objetivos e achados?",
            "Referências seguem as normas RBO (http://www.rbo.org.br)?",
        ]),
        ("CONFORMIDADE", [
            "Nomes de autores AUSENTES no título e corpo do trabalho?",
            "Instituições AUSENTES no título e corpo do trabalho?",
            "Trabalho NÃO promove empresas ou produtos comerciais?",
            "Número de autores é 6 ou menos?",
            "Subgrupo temático selecionado corretamente?",
            "Abstract em inglês enviado (máx. 250 palavras)?",
        ]),
        ("QUALIDADE VISUAL", [
            "Fonte mínima de 20pt para legibilidade?",
            "Contraste adequado entre texto e fundo?",
            "Figuras em alta resolução (≥300 dpi)?",
            "Tabelas com legendas e unidades explícitas?",
            "Layout segue hierarquia visual clara?",
        ]),
    ]

    total = 0
    aprovados = 0

    for categoria, itens in criterios_obrigatorios:
        print(f"\n📋 {categoria}")
        print("-" * 40)
        for item in itens:
            resposta = input(f"  [ ] {item} (s/n): ").strip().lower()
            total += 1
            if resposta == 's':
                aprovados += 1
                print(f"      ✅ OK")
            else:
                print(f"      ❌ ATENÇÃO: Corrija antes de submeter!")

    print()
    print("=" * 60)
    percentual = (aprovados / total) * 100
    print(f"  RESULTADO: {aprovados}/{total} critérios aprovados ({percentual:.0f}%)")
    print()

    if percentual == 100:
        print("  🏆 EXCELENTE! Pôster pronto para submissão.")
    elif percentual >= 80:
        print("  ✅ BOM! Revise os itens marcados como ❌ antes de submeter.")
    else:
        print("  ⚠️  ATENÇÃO! Muitos critérios precisam de correção.")
        print("      O pôster pode ser desclassificado.")

    print()
    print("  📧 Dúvidas: temalivre@mezclaeventos.com.br")
    print("  📱 WhatsApp: (21) 97310-9724")
    print("  🔗 Submissão: https://sbcj.entity.itarget.com.br/offers/4415/211")
    print("=" * 60)


if __name__ == "__main__":
    validar_poster()
