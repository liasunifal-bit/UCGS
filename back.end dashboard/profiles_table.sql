-- ==========================================
-- TABELA: public.profiles (Profissionais do Sistema)
-- Execute no SQL Editor do Supabase após tabelas_clinicas.sql
-- ==========================================

-- Tipos enumerados para categorias profissionais
CREATE TABLE IF NOT EXISTS public.profiles (
    id           UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nome         TEXT NOT NULL,
    cpf          TEXT UNIQUE NOT NULL,
    telefone     TEXT,
    categoria    TEXT NOT NULL,  -- medico, enfermeiro, fisioterapeuta, dentista, psicologo, admin
    num_registro TEXT,           -- CRM, COREN, CREFITO, CRO, CRP
    setor        TEXT,           -- UTI, Clínica Médica, Ambulatório, etc.
    foto_url     TEXT,
    ativo        BOOLEAN DEFAULT TRUE,
    criado_em    TIMESTAMPTZ DEFAULT now() NOT NULL,
    atualizado_em TIMESTAMPTZ DEFAULT now()
);

-- Habilitar RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Políticas de acesso
-- Profissional pode ver seu próprio perfil
CREATE POLICY "Usuário pode ver seu perfil"
    ON public.profiles FOR SELECT
    USING (auth.uid() = id);

-- Profissional pode atualizar seu próprio perfil
CREATE POLICY "Usuário pode atualizar seu perfil"
    ON public.profiles FOR UPDATE
    USING (auth.uid() = id);

-- Qualquer autenticado pode ver perfis de outros (para exibir nome no prontuário)
CREATE POLICY "Autenticados podem ver todos os perfis"
    ON public.profiles FOR SELECT
    USING (auth.role() = 'authenticated');

-- Somente o próprio usuário pode inserir seu perfil
CREATE POLICY "Usuário pode inserir seu perfil"
    ON public.profiles FOR INSERT
    WITH CHECK (auth.uid() = id);

-- ==========================================
-- TRIGGER: Criação automática de perfil básico ao registrar
-- Garante que auth.users sempre tenha um registro em profiles
-- ==========================================
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, nome, cpf, categoria)
    VALUES (
        NEW.id,
        COALESCE(NEW.raw_user_meta_data->>'nome', 'Usuário UCGS'),
        COALESCE(NEW.raw_user_meta_data->>'cpf', 'PENDENTE'),
        COALESCE(NEW.raw_user_meta_data->>'categoria', 'pendente')
    )
    ON CONFLICT (id) DO NOTHING;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Vincula o trigger ao evento de criação de usuário
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ==========================================
-- FUNÇÃO: Atualizar timestamp automaticamente
-- ==========================================
CREATE OR REPLACE FUNCTION public.update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_profiles_updated_at ON public.profiles;
CREATE TRIGGER trg_profiles_updated_at
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();
