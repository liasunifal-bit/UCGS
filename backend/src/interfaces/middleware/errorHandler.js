/**
 * Middleware — Tratamento centralizado de erros
 */

// eslint-disable-next-line no-unused-vars
function errorHandler(err, req, res, next) {
  const status = err.status || 500;
  const message = err.message || 'Erro interno do servidor';

  if (process.env.NODE_ENV === 'development') {
    console.error(`[ERROR] ${status} — ${req.method} ${req.path}:`, err);
  }

  res.status(status).json({
    error: message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
  });
}

module.exports = { errorHandler };
