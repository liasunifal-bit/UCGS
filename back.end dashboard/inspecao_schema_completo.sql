-- ============================================================
-- ANÁLISE COMPLETA DO SCHEMA PUBLIC — UCGS
-- Cole este script no SQL Editor do Supabase e execute
-- ============================================================

-- 1. TODAS AS TABELAS DO SCHEMA PUBLIC
SELECT 
    t.table_name                                    AS tabela,
    pg_size_pretty(pg_total_relation_size(
        ('"public"."' || t.table_name || '"')::regclass
    ))                                              AS tamanho,
    (SELECT count(*) FROM information_schema.columns c 
     WHERE c.table_schema = 'public' 
       AND c.table_name = t.table_name)             AS num_colunas,
    obj_description(
        ('"public"."' || t.table_name || '"')::regclass, 
        'pg_class'
    )                                               AS descricao
FROM information_schema.tables t
WHERE t.table_schema = 'public'
  AND t.table_type = 'BASE TABLE'
ORDER BY t.table_name;

-- ============================================================

-- 2. TODAS AS COLUNAS POR TABELA
SELECT 
    c.table_name                AS tabela,
    c.column_name               AS coluna,
    c.data_type                 AS tipo,
    c.is_nullable               AS nulo_permitido,
    c.column_default            AS valor_padrao,
    c.character_maximum_length  AS tamanho_max
FROM information_schema.columns c
WHERE c.table_schema = 'public'
ORDER BY c.table_name, c.ordinal_position;

-- ============================================================

-- 3. TODAS AS POLÍTICAS RLS ATIVAS
SELECT 
    schemaname  AS schema,
    tablename   AS tabela,
    policyname  AS politica,
    cmd         AS operacao,
    qual        AS using_expr,
    with_check  AS check_expr
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, cmd;

-- ============================================================

-- 4. TODAS AS FOREIGN KEYS (RELACIONAMENTOS)
SELECT
    tc.table_name           AS tabela_origem,
    kcu.column_name         AS coluna_origem,
    ccu.table_name          AS tabela_destino,
    ccu.column_name         AS coluna_destino,
    rc.delete_rule          AS ao_deletar
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.referential_constraints AS rc
    ON tc.constraint_name = rc.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = rc.unique_constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public'
ORDER BY tc.table_name;

-- ============================================================

-- 5. TODOS OS TRIGGERS ATIVOS
SELECT 
    trigger_name            AS trigger,
    event_object_table      AS tabela,
    event_manipulation      AS evento,
    action_timing           AS momento,
    action_statement        AS funcao
FROM information_schema.triggers
WHERE trigger_schema = 'public'
   OR event_object_schema = 'public'
ORDER BY event_object_table, event_manipulation;

-- ============================================================

-- 6. CONTAGEM DE REGISTROS POR TABELA (dados reais)
DO $$
DECLARE
    tbl RECORD;
    cnt BIGINT;
BEGIN
    FOR tbl IN 
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
          AND table_type = 'BASE TABLE'
    LOOP
        EXECUTE format('SELECT count(*) FROM public.%I', tbl.table_name) INTO cnt;
        RAISE NOTICE 'Tabela: % → % registros', tbl.table_name, cnt;
    END LOOP;
END;
$$;
