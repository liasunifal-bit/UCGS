/**
 * UCGS Backend — Rotas de Pacientes
 *
 * CRUD completo da tabela `pacientes` no Supabase.
 *
 * Endpoints:
 *   POST   /api/pacientes      → Cadastrar paciente
 *   GET    /api/pacientes      → Listar pacientes
 *   GET    /api/pacientes/:id  → Buscar por ID
 *   PATCH  /api/pacientes/:id  → Atualizar paciente
 *   DELETE /api/pacientes/:id  → Soft-delete (ativo=false)
 */

const express = require('express');
const router = express.Router();
const supabase = require('../services/supabaseProxy');
const {
  validarObrigatorios,
  validarCPF,
  validarEmail,
  validarData,
  validarUUID,
  sanitizar,
  limparCPF,
  erroValidacao
} = require('../utils/validators');

// ============================================================
// POST /api/pacientes — Cadastrar novo paciente
// ============================================================
router.post('/', async (req, res, next) => {
  try {
    const body = req.body;

    // 1. Validar campos obrigatórios
    const { valido, faltando } = validarObrigatorios(
      ['nome', 'cpf', 'nascimento', 'sexo'],
      body
    );

    if (!valido) {
      throw erroValidacao(
        `Campos obrigatórios faltando: ${faltando.join(', ')}`
      );
    }

    // 2. Validações específicas
    if (!validarCPF(body.cpf)) {
      throw erroValidacao('CPF inválido. Envie 11 dígitos numéricos.');
    }

    if (body.email && !validarEmail(body.email)) {
      throw erroValidacao('Email com formato inválido.');
    }

    if (!validarData(body.nascimento)) {
      throw erroValidacao('Data de nascimento inválida. Use o formato YYYY-MM-DD.');
    }

    const sexosPermitidos = ['masculino', 'feminino', 'outro', 'nao_informado'];
    if (!sexosPermitidos.includes(body.sexo)) {
      throw erroValidacao(
        `Sexo inválido. Valores aceitos: ${sexosPermitidos.join(', ')}`
      );
    }

    // 3. Mapeamento Frontend → Supabase
    const dadosParaSupabase = {
      nome:         sanitizar(body.nome),
      cpf:          limparCPF(body.cpf),
      nascimento:   body.nascimento,
      sexo:         body.sexo,
      telefone:     body.telefone     ? sanitizar(body.telefone)     : null,
      email:        body.email        ? sanitizar(body.email)        : null,
      logradouro:   body.logradouro   ? sanitizar(body.logradouro)   : null,
      numero:       body.numero       ? sanitizar(body.numero)       : null,
      complemento:  body.complemento  ? sanitizar(body.complemento)  : null,
      bairro:       body.bairro       ? sanitizar(body.bairro)       : null,
      cidade:       body.cidade       ? sanitizar(body.cidade)       : null,
      uf:           body.uf           ? body.uf.toUpperCase()        : null,
      cep:          body.cep          ? body.cep.replace(/\D/g, '')  : null,
      observacoes:  body.observacoes  ? sanitizar(body.observacoes)  : null
    };

    console.log('📋 Dados mapeados para Supabase:', dadosParaSupabase);

    // 4. Inserir no Supabase
    const resultado = await supabase.insert('pacientes', dadosParaSupabase, req.userToken);

    res.status(201).json({
      sucesso: true,
      mensagem: 'Paciente cadastrado com sucesso',
      dados: resultado
    });

  } catch (err) {
    next(err);
  }
});

// ============================================================
// GET /api/pacientes — Listar pacientes
// ============================================================
router.get('/', async (req, res, next) => {
  try {
    const options = {
      order: 'nome.asc'
    };

    // Filtro de busca por nome (query param ?busca=...)
    if (req.query.busca) {
      options.filters = `nome=ilike.*${req.query.busca}*`;
    }

    // Filtro por status ativo (default: apenas ativos)
    if (req.query.ativo !== 'todos') {
      const filtroAtivo = 'ativo=eq.true';
      options.filters = options.filters
        ? `${options.filters}&${filtroAtivo}`
        : filtroAtivo;
    }

    // Limite
    if (req.query.limite) {
      options.limit = parseInt(req.query.limite) || 50;
    }

    const pacientes = await supabase.select('pacientes', req.userToken, options);

    res.json({
      sucesso: true,
      total: Array.isArray(pacientes) ? pacientes.length : 0,
      dados: pacientes
    });

  } catch (err) {
    next(err);
  }
});

// ============================================================
// GET /api/pacientes/:id — Buscar paciente por ID
// ============================================================
router.get('/:id', async (req, res, next) => {
  try {
    if (!validarUUID(req.params.id)) {
      throw erroValidacao('ID inválido. Envie um UUID válido.');
    }

    const paciente = await supabase.select('pacientes', req.userToken, {
      filters: `id=eq.${req.params.id}`,
      single: true
    });

    res.json({
      sucesso: true,
      dados: paciente
    });

  } catch (err) {
    // Se o Supabase retornar 406 (nenhum registro), tratar como 404
    if (err.status === 406) {
      return res.status(404).json({
        sucesso: false,
        erro: 'Paciente não encontrado'
      });
    }
    next(err);
  }
});

// ============================================================
// PATCH /api/pacientes/:id — Atualizar paciente
// ============================================================
router.patch('/:id', async (req, res, next) => {
  try {
    if (!validarUUID(req.params.id)) {
      throw erroValidacao('ID inválido. Envie um UUID válido.');
    }

    const body = req.body;

    if (!body || Object.keys(body).length === 0) {
      throw erroValidacao('Nenhum campo para atualizar foi enviado.');
    }

    // Montar objeto apenas com campos enviados
    const dadosAtualizacao = {};
    const camposPermitidos = [
      'nome', 'cpf', 'nascimento', 'sexo', 'telefone', 'email',
      'logradouro', 'numero', 'complemento', 'bairro', 'cidade',
      'uf', 'cep', 'observacoes', 'ativo'
    ];

    for (const campo of camposPermitidos) {
      if (body[campo] !== undefined) {
        // Aplicar sanitização/transformação por campo
        if (campo === 'cpf') {
          if (!validarCPF(body.cpf)) throw erroValidacao('CPF inválido.');
          dadosAtualizacao.cpf = limparCPF(body.cpf);
        } else if (campo === 'email') {
          if (body.email && !validarEmail(body.email)) throw erroValidacao('Email inválido.');
          dadosAtualizacao.email = body.email ? sanitizar(body.email) : null;
        } else if (campo === 'nascimento') {
          if (!validarData(body.nascimento)) throw erroValidacao('Data inválida.');
          dadosAtualizacao.nascimento = body.nascimento;
        } else if (campo === 'uf') {
          dadosAtualizacao.uf = body.uf ? body.uf.toUpperCase() : null;
        } else if (campo === 'cep') {
          dadosAtualizacao.cep = body.cep ? body.cep.replace(/\D/g, '') : null;
        } else if (campo === 'ativo') {
          dadosAtualizacao.ativo = Boolean(body.ativo);
        } else if (typeof body[campo] === 'string') {
          dadosAtualizacao[campo] = sanitizar(body[campo]);
        } else {
          dadosAtualizacao[campo] = body[campo];
        }
      }
    }

    // Adicionar timestamp de atualização
    dadosAtualizacao.updated_at = new Date().toISOString();

    console.log('📋 Dados de atualização:', dadosAtualizacao);

    const resultado = await supabase.update(
      'pacientes',
      dadosAtualizacao,
      req.userToken,
      `id=eq.${req.params.id}`
    );

    res.json({
      sucesso: true,
      mensagem: 'Paciente atualizado com sucesso',
      dados: resultado
    });

  } catch (err) {
    next(err);
  }
});

// ============================================================
// DELETE /api/pacientes/:id — Soft-delete (ativo=false)
// ============================================================
router.delete('/:id', async (req, res, next) => {
  try {
    if (!validarUUID(req.params.id)) {
      throw erroValidacao('ID inválido. Envie um UUID válido.');
    }

    // Soft-delete: apenas marca como inativo
    // A política RLS bloqueia DELETE físico (polcmd='d' → false)
    const resultado = await supabase.update(
      'pacientes',
      { ativo: false, updated_at: new Date().toISOString() },
      req.userToken,
      `id=eq.${req.params.id}`
    );

    res.json({
      sucesso: true,
      mensagem: 'Paciente desativado com sucesso',
      dados: resultado
    });

  } catch (err) {
    next(err);
  }
});

module.exports = router;
