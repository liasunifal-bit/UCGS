-- ============================================================
-- CORREÇÃO DO TRIGGER handle_new_user
-- Alinhado com o schema real da tabela public.profiles
-- Execute no SQL Editor do Supabase
-- ============================================================

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (
        id,
        nome_completo,
        email,
        role,
        especialidade,
        registro_profissional,
        matricula,
        setor,
        ativo
    )
    VALUES (
        NEW.id,
        COALESCE(NEW.raw_user_meta_data->>'nome_completo', 'Usuário UCGS'),
        COALESCE(NEW.email, ''),
        COALESCE(NEW.raw_user_meta_data->>'role', 'enfermeiro'),
        NEW.raw_user_meta_data->>'especialidade',
        NEW.raw_user_meta_data->>'registro_profissional',
        NEW.raw_user_meta_data->>'matricula',
        NEW.raw_user_meta_data->>'setor',
        TRUE
    )
    ON CONFLICT (id) DO UPDATE SET
        nome_completo        = COALESCE(EXCLUDED.nome_completo, public.profiles.nome_completo),
        role                 = COALESCE(EXCLUDED.role, public.profiles.role),
        especialidade        = COALESCE(EXCLUDED.especialidade, public.profiles.especialidade),
        registro_profissional= COALESCE(EXCLUDED.registro_profissional, public.profiles.registro_profissional),
        matricula            = COALESCE(EXCLUDED.matricula, public.profiles.matricula),
        setor                = COALESCE(EXCLUDED.setor, public.profiles.setor),
        updated_at           = now();

    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Recriar o trigger vinculado ao auth.users
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
