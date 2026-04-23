-- ==========================================
-- SCRIPT 1: NUTRIÇÃO E FISIOTERAPIA
-- Integração ao Schema UCGS
-- ==========================================

-- ==========================================
-- MÓDULO: NUTRIÇÃO
-- ==========================================

-- 1. Restrições Alimentares (Alergias, Intolerâncias) do Paciente
CREATE TABLE IF NOT EXISTS public.restricoes_alimentares_paciente (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    tipo TEXT NOT NULL CHECK (tipo IN ('alergia', 'intolerancia', 'preferencia', 'aversao', 'religiosa', 'outra')),
    descricao TEXT NOT NULL,
    severidade TEXT CHECK (severidade IN ('leve', 'moderada', 'grave')),
    criado_por UUID REFERENCES public.profiles(id),
    criado_em TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 2. Avaliações Nutricionais (Antropometria, Recordatório)
CREATE TABLE IF NOT EXISTS public.avaliacoes_nutricionais (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    nutricionista_id UUID NOT NULL REFERENCES public.profiles(id),
    atendimento_id UUID REFERENCES public.atendimentos_medicos(id) ON DELETE SET NULL,
    peso_kg NUMERIC(5,2),
    altura_cm NUMERIC(5,2),
    imc NUMERIC(4,2),
    classificacao_imc TEXT,
    circunferencia_cintura_cm NUMERIC(5,2),
    circunferencia_quadril_cm NUMERIC(5,2),
    massa_gorda_perc NUMERIC(5,2),
    massa_magra_perc NUMERIC(5,2),
    taxa_metabolica_basal NUMERIC(6,2),
    meta_calorica_kcal NUMERIC(6,2),
    observacoes_recordatorio TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 3. Planos Alimentares (Macronutrientes e Estratégia)
CREATE TABLE IF NOT EXISTS public.planos_alimentares (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    nutricionista_id UUID NOT NULL REFERENCES public.profiles(id),
    avaliacao_nutricional_id UUID REFERENCES public.avaliacoes_nutricionais(id) ON DELETE SET NULL,
    nome_plano TEXT NOT NULL,
    estrategia TEXT, -- Ex: Low Carb, Jejum Intermitente, Hipertrofia
    calorias_totais_kcal NUMERIC(6,2),
    carboidratos_g NUMERIC(6,2),
    proteinas_g NUMERIC(6,2),
    gorduras_g NUMERIC(6,2),
    agua_ml NUMERIC(6,2),
    orientacoes_gerais TEXT,
    status TEXT DEFAULT 'ativo' CHECK (status IN ('ativo', 'inativo', 'concluido')),
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 4. Refeições do Plano (Itens consolidados em JSONB conforme aprovado)
CREATE TABLE IF NOT EXISTS public.plano_refeicoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plano_alimentar_id UUID NOT NULL REFERENCES public.planos_alimentares(id) ON DELETE CASCADE,
    nome_refeicao TEXT NOT NULL, -- Ex: Café da Manhã, Almoço
    horario TIME,
    itens JSONB DEFAULT '[]'::jsonb, -- Array de objetos: [{"alimento": "Ovo", "qtd": 2, "unidade": "un", "calorias": 140}]
    substituicoes TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- ==========================================
-- MÓDULO: FISIOTERAPIA
-- (Medições mantidas em formato de TABELA conforme exigência)
-- ==========================================

-- 5. Catálogo de Exercícios (Referência)
CREATE TABLE IF NOT EXISTS public.catalogo_exercicios_fisioterapia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome TEXT NOT NULL,
    categoria TEXT, -- Ex: Alongamento, Fortalecimento, Mobilidade
    regiao_corporal TEXT,
    instrucoes TEXT,
    video_url TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 6. Avaliação de Fisioterapia (Tabela Pai)
CREATE TABLE IF NOT EXISTS public.avaliacoes_fisioterapia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    fisioterapeuta_id UUID NOT NULL REFERENCES public.profiles(id),
    atendimento_id UUID REFERENCES public.atendimentos_medicos(id) ON DELETE SET NULL,
    queixa_principal TEXT,
    hda TEXT, -- História da Doença Atual
    diagnostico_cinesiofuncional TEXT,
    inspecao_palpacao TEXT,
    objetivos_terapeuticos TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 7. Medições Fisioterapia: Escala Visual Analógica (EVA) de Dor
CREATE TABLE IF NOT EXISTS public.fisioterapia_medicoes_eva (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    avaliacao_id UUID NOT NULL REFERENCES public.avaliacoes_fisioterapia(id) ON DELETE CASCADE,
    data_medicao DATE DEFAULT CURRENT_DATE,
    nota_repouso INTEGER CHECK (nota_repouso BETWEEN 0 AND 10),
    nota_movimento INTEGER CHECK (nota_movimento BETWEEN 0 AND 10),
    local_dor TEXT,
    caracteristica_dor TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 8. Medições Fisioterapia: Goniometria (Amplitude de Movimento)
CREATE TABLE IF NOT EXISTS public.fisioterapia_medicoes_goniometria (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    avaliacao_id UUID NOT NULL REFERENCES public.avaliacoes_fisioterapia(id) ON DELETE CASCADE,
    articulacao TEXT NOT NULL,
    movimento TEXT NOT NULL, -- Ex: Flexão, Extensão, Abdução
    graus_direito NUMERIC(5,2),
    graus_esquerdo NUMERIC(5,2),
    valor_referencia NUMERIC(5,2),
    observacoes TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 9. Medições Fisioterapia: Força Muscular (Escala de Kendall 0-5)
CREATE TABLE IF NOT EXISTS public.fisioterapia_medicoes_forca (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    avaliacao_id UUID NOT NULL REFERENCES public.avaliacoes_fisioterapia(id) ON DELETE CASCADE,
    grupo_muscular TEXT NOT NULL,
    grau_forca_direito INTEGER CHECK (grau_forca_direito BETWEEN 0 AND 5),
    grau_forca_esquerdo INTEGER CHECK (grau_forca_esquerdo BETWEEN 0 AND 5),
    observacoes TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 10. Plano de Tratamento de Fisioterapia
CREATE TABLE IF NOT EXISTS public.planos_fisioterapia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    fisioterapeuta_id UUID NOT NULL REFERENCES public.profiles(id),
    avaliacao_fisioterapia_id UUID REFERENCES public.avaliacoes_fisioterapia(id) ON DELETE SET NULL,
    condutas_propostas TEXT,
    frequencia_semanal INTEGER,
    previsao_sessoes INTEGER,
    status TEXT DEFAULT 'ativo' CHECK (status IN ('ativo', 'alta', 'evasao', 'pausado')),
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 11. Exercícios do Plano de Fisioterapia (Junção com o Catálogo)
CREATE TABLE IF NOT EXISTS public.plano_fisioterapia_itens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plano_fisioterapia_id UUID NOT NULL REFERENCES public.planos_fisioterapia(id) ON DELETE CASCADE,
    exercicio_id UUID NOT NULL REFERENCES public.catalogo_exercicios_fisioterapia(id),
    series INTEGER,
    repeticoes TEXT, -- TEXT para permitir "10 a 15" ou "Até a falha"
    carga TEXT,
    observacoes_execucao TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 12. Sessões/Evoluções de Fisioterapia
CREATE TABLE IF NOT EXISTS public.sessoes_fisioterapia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plano_fisioterapia_id UUID NOT NULL REFERENCES public.planos_fisioterapia(id) ON DELETE CASCADE,
    fisioterapeuta_id UUID NOT NULL REFERENCES public.profiles(id),
    data_sessao TIMESTAMPTZ DEFAULT now() NOT NULL,
    evolucao_clinica TEXT NOT NULL, -- Como o paciente respondeu
    condutas_realizadas TEXT,
    proxima_sessao DATE,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- ==========================================
-- HABILITAR RLS NAS NOVAS TABELAS
-- ==========================================
ALTER TABLE public.restricoes_alimentares_paciente ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.avaliacoes_nutricionais ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.planos_alimentares ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.plano_refeicoes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.catalogo_exercicios_fisioterapia ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.avaliacoes_fisioterapia ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fisioterapia_medicoes_eva ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fisioterapia_medicoes_goniometria ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fisioterapia_medicoes_forca ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.planos_fisioterapia ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.plano_fisioterapia_itens ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sessoes_fisioterapia ENABLE ROW LEVEL SECURITY;

-- ==========================================
-- POLÍTICAS GENÉRICAS (Para simplificar o desenvolvimento)
-- Na prática, essas políticas devem restringir edição ao próprio autor (auth.uid())
-- Mas para facilitar a integração inicial, permitiremos leitura e escrita para todos os autenticados.
-- ==========================================
DO $$ 
DECLARE 
    t TEXT;
BEGIN 
    FOR t IN 
        SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' 
        AND table_name IN (
            'restricoes_alimentares_paciente', 'avaliacoes_nutricionais', 'planos_alimentares', 'plano_refeicoes',
            'catalogo_exercicios_fisioterapia', 'avaliacoes_fisioterapia', 'fisioterapia_medicoes_eva',
            'fisioterapia_medicoes_goniometria', 'fisioterapia_medicoes_forca', 'planos_fisioterapia',
            'plano_fisioterapia_itens', 'sessoes_fisioterapia'
        )
    LOOP
        EXECUTE format('CREATE POLICY "Acesso Total para Autenticados - Leitura" ON public.%I FOR SELECT USING (auth.role() = ''authenticated'');', t);
        EXECUTE format('CREATE POLICY "Acesso Total para Autenticados - Insercao" ON public.%I FOR INSERT WITH CHECK (auth.role() = ''authenticated'');', t);
        EXECUTE format('CREATE POLICY "Acesso Total para Autenticados - Atualizacao" ON public.%I FOR UPDATE USING (auth.role() = ''authenticated'');', t);
        EXECUTE format('CREATE POLICY "Acesso Total para Autenticados - Exclusao" ON public.%I FOR DELETE USING (auth.role() = ''authenticated'');', t);
    END LOOP;
END $$;
