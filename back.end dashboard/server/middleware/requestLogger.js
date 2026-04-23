/**
 * UCGS Backend — Request Logger
 *
 * Loga detalhes de cada requisição para debug.
 * Em produção, reduzir verbosidade.
 */

function requestLogger(req, res, next) {
  const inicio = Date.now();

  console.log(`\n${'═'.repeat(60)}`);
  console.log(`📥 ${req.method} ${req.path}`);
  console.log(`🕐 ${new Date().toISOString()}`);
  console.log(`🔑 Token presente: ${!!req.headers.authorization}`);

  if (req.method !== 'GET' && req.body && Object.keys(req.body).length > 0) {
    console.log('📦 Payload recebido:', JSON.stringify(req.body, null, 2));
  }

  if (Object.keys(req.query).length > 0) {
    console.log('🔍 Query params:', req.query);
  }

  // Interceptar a resposta para logar o resultado
  const originalJson = res.json.bind(res);
  res.json = function (data) {
    const duracao = Date.now() - inicio;
    console.log(`📤 Resposta: ${res.statusCode} (${duracao}ms)`);

    if (res.statusCode >= 400) {
      console.log('⚠️  Erro:', JSON.stringify(data, null, 2));
    }

    console.log(`${'═'.repeat(60)}\n`);
    return originalJson(data);
  };

  next();
}

module.exports = requestLogger;
