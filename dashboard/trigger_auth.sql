-- ============================================================================
-- AUTENTICAÇÃO JWT E ESPELHAMENTO DE DADOS (AUTH -> PUBLIC)
-- ============================================================================
-- Este trigger escuta qualquer novo usuário que se cadastrar na API padrão do Supabase
-- e automaticamente clona suas informações seguras para a nossa tabela public.profiles

CREATE OR REPLACE FUNCTION public.fn_handle_new_user()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  INSERT INTO public.profiles (
    id, 
    nome_completo, 
    email, 
    role, 
    ativo
  )
  VALUES (
    new.id, 
    COALESCE(new.raw_user_meta_data->>'nome_completo', split_part(new.email, '@', 1)),  -- pega o nome ou a 1ª parte do email
    new.email, 
    COALESCE(new.raw_user_meta_data->>'role', 'enfermeiro'), -- Padrão enfermeiro se não vier nada
    true
  );
  RETURN new;
END;
$$;

-- Previne erros caso a trigger já exista se este script for rodado 2x
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.fn_handle_new_user();
