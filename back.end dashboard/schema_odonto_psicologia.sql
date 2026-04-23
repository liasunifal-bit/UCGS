-- ==========================================
-- SCRIPT 2: ODONTOLOGIA E PSICOLOGIA
-- Integração ao Schema UCGS
-- ==========================================

-- ==========================================
-- MÓDULO: ODONTOLOGIA
-- ==========================================

-- 1. Avaliações Odontológicas (Anamnese geral, índices)
CREATE TABLE IF NOT EXISTS public.avaliacoes_odontologicas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    dentista_id UUID NOT NULL REFERENCES public.profiles(id),
    atendimento_id UUID REFERENCES public.atendimentos_medicos(id) ON DELETE SET NULL,
    motivo_consulta TEXT,
    historia_medica_odontologica TEXT,
    higiene_bucal TEXT,
    sangramento_gengival BOOLEAN DEFAULT FALSE,
    indice_placa NUMERIC(5,2),
    indice_sangramento NUMERIC(5,2),
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 2. Odontograma (1 linha por dente para suportar relatórios analíticos CPO-D)
CREATE TABLE IF NOT EXISTS public.odontograma_dentes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    avaliacao_odontologica_id UUID NOT NULL REFERENCES public.avaliacoes_odontologicas(id) ON DELETE CASCADE,
    numero_dente VARCHAR(3) NOT NULL, -- Ex: 11, 12, 36, 48
    condicao TEXT NOT NULL CHECK (condicao IN ('higido', 'carie', 'restaurado', 'ausente', 'extraido', 'coroa', 'implante', 'canal', 'selante', 'outro')),
    faces_afetadas TEXT, -- Ex: O, M, D, V, L
    observacoes TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 3. Procedimentos Odontológicos (JSONB para array simples de dentes afetados)
CREATE TABLE IF NOT EXISTS public.procedimentos_odontologicos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    dentista_id UUID NOT NULL REFERENCES public.profiles(id),
    atendimento_id UUID REFERENCES public.atendimentos_medicos(id) ON DELETE SET NULL,
    nome_procedimento TEXT NOT NULL,
    dentes_afetados JSONB DEFAULT '[]'::jsonb, -- Array simples de strings: ["11", "12"]
    valor NUMERIC(10,2),
    status TEXT DEFAULT 'planejado' CHECK (status IN ('planejado', 'em_andamento', 'concluido', 'cancelado')),
    data_realizacao TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 4. Evoluções Odontológicas (SOAP)
CREATE TABLE IF NOT EXISTS public.evolucoes_odontologicas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    dentista_id UUID NOT NULL REFERENCES public.profiles(id),
    subjetivo TEXT,
    objetivo TEXT,
    avaliacao TEXT,
    plano TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 5. Exames de Imagem Odontológicos (Radiografias, Fotos)
CREATE TABLE IF NOT EXISTS public.exames_imagem_odontologicos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    dentista_id UUID NOT NULL REFERENCES public.profiles(id),
    tipo TEXT NOT NULL CHECK (tipo IN ('panoramica', 'periapical', 'interproximal', 'tomografia', 'foto_intraoral', 'foto_extraoral', 'outro')),
    descricao TEXT,
    url_arquivo TEXT NOT NULL,
    data_exame DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);


-- ==========================================
-- MÓDULO: PSICOLOGIA
-- ==========================================

-- 6. Avaliações Psicológicas (Absorve Estado Mental e Risco 1:1)
CREATE TABLE IF NOT EXISTS public.avaliacoes_psicologicas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    psicologo_id UUID NOT NULL REFERENCES public.profiles(id),
    atendimento_id UUID REFERENCES public.atendimentos_medicos(id) ON DELETE SET NULL,
    motivo_encaminhamento TEXT,
    hda TEXT, -- História da Doença Atual (Psicológica)
    historia_familiar TEXT,
    historia_social TEXT,
    
    -- Absorção 1:1 de Estado Mental
    aparencia TEXT,
    atitude TEXT,
    consciencia TEXT,
    orientacao TEXT,
    memoria TEXT,
    pensamento TEXT,
    linguagem TEXT,
    humor_afeto TEXT,
    
    -- Absorção 1:1 de Avaliação de Risco
    risco_suicidio TEXT CHECK (risco_suicidio IN ('baixo', 'medio', 'alto', 'ausente')),
    risco_agressividade TEXT CHECK (risco_agressividade IN ('baixo', 'medio', 'alto', 'ausente')),
    fatores_protetivos TEXT,
    
    hipotese_diagnostica TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 7. Plano Terapêutico Psicológico
CREATE TABLE IF NOT EXISTS public.planos_terapeuticos_psicologia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    psicologo_id UUID NOT NULL REFERENCES public.profiles(id),
    avaliacao_psicologica_id UUID REFERENCES public.avaliacoes_psicologicas(id) ON DELETE SET NULL,
    abordagem_teorica TEXT NOT NULL, -- Ex: TCC, Psicanálise, Humanista
    frequencia_sessoes TEXT,
    previsao_alta DATE,
    status TEXT DEFAULT 'ativo' CHECK (status IN ('ativo', 'alta', 'abandono', 'encaminhado')),
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 8. Objetivos Terapêuticos da Psicologia (Tabela filha de Plano)
CREATE TABLE IF NOT EXISTS public.objetivos_terapeuticos_psicologia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plano_terapeutico_id UUID NOT NULL REFERENCES public.planos_terapeuticos_psicologia(id) ON DELETE CASCADE,
    descricao_objetivo TEXT NOT NULL,
    status TEXT DEFAULT 'em_andamento' CHECK (status IN ('nao_iniciado', 'em_andamento', 'alcancado', 'cancelado')),
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 9. Evoluções de Psicologia (Sessões com intervenções em JSONB)
CREATE TABLE IF NOT EXISTS public.evolucoes_psicologia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    psicologo_id UUID NOT NULL REFERENCES public.profiles(id),
    plano_terapeutico_id UUID REFERENCES public.planos_terapeuticos_psicologia(id) ON DELETE SET NULL,
    relato_sessao TEXT NOT NULL,
    intervencoes JSONB DEFAULT '[]'::jsonb, -- Array de strings: ["escuta ativa", "reestruturação cognitiva"]
    observacoes_comportamentais TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);


-- ==========================================
-- HABILITAR RLS NAS NOVAS TABELAS
-- ==========================================
ALTER TABLE public.avaliacoes_odontologicas ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.odontograma_dentes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.procedimentos_odontologicos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.evolucoes_odontologicas ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.exames_imagem_odontologicos ENABLE ROW LEVEL SECURITY;

ALTER TABLE public.avaliacoes_psicologicas ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.planos_terapeuticos_psicologia ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.objetivos_terapeuticos_psicologia ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.evolucoes_psicologia ENABLE ROW LEVEL SECURITY;

-- ==========================================
-- POLÍTICAS GENÉRICAS 
-- ==========================================
DO $$ 
DECLARE 
    t TEXT;
BEGIN 
    FOR t IN 
        SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' 
        AND table_name IN (
            'avaliacoes_odontologicas', 'odontograma_dentes', 'procedimentos_odontologicos', 'evolucoes_odontologicas', 'exames_imagem_odontologicos',
            'avaliacoes_psicologicas', 'planos_terapeuticos_psicologia', 'objetivos_terapeuticos_psicologia', 'evolucoes_psicologia'
        )
    LOOP
        EXECUTE format('CREATE POLICY "Acesso Total para Autenticados - Leitura" ON public.%I FOR SELECT USING (auth.role() = ''authenticated'');', t);
        EXECUTE format('CREATE POLICY "Acesso Total para Autenticados - Insercao" ON public.%I FOR INSERT WITH CHECK (auth.role() = ''authenticated'');', t);
        EXECUTE format('CREATE POLICY "Acesso Total para Autenticados - Atualizacao" ON public.%I FOR UPDATE USING (auth.role() = ''authenticated'');', t);
        EXECUTE format('CREATE POLICY "Acesso Total para Autenticados - Exclusao" ON public.%I FOR DELETE USING (auth.role() = ''authenticated'');', t);
    END LOOP;
END $$;
