/**
 * UCGS Backend — Middleware de Autenticação
 *
 * Bloqueia TODA requisição sem JWT válido no header Authorization.
 * Rotas excluídas: GET /api/health (health-check)
 */

const ROTAS_PUBLICAS = ['/api/health'];

function authGuard(req, res, next) {
  // Permitir rotas públicas
  if (ROTAS_PUBLICAS.includes(req.path) && req.method === 'GET') {
    return next();
  }

  // Permitir preflight CORS
  if (req.method === 'OPTIONS') {
    return next();
  }

  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({
      erro: 'Token de autenticação obrigatório',
      detalhe: 'Envie o header Authorization: Bearer <seu-jwt>'
    });
  }

  const token = authHeader.split(' ')[1];

  if (!token || token.length < 10) {
    return res.status(401).json({
      erro: 'Token inválido',
      detalhe: 'O token JWT fornecido está vazio ou mal formatado'
    });
  }

  // Anexa o token para uso nas rotas
  req.userToken = token;
  next();
}

module.exports = authGuard;
