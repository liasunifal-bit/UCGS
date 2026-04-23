-- ==========================================
-- SCRIPT DE CRIAÇÃO: TABELAS CLÍNICAS & RLS
-- ==========================================
-- ⚠️ IMPORTANTE: Execute este script no SQL Editor do seu projeto Supabase.

-- 1. Tabela Pacientes
CREATE TABLE IF NOT EXISTS public.pacientes (
    id UUID DEFAULT extensions.uuid_generate_v4() PRIMARY KEY,
    nome TEXT NOT NULL,
    cpf TEXT UNIQUE NOT NULL,
    nascimento DATE NOT NULL,
    sexo TEXT NOT NULL,
    telefone TEXT,
    email TEXT,
    prontuario TEXT UNIQUE,
    status TEXT DEFAULT 'ativo',
    logradouro TEXT,
    numero TEXT,
    complemento TEXT,
    bairro TEXT,
    cidade TEXT,
    uf TEXT,
    cep TEXT,
    observacoes TEXT,
    data_cadastro TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- Habilitar RLS na tabela pacientes
ALTER TABLE public.pacientes ENABLE ROW LEVEL SECURITY;

-- Políticas (Policies) para Pacientes
-- Apenas usuários autenticados (profissionais) podem visualizar os pacientes
CREATE POLICY "Profissionais podem visualizar pacientes" 
    ON public.pacientes FOR SELECT 
    USING (auth.role() = 'authenticated');

-- Apenas profissionais autenticados podem inserir pacientes
CREATE POLICY "Profissionais podem inserir pacientes" 
    ON public.pacientes FOR INSERT 
    WITH CHECK (auth.role() = 'authenticated');

-- Apenas profissionais autenticados podem atualizar pacientes
CREATE POLICY "Profissionais podem atualizar pacientes" 
    ON public.pacientes FOR UPDATE 
    USING (auth.role() = 'authenticated');

-- 2. Tabela Evoluções (Prontuário)
CREATE TABLE IF NOT EXISTS public.evolucoes (
    id UUID DEFAULT extensions.uuid_generate_v4() PRIMARY KEY,
    paciente_id UUID REFERENCES public.pacientes(id) ON DELETE CASCADE,
    tipo TEXT NOT NULL, -- Ex: Evolução Clínica, Prescrição, etc.
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    conduta TEXT,
    especialidade TEXT,
    autor_id UUID REFERENCES auth.users(id), -- Referência ao usuário logado
    data_criacao TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- Habilitar RLS na tabela evolucoes
ALTER TABLE public.evolucoes ENABLE ROW LEVEL SECURITY;

-- Políticas (Policies) para Evoluções
-- Todos os profissionais podem ler evoluções
CREATE POLICY "Profissionais podem ver evoluções" 
    ON public.evolucoes FOR SELECT 
    USING (auth.role() = 'authenticated');

-- Apenas profissionais autenticados podem inserir evoluções (o autor será validado no backend)
CREATE POLICY "Profissionais podem inserir evoluções" 
    ON public.evolucoes FOR INSERT 
    WITH CHECK (auth.role() = 'authenticated' AND auth.uid() = autor_id);

-- Somente o próprio autor da evolução pode editá-la (ou admins, caso exista configuração adicional)
CREATE POLICY "Autor pode editar sua própria evolução" 
    ON public.evolucoes FOR UPDATE 
    USING (auth.uid() = autor_id);

-- (Opcional) Trigger simples para autogerar o número do prontuário (PRN-XXXXXX)
CREATE OR REPLACE FUNCTION set_prontuario_seq()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.prontuario IS NULL OR NEW.prontuario = '' THEN
        -- Extraindo um código base da sequence ou timestamp (Exemplo simplificado)
        NEW.prontuario := 'PRN-' || to_char(CURRENT_TIMESTAMP, 'YYYYMMDDHH24MISS');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_set_prontuario
BEFORE INSERT ON public.pacientes
FOR EACH ROW EXECUTE FUNCTION set_prontuario_seq();
