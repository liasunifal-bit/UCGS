/**
 * Application — Services (Use Cases)
 * Orquestra repositórios e aplica regras de negócio.
 */
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const {
  AlertaRepository,
  KpiRepository,
  MapaRepository,
  ManutencaoRepository,
  VacinaRepository,
  ProtocoloRepository,
  AcidenteRepository,
  UsuarioRepository,
} = require('../infrastructure/repositories');

// ─── Auth ────────────────────────────────────────────────────────────────────
const AuthService = {
  async login(email, senha) {
    const usuario = UsuarioRepository.findByEmail(email);
    if (!usuario) throw { status: 401, message: 'Credenciais inválidas' };

    const senhaOk = await bcrypt.compare(senha, usuario.senha_hash);
    if (!senhaOk) throw { status: 401, message: 'Credenciais inválidas' };

    const token = jwt.sign(
      { id: usuario.id, email: usuario.email, papel: usuario.papel },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRES_IN || '8h' }
    );

    return { token, usuario: { id: usuario.id, nome: usuario.nome, email: usuario.email, papel: usuario.papel } };
  },
};

// ─── Alertas ─────────────────────────────────────────────────────────────────
const AlertaService = {
  listar(filtros) {
    return AlertaRepository.findAll(filtros);
  },

  resolver(id) {
    const alerta = AlertaRepository.findById(id);
    if (!alerta) throw { status: 404, message: 'Alerta não encontrado' };
    if (alerta.resolvido) throw { status: 400, message: 'Alerta já resolvido' };
    AlertaRepository.resolver(id);
    return { message: 'Alerta resolvido com sucesso' };
  },

  criar(data) {
    if (!data.tipo || !data.titulo || !data.ala) {
      throw { status: 400, message: 'Campos obrigatórios: tipo, titulo, ala' };
    }
    return AlertaRepository.create(data);
  },
};

// ─── KPIs ─────────────────────────────────────────────────────────────────────
const KpiService = {
  get() { return KpiRepository.get(); },
};

// ─── Mapas ───────────────────────────────────────────────────────────────────
const MapaService = {
  listar() { return MapaRepository.findAll(); },

  atualizar(id, data) {
    const mapa = MapaRepository.findById(id);
    if (!mapa) throw { status: 404, message: 'Mapa não encontrado' };
    MapaRepository.update(id, data);
    return MapaRepository.findById(id);
  },
};

// ─── Manutenção ───────────────────────────────────────────────────────────────
const ManutencaoService = {
  listar(filtro) { return ManutencaoRepository.findAll(filtro); },

  executar(id, data) {
    const item = ManutencaoRepository.findById(id);
    if (!item) throw { status: 404, message: 'Manutenção não encontrada' };
    if (!data.dataRealizada || !data.proximaData) {
      throw { status: 400, message: 'Campos obrigatórios: dataRealizada, proximaData' };
    }
    ManutencaoRepository.executar(id, data);
    return ManutencaoRepository.findById(id);
  },
};

// ─── Vacinas ─────────────────────────────────────────────────────────────────
const VacinaService = {
  listar() { return VacinaRepository.findAll(); },

  atualizar(id, data) {
    const item = VacinaRepository.findById(id);
    if (!item) throw { status: 404, message: 'Vacina não encontrada' };
    VacinaRepository.update(id, data);
    return VacinaRepository.findById(id);
  },
};

// ─── Protocolos ──────────────────────────────────────────────────────────────
const ProtocoloService = {
  listar() { return ProtocoloRepository.findAll(); },

  atualizar(id, data) {
    const item = ProtocoloRepository.findById(id);
    if (!item) throw { status: 404, message: 'Protocolo não encontrado' };
    ProtocoloRepository.update(id, data);
    return ProtocoloRepository.findById(id);
  },
};

// ─── Acidentes ───────────────────────────────────────────────────────────────
const AcidenteService = {
  listar(filtro) { return AcidenteRepository.findAll(filtro); },

  registrar(data) {
    if (!data.data || !data.tipo) {
      throw { status: 400, message: 'Campos obrigatórios: data, tipo' };
    }
    const result = AcidenteRepository.create(data);
    return AcidenteRepository.findById(result.lastInsertRowid);
  },
};

module.exports = {
  AuthService,
  AlertaService,
  KpiService,
  MapaService,
  ManutencaoService,
  VacinaService,
  ProtocoloService,
  AcidenteService,
};
