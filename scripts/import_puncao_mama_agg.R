# Importação e Agrupamento Anual de Punção de Mama por Agulha Grossa
# Período: 2020 a 2025
# Procedimento: 0201010607
# Esse script foi **MUITO OTIMIZADO** para não estourar a memória.

library(microdatasus)
library(dplyr)

# Modifique ESTADO para o estado desejado ou "" se quiser todo o Brasil (ATENÇÃO: Todo o BR são dezenas de GBs de download!)
ESTADO <- "MG"
ANOS <- 2020:2025

# Tabela para guardar a contagem anual
resultado_anual <- data.frame(Ano = integer(), Quantidade = integer())

# Tabela para guardar os microdados filtrados de todos os anos
dados_completos_filtrados <- data.frame()

for (ano in ANOS) {
  cat(sprintf("\n[==== Processando o ano %d para o Estado %s ====]\n", ano, ESTADO))
  
  # Como 2025 ainda está na metade/começo (ex: até o mês atual),
  # o microdatasus lida sozinho baixando apenas os meses disponíveis
  
  # Vamos baixar os dados brutos de janeiro a dezembro de cada ano
  dados_brutos_ano <- tryCatch({
    fetch_datasus(
      year_start = ano,
      year_end = ano,
      month_start = 1,
      month_end = 12,
      uf = ESTADO,
      information_system = "SIA-PA"
    )
  }, error = function(e) {
    cat("Erro ou dados ausentes para este ano:", e$message, "\n")
    return(NULL)
  })
  
  if (!is.null(dados_brutos_ano) && nrow(dados_brutos_ano) > 0) {
    cat(sprintf("-> Download bruto extraído. Foram baixadas %d linhas do SUS.\n", nrow(dados_brutos_ano)))
    
    # 🌟 OTIMIZAÇÃO CRÍTICA:
    # Em de vez de processar (process_sia) os milhões de dados para depois filtrar,
    # nós filtramos os dados 'Crus' primeiro, onde a coluna PA_PROC_ID já tem o código!
    dados_filtrados_brutos <- dados_brutos_ano %>%
      filter(PA_PROC_ID == "0201010607")
    
    # Agora sim, usamos o process_sia apenas nas dezenas ou centenas de linhas filtradas!
    # Isso faz o dicionário rodar em 1 segundo em vez de 30 minutos!
    cat(sprintf("-> Aplicando process_sia nos %d registros filtrados do ano %d...\n", nrow(dados_filtrados_brutos), ano))
    
    if (nrow(dados_filtrados_brutos) > 0) {
      dados_processados_ano <- process_sia(dados_filtrados_brutos)
      
      # Salvar a contagem do ano no resultado
      quantidade <- nrow(dados_processados_ano)
    } else {
      quantidade <- 0
      dados_processados_ano <- data.frame()
    }
    
    cat(sprintf("---> Total do ano %d: *%d* punções de mama realizadas.\n", ano, quantidade))
    
    resultado_anual <- rbind(resultado_anual, data.frame(Ano = ano, Quantidade = quantidade))
    dados_completos_filtrados <- bind_rows(dados_completos_filtrados, dados_processados_ano)
    
  } else {
    cat(sprintf("---> Nenhum dado processado para o ano %d.\n", ano))
  }
}

cat("\n=======================================================\n")
cat("RESULTADO FINAL: QUANTIDADE DE PUNÇÃO DE MAMA POR ANO\n")
print(resultado_anual)

# Salvar o consolidado das quantidades
write.csv(resultado_anual, sprintf("quantidade_por_ano_puncao_mama_%s_2020_2025.csv", ESTADO), row.names = FALSE)
cat("\nAs quantidades por ano foram salvas no arquivo 'quantidade_por_ano_puncao_mama.csv'\n")

# Salvar também TODOS os registros unidos de todos os anos (microdados) em outro arquivo
if(nrow(dados_completos_filtrados) > 0) {
    write.csv(dados_completos_filtrados, sprintf("microdados_puncao_mama_%s_2020_2025.csv", ESTADO), row.names = FALSE)
    cat(sprintf("Os microdados completos foram salvos no arquivo 'microdados_puncao_mama_%s_2020_2025.csv'\n", ESTADO))
}
