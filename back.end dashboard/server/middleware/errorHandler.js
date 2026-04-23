/**
 * UCGS Backend — Error Handler Global
 *
 * Captura todos os erros não tratados e retorna resposta JSON padronizada.
 */

function errorHandler(err, req, res, _next) {
  console.error('❌ Erro não tratado:', {
    mensagem: err.message,
    rota: `${req.method} ${req.path}`,
    stack: process.env.NODE_ENV === 'production' ? undefined : err.stack
  });

  // Erro de JSON malformado (body-parser)
  if (err.type === 'entity.parse.failed') {
    return res.status(400).json({
      erro: 'JSON inválido',
      detalhe: 'O corpo da requisição não é um JSON válido'
    });
  }

  // Erro de validação customizado
  if (err.status === 400) {
    return res.status(400).json({
      erro: 'Dados inválidos',
      detalhe: err.message
    });
  }

  // Erro do Supabase (upstream)
  if (err.supabaseError) {
    return res.status(502).json({
      erro: 'Erro no banco de dados',
      detalhe: err.message,
      codigo_supabase: err.supabaseCode || null
    });
  }

  // Erro genérico
  res.status(err.status || 500).json({
    erro: 'Erro interno do servidor',
    detalhe: process.env.NODE_ENV === 'production'
      ? 'Ocorreu um erro inesperado'
      : err.message
  });
}

module.exports = errorHandler;
