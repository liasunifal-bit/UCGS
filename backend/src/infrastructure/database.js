/**
 * Infrastructure — Database (sql.js)
 * sql.js = SQLite compilado como WebAssembly → zero dependências nativas.
 * Persiste em disco lendo/escrevendo o arquivo binário a cada operação DML.
 */
require('dotenv').config();
const path = require('path');
const fs = require('fs');
const initSqlJs = require('sql.js');

const DB_PATH = process.env.DB_PATH || path.join(__dirname, '../../data/sst.sqlite');
fs.mkdirSync(path.dirname(DB_PATH), { recursive: true });

let db = null;

// ─── Persistência ─────────────────────────────────────────────────────────────
function save() {
  const data = db.export();
  fs.writeFileSync(DB_PATH, Buffer.from(data));
}

// ─── Helpers síncronos parecidos com better-sqlite3 ──────────────────────────
function run(sql, params = []) {
  db.run(sql, params);
  save();
  // lastInsertRowid via SELECT last_insert_rowid()
  const [row] = db.exec('SELECT last_insert_rowid() AS id');
  const rowid = row ? row.values[0][0] : null;
  return { lastInsertRowid: rowid };
}

function all(sql, params = []) {
  const result = db.exec(sql, params);
  if (!result.length) return [];
  const { columns, values } = result[0];
  return values.map(row => {
    const obj = {};
    columns.forEach((col, i) => { obj[col] = row[i]; });
    return obj;
  });
}

function get(sql, params = []) {
  const rows = all(sql, params);
  return rows[0] || undefined;
}

function prepare(sql) {
  return {
    run: (...args) => {
      const params = args.length === 1 && Array.isArray(args[0]) ? args[0] : args;
      return run(sql, params);
    },
    get: (...args) => {
      const params = args.length === 1 && Array.isArray(args[0]) ? args[0] : args;
      return get(sql, params);
    },
    all: (...args) => {
      const params = args.length === 1 && Array.isArray(args[0]) ? args[0] : args;
      return all(sql, params);
    },
  };
}

// ─── DDL ──────────────────────────────────────────────────────────────────────
function createTables() {
  const stmts = [
    `CREATE TABLE IF NOT EXISTS usuarios (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      nome         TEXT NOT NULL,
      email        TEXT UNIQUE NOT NULL,
      senha_hash   TEXT NOT NULL,
      papel        TEXT DEFAULT 'tecnico',
      criado_em    TEXT DEFAULT (datetime('now')),
      atualizado_em TEXT DEFAULT (datetime('now'))
    )`,
    `CREATE TABLE IF NOT EXISTS alertas (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      tipo         TEXT NOT NULL,
      titulo       TEXT NOT NULL,
      descricao    TEXT,
      prazo        TEXT,
      ala          TEXT,
      prioridade   INTEGER DEFAULT 2,
      resolvido    INTEGER DEFAULT 0,
      criado_em    TEXT DEFAULT (datetime('now')),
      atualizado_em TEXT DEFAULT (datetime('now'))
    )`,
    `CREATE TABLE IF NOT EXISTS mapas_risco (
      id               INTEGER PRIMARY KEY AUTOINCREMENT,
      ala              TEXT NOT NULL,
      status           TEXT DEFAULT 'Pendente',
      data_atualizacao TEXT,
      total_riscos     INTEGER DEFAULT 0,
      criticos         INTEGER DEFAULT 0,
      atualizado_em    TEXT DEFAULT (datetime('now'))
    )`,
    `CREATE TABLE IF NOT EXISTS manutencoes (
      id                  INTEGER PRIMARY KEY AUTOINCREMENT,
      equipamento         TEXT NOT NULL,
      status              TEXT DEFAULT 'Em dia',
      ultima_manutencao   TEXT,
      proxima_manutencao  TEXT,
      atualizado_em       TEXT DEFAULT (datetime('now'))
    )`,
    `CREATE TABLE IF NOT EXISTS vacinas (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      nome         TEXT NOT NULL,
      aplicadas    INTEGER DEFAULT 0,
      pendentes    INTEGER DEFAULT 0,
      estoque      INTEGER DEFAULT 0,
      atualizado_em TEXT DEFAULT (datetime('now'))
    )`,
    `CREATE TABLE IF NOT EXISTS protocolos (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      tipo         TEXT NOT NULL,
      total        INTEGER DEFAULT 0,
      revisados    INTEGER DEFAULT 0,
      pendentes    INTEGER DEFAULT 0,
      observacao   TEXT,
      atualizado_em TEXT DEFAULT (datetime('now'))
    )`,
    `CREATE TABLE IF NOT EXISTS acidentes (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      data         TEXT NOT NULL,
      tipo         TEXT,
      envolvido    TEXT,
      descricao    TEXT,
      gravidade    TEXT DEFAULT 'Leve',
      ala          TEXT,
      criado_em    TEXT DEFAULT (datetime('now'))
    )`,
  ];
  stmts.forEach(s => db.run(s));
  save();
}

// ─── Init assíncrono ──────────────────────────────────────────────────────────
let _initPromise = null;

async function initDatabase() {
  if (_initPromise) return _initPromise;
  _initPromise = (async () => {
    const SQL = await initSqlJs();
    if (fs.existsSync(DB_PATH)) {
      const fileBuffer = fs.readFileSync(DB_PATH);
      db = new SQL.Database(fileBuffer);
    } else {
      db = new SQL.Database();
    }
    db.run('PRAGMA foreign_keys = ON');
    createTables();
    // Expõe prepare no objeto db (apenas para compatibilidade interna)
    db.prepare = prepare;
    console.log('✅ Banco de dados inicializado:', DB_PATH);
  })();
  return _initPromise;
}

// Proxy para que repositories.js possa chamar db.prepare antes do await
const dbProxy = new Proxy({}, {
  get: (_, prop) => {
    if (!db) throw new Error('Banco ainda não inicializado. Aguarde initDatabase().');
    if (prop === 'prepare') return prepare;
    return db[prop];
  },
});

module.exports = { db: dbProxy, initDatabase, run, all, get, prepare };
