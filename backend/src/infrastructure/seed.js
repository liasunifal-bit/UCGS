/**
 * Infrastructure — Seed de dados iniciais
 * Exporta seedDatabase() chamada pelo bootstrap do server.
 */
require('dotenv').config();
const bcrypt = require('bcryptjs');
const { prepare, run } = require('./database');

async function seedDatabase() {
  console.log('🌱 Verificando seed do banco SST...');

  // ─── Usuários ──────────────────────────────────────────────────
  const senhaHash = bcrypt.hashSync('admin123', 10);
  prepare(`INSERT OR IGNORE INTO usuarios (nome, email, senha_hash, papel) VALUES (?, ?, ?, ?)`)
    .run('Administrador SST', 'admin@sst.gov', senhaHash, 'admin');
  prepare(`INSERT OR IGNORE INTO usuarios (nome, email, senha_hash, papel) VALUES (?, ?, ?, ?)`)
    .run('Técnico de Segurança', 'tecnico@sst.gov', bcrypt.hashSync('tecnico123', 10), 'tecnico');

  // Pula o restante se já existem dados
  const { count } = prepare('SELECT COUNT(*) AS count FROM alertas').get();
  if (Number(count) > 0) {
    console.log('✅ Banco já possui dados — seed ignorado.');
    return;
  }

  // ─── Alertas ───────────────────────────────────────────────────
  const insAlerta = prepare(`INSERT INTO alertas (tipo, titulo, descricao, prazo, ala, prioridade) VALUES (?, ?, ?, ?, ?, ?)`);
  [
    ['URGENTE', 'EPIs Vencidos — Ala B', 'Equipamentos com validade expirada em março/2026', '2026-03-25', 'Ala B', 1],
    ['URGENTE', 'Extintores sem recarga', '12 extintores vencidos detectados na inspeção trimestral', '2026-03-22', 'Ala C', 1],
    ['ATENCAO', 'Manutenção Preventiva Atrasada', 'Gerador secundário com manutenção prescrita há 45 dias', '2026-03-28', 'Central', 2],
    ['ATENCAO', 'Treinamento NR-18 Pendente', '23 funcionários sem certificação obrigatória', '2026-04-05', 'Administração', 2],
    ['ATENCAO', 'Iluminação de emergência', '4 luminárias com falha na Ala D', '2026-03-30', 'Ala D', 2],
    ['PENDENTE', 'Revisão Mapa de Risco Ala A', 'Revisão anual obrigatória vencendo em 10 dias', '2026-04-01', 'Ala A', 3],
    ['PENDENTE', 'Calibração de detectores de gás', 'Detectores sem calibração há 6 meses', '2026-04-10', 'Ala E', 3],
  ].forEach(r => insAlerta.run(...r));

  // ─── Mapas de Risco ────────────────────────────────────────────
  const insMapa = prepare(`INSERT INTO mapas_risco (ala, status, data_atualizacao, total_riscos, criticos) VALUES (?, ?, ?, ?, ?)`);
  [
    ['Ala A — Triagem', 'Vencido', '2025-10-12', 8, 2],
    ['Ala B — Custódia', 'Atualizado', '2026-02-18', 12, 1],
    ['Ala C — Máxima Segurança', 'Atualizado', '2026-03-01', 18, 4],
    ['Ala D — Feminina', 'Pendente', '2026-01-20', 6, 0],
    ['Ala E — Provisória', 'Atualizado', '2026-02-28', 9, 2],
    ['Ala Médica', 'Atualizado', '2026-03-10', 14, 3],
    ['Área Externa / Pátio', 'Vencido', '2025-09-05', 5, 1],
  ].forEach(r => insMapa.run(...r));

  // ─── Manutenções ───────────────────────────────────────────────
  const insMan = prepare(`INSERT INTO manutencoes (equipamento, status, ultima_manutencao, proxima_manutencao) VALUES (?, ?, ?, ?)`);
  [
    ['Gerador Diesel Principal', 'Em dia', '2025-12-15', '2026-06-15'],
    ['Gerador Diesel Secundário', 'Atrasado', '2025-09-10', '2026-03-10'],
    ['Sistema HVAC — Ala C', 'Em dia', '2026-02-01', '2026-08-01'],
    ['Sistema HVAC — Ala Médica', 'Atrasado', '2025-11-20', '2026-02-20'],
    ['Elevador de Carga', 'Em dia', '2026-01-15', '2026-07-15'],
    ['Compressor de Ar Industrial', 'Em dia', '2026-02-10', '2026-05-10'],
    ['Quadro Elétrico Principal', 'Atrasado', '2025-10-05', '2026-01-05'],
    ['Bomba de Incêndio', 'Em dia', '2026-01-20', '2026-07-20'],
  ].forEach(r => insMan.run(...r));

  // ─── Vacinas ───────────────────────────────────────────────────
  const insVac = prepare(`INSERT INTO vacinas (nome, aplicadas, pendentes, estoque) VALUES (?, ?, ?, ?)`);
  [
    ['COVID-19 (Booster)', 312, 45, 120],
    ['Hepatite B', 287, 18, 95],
    ['Tétano', 256, 31, 78],
    ['Influenza', 342, 12, 210],
    ['Febre Amarela', 89, 4, 45],
    ['Hepatite A', 198, 22, 60],
  ].forEach(r => insVac.run(...r));

  // ─── Protocolos ────────────────────────────────────────────────
  const insProt = prepare(`INSERT INTO protocolos (tipo, total, revisados, pendentes) VALUES (?, ?, ?, ?)`);
  [
    ['Emergência e Evacuação', 24, 21, 3],
    ['Uso de EPIs', 18, 18, 0],
    ['Manuseio de Substâncias', 12, 9, 3],
    ['Prevenção de Incêndio', 16, 14, 2],
    ['Controle de Infecções', 20, 17, 3],
    ['Trabalho em Altura', 8, 6, 2],
  ].forEach(r => insProt.run(...r));

  // ─── Acidentes ─────────────────────────────────────────────────
  const insAc = prepare(`INSERT INTO acidentes (data, tipo, envolvido, descricao, gravidade, ala) VALUES (?, ?, ?, ?, ?, ?)`);
  [
    ['2025-11-12', 'Queda', 'Funcionário', 'Queda em rampa escorregadia após chuva', 'Leve', 'Área Externa'],
    ['2025-10-28', 'Corte', 'Funcionário', 'Laceração na mão durante manuseio de equip.', 'Leve', 'Ala B'],
    ['2025-09-05', 'Ergonômico', 'Funcionário', 'LER por esforço repetitivo no setor adm.', 'Moderado', 'Administração'],
    ['2025-08-17', 'Elétrico', 'Funcionário', 'Choque leve em quadro sem sinalização', 'Moderado', 'Ala C'],
    ['2025-07-22', 'Incêndio', 'Funcionário', 'Pequeno foco no almoxarifado — controlado', 'Grave', 'Almoxarifado'],
    ['2025-06-11', 'Queda', 'Funcionário', 'Queda de objeto da prateleira alta', 'Leve', 'Ala A'],
  ].forEach(r => insAc.run(...r));

  console.log('✅ Seed concluído com sucesso!');
  console.log('   👤 admin@sst.gov / admin123');
  console.log('   👤 tecnico@sst.gov / tecnico123');
}

module.exports = { seedDatabase };
