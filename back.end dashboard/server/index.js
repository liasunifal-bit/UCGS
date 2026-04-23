/**
 * UCGS Backend — Entry Point
 *
 * Servidor Express.js que atua como proxy entre o frontend UCGS
 * e o Supabase REST API.
 *
 * Uso:
 *   npm start       → Iniciar em produção
 *   npm run dev     → Iniciar com hot-reload (Node 18+)
 */

require('dotenv').config();

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');

// Middlewares
const authGuard = require('./middleware/authGuard');
const errorHandler = require('./middleware/errorHandler');
const requestLogger = require('./middleware/requestLogger');

// Rotas
const pacientesRoutes = require('./routes/pacientes');

// ============================================================
// CONFIGURAÇÃO
// ============================================================
const app = express();
const PORT = process.env.PORT || 3001;

// ============================================================
// MIDDLEWARE STACK (ordem importa!)
// ============================================================

// 1. Segurança — headers HTTP seguros
app.use(helmet());

// 2. CORS — permitir requisições do frontend
app.use(cors({
  origin: process.env.FRONTEND_ORIGIN || '*',
  methods: ['GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
}));

// 3. Body parser — parsear JSON do body
app.use(express.json({ limit: '10mb' }));

// 4. Logger — registrar cada requisição
app.use(requestLogger);

// ============================================================
// ROTAS PÚBLICAS (sem autenticação)
// ============================================================

// Health check (público, sem auth)
app.get('/api/health', (_req, res) => {
  res.json({
    status: 'online',
    servidor: 'UCGS Backend',
    versao: '1.0.0',
    timestamp: new Date().toISOString(),
    supabase_url: process.env.SUPABASE_URL ? 'configurado' : 'FALTANDO'
  });
});

// ============================================================
// AUTH GUARD — aplicado a todas as rotas abaixo
// ============================================================
app.use('/api', authGuard);

// ============================================================
// ROTAS PROTEGIDAS (requerem JWT)
// ============================================================

// Módulo: Pacientes
app.use('/api/pacientes', pacientesRoutes);

// ============================================================
// ROTAS FUTURAS (Fases 2-5)
// ============================================================
// app.use('/api/processos-enfermagem', processosEnfermagemRoutes);
// app.use('/api/atendimentos', atendimentosRoutes);
// app.use('/api/avaliacoes-nutricionais', avaliacoesNutriRoutes);
// app.use('/api/planos-alimentares', planosAlimentaresRoutes);
// app.use('/api/avaliacoes-fisioterapia', avaliacoesFisioRoutes);
// app.use('/api/sessoes-fisioterapia', sessoesFisioRoutes);
// app.use('/api/avaliacoes-odontologicas', avaliacoesOdontoRoutes);
// app.use('/api/avaliacoes-psicologicas', avaliacoesPsicoRoutes);
// app.use('/api/mapas-risco', mapasRiscoRoutes);
// app.use('/api/acidentes-trabalho', acidentesRoutes);

// ============================================================
// ROTA 404 — Endpoint não encontrado
// ============================================================
app.use('/api/*', (_req, res) => {
  res.status(404).json({
    erro: 'Endpoint não encontrado',
    detalhe: 'Verifique a URL e o método HTTP'
  });
});

// ============================================================
// ERROR HANDLER GLOBAL (deve ser o último middleware)
// ============================================================
app.use(errorHandler);

// ============================================================
// INICIAR SERVIDOR
// ============================================================
app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════════════════════╗
║                                                        ║
║   🏥  UCGS Backend — Servidor Iniciado                 ║
║                                                        ║
║   📡  URL:  http://localhost:${PORT}                     ║
║   🔗  Supabase: ${process.env.SUPABASE_URL ? '✅ Configurado' : '❌ FALTANDO'}                ║
║   🔑  Anon Key: ${process.env.SUPABASE_ANON_KEY ? '✅ Presente' : '❌ FALTANDO'}                  ║
║                                                        ║
║   📋  Rotas ativas:                                    ║
║       POST   /api/pacientes                            ║
║       GET    /api/pacientes                            ║
║       GET    /api/pacientes/:id                        ║
║       PATCH  /api/pacientes/:id                        ║
║       DELETE /api/pacientes/:id                        ║
║       GET    /api/health                               ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
  `);
});

module.exports = app;
