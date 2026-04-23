# Importação de dados de Punção de Mama por Agulha Grossa (Core Biopsy)
# Código do Procedimento no SUS: 0201010607
# Sistema de Informação: SIA-PA (Produção Ambulatorial)

# Instalar o pacote microdatasus caso não esteja instalado
if (!requireNamespace("remotes", quietly = TRUE)) {
  install.packages("remotes", repos = "http://cran.us.r-project.org")
}
if (!requireNamespace("microdatasus", quietly = TRUE)) {
  remotes::install_github("rfsaldanha/microdatasus")
}
if (!requireNamespace("dplyr", quietly = TRUE)) {
  install.packages("dplyr", repos = "http://cran.us.r-project.org")
}

library(microdatasus)
library(dplyr)

# Parâmetros padrão - O usuário pode alterar para os estados/meses/anos desejados
ESTADO <- "MG" 
ANO <- 2023
MES <- 1

cat(sprintf("Baixando dados do SIA-PA para UF=%s, Ano=%s, Mes=%s...\n", ESTADO, ANO, MES))

# 1. Baixar os dados brutos do SIA (Produção Ambulatorial)
# fetch_datasus pode receber year_start, month_start, month_end, uf, information_system
dados_sia <- fetch_datasus(
  year_start = ANO,
  year_end = ANO,
  month_start = MES,
  month_end = MES,
  uf = ESTADO,
  information_system = "SIA-PA"
)

# 2. Pré-processar os dados
cat("Processando os dados usando process_sia...\n")
dados_processados <- process_sia(dados_sia)

# 3. Filtrar pelo procedimento "Punção de Mama por Agulha Grossa" (Código 0201010607)
cat("Filtrando pelo procedimento 0201010607 (Punção de Mama por Agulha Grossa)...\n")
dados_puncao <- dados_processados %>%
  filter(PA_PROC_ID == "0201010607")

# 4. Exibir o resultado
cat(sprintf("Foram encontrados %d registros\n", nrow(dados_puncao)))

# Salvar os resultados em um CSV
output_file <- sprintf("puncao_mama_%s_%s_%s.csv", ESTADO, ANO, MES)
write.csv(dados_puncao, output_file, row.names = FALSE)
cat(sprintf("Dados salvos em '%s'\n", output_file))
