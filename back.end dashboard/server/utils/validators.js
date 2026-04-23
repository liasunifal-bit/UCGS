/**
 * UCGS Backend — Validadores
 *
 * Funções de validação reutilizáveis para campos do sistema clínico.
 */

/**
 * Valida que todos os campos obrigatórios estão presentes e não vazios.
 * @param {string[]} campos - Lista de nomes de campos obrigatórios
 * @param {object} body - Corpo da requisição
 * @returns {{ valido: boolean, faltando: string[] }}
 */
function validarObrigatorios(campos, body) {
  const faltando = [];

  for (const campo of campos) {
    const valor = body[campo];
    if (valor === undefined || valor === null || valor === '') {
      faltando.push(campo);
    }
  }

  return {
    valido: faltando.length === 0,
    faltando
  };
}

/**
 * Valida formato de CPF (apenas formato, não dígitos verificadores).
 * Aceita: "123.456.789-00" ou "12345678900"
 * @param {string} cpf
 * @returns {boolean}
 */
function validarCPF(cpf) {
  if (!cpf) return false;
  const limpo = cpf.replace(/\D/g, '');
  return limpo.length === 11;
}

/**
 * Valida formato básico de email.
 * @param {string} email
 * @returns {boolean}
 */
function validarEmail(email) {
  if (!email) return true; // Email é opcional em pacientes
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

/**
 * Valida formato de data (YYYY-MM-DD).
 * @param {string} data
 * @returns {boolean}
 */
function validarData(data) {
  if (!data) return false;
  const regex = /^\d{4}-\d{2}-\d{2}$/;
  if (!regex.test(data)) return false;

  const d = new Date(data);
  return d instanceof Date && !isNaN(d);
}

/**
 * Valida formato de UUID.
 * @param {string} uuid
 * @returns {boolean}
 */
function validarUUID(uuid) {
  if (!uuid) return false;
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(uuid);
}

/**
 * Limpa e padroniza uma string: trim + colapsar espaços.
 * @param {string} str
 * @returns {string}
 */
function sanitizar(str) {
  if (typeof str !== 'string') return str;
  return str.trim().replace(/\s+/g, ' ');
}

/**
 * Limpa CPF para formato numérico (11 dígitos).
 * @param {string} cpf
 * @returns {string}
 */
function limparCPF(cpf) {
  if (!cpf) return cpf;
  return cpf.replace(/\D/g, '');
}

/**
 * Cria um erro de validação padronizado.
 * @param {string} mensagem
 * @returns {Error}
 */
function erroValidacao(mensagem) {
  const err = new Error(mensagem);
  err.status = 400;
  return err;
}

module.exports = {
  validarObrigatorios,
  validarCPF,
  validarEmail,
  validarData,
  validarUUID,
  sanitizar,
  limparCPF,
  erroValidacao
};
