-- ==========================================
-- SCRIPT 3: TABELAS TRANSVERSAIS, VACINAS, SEG. TRABALHO E AUDITORIA
-- Integração ao Schema UCGS
-- ==========================================

-- ==========================================
-- MÓDULO: CAMADA 0 (AUDITORIA)
-- ==========================================

CREATE TABLE IF NOT EXISTS public.audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tabela TEXT NOT NULL,
    registro_id UUID NOT NULL,
    acao TEXT NOT NULL CHECK (acao IN ('INSERT', 'UPDATE', 'DELETE', 'LOGIN', 'ACESSO')),
    usuario_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    dados_antigos JSONB,
    dados_novos JSONB,
    ip_address TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- ==========================================
-- MÓDULO: CAMADA 7 (VACINAS + EXAMES CLINICOS GERAIS)
-- ==========================================

-- 1. Catálogo de Vacinas (Referência PNI)
CREATE TABLE IF NOT EXISTS public.vacinas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome TEXT NOT NULL,
    doenca_alvo TEXT,
    esquema_basico TEXT, -- Ex: 3 doses (2, 4 e 6 meses)
    idade_recomendada TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 2. Doses de Vacina Aplicadas no Paciente
CREATE TABLE IF NOT EXISTS public.doses_vacina (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    vacina_id UUID NOT NULL REFERENCES public.vacinas(id),
    profissional_id UUID NOT NULL REFERENCES public.profiles(id),
    dose TEXT NOT NULL, -- Ex: 1ª dose, Reforço
    lote TEXT,
    validade DATE,
    data_aplicacao DATE DEFAULT CURRENT_DATE NOT NULL,
    observacoes TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 3. Exames Clínicos e Laboratoriais (Resultados)
CREATE TABLE IF NOT EXISTS public.exames_clinicos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    profissional_solicitante_id UUID REFERENCES public.profiles(id),
    atendimento_id UUID REFERENCES public.atendimentos_medicos(id) ON DELETE SET NULL,
    tipo_exame TEXT NOT NULL, -- Ex: Hemograma, Raio-X Torax, Glicemia
    data_solicitacao DATE,
    data_realizacao DATE,
    resultado TEXT,
    valor_referencia TEXT,
    status TEXT DEFAULT 'solicitado' CHECK (status IN ('solicitado', 'agendado', 'realizado', 'cancelado')),
    url_laudo TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- ==========================================
-- MÓDULO: CAMADA 8 (SEGURANÇA DO TRABALHO)
-- ==========================================

-- 4. Mapas de Risco das Instalações da Clínica/Universidade
CREATE TABLE IF NOT EXISTS public.mapas_risco (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    setor TEXT NOT NULL,
    tipo_risco TEXT NOT NULL CHECK (tipo_risco IN ('fisico', 'quimico', 'biologico', 'ergonomico', 'acidente')),
    nivel_risco TEXT CHECK (nivel_risco IN ('baixo', 'medio', 'alto')),
    medidas_preventivas TEXT,
    data_inspecao DATE,
    responsavel_id UUID REFERENCES public.profiles(id),
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 5. Protocolos de Manutenção de Equipamentos
CREATE TABLE IF NOT EXISTS public.protocolos_manutencao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    equipamento TEXT NOT NULL,
    setor TEXT,
    ultima_manutencao DATE,
    proxima_manutencao DATE,
    status TEXT DEFAULT 'ok' CHECK (status IN ('ok', 'manutencao_pendente', 'em_manutencao', 'quebrado')),
    observacoes TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 6. Registro de Acidentes de Trabalho (CAT)
CREATE TABLE IF NOT EXISTS public.registro_acidentes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    funcionario_id UUID REFERENCES public.profiles(id),
    paciente_envolvido_id UUID REFERENCES public.pacientes(id), -- Se for acidente biológico com paciente-fonte
    data_hora TIMESTAMPTZ NOT NULL,
    local TEXT,
    descricao_acidente TEXT NOT NULL,
    tipo_lesao TEXT,
    conduta_imediata TEXT,
    notificado_cat BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- ==========================================
-- MÓDULO: CAMADA 9 (CROSS-MÓDULO - GENÉRICAS)
-- ==========================================

-- 7. Notificações do Sistema
CREATE TABLE IF NOT EXISTS public.notificacoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_destino_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    titulo TEXT NOT NULL,
    mensagem TEXT NOT NULL,
    lida BOOLEAN DEFAULT FALSE,
    link_acao TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 8. Condições Clínicas Genéricas (Alergias sistêmicas, Doenças, Contraindicações - Fisio/Odonto)
CREATE TABLE IF NOT EXISTS public.avaliacao_condicoes_clinicas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    modulo TEXT NOT NULL, -- Ex: 'odontologia', 'fisioterapia', 'geral'
    entidade_id UUID, -- ID da avaliacao que originou (polimórfico fraco)
    tipo TEXT NOT NULL, -- Ex: 'doenca_sistemica', 'alergia', 'contraindicacao'
    descricao TEXT NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 9. Medicamentos em Uso (Genérica - Fisio/Odonto/Psico/Geral)
CREATE TABLE IF NOT EXISTS public.medicamentos_em_uso (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    modulo TEXT NOT NULL, -- Ex: 'odontologia', 'fisioterapia', 'psicologia'
    entidade_id UUID, -- ID da avaliacao que originou
    nome_medicamento TEXT NOT NULL,
    posologia TEXT,
    motivo TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- 10. Observações Clínicas Categorizadas
CREATE TABLE IF NOT EXISTS public.observacoes_clinicas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    modulo TEXT NOT NULL,
    entidade_id UUID, 
    categoria TEXT NOT NULL, -- Ex: 'alerta_comportamental', 'orientacao_familiar'
    texto TEXT NOT NULL,
    profissional_id UUID REFERENCES public.profiles(id),
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);


-- ==========================================
-- HABILITAR RLS NAS NOVAS TABELAS
-- ==========================================
ALTER TABLE public.audit_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.vacinas ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.doses_vacina ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.exames_clinicos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.mapas_risco ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.protocolos_manutencao ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.registro_acidentes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notificacoes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.avaliacao_condicoes_clinicas ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.medicamentos_em_uso ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.observacoes_clinicas ENABLE ROW LEVEL SECURITY;

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
            'vacinas', 'doses_vacina', 'exames_clinicos', 'mapas_risco', 'protocolos_manutencao',
            'registro_acidentes', 'notificacoes', 'avaliacao_condicoes_clinicas', 'medicamentos_em_uso', 'observacoes_clinicas'
        )
    LOOP
        EXECUTE format('CREATE POLICY "Acesso Total para Autenticados - Leitura" ON public.%I FOR SELECT USING (auth.role() = ''authenticated'');', t);
        EXECUTE format('CREATE POLICY "Acesso Total para Autenticados - Insercao" ON public.%I FOR INSERT WITH CHECK (auth.role() = ''authenticated'');', t);
        EXECUTE format('CREATE POLICY "Acesso Total para Autenticados - Atualizacao" ON public.%I FOR UPDATE USING (auth.role() = ''authenticated'');', t);
        EXECUTE format('CREATE POLICY "Acesso Total para Autenticados - Exclusao" ON public.%I FOR DELETE USING (auth.role() = ''authenticated'');', t);
    END LOOP;
END $$;

-- Política restritiva para Audit Log (Ninguém apaga auditoria)
CREATE POLICY "Auditoria Leitura Admin" ON public.audit_log FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Auditoria Insercao" ON public.audit_log FOR INSERT WITH CHECK (auth.role() = 'authenticated');
