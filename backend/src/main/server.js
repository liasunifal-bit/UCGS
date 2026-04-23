/**
 * Main — Bootstrap do servidor Express (SST Dashboard API)
 * Usa sql.js (WebAssembly) — initDatabase() é assíncrono.
 */
require('dotenv').config();
const express     = require('express');
const cors        = require('cors');
const rateLimit   = require('express-rate-limit');
const swaggerUi   = require('swagger-ui-express');
const { initDatabase }  = require('../infrastructure/database');
const { errorHandler }  = require('../interfaces/middleware/errorHandler');
const { seedDatabase }  = require('../infrastructure/seed');

// ─── Rotas ─────────────────────────────────────────────────────────────────
const authRoutes       = require('../interfaces/routes/auth');
const alertasRoutes    = require('../interfaces/routes/alertas');
const mapasRoutes      = require('../interfaces/routes/mapas');
const manutencaoRoutes = require('../interfaces/routes/manutencao');
const vacinasRoutes    = require('../interfaces/routes/vacinas');
const protocolosRoutes = require('../interfaces/routes/protocolos');
const acidentes        = require('../interfaces/routes/acidentes');

// ─── App ────────────────────────────────────────────────────────────────────
const app = express();

app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use('/api', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 500,
  message: { error: 'Muitas requisições — aguarde alguns minutos.' },
}));

// ─── Swagger ────────────────────────────────────────────────────────────────
const swaggerDoc = {
  openapi: '3.0.0',
  info: {
    title: 'SST Dashboard API',
    version: '1.0.0',
    description: 'API REST — Dashboard de Segurança do Trabalho (Sistema Prisional)',
    contact: { name: 'Equipe SST' },
  },
  servers: [{ url: `http://localhost:${process.env.PORT || 3001}` }],
  components: {
    securitySchemes: { bearerAuth: { type: 'http', scheme: 'bearer', bearerFormat: 'JWT' } },
  },
  paths: {
    '/api/auth/login': { post: { tags:['Auth'], summary:'Login', requestBody:{ required:true, content:{ 'application/json':{ schema:{ type:'object', properties:{ email:{type:'string',example:'admin@sst.gov'}, password:{type:'string',example:'admin123'} } } } } }, responses:{ 200:{description:'Token JWT'}, 401:{description:'Inválido'} } } },
    '/api/alertas': {
      get:  { tags:['Alertas'], summary:'Listar', security:[{bearerAuth:[]}], parameters:[{in:'query',name:'resolvido',schema:{type:'boolean'}},{in:'query',name:'tipo',schema:{type:'string'}}], responses:{200:{description:'OK'}} },
      post: { tags:['Alertas'], summary:'Criar', security:[{bearerAuth:[]}], requestBody:{required:true,content:{'application/json':{schema:{type:'object',required:['tipo','titulo','ala'],properties:{tipo:{type:'string'},titulo:{type:'string'},descricao:{type:'string'},prazo:{type:'string'},ala:{type:'string'},prioridade:{type:'integer'}}}}}}, responses:{201:{description:'Criado'}} },
    },
    '/api/alertas/{id}/resolver': { patch:{ tags:['Alertas'], summary:'Resolver', security:[{bearerAuth:[]}], parameters:[{in:'path',name:'id',required:true,schema:{type:'integer'}}], responses:{200:{description:'OK'},404:{description:'Não encontrado'}} } },
    '/api/alertas/kpis': { get:{ tags:['KPIs'], summary:'KPIs gerais', security:[{bearerAuth:[]}], responses:{200:{description:'OK'}} } },
    '/api/mapas': { get:{ tags:['Mapas'], summary:'Listar', security:[{bearerAuth:[]}], responses:{200:{description:'OK'}} } },
    '/api/mapas/{id}': { put:{ tags:['Mapas'], summary:'Atualizar', security:[{bearerAuth:[]}], parameters:[{in:'path',name:'id',required:true,schema:{type:'integer'}}], responses:{200:{description:'OK'}} } },
    '/api/manutencao': { get:{ tags:['Manutenção'], summary:'Listar', security:[{bearerAuth:[]}], responses:{200:{description:'OK'}} } },
    '/api/manutencao/{id}/executar': { patch:{ tags:['Manutenção'], summary:'Executar', security:[{bearerAuth:[]}], parameters:[{in:'path',name:'id',required:true,schema:{type:'integer'}}], responses:{200:{description:'OK'}} } },
    '/api/vacinas': { get:{ tags:['Vacinas'], summary:'Listar', security:[{bearerAuth:[]}], responses:{200:{description:'OK'}} } },
    '/api/vacinas/{id}': { put:{ tags:['Vacinas'], summary:'Atualizar', security:[{bearerAuth:[]}], parameters:[{in:'path',name:'id',required:true,schema:{type:'integer'}}], responses:{200:{description:'OK'}} } },
    '/api/protocolos': { get:{ tags:['Protocolos'], summary:'Listar', security:[{bearerAuth:[]}], responses:{200:{description:'OK'}} } },
    '/api/protocolos/{id}': { put:{ tags:['Protocolos'], summary:'Atualizar', security:[{bearerAuth:[]}], parameters:[{in:'path',name:'id',required:true,schema:{type:'integer'}}], responses:{200:{description:'OK'}} } },
    '/api/acidentes': {
      get:  { tags:['Acidentes'], summary:'Listar', security:[{bearerAuth:[]}], responses:{200:{description:'OK'}} },
      post: { tags:['Acidentes'], summary:'Registrar', security:[{bearerAuth:[]}], responses:{201:{description:'Criado'}} },
    },
  },
};
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDoc, {
  customCss: '.swagger-ui .topbar { background-color: #1a1a2e; }',
  customSiteTitle: 'SST Dashboard API',
}));

// ─── Health ─────────────────────────────────────────────────────────────────
app.get('/health', (_, res) => res.json({ status: 'ok', timestamp: new Date().toISOString(), version: '1.0.0' }));

// ─── Rotas API ───────────────────────────────────────────────────────────────
app.use('/api/auth',       authRoutes);
app.use('/api/alertas',    alertasRoutes);
app.use('/api/mapas',      mapasRoutes);
app.use('/api/manutencao', manutencaoRoutes);
app.use('/api/vacinas',    vacinasRoutes);
app.use('/api/protocolos', protocolosRoutes);
app.use('/api/acidentes',  acidentes);

// 404
app.use((req, res) => res.status(404).json({ error: `Rota não encontrada: ${req.method} ${req.path}` }));

// Error handler
app.use(errorHandler);

// ─── Bootstrap ───────────────────────────────────────────────────────────────
const PORT = process.env.PORT || 3001;

async function bootstrap() {
  await initDatabase();
  await seedDatabase();
  app.listen(PORT, () => {
    console.log(`\n🚀 SST Dashboard API → http://localhost:${PORT}`);
    console.log(`📚 Swagger UI        → http://localhost:${PORT}/api-docs`);
    console.log(`❤️  Health            → http://localhost:${PORT}/health`);
    console.log(`\n   POST /api/auth/login  →  { email: 'admin@sst.gov', password: 'admin123' }\n`);
  });
}

bootstrap().catch(err => {
  console.error('❌ Erro ao iniciar servidor:', err);
  process.exit(1);
});

module.exports = app;
