-- ==========================================
-- SCRIPT 4: VIEWS PARA DASHBOARDS E RELATÓRIOS
-- Integração ao Schema UCGS
-- ==========================================

-- V1: Histórico nutricional do paciente (Substitui tabela dedicada para evitar redundância)
CREATE OR REPLACE VIEW public.vw_historico_nutricional AS
SELECT
  an.paciente_id,
  an.id AS avaliacao_id,
  an.nutricionista_id,
  p.nome AS nutricionista_nome,
  an.peso_kg, 
  an.imc, 
  an.meta_calorica_kcal,
  an.created_at AS data_avaliacao,
  pa.nome_plano,
  pa.status AS status_plano
FROM public.avaliacoes_nutricionais an
LEFT JOIN public.planos_alimentares pa ON pa.avaliacao_nutricional_id = an.id
LEFT JOIN public.profiles p ON p.id = an.nutricionista_id
ORDER BY an.created_at DESC;

-- V2: Dashboard de métricas gerais da Clínica / Universidade
CREATE OR REPLACE VIEW public.vw_dashboard_metricas AS
SELECT
  (SELECT count(*) FROM public.pacientes) AS total_pacientes,
  (SELECT count(*) FROM public.atendimentos_medicos WHERE DATE(data_atendimento) = CURRENT_DATE) AS atendimentos_hoje,
  (SELECT count(*) FROM public.processos_enfermagem WHERE status = 'em_andamento') AS processos_enf_ativos,
  (SELECT count(*) FROM public.registro_acidentes WHERE data_hora >= now() - interval '30 days') AS acidentes_30d;

-- V3: Resumo CPO-D Odontológico por paciente (Poder analítico extraído do odontograma granular)
CREATE OR REPLACE VIEW public.vw_cpod_resumo AS
SELECT
  ao.paciente_id,
  ao.id AS avaliacao_id,
  ao.created_at AS data_avaliacao,
  count(*) FILTER (WHERE od.condicao = 'carie') AS cariados,
  count(*) FILTER (WHERE od.condicao = 'ausente' OR od.condicao = 'extraido') AS perdidos,
  count(*) FILTER (WHERE od.condicao = 'restaurado') AS obturados,
  (
    count(*) FILTER (WHERE od.condicao = 'carie') +
    count(*) FILTER (WHERE od.condicao = 'ausente' OR od.condicao = 'extraido') +
    count(*) FILTER (WHERE od.condicao = 'restaurado')
  ) AS indice_cpod
FROM public.avaliacoes_odontologicas ao
JOIN public.odontograma_dentes od ON od.avaliacao_odontologica_id = ao.id
GROUP BY ao.paciente_id, ao.id, ao.created_at;
