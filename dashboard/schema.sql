-- =============================================================================
-- UCGS — Universidade + Comunidade + Gestão em Saúde
-- Schema SQL para Supabase (PostgreSQL 15+)
-- Gerado em: 18/04/2026
-- Baseado em: sistema_UCGS_atualizado_v25 (1).html — 15/15 módulos mapeados
-- =============================================================================
-- ORDEM DE EXECUÇÃO:
--   1. Extensions
--   2. Funções auxiliares (triggers)
--   3. Tabelas de infraestrutura (profiles, audit_log, notificacoes)
--   4. Tabelas clínicas por módulo
--   5. Índices
--   6. RLS Policies
--   7. Triggers
--   8. Storage buckets (comentado — executar via Dashboard do Supabase)
-- =============================================================================


-- ============================================================================
-- 1. EXTENSIONS
-- ============================================================================
CREATE EXTENSION IF NOT EXISTS "pgcrypto";     -- gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "unaccent";     -- busca sem acento
CREATE EXTENSION IF NOT EXISTS "pg_trgm";      -- busca fuzzy (LIKE rápido)


-- ============================================================================
-- 2. FUNÇÕES AUXILIARES
-- ============================================================================

-- Função: Atualiza updated_at automaticamente
CREATE OR REPLACE FUNCTION public.fn_set_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$;

-- Função: Gera número de prontuário sequencial (PRN-000001)
CREATE OR REPLACE FUNCTION public.fn_gerar_prontuario()
RETURNS text
LANGUAGE plpgsql
AS $$
DECLARE
  proximo_numero integer;
BEGIN
  proximo_numero := (
    SELECT COALESCE(MAX(CAST(SUBSTRING(prontuario FROM 5) AS integer)), 0) + 1
    FROM public.pacientes
  );
  RETURN 'PRN-' || LPAD(proximo_numero::text, 6, '0');
END;
$$;

-- Função: Audit log genérico
CREATE OR REPLACE FUNCTION public.fn_audit_log()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_usuario_id uuid;
BEGIN
  -- Tenta pegar o usuário logado via Supabase JWT
  BEGIN
    v_usuario_id := (auth.uid())::uuid;
  EXCEPTION WHEN OTHERS THEN
    v_usuario_id := NULL;
  END;

  INSERT INTO public.audit_log (
    tabela, operacao, registro_id, usuario_id, dados_antes, dados_depois
  ) VALUES (
    TG_TABLE_NAME,
    TG_OP,
    CASE WHEN TG_OP = 'DELETE' THEN OLD.id ELSE NEW.id END,
    v_usuario_id,
    CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN to_jsonb(OLD) ELSE NULL END,
    CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN to_jsonb(NEW) ELSE NULL END
  );

  RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$;

-- Função: Retorna role do usuário atual
CREATE OR REPLACE FUNCTION public.fn_get_my_role()
RETURNS text
LANGUAGE plpgsql
STABLE
SECURITY DEFINER
AS $$
BEGIN
  RETURN (SELECT role FROM public.profiles WHERE id = auth.uid() LIMIT 1);
END;
$$;

-- Função: Verifica se usuário é admin
CREATE OR REPLACE FUNCTION public.fn_is_admin()
RETURNS boolean
LANGUAGE plpgsql
STABLE
SECURITY DEFINER
AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'admin'
  );
END;
$$;

-- Função: Notificação automática de vencimento (usada por triggers)
CREATE OR REPLACE FUNCTION public.fn_notificar_vencimento()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_titulo text;
  v_mensagem text;
  v_ref_tabela text := TG_TABLE_NAME;
BEGIN
  IF TG_TABLE_NAME = 'doses_vacina' THEN
    IF NEW.data_validade IS NOT NULL AND NEW.data_validade <= (NOW() + INTERVAL '30 days')::date THEN
      v_titulo := 'Vacina vencendo em breve';
      v_mensagem := 'Dose de vacina para o paciente vence em ' || TO_CHAR(NEW.data_validade, 'DD/MM/YYYY');
      INSERT INTO public.notificacoes (usuario_id, titulo, mensagem, tipo, referencia_tabela, referencia_id)
        SELECT id, v_titulo, v_mensagem, 'vacinas', v_ref_tabela, NEW.id
        FROM public.profiles WHERE role IN ('admin', 'enfermeiro', 'sesmt') AND ativo = true;
    END IF;
  END IF;

  IF TG_TABLE_NAME = 'protocolos_manutencao' THEN
    IF NEW.data_proxima_manutencao IS NOT NULL AND NEW.data_proxima_manutencao <= (NOW() + INTERVAL '7 days')::date THEN
      v_titulo := 'Manutenção programada se aproximando';
      v_mensagem := 'Protocolo de manutenção vence em ' || TO_CHAR(NEW.data_proxima_manutencao, 'DD/MM/YYYY');
      INSERT INTO public.notificacoes (usuario_id, titulo, mensagem, tipo, referencia_tabela, referencia_id)
        SELECT id, v_titulo, v_mensagem, 'protocolos', v_ref_tabela, NEW.id
        FROM public.profiles WHERE role IN ('admin', 'sesmt') AND ativo = true;
    END IF;
  END IF;

  RETURN NEW;
END;
$$;


-- ============================================================================
-- 3. TABELAS DE INFRAESTRUTURA
-- ============================================================================

-- 3.1 Profiles (espelho de auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
  id                   uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  nome_completo        text NOT NULL,
  email                text NOT NULL,
  avatar_url           text,
  iniciais             text GENERATED ALWAYS AS (
    UPPER(SUBSTRING(nome_completo FROM 1 FOR 1)) ||
    COALESCE(UPPER(SUBSTRING(REVERSE(SPLIT_PART(nome_completo, ' ', -1)) FROM LENGTH(SPLIT_PART(nome_completo, ' ', -1)) FOR 1)), '')
  ) STORED,
  role                 text NOT NULL DEFAULT 'enfermeiro'
                         CHECK (role IN ('admin','medico','enfermeiro','fisio','dentista','psicologo','nutricionista','sesmt')),
  especialidade        text,
  registro_profissional text,          -- CRM / COREN / CRO / CFP / CRN / CREFITO
  matricula            text,           -- Ex: UCGS-2024-0847
  setor                text,
  preferencias         jsonb NOT NULL DEFAULT '{
    "tema": "dark",
    "notificacoes": {"vacinas": true, "protocolos": true, "urgentes": true},
    "pagina_inicial": "dashboard",
    "densidade_tabela": "confortavel"
  }'::jsonb,
  ativo                boolean NOT NULL DEFAULT true,
  created_at           timestamptz NOT NULL DEFAULT NOW(),
  updated_at           timestamptz NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.profiles IS 'Espelho de auth.users — dados de perfil dos profissionais de saúde';
COMMENT ON COLUMN public.profiles.role IS 'Papel do usuário: admin | medico | enfermeiro | fisio | dentista | psicologo | nutricionista | sesmt';

-- 3.2 Audit Log
CREATE TABLE IF NOT EXISTS public.audit_log (
  id          bigserial PRIMARY KEY,
  tabela      text NOT NULL,
  operacao    text NOT NULL CHECK (operacao IN ('INSERT','UPDATE','DELETE')),
  registro_id uuid,
  usuario_id  uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  dados_antes jsonb,
  dados_depois jsonb,
  ip_address  inet,
  created_at  timestamptz NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.audit_log IS 'Log de auditoria de todas as operações críticas do sistema';

-- 3.3 Notificações
CREATE TABLE IF NOT EXISTS public.notificacoes (
  id                 uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  usuario_id         uuid NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  titulo             text NOT NULL,
  mensagem           text,
  tipo               text NOT NULL DEFAULT 'info'
                       CHECK (tipo IN ('vacinas','protocolos','urgente','info','sucesso','acidente')),
  lida               boolean NOT NULL DEFAULT false,
  referencia_tabela  text,
  referencia_id      uuid,
  created_at         timestamptz NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.notificacoes IS 'Notificações internas do sistema para os profissionais';


-- ============================================================================
-- 4. TABELAS CLÍNICAS POR MÓDULO
-- ============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- 4.1 MÓDULO PACIENTES
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.pacientes (
  id                   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  prontuario           text UNIQUE,             -- Gerado por fn_gerar_prontuario()
  nome                 text NOT NULL,
  data_nascimento      date,
  sexo                 text CHECK (sexo IN ('M','F','O')),
  cpf                  text UNIQUE,
  telefone             text,
  email                text,
  endereco             jsonb DEFAULT '{}',      -- {logradouro, numero, complemento, bairro, cidade, uf, cep}
  observacoes_clinicas text,                    -- Alergias, condições crônicas, medicações
  status               text NOT NULL DEFAULT 'ativo'
                         CHECK (status IN ('ativo','inativo','alta','obito')),
  categoria            text NOT NULL DEFAULT 'interno'
                         CHECK (categoria IN ('interno','funcionario')),  -- Contexto prisional
  foto_url             text,
  deleted_at           timestamptz,             -- Soft delete
  created_at           timestamptz NOT NULL DEFAULT NOW(),
  updated_at           timestamptz NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.pacientes IS 'Cadastro central de pacientes — internos e funcionários da unidade';

-- Trigger para gerar prontuário automaticamente
CREATE OR REPLACE FUNCTION public.fn_auto_prontuario()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.prontuario IS NULL THEN
    NEW.prontuario := public.fn_gerar_prontuario();
  END IF;
  RETURN NEW;
END;
$$;

CREATE TRIGGER trg_pacientes_prontuario
  BEFORE INSERT ON public.pacientes
  FOR EACH ROW EXECUTE FUNCTION public.fn_auto_prontuario();


-- ─────────────────────────────────────────────────────────────────────────────
-- 4.2 MÓDULO PRONTUÁRIO ELETRÔNICO (Entradas consolidadas)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.entradas_prontuario (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  paciente_id     uuid NOT NULL REFERENCES public.pacientes(id) ON DELETE RESTRICT,
  profissional_id uuid NOT NULL REFERENCES public.profiles(id) ON DELETE RESTRICT,
  especialidade   text NOT NULL
                    CHECK (especialidade IN ('medico','enfermagem','fisio','odonto','psi','nutricao','sesmt')),
  tipo_entrada    text NOT NULL
                    CHECK (tipo_entrada IN ('evolucao','prescricao','exame','procedimento','enfermagem','intercorrencia','alta')),
  data_entrada    timestamptz NOT NULL DEFAULT NOW(),
  titulo          text NOT NULL,
  conteudo        text,
  dados_extras    jsonb DEFAULT '{}',  -- Campos específicos por especialidade
  status          text NOT NULL DEFAULT 'finalizado'
                    CHECK (status IN ('rascunho','finalizado','assinado')),
  created_at      timestamptz NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.entradas_prontuario IS 'Timeline consolidada de todas as evoluções multidisciplinares por paciente';


-- ─────────────────────────────────────────────────────────────────────────────
-- 4.3 MÓDULO MAPA DE RISCO
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.mapas_risco (
  id                        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  setor                     text NOT NULL,
  tipo_risco_predominante   text NOT NULL DEFAULT 'biologico'
                              CHECK (tipo_risco_predominante IN ('biologico','fisico','quimico','ergonomico','outros')),
  nivel_risco               text NOT NULL DEFAULT 'medio'
                              CHECK (nivel_risco IN ('baixo','medio','alto','critico')),
  status                    text NOT NULL DEFAULT 'em_dia'
                              CHECK (status IN ('em_dia','proximo_vencimento','vencido')),
  data_ultima_revisao       date,
  data_proxima_revisao      date,
  periodicidade_meses       integer NOT NULL DEFAULT 6,
  imagem_url                text,
  descricao                 text,
  responsavel_id            uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  created_by                uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  deleted_at                timestamptz,
  created_at                timestamptz NOT NULL DEFAULT NOW(),
  updated_at                timestamptz NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.mapas_risco IS 'Mapas de risco do PPRA/PGR por setor da unidade';


-- ─────────────────────────────────────────────────────────────────────────────
-- 4.4 MÓDULO PROTOCOLO DE MANUTENÇÃO
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.protocolos_manutencao (
  id                       uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  equipamento              text NOT NULL,
  equipamento_icone        text,
  tipo_manutencao          text NOT NULL
                             CHECK (tipo_manutencao IN ('preventiva','corretiva','verificacao_estoque','reposicao')),
  periodicidade            text NOT NULL
                             CHECK (periodicidade IN ('semanal','mensal','trimestral','semestral','anual')),
  data_ultima_manutencao   date,
  data_proxima_manutencao  date,
  status                   text NOT NULL DEFAULT 'ok'
                             CHECK (status IN ('ok','proximo','em_atraso','programado')),
  responsavel_id           uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  observacoes              text,
  checklist                jsonb DEFAULT '[]',  -- [{item, concluido, obs}]
  created_at               timestamptz NOT NULL DEFAULT NOW(),
  updated_at               timestamptz NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.historico_manutencao (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  protocolo_id    uuid NOT NULL REFERENCES public.protocolos_manutencao(id) ON DELETE CASCADE,
  realizado_por_id uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  data_execucao   timestamptz NOT NULL DEFAULT NOW(),
  tipo            text NOT NULL CHECK (tipo IN ('preventiva','corretiva','reposicao','verificacao')),
  descricao       text,
  checklist_snap  jsonb DEFAULT '[]',  -- Snapshot do checklist na data da execução
  created_at      timestamptz NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.protocolos_manutencao IS 'Protocolos de manutenção de equipamentos de segurança';


-- ─────────────────────────────────────────────────────────────────────────────
-- 4.5 MÓDULO VACINAS
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.vacinas (
  id                       uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  nome                     text NOT NULL UNIQUE,
  doses_recomendadas       integer NOT NULL DEFAULT 1,
  intervalo_reforco_meses  integer,
  descricao                text,
  created_at               timestamptz NOT NULL DEFAULT NOW()
);

-- Seed com vacinas padrão
INSERT INTO public.vacinas (nome, doses_recomendadas, intervalo_reforco_meses) VALUES
  ('Hepatite B', 3, NULL),
  ('Tétano (dT/dTpa)', 3, 120),        -- Reforço a cada 10 anos
  ('Influenza', 1, 12),                 -- Anual
  ('COVID-19', 2, NULL),
  ('Febre Amarela', 1, NULL),
  ('Hepatite A', 2, NULL)
ON CONFLICT (nome) DO NOTHING;

CREATE TABLE IF NOT EXISTS public.doses_vacina (
  id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  paciente_id      uuid NOT NULL REFERENCES public.pacientes(id) ON DELETE RESTRICT,
  vacina_id        uuid NOT NULL REFERENCES public.vacinas(id) ON DELETE RESTRICT,
  numero_dose      integer NOT NULL DEFAULT 1,
  data_aplicacao   date NOT NULL,
  data_validade    date,
  aplicado_por_id  uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  lote             text,
  local_aplicacao  text,
  status           text NOT NULL DEFAULT 'ok'
                     CHECK (status IN ('ok','vencendo','vencido','pendente')),
  observacoes      text,
  created_at       timestamptz NOT NULL DEFAULT NOW(),
  UNIQUE (paciente_id, vacina_id, numero_dose)
);

COMMENT ON TABLE public.doses_vacina IS 'Cartão vacinal individual — registro de cada dose aplicada';


-- ─────────────────────────────────────────────────────────────────────────────
-- 4.6 MÓDULO EXAMES CLÍNICOS
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.exames_clinicos (
  id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  paciente_id      uuid NOT NULL REFERENCES public.pacientes(id) ON DELETE RESTRICT,
  solicitante_id   uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  nome_exame       text NOT NULL,
  tipo             text NOT NULL CHECK (tipo IN ('laboratorial','imagem','outro')),
  categoria        text,                   -- Ex: "Hematologia", "Radiologia"
  data_solicitacao date,
  data_coleta      date,
  data_resultado   date,
  resultado_valor  text,
  unidade          text,                   -- Ex: "mg/dL"
  referencia_min   numeric,
  referencia_max   numeric,
  referencia_texto text,                   -- Para exames qualitativos (Reagente/Não Reagente)
  status           text NOT NULL DEFAULT 'normal'
                     CHECK (status IN ('normal','alerta','critico','pendente')),
  arquivo_url      text,                   -- Storage: laudo PDF / imagem
  observacoes      text,
  created_at       timestamptz NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.exames_clinicos IS 'Resultados de exames laboratoriais e de imagem por paciente';


-- ─────────────────────────────────────────────────────────────────────────────
-- 4.7 MÓDULO PROCESSO DE ENFERMAGEM / SAE
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.processos_sae (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  paciente_id             uuid NOT NULL REFERENCES public.pacientes(id) ON DELETE RESTRICT,
  enfermeiro_id           uuid NOT NULL REFERENCES public.profiles(id) ON DELETE RESTRICT,
  data_atendimento        date NOT NULL DEFAULT CURRENT_DATE,
  hora_atendimento        time NOT NULL DEFAULT CURRENT_TIME,
  coren                   text,                 -- Registro COREN do enfermeiro
  setor_paciente          text,                 -- Setor/local de trabalho do paciente
  funcao_paciente         text,                 -- Cargo/função
  tipo_risco_ocupacional  text
                            CHECK (tipo_risco_ocupacional IN ('biologico','fisico','quimico','ergonomico','acidente','nenhum')),
  tempo_exposicao         text,
  -- ETAPA 1: COLETA
  queixa_principal        text NOT NULL,
  historico_doencas       text,
  sinais_vitais           jsonb DEFAULT '{}',   -- {pa, fc, fr, temp, spo2, eva}
  achados_exame_fisico    jsonb DEFAULT '{}',   -- Checkboxes selecionados
  obs_exame_fisico        text,
  -- ETAPA 2: DIAGNÓSTICO NANDA
  diagnosticos_nanda      jsonb DEFAULT '[]',   -- [{codigo, nome, descricao, categoria, selecionado}]
  -- ETAPA 3: PLANEJAMENTO NOC/NIC
  planejamento_noc        jsonb DEFAULT '[]',   -- [{codigo, nome, descricao}]
  planejamento_nic        jsonb DEFAULT '[]',   -- [{codigo, nome, descricao}]
  meta_criterios          text,
  -- CONTROLE
  status                  text NOT NULL DEFAULT 'rascunho'
                            CHECK (status IN ('rascunho','em_andamento','finalizado')),
  deleted_at              timestamptz,
  created_at              timestamptz NOT NULL DEFAULT NOW(),
  updated_at              timestamptz NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.evolucoes_sae (
  id                        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  sae_id                    uuid NOT NULL REFERENCES public.processos_sae(id) ON DELETE CASCADE,
  enfermeiro_id             uuid NOT NULL REFERENCES public.profiles(id) ON DELETE RESTRICT,
  data_evolucao             date NOT NULL DEFAULT CURRENT_DATE,
  hora_evolucao             time NOT NULL DEFAULT CURRENT_TIME,
  tipo_registro             text NOT NULL DEFAULT 'evolucao_clinica'
                              CHECK (tipo_registro IN ('evolucao_clinica','intercorrencia','procedimento','alta','reavaliacao')),
  texto_soap                text NOT NULL,       -- Formato S/O/A/P
  diagnostico_relacionado   text,                -- Código NANDA relacionado
  tags                      jsonb DEFAULT '[]',
  created_at                timestamptz NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.processos_sae IS 'SAE — Sistematização da Assistência de Enfermagem com fluxo NANDA→NOC→NIC';


-- ─────────────────────────────────────────────────────────────────────────────
-- 4.8 MÓDULO NUTRIÇÃO
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.avaliacoes_nutri (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  paciente_id         uuid NOT NULL REFERENCES public.pacientes(id) ON DELETE RESTRICT,
  nutricionista_id    uuid NOT NULL REFERENCES public.profiles(id) ON DELETE RESTRICT,
  data_avaliacao      date NOT NULL DEFAULT CURRENT_DATE,
  peso_kg             numeric(5,2),
  altura_m            numeric(4,2),
  idade               integer,
  sexo                text CHECK (sexo IN ('M','F')),
  circ_abdominal_cm   numeric(5,1),
  circ_braco_cm       numeric(5,1),
  gordura_pct         numeric(5,2),
  nivel_atividade     numeric(3,2) DEFAULT 1.2,  -- Fator de atividade (1.2-1.9)
  imc                 numeric(5,2) GENERATED ALWAYS AS (
    CASE WHEN altura_m > 0 THEN ROUND((peso_kg / (altura_m * altura_m))::numeric, 2) ELSE NULL END
  ) STORED,
  classificacao_imc   text
                        CHECK (classificacao_imc IN ('abaixo_peso','normal','sobrepeso','obesidade_i','obesidade_ii','obesidade_iii')),
  tmb_harris          numeric(7,2),
  get_calculado       numeric(7,2),
  meta_calorica       numeric(7,2),
  objetivo            text CHECK (objetivo IN ('manutencao','perda_peso','ganho_peso')),
  obs_clinicas        text,
  created_at          timestamptz NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.planos_alimentares (
  id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  paciente_id      uuid NOT NULL REFERENCES public.pacientes(id) ON DELETE RESTRICT,
  nutricionista_id uuid NOT NULL REFERENCES public.profiles(id) ON DELETE RESTRICT,
  data_prescricao  date NOT NULL DEFAULT CURRENT_DATE,
  kcal_total       numeric(7,2),
  carb_g           numeric(6,2),
  prot_g           numeric(6,2),
  lip_g            numeric(6,2),
  refeicoes        jsonb DEFAULT '[]',  -- [{nome, horario, alimentos: [{nome, qtd, kcal, carb, prot, lip}]}]
  status           text NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo','arquivado')),
  created_at       timestamptz NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.restricoes_alimentares (
  id                   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  paciente_id          uuid NOT NULL UNIQUE REFERENCES public.pacientes(id) ON DELETE CASCADE,
  alergias             jsonb DEFAULT '[]',          -- ["Amendoim", "Lactose"...]
  intolerancias        jsonb DEFAULT '[]',
  dietas_terapeuticas  jsonb DEFAULT '[]',          -- ["Diabetica", "Hipossodica"...]
  preferencias         jsonb DEFAULT '[]',          -- ["Halal", "Vegana"...]
  obs_adicionais       text,
  updated_at           timestamptz NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.avaliacoes_nutri IS 'Avaliação antropométrica e nutricional com cálculo de IMC automático';


-- ─────────────────────────────────────────────────────────────────────────────
-- 4.9 MÓDULO FISIOTERAPIA
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.avaliacoes_fisio (
  id                   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  paciente_id          uuid NOT NULL REFERENCES public.pacientes(id) ON DELETE RESTRICT,
  fisioterapeuta_id    uuid NOT NULL REFERENCES public.profiles(id) ON DELETE RESTRICT,
  data_avaliacao       timestamptz NOT NULL DEFAULT NOW(),
  diagnostico_fisio    text,
  queixa_principal     text,
  historia_clinica     text,
  avaliacao_postural   jsonb DEFAULT '{}',         -- {segmento: achado}
  amplitude_movimento  jsonb DEFAULT '{}',         -- {articulacao: {dir_graus, esq_graus}}
  testes_especiais     jsonb DEFAULT '[]',         -- [{teste, resultado, obs}]
  escala_dor_inicial   integer CHECK (escala_dor_inicial BETWEEN 0 AND 10),
  objetivos            text,
  plano_tratamento     jsonb DEFAULT '{}',         -- {exercicios, frequencia, carga}
  sessoes_previstas    integer,
  status               text NOT NULL DEFAULT 'ativo'
                         CHECK (status IN ('ativo','alta','suspenso')),
  created_at           timestamptz NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.sessoes_fisio (
  id                   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  avaliacao_id         uuid NOT NULL REFERENCES public.avaliacoes_fisio(id) ON DELETE CASCADE,
  paciente_id          uuid NOT NULL REFERENCES public.pacientes(id) ON DELETE RESTRICT,
  fisioterapeuta_id    uuid NOT NULL REFERENCES public.profiles(id) ON DELETE RESTRICT,
  data_sessao          date NOT NULL DEFAULT CURRENT_DATE,
  numero_sessao        integer NOT NULL,
  comparecimento       boolean NOT NULL DEFAULT true,
  escala_dor_inicio    integer CHECK (escala_dor_inicio BETWEEN 0 AND 10),
  escala_dor_fim       integer CHECK (escala_dor_fim BETWEEN 0 AND 10),
  exercicios_realizados jsonb DEFAULT '[]',
  evolucao             text,
  created_at           timestamptz NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.avaliacoes_fisio IS 'Avaliação fisioterapêutica com amplitude de movimento e plano de tratamento';


-- ─────────────────────────────────────────────────────────────────────────────
-- 4.10 MÓDULO ODONTOLOGIA
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.prontuarios_odonto (
  id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  paciente_id       uuid NOT NULL REFERENCES public.pacientes(id) ON DELETE RESTRICT,
  dentista_id       uuid NOT NULL REFERENCES public.profiles(id) ON DELETE RESTRICT,
  data_avaliacao    timestamptz NOT NULL DEFAULT NOW(),
  odontograma       jsonb DEFAULT '{}',   -- {dente_11: {status, faces, obs}, ...}
  cpod_c            integer NOT NULL DEFAULT 0,   -- Cariados
  cpod_p            integer NOT NULL DEFAULT 0,   -- Perdidos/ausentes
  cpod_o            integer NOT NULL DEFAULT 0,   -- Obturados
  queixa_principal  text,
  historia_medica   text,
  plano_tratamento  text,
  created_at        timestamptz NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.procedimentos_odonto (
  id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  prontuario_id  uuid NOT NULL REFERENCES public.prontuarios_odonto(id) ON DELETE CASCADE,
  paciente_id    uuid NOT NULL REFERENCES public.pacientes(id) ON DELETE RESTRICT,
  dentista_id    uuid NOT NULL REFERENCES public.profiles(id) ON DELETE RESTRICT,
  data_proc      date NOT NULL DEFAULT CURRENT_DATE,
  dente          text,                    -- Ex: "11", "36", "Todos"
  procedimento   text NOT NULL,
  material       text,
  custo          numeric(8,2),
  status         text NOT NULL DEFAULT 'realizado'
                   CHECK (status IN ('planejado','realizado','cancelado')),
  obs            text,
  created_at     timestamptz NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.imagens_odonto (
  id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  prontuario_id  uuid NOT NULL REFERENCES public.prontuarios_odonto(id) ON DELETE CASCADE,
  paciente_id    uuid NOT NULL REFERENCES public.pacientes(id) ON DELETE RESTRICT,
  tipo           text NOT NULL CHECK (tipo IN ('radiografia','fotografia','modelo')),
  url            text NOT NULL,
  descricao      text,
  data_captura   date,
  created_at     timestamptz NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.prontuarios_odonto IS 'Prontuário odontológico com odontograma e índice CPO-D';


-- ─────────────────────────────────────────────────────────────────────────────
-- 4.11 MÓDULO PSICOLOGIA CLÍNICA
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.sessoes_psicologia (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  paciente_id             uuid NOT NULL REFERENCES public.pacientes(id) ON DELETE RESTRICT,
  psicologo_id            uuid NOT NULL REFERENCES public.profiles(id) ON DELETE RESTRICT,
  data_sessao             timestamptz NOT NULL DEFAULT NOW(),
  numero_sessao           integer NOT NULL,
  tipo_sessao             text NOT NULL DEFAULT 'terapia'
                            CHECK (tipo_sessao IN ('avaliacao','terapia','retorno','grupo','emergencia')),
  queixa                  text,
  historia                text,
  estado_mental           jsonb DEFAULT '{}',   -- {humor, pensamento, percepcao, orientacao, memoria}
  risco_suicida           text NOT NULL DEFAULT 'nenhum'
                            CHECK (risco_suicida IN ('nenhum','baixo','moderado','alto','iminente')),
  risco_autolesao         text NOT NULL DEFAULT 'nenhum'
                            CHECK (risco_autolesao IN ('nenhum','baixo','moderado','alto')),
  diagnosticos            jsonb DEFAULT '[]',   -- [{codigo_cid, nome, severidade, status}]
  objetivos_terapeuticos  jsonb DEFAULT '[]',   -- [{descricao, progresso_pct, status}]
  conduta                 text,
  tecnicas_utilizadas     jsonb DEFAULT '[]',
  status_sessao           text NOT NULL DEFAULT 'finalizada'
                            CHECK (status_sessao IN ('rascunho','finalizada','assinada')),
  created_at              timestamptz NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.sessoes_psicologia IS 'Registro de sessões psicológicas com diagnóstico CID/DSM e avaliação de risco';


-- ─────────────────────────────────────────────────────────────────────────────
-- 4.12 MÓDULO HISTÓRICO DE EVENTOS
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.historico_eventos (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  categoria           text NOT NULL
                        CHECK (categoria IN ('protocolos','relatorios','enfermagem','vacinas','acidentes')),
  titulo              text NOT NULL,
  descricao           text,
  status              text NOT NULL DEFAULT 'vigente'
                        CHECK (status IN ('vigente','pendente','concluido','urgente','agendado','gerado','arquivado')),
  prioridade          text NOT NULL DEFAULT 'media'
                        CHECK (prioridade IN ('baixa','media','alta','urgente')),
  responsavel_id      uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  responsavel_nome    text,                -- Cache para exibição rápida sem JOIN
  data_evento         date NOT NULL DEFAULT CURRENT_DATE,
  referencia_tabela   text,                -- Tabela de origem (ex: "mapas_risco")
  referencia_id       uuid,                -- ID do registro relacionado
  created_at          timestamptz NOT NULL DEFAULT NOW(),
  updated_at          timestamptz NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.historico_eventos IS 'Log categorizado de eventos do sistema — Acidentes, Protocolos, Vacinas, Relatórios';


-- ─────────────────────────────────────────────────────────────────────────────
-- 4.13 MÓDULO RELATÓRIOS (Cache de métricas)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.snapshots_metricas (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  periodo_inicio  date NOT NULL,
  periodo_fim     date NOT NULL,
  tipo_metrica    text NOT NULL
                    CHECK (tipo_metrica IN ('acidentes','vacinacao','dias_sem_acidente','mapas_risco','manutencao')),
  valor           numeric(10,2) NOT NULL,
  detalhes        jsonb DEFAULT '{}',   -- Breakdown por setor/tipo
  gerado_por_id   uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  created_at      timestamptz NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.snapshots_metricas IS 'Cache de agregações para o módulo de Relatórios/Análises e Métricas';


-- ============================================================================
-- 5. ÍNDICES DE PERFORMANCE
-- ============================================================================

-- pacientes
CREATE INDEX IF NOT EXISTS idx_pacientes_cpf         ON public.pacientes(cpf);
CREATE INDEX IF NOT EXISTS idx_pacientes_prontuario  ON public.pacientes(prontuario);
CREATE INDEX IF NOT EXISTS idx_pacientes_status      ON public.pacientes(status);
CREATE INDEX IF NOT EXISTS idx_pacientes_nome_trgm   ON public.pacientes USING gin(nome gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_pacientes_deleted     ON public.pacientes(deleted_at) WHERE deleted_at IS NULL;

-- entradas_prontuario
CREATE INDEX IF NOT EXISTS idx_entradas_paciente    ON public.entradas_prontuario(paciente_id, data_entrada DESC);
CREATE INDEX IF NOT EXISTS idx_entradas_profissional ON public.entradas_prontuario(profissional_id);
CREATE INDEX IF NOT EXISTS idx_entradas_tipo        ON public.entradas_prontuario(tipo_entrada);

-- mapas_risco
CREATE INDEX IF NOT EXISTS idx_mapas_status         ON public.mapas_risco(status);
CREATE INDEX IF NOT EXISTS idx_mapas_revisao        ON public.mapas_risco(data_proxima_revisao);
CREATE INDEX IF NOT EXISTS idx_mapas_created        ON public.mapas_risco(created_at DESC);

-- protocolos_manutencao
CREATE INDEX IF NOT EXISTS idx_manut_status         ON public.protocolos_manutencao(status);
CREATE INDEX IF NOT EXISTS idx_manut_data_proxima   ON public.protocolos_manutencao(data_proxima_manutencao);

-- doses_vacina
CREATE INDEX IF NOT EXISTS idx_doses_paciente       ON public.doses_vacina(paciente_id);
CREATE INDEX IF NOT EXISTS idx_doses_validade       ON public.doses_vacina(data_validade) WHERE status != 'vencido';
CREATE INDEX IF NOT EXISTS idx_doses_status         ON public.doses_vacina(status);

-- exames_clinicos
CREATE INDEX IF NOT EXISTS idx_exames_paciente      ON public.exames_clinicos(paciente_id, data_resultado DESC);
CREATE INDEX IF NOT EXISTS idx_exames_status        ON public.exames_clinicos(status);
CREATE INDEX IF NOT EXISTS idx_exames_nome_trgm     ON public.exames_clinicos USING gin(nome_exame gin_trgm_ops);

-- processos_sae
CREATE INDEX IF NOT EXISTS idx_sae_paciente         ON public.processos_sae(paciente_id, data_atendimento DESC);
CREATE INDEX IF NOT EXISTS idx_sae_enfermeiro       ON public.processos_sae(enfermeiro_id);
CREATE INDEX IF NOT EXISTS idx_sae_status           ON public.processos_sae(status);
CREATE INDEX IF NOT EXISTS idx_sae_deleted          ON public.processos_sae(deleted_at) WHERE deleted_at IS NULL;

-- eval nutrição
CREATE INDEX IF NOT EXISTS idx_nutri_paciente       ON public.avaliacoes_nutri(paciente_id, data_avaliacao DESC);

-- fisioterapia
CREATE INDEX IF NOT EXISTS idx_fisio_paciente       ON public.avaliacoes_fisio(paciente_id, data_avaliacao DESC);
CREATE INDEX IF NOT EXISTS idx_sessoes_avaliacao    ON public.sessoes_fisio(avaliacao_id, data_sessao DESC);

-- odonto
CREATE INDEX IF NOT EXISTS idx_odonto_paciente      ON public.prontuarios_odonto(paciente_id, data_avaliacao DESC);
CREATE INDEX IF NOT EXISTS idx_procs_odonto         ON public.procedimentos_odonto(prontuario_id);

-- psicologia
CREATE INDEX IF NOT EXISTS idx_psi_paciente         ON public.sessoes_psicologia(paciente_id, data_sessao DESC);
CREATE INDEX IF NOT EXISTS idx_psi_psicologo        ON public.sessoes_psicologia(psicologo_id);

-- histórico
CREATE INDEX IF NOT EXISTS idx_hist_categoria       ON public.historico_eventos(categoria);
CREATE INDEX IF NOT EXISTS idx_hist_status          ON public.historico_eventos(status);
CREATE INDEX IF NOT EXISTS idx_hist_data            ON public.historico_eventos(data_evento DESC);
CREATE INDEX IF NOT EXISTS idx_hist_ref             ON public.historico_eventos(referencia_tabela, referencia_id);

-- notificações
CREATE INDEX IF NOT EXISTS idx_notif_usuario        ON public.notificacoes(usuario_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_notif_lida           ON public.notificacoes(usuario_id, lida) WHERE lida = false;

-- audit_log
CREATE INDEX IF NOT EXISTS idx_audit_tabela         ON public.audit_log(tabela, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_usuario        ON public.audit_log(usuario_id);
CREATE INDEX IF NOT EXISTS idx_audit_registro       ON public.audit_log(registro_id);

-- snapshots
CREATE INDEX IF NOT EXISTS idx_snap_tipo_periodo    ON public.snapshots_metricas(tipo_metrica, periodo_inicio, periodo_fim);


-- ============================================================================
-- 6. ROW LEVEL SECURITY (RLS)
-- ============================================================================
-- Princípio: DENY BY DEFAULT — habilitar RLS em todas as tabelas
-- Depois criar policies explícitas para cada role

ALTER TABLE public.profiles              ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_log             ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notificacoes          ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.pacientes             ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.entradas_prontuario   ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.mapas_risco           ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.protocolos_manutencao ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.historico_manutencao  ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.vacinas               ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.doses_vacina          ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.exames_clinicos       ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.processos_sae         ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.evolucoes_sae         ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.avaliacoes_nutri      ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.planos_alimentares    ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.restricoes_alimentares ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.avaliacoes_fisio      ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sessoes_fisio         ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.prontuarios_odonto    ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.procedimentos_odonto  ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.imagens_odonto        ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sessoes_psicologia    ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.historico_eventos     ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.snapshots_metricas    ENABLE ROW LEVEL SECURITY;


-- ── PROFILES ────────────────────────────────────────────────────────────────
CREATE POLICY "profiles: admin vê todos"
  ON public.profiles FOR SELECT
  USING (public.fn_is_admin());

CREATE POLICY "profiles: usuário vê o próprio"
  ON public.profiles FOR SELECT
  USING (id = auth.uid());

CREATE POLICY "profiles: usuário edita o próprio"
  ON public.profiles FOR UPDATE
  USING (id = auth.uid())
  WITH CHECK (id = auth.uid() AND role = (SELECT role FROM public.profiles WHERE id = auth.uid()));

CREATE POLICY "profiles: admin edita todos"
  ON public.profiles FOR ALL
  USING (public.fn_is_admin());


-- ── PACIENTES ───────────────────────────────────────────────────────────────
CREATE POLICY "pacientes: todos profissionais visualizam"
  ON public.pacientes FOR SELECT
  USING (auth.uid() IS NOT NULL AND deleted_at IS NULL);

CREATE POLICY "pacientes: admin CRUD total"
  ON public.pacientes FOR ALL
  USING (public.fn_is_admin());

CREATE POLICY "pacientes: sesmt insere e edita"
  ON public.pacientes FOR INSERT
  WITH CHECK (public.fn_get_my_role() = 'sesmt');

CREATE POLICY "pacientes: sesmt edita"
  ON public.pacientes FOR UPDATE
  USING (public.fn_get_my_role() = 'sesmt');


-- ── PRONTUÁRIO (ENTRADAS) ───────────────────────────────────────────────────
CREATE POLICY "entradas: todos leem"
  ON public.entradas_prontuario FOR SELECT
  USING (auth.uid() IS NOT NULL);

CREATE POLICY "entradas: profissional insere a própria"
  ON public.entradas_prontuario FOR INSERT
  WITH CHECK (profissional_id = auth.uid());

CREATE POLICY "entradas: profissional edita a própria (rascunho)"
  ON public.entradas_prontuario FOR UPDATE
  USING (profissional_id = auth.uid() AND status = 'rascunho');

CREATE POLICY "entradas: admin CRUD"
  ON public.entradas_prontuario FOR ALL
  USING (public.fn_is_admin());


-- ── MAPAS DE RISCO ──────────────────────────────────────────────────────────
CREATE POLICY "mapas_risco: todos leem"
  ON public.mapas_risco FOR SELECT
  USING (auth.uid() IS NOT NULL AND deleted_at IS NULL);

CREATE POLICY "mapas_risco: sesmt e enfermeiro CRUD"
  ON public.mapas_risco FOR ALL
  USING (public.fn_get_my_role() IN ('admin','sesmt','enfermeiro'));


-- ── PROTOCOLOS MANUTENÇÃO ───────────────────────────────────────────────────
CREATE POLICY "manutencao: todos leem"
  ON public.protocolos_manutencao FOR SELECT
  USING (auth.uid() IS NOT NULL);

CREATE POLICY "manutencao: sesmt e admin CRUD"
  ON public.protocolos_manutencao FOR ALL
  USING (public.fn_get_my_role() IN ('admin','sesmt'));


-- ── VACINAS (catálogo) ──────────────────────────────────────────────────────
CREATE POLICY "vacinas: todos leem catálogo"
  ON public.vacinas FOR SELECT
  USING (auth.uid() IS NOT NULL);

CREATE POLICY "vacinas: admin gerencia catálogo"
  ON public.vacinas FOR ALL
  USING (public.fn_is_admin());


-- ── DOSES VACINA ────────────────────────────────────────────────────────────
CREATE POLICY "doses: todos leem"
  ON public.doses_vacina FOR SELECT
  USING (auth.uid() IS NOT NULL);

CREATE POLICY "doses: enfermeiro e sesmt CRUD"
  ON public.doses_vacina FOR ALL
  USING (public.fn_get_my_role() IN ('admin','enfermeiro','sesmt'));


-- ── EXAMES CLÍNICOS ─────────────────────────────────────────────────────────
CREATE POLICY "exames: todos visualizam"
  ON public.exames_clinicos FOR SELECT
  USING (auth.uid() IS NOT NULL);

CREATE POLICY "exames: médico e admin CRUD"
  ON public.exames_clinicos FOR ALL
  USING (public.fn_get_my_role() IN ('admin','medico'));


-- ── SAE / PROCESSO ENFERMAGEM ───────────────────────────────────────────────
CREATE POLICY "sae: todos visualizam"
  ON public.processos_sae FOR SELECT
  USING (auth.uid() IS NOT NULL AND deleted_at IS NULL);

CREATE POLICY "sae: enfermeiro gerencia o próprio"
  ON public.processos_sae FOR INSERT
  WITH CHECK (enfermeiro_id = auth.uid() AND public.fn_get_my_role() IN ('enfermeiro','admin','sesmt'));

CREATE POLICY "sae: enfermeiro edita o próprio"
  ON public.processos_sae FOR UPDATE
  USING (enfermeiro_id = auth.uid() AND public.fn_get_my_role() = 'enfermeiro');

CREATE POLICY "sae: admin CRUD"
  ON public.processos_sae FOR ALL
  USING (public.fn_is_admin());

CREATE POLICY "evolucoes_sae: todos leem"
  ON public.evolucoes_sae FOR SELECT
  USING (auth.uid() IS NOT NULL);

CREATE POLICY "evolucoes_sae: enfermeiro insere"
  ON public.evolucoes_sae FOR INSERT
  WITH CHECK (enfermeiro_id = auth.uid() AND public.fn_get_my_role() IN ('enfermeiro','admin'));


-- ── NUTRIÇÃO ────────────────────────────────────────────────────────────────
CREATE POLICY "nutri: todos leem"
  ON public.avaliacoes_nutri FOR SELECT USING (auth.uid() IS NOT NULL);

CREATE POLICY "nutri: nutricionista CRUD próprios"
  ON public.avaliacoes_nutri FOR ALL
  USING (nutricionista_id = auth.uid() AND public.fn_get_my_role() IN ('nutricionista','admin'));

CREATE POLICY "planos: todos leem"
  ON public.planos_alimentares FOR SELECT USING (auth.uid() IS NOT NULL);

CREATE POLICY "planos: nutricionista CRUD"
  ON public.planos_alimentares FOR ALL
  USING (nutricionista_id = auth.uid() AND public.fn_get_my_role() IN ('nutricionista','admin'));

CREATE POLICY "restricoes: todos leem"
  ON public.restricoes_alimentares FOR SELECT USING (auth.uid() IS NOT NULL);

CREATE POLICY "restricoes: nutricionista e enfermeiro CRUD"
  ON public.restricoes_alimentares FOR ALL
  USING (public.fn_get_my_role() IN ('nutricionista','enfermeiro','admin'));


-- ── FISIOTERAPIA ────────────────────────────────────────────────────────────
CREATE POLICY "fisio_aval: todos leem"
  ON public.avaliacoes_fisio FOR SELECT USING (auth.uid() IS NOT NULL);

CREATE POLICY "fisio_aval: fisioterapeuta CRUD próprios"
  ON public.avaliacoes_fisio FOR ALL
  USING (fisioterapeuta_id = auth.uid() AND public.fn_get_my_role() IN ('fisio','admin'));

CREATE POLICY "sessoes_fisio: todos leem"
  ON public.sessoes_fisio FOR SELECT USING (auth.uid() IS NOT NULL);

CREATE POLICY "sessoes_fisio: fisioterapeuta CRUD"
  ON public.sessoes_fisio FOR ALL
  USING (fisioterapeuta_id = auth.uid() AND public.fn_get_my_role() IN ('fisio','admin'));


-- ── ODONTOLOGIA ─────────────────────────────────────────────────────────────
CREATE POLICY "odonto: todos leem"
  ON public.prontuarios_odonto FOR SELECT USING (auth.uid() IS NOT NULL);

CREATE POLICY "odonto: dentista CRUD próprios"
  ON public.prontuarios_odonto FOR ALL
  USING (dentista_id = auth.uid() AND public.fn_get_my_role() IN ('dentista','admin'));

CREATE POLICY "procs_odonto: todos leem"
  ON public.procedimentos_odonto FOR SELECT USING (auth.uid() IS NOT NULL);

CREATE POLICY "procs_odonto: dentista CRUD"
  ON public.procedimentos_odonto FOR ALL
  USING (dentista_id = auth.uid() AND public.fn_get_my_role() IN ('dentista','admin'));

CREATE POLICY "imgs_odonto: todos leem"
  ON public.imagens_odonto FOR SELECT USING (auth.uid() IS NOT NULL);

CREATE POLICY "imgs_odonto: dentista insere"
  ON public.imagens_odonto FOR INSERT
  WITH CHECK (public.fn_get_my_role() IN ('dentista','admin'));


-- ── PSICOLOGIA ──────────────────────────────────────────────────────────────
-- Dados de psicologia possuem acesso RESTRITO — somente o próprio psicólogo e admin
CREATE POLICY "psi: psicologo lê próprios + admin"
  ON public.sessoes_psicologia FOR SELECT
  USING (psicologo_id = auth.uid() OR public.fn_is_admin());

CREATE POLICY "psi: psicologo CRUD próprios"
  ON public.sessoes_psicologia FOR ALL
  USING (psicologo_id = auth.uid() AND public.fn_get_my_role() IN ('psicologo','admin'));


-- ── HISTÓRICO DE EVENTOS ────────────────────────────────────────────────────
CREATE POLICY "hist: todos leem"
  ON public.historico_eventos FOR SELECT USING (auth.uid() IS NOT NULL);

CREATE POLICY "hist: sesmt e admin CRUD"
  ON public.historico_eventos FOR ALL
  USING (public.fn_get_my_role() IN ('admin','sesmt','enfermeiro'));


-- ── NOTIFICAÇÕES ────────────────────────────────────────────────────────────
CREATE POLICY "notif: usuário lê as próprias"
  ON public.notificacoes FOR SELECT
  USING (usuario_id = auth.uid());

CREATE POLICY "notif: usuário marca como lida"
  ON public.notificacoes FOR UPDATE
  USING (usuario_id = auth.uid())
  WITH CHECK (usuario_id = auth.uid());

CREATE POLICY "notif: sistema (service role) insere"
  ON public.notificacoes FOR INSERT
  WITH CHECK (true);  -- Inserções via triggers SECURITY DEFINER


-- ── AUDIT LOG ───────────────────────────────────────────────────────────────
CREATE POLICY "audit: apenas admin lê"
  ON public.audit_log FOR SELECT
  USING (public.fn_is_admin());
-- Escritas via trigger SECURITY DEFINER — sem policy de INSERT para usuários


-- ── SNAPSHOTS MÉTRICAS ──────────────────────────────────────────────────────
CREATE POLICY "snap: todos leem"
  ON public.snapshots_metricas FOR SELECT USING (auth.uid() IS NOT NULL);

CREATE POLICY "snap: sesmt e admin CRUD"
  ON public.snapshots_metricas FOR ALL
  USING (public.fn_get_my_role() IN ('admin','sesmt'));


-- ============================================================================
-- 7. TRIGGERS
-- ============================================================================

-- updated_at automático
CREATE TRIGGER trg_profiles_updated_at
  BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION public.fn_set_updated_at();

CREATE TRIGGER trg_pacientes_updated_at
  BEFORE UPDATE ON public.pacientes
  FOR EACH ROW EXECUTE FUNCTION public.fn_set_updated_at();

CREATE TRIGGER trg_mapas_updated_at
  BEFORE UPDATE ON public.mapas_risco
  FOR EACH ROW EXECUTE FUNCTION public.fn_set_updated_at();

CREATE TRIGGER trg_manut_updated_at
  BEFORE UPDATE ON public.protocolos_manutencao
  FOR EACH ROW EXECUTE FUNCTION public.fn_set_updated_at();

CREATE TRIGGER trg_sae_updated_at
  BEFORE UPDATE ON public.processos_sae
  FOR EACH ROW EXECUTE FUNCTION public.fn_set_updated_at();

CREATE TRIGGER trg_hist_updated_at
  BEFORE UPDATE ON public.historico_eventos
  FOR EACH ROW EXECUTE FUNCTION public.fn_set_updated_at();

CREATE TRIGGER trg_restricoes_updated_at
  BEFORE UPDATE ON public.restricoes_alimentares
  FOR EACH ROW EXECUTE FUNCTION public.fn_set_updated_at();

-- Trigger: Espelhar novo user do auth.users → public.profiles
CREATE OR REPLACE FUNCTION public.fn_on_auth_user_created()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
  INSERT INTO public.profiles (id, nome_completo, email)
  VALUES (NEW.id, COALESCE(NEW.raw_user_meta_data->>'nome_completo', 'Novo Usuário'), NEW.email)
  ON CONFLICT (id) DO NOTHING;
  RETURN NEW;
END;
$$;

CREATE TRIGGER trg_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.fn_on_auth_user_created();

-- Triggers de audit log nas tabelas críticas
CREATE TRIGGER trg_audit_atendimentos
  AFTER INSERT OR UPDATE OR DELETE ON public.entradas_prontuario
  FOR EACH ROW EXECUTE FUNCTION public.fn_audit_log();

CREATE TRIGGER trg_audit_sae
  AFTER INSERT OR UPDATE OR DELETE ON public.processos_sae
  FOR EACH ROW EXECUTE FUNCTION public.fn_audit_log();

CREATE TRIGGER trg_audit_psicologia
  AFTER INSERT OR UPDATE OR DELETE ON public.sessoes_psicologia
  FOR EACH ROW EXECUTE FUNCTION public.fn_audit_log();

CREATE TRIGGER trg_audit_odonto
  AFTER INSERT OR UPDATE OR DELETE ON public.prontuarios_odonto
  FOR EACH ROW EXECUTE FUNCTION public.fn_audit_log();

CREATE TRIGGER trg_audit_fisio
  AFTER INSERT OR UPDATE OR DELETE ON public.avaliacoes_fisio
  FOR EACH ROW EXECUTE FUNCTION public.fn_audit_log();

CREATE TRIGGER trg_audit_mapas
  AFTER INSERT OR UPDATE OR DELETE ON public.mapas_risco
  FOR EACH ROW EXECUTE FUNCTION public.fn_audit_log();

CREATE TRIGGER trg_audit_doses
  AFTER INSERT OR UPDATE OR DELETE ON public.doses_vacina
  FOR EACH ROW EXECUTE FUNCTION public.fn_audit_log();

-- Triggers de notificação automática
CREATE TRIGGER trg_notif_doses_vencimento
  AFTER INSERT OR UPDATE OF data_validade ON public.doses_vacina
  FOR EACH ROW EXECUTE FUNCTION public.fn_notificar_vencimento();

CREATE TRIGGER trg_notif_manut_vencimento
  AFTER INSERT OR UPDATE OF data_proxima_manutencao ON public.protocolos_manutencao
  FOR EACH ROW EXECUTE FUNCTION public.fn_notificar_vencimento();


-- ============================================================================
-- 8. VIEWS ANALÍTICAS
-- ============================================================================

-- View: Dashboard KPIs
CREATE OR REPLACE VIEW public.vw_dashboard_kpis AS
SELECT
  (SELECT COUNT(*) FROM public.mapas_risco WHERE status != 'vencido' AND deleted_at IS NULL)     AS mapas_ativos,
  (SELECT COUNT(*) FROM public.mapas_risco WHERE status = 'vencido' AND deleted_at IS NULL)      AS mapas_vencidos,
  (SELECT COUNT(*) FROM public.protocolos_manutencao WHERE status = 'ok')                        AS protocolos_ok,
  (SELECT COUNT(*) FROM public.protocolos_manutencao WHERE status = 'em_atraso')                 AS protocolos_atraso,
  (SELECT COUNT(*) FROM public.doses_vacina WHERE status = 'ok')                                 AS doses_ok,
  (SELECT COUNT(*) FROM public.doses_vacina WHERE status IN ('vencendo','vencido'))               AS doses_vencendo,
  (SELECT COUNT(*) FROM public.historico_eventos WHERE categoria = 'acidentes'
    AND data_evento >= DATE_TRUNC('month', CURRENT_DATE))                                        AS acidentes_mes,
  (SELECT COUNT(*) FROM public.pacientes WHERE deleted_at IS NULL AND status = 'ativo')          AS total_pacientes_ativos;

-- View: KPI de vacinação por paciente
CREATE OR REPLACE VIEW public.vw_status_vacinal AS
SELECT
  p.id            AS paciente_id,
  p.nome          AS paciente_nome,
  p.categoria,
  v.nome          AS vacina,
  MAX(dv.numero_dose) AS doses_recebidas,
  v.doses_recomendadas,
  CASE
    WHEN MAX(dv.numero_dose) >= v.doses_recomendadas THEN 'completo'
    WHEN MAX(dv.numero_dose) > 0 THEN 'incompleto'
    ELSE 'nenhuma_dose'
  END AS status_vacinal
FROM public.pacientes p
CROSS JOIN public.vacinas v
LEFT JOIN public.doses_vacina dv ON dv.paciente_id = p.id AND dv.vacina_id = v.id
WHERE p.deleted_at IS NULL
GROUP BY p.id, p.nome, p.categoria, v.id, v.nome, v.doses_recomendadas;


-- ============================================================================
-- 9. STORAGE BUCKETS (executar no Dashboard Supabase ou via API)
-- ============================================================================
-- Descomente e execute via API do Supabase Storage se preferir SQL:
--
-- INSERT INTO storage.buckets (id, name, public) VALUES ('avatars', 'avatars', true);
-- INSERT INTO storage.buckets (id, name, public) VALUES ('mapas-risco', 'mapas-risco', false);
-- INSERT INTO storage.buckets (id, name, public) VALUES ('imagens-odonto', 'imagens-odonto', false);
-- INSERT INTO storage.buckets (id, name, public) VALUES ('documentos-pacientes', 'documentos-pacientes', false);
-- INSERT INTO storage.buckets (id, name, public) VALUES ('exports', 'exports', false);
--
-- Policies de Storage (executar após criar buckets):
-- CREATE POLICY "avatars: leitura pública"
--   ON storage.objects FOR SELECT USING (bucket_id = 'avatars');
--
-- CREATE POLICY "mapas-risco: profisionais autenticados"
--   ON storage.objects FOR ALL
--   USING (bucket_id = 'mapas-risco' AND auth.uid() IS NOT NULL);
--
-- CREATE POLICY "documentos-pacientes: profissionais autenticados"
--   ON storage.objects FOR ALL
--   USING (bucket_id = 'documentos-pacientes' AND auth.uid() IS NOT NULL);


-- ============================================================================
-- FIM DO SCHEMA UCGS — v1.0
-- Total de tabelas: 24
-- Total de índices: 35+
-- Total de policies RLS: 40+
-- Total de triggers: 18
-- ============================================================================
