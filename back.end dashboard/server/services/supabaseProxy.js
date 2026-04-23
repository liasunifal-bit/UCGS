/**
 * UCGS Backend — Supabase Proxy Service
 *
 * Camada de comunicação com a API REST do Supabase.
 * Todas as chamadas passam por aqui para garantir:
 * - Headers corretos (apikey + Authorization)
 * - Tratamento de erros padronizado
 * - Logging de debug
 */

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;

/**
 * Executa uma requisição ao Supabase REST API.
 *
 * @param {string} method - HTTP method (GET, POST, PATCH, DELETE)
 * @param {string} table - Nome da tabela no Supabase
 * @param {object} options
 * @param {string} options.userToken - JWT do usuário autenticado
 * @param {object} [options.data] - Dados para POST/PATCH
 * @param {string} [options.filters] - Filtros PostgREST (ex: "id=eq.uuid")
 * @param {string} [options.select] - Colunas para retornar (default: *)
 * @param {string} [options.order] - Ordenação (ex: "nome.asc")
 * @param {number} [options.limit] - Limite de registros
 * @param {boolean} [options.single] - Retornar objeto único
 * @returns {Promise<object>} Resposta parseada do Supabase
 */
async function supabaseRequest(method, table, options = {}) {
  const {
    userToken,
    data = null,
    filters = '',
    select = '*',
    order = null,
    limit = null,
    single = false
  } = options;

  // Montar URL
  const params = [`select=${encodeURIComponent(select)}`];
  if (filters) params.push(filters);
  if (order) params.push(`order=${order}`);
  if (limit) params.push(`limit=${limit}`);

  const url = `${SUPABASE_URL}/rest/v1/${table}?${params.join('&')}`;

  // Montar headers
  const headers = {
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': `Bearer ${userToken}`,
    'Content-Type': 'application/json'
  };

  // Header Prefer para POST/PATCH (retornar representação)
  if (method === 'POST' || method === 'PATCH') {
    headers['Prefer'] = 'return=representation';
  }

  // Header para registro único
  if (single) {
    headers['Accept'] = 'application/vnd.pgrst.object+json';
  }

  // Opções do fetch
  const fetchOptions = { method, headers };
  if (data && (method === 'POST' || method === 'PATCH')) {
    fetchOptions.body = JSON.stringify(data);
  }

  console.log(`🔄 Supabase: ${method} ${table}`, filters ? `[${filters}]` : '');

  // Executar requisição
  const response = await fetch(url, fetchOptions);
  const responseText = await response.text();

  // Parsear resposta
  let responseData;
  try {
    responseData = responseText ? JSON.parse(responseText) : null;
  } catch {
    responseData = responseText;
  }

  // Tratar erro
  if (!response.ok) {
    console.error('❌ Supabase erro:', response.status, responseData);

    const error = new Error(
      (responseData && responseData.message) ||
      (responseData && responseData.msg) ||
      `Erro ${response.status} do Supabase`
    );
    error.status = response.status;
    error.supabaseError = true;
    error.supabaseCode = responseData && responseData.code;
    error.supabaseDetails = responseData;
    throw error;
  }

  console.log(`✅ Supabase: ${response.status} OK`);
  return responseData;
}

/**
 * Atalhos para operações comuns
 */
const supabase = {
  /**
   * INSERT — Inserir registro(s) na tabela
   */
  async insert(table, data, userToken) {
    return supabaseRequest('POST', table, { userToken, data });
  },

  /**
   * SELECT — Buscar registros da tabela
   */
  async select(table, userToken, options = {}) {
    return supabaseRequest('GET', table, { userToken, ...options });
  },

  /**
   * UPDATE — Atualizar registro(s) com filtro
   */
  async update(table, data, userToken, filters) {
    if (!filters) {
      throw new Error('SEGURANÇA: UPDATE sem filtro é proibido');
    }
    return supabaseRequest('PATCH', table, { userToken, data, filters });
  },

  /**
   * DELETE — Remover registro(s) com filtro
   */
  async remove(table, userToken, filters) {
    if (!filters) {
      throw new Error('SEGURANÇA: DELETE sem filtro é proibido');
    }
    return supabaseRequest('DELETE', table, { userToken, filters });
  }
};

module.exports = supabase;
