/**
 * Infrastructure — Repositórios (acesso ao banco)
 * Padrão Repository: isola a lógica de persistência das demais camadas.
 */
const { db } = require('./database');

// ─── Alertas ────────────────────────────────────────────────────────────────
const AlertaRepository = {
  findAll: (filtros = {}) => {
    let sql = 'SELECT * FROM alertas WHERE 1=1';
    const params = [];

    if (filtros.resolvido !== undefined) {
      sql += ' AND resolvido = ?';
      params.push(filtros.resolvido ? 1 : 0);
    }
    if (filtros.tipo) {
      sql += ' AND tipo = ?';
      params.push(filtros.tipo);
    }
    sql += ' ORDER BY prioridade ASC, criado_em DESC';
    return db.prepare(sql).all(...params);
  },

  findById: (id) => db.prepare('SELECT * FROM alertas WHERE id = ?').get(id),

  resolver: (id) => db.prepare(
    "UPDATE alertas SET resolvido = 1, atualizado_em = datetime('now') WHERE id = ?"
  ).run(id),

  create: (data) => {
    const stmt = db.prepare(
      'INSERT INTO alertas (tipo, titulo, descricao, prazo, ala, prioridade) VALUES (?, ?, ?, ?, ?, ?)'
    );
    return stmt.run(data.tipo, data.titulo, data.descricao, data.prazo, data.ala, data.prioridade || 2);
  },
};

// ─── KPIs ────────────────────────────────────────────────────────────────────
const KpiRepository = {
  get: () => {
    const alertasUrgentes = db.prepare(
      "SELECT COUNT(*) as total FROM alertas WHERE tipo = 'URGENTE' AND resolvido = 0"
    ).get().total;

    const manutAtrasadas = db.prepare(
      "SELECT COUNT(*) as total FROM manutencoes WHERE status = 'Atrasado'"
    ).get().total;

    const vacPendentes = db.prepare(
      'SELECT SUM(pendentes) as total FROM vacinas'
    ).get().total || 0;

    const protRevisados = db.prepare(
      'SELECT SUM(revisados) as rev, SUM(total) as tot FROM protocolos'
    ).get();
    const conformidade = protRevisados.tot > 0
      ? Math.round((protRevisados.rev / protRevisados.tot) * 100)
      : 0;

    const totalAcidentes = db.prepare(
      "SELECT COUNT(*) as total FROM acidentes WHERE data >= date('now', '-6 months')"
    ).get().total;

    return {
      alertasUrgentes,
      manutAtrasadas,
      vacPendentes,
      conformidade,
      totalAcidentes,
    };
  },
};

// ─── Mapas de Risco ──────────────────────────────────────────────────────────
const MapaRepository = {
  findAll: () => db.prepare('SELECT * FROM mapas_risco ORDER BY ala').all(),

  findById: (id) => db.prepare('SELECT * FROM mapas_risco WHERE id = ?').get(id),

  update: (id, data) => db.prepare(
    "UPDATE mapas_risco SET status = ?, data_atualizacao = ?, total_riscos = ?, criticos = ?, atualizado_em = datetime('now') WHERE id = ?"
  ).run(data.status, data.dataAtualizacao, data.totalRiscos, data.criticos, id),
};

// ─── Manutenções ─────────────────────────────────────────────────────────────
const ManutencaoRepository = {
  findAll: (filtro = {}) => {
    let sql = 'SELECT * FROM manutencoes WHERE 1=1';
    const params = [];
    if (filtro.status) { sql += ' AND status = ?'; params.push(filtro.status); }
    sql += ' ORDER BY status DESC, proxima_manutencao ASC';
    return db.prepare(sql).all(...params);
  },

  findById: (id) => db.prepare('SELECT * FROM manutencoes WHERE id = ?').get(id),

  executar: (id, data) => db.prepare(
    "UPDATE manutencoes SET status = 'Em dia', ultima_manutencao = ?, proxima_manutencao = ?, atualizado_em = datetime('now') WHERE id = ?"
  ).run(data.dataRealizada, data.proximaData, id),
};

// ─── Vacinas ─────────────────────────────────────────────────────────────────
const VacinaRepository = {
  findAll: () => db.prepare('SELECT * FROM vacinas ORDER BY nome').all(),

  findById: (id) => db.prepare('SELECT * FROM vacinas WHERE id = ?').get(id),

  update: (id, data) => db.prepare(
    "UPDATE vacinas SET aplicadas = ?, pendentes = ?, estoque = ?, atualizado_em = datetime('now') WHERE id = ?"
  ).run(data.aplicadas, data.pendentes, data.estoque, id),
};

// ─── Protocolos ──────────────────────────────────────────────────────────────
const ProtocoloRepository = {
  findAll: () => db.prepare('SELECT * FROM protocolos ORDER BY tipo').all(),

  findById: (id) => db.prepare('SELECT * FROM protocolos WHERE id = ?').get(id),

  update: (id, data) => db.prepare(
    "UPDATE protocolos SET revisados = ?, pendentes = ?, observacao = ?, atualizado_em = datetime('now') WHERE id = ?"
  ).run(data.revisados, data.pendentes, data.observacao, id),
};

// ─── Acidentes ───────────────────────────────────────────────────────────────
const AcidenteRepository = {
  findAll: (filtro = {}) => {
    let sql = 'SELECT * FROM acidentes WHERE 1=1';
    const params = [];
    if (filtro.gravidade) { sql += ' AND gravidade = ?'; params.push(filtro.gravidade); }
    sql += ' ORDER BY data DESC';
    return db.prepare(sql).all(...params);
  },

  findById: (id) => db.prepare('SELECT * FROM acidentes WHERE id = ?').get(id),

  create: (data) => db.prepare(
    'INSERT INTO acidentes (data, tipo, envolvido, descricao, gravidade, ala) VALUES (?, ?, ?, ?, ?, ?)'
  ).run(data.data, data.tipo, data.envolvido, data.descricao, data.gravidade, data.ala),
};

// ─── Usuários ─────────────────────────────────────────────────────────────────
const UsuarioRepository = {
  findByEmail: (email) => db.prepare('SELECT * FROM usuarios WHERE email = ?').get(email),
};

module.exports = {
  AlertaRepository,
  KpiRepository,
  MapaRepository,
  ManutencaoRepository,
  VacinaRepository,
  ProtocoloRepository,
  AcidenteRepository,
  UsuarioRepository,
};
