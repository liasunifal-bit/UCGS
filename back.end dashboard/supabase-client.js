/**
 * UCGS — Supabase Client
 * Módulo de integração entre o frontend e o Supabase via REST API.
 * 
 * COMO USAR:
 * 1. Adicione no HTML: <script src="supabase-client.js"></script>
 * 2. Chame: await SupabaseClient.auth.login(email, senha)
 * 3. Depois: await SupabaseClient.from('pacientes').select()
 */

const SupabaseClient = (function () {

  // ============================================================
  // CONFIGURAÇÃO — Seus dados do projeto Supabase
  // ============================================================
  const CONFIG = {
    url: 'https://llqphjlpypnyvknpfdyn.supabase.co',
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow'
  };

  // ============================================================
  // GERENCIAMENTO DE SESSÃO (Token JWT)
  // ============================================================
  function getSession() {
    const raw = localStorage.getItem('ucgs_session');
    if (!raw) return null;
    try { return JSON.parse(raw); } catch { return null; }
  }

  function saveSession(data) {
    localStorage.setItem('ucgs_session', JSON.stringify({
      access_token: data.access_token,
      refresh_token: data.refresh_token,
      user: data.user
    }));
  }

  function clearSession() {
    localStorage.removeItem('ucgs_session');
  }

  function getToken() {
    const session = getSession();
    return session ? session.access_token : null;
  }

  function getUser() {
    const session = getSession();
    return session ? session.user : null;
  }

  // ============================================================
  // HEADERS BASE
  // ============================================================
  function baseHeaders() {
    return {
      'apikey': CONFIG.anonKey,
      'Content-Type': 'application/json'
    };
  }

  function authHeaders() {
    const token = getToken();
    const headers = baseHeaders();
    if (token) {
      headers['Authorization'] = 'Bearer ' + token;
    }
    return headers;
  }

  // ============================================================
  // MÓDULO DE AUTENTICAÇÃO
  // ============================================================
  const auth = {

    /** Login com email e senha */
    async login(email, password) {
      const res = await fetch(CONFIG.url + '/auth/v1/token?grant_type=password', {
        method: 'POST',
        headers: baseHeaders(),
        body: JSON.stringify({ email, password })
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error_description || data.msg || 'Erro no login');
      }

      saveSession(data);
      return data;
    },

    /** Cadastro de novo usuário */
    async signup(email, password, metadata) {
      const res = await fetch(CONFIG.url + '/auth/v1/signup', {
        method: 'POST',
        headers: baseHeaders(),
        body: JSON.stringify({
          email,
          password,
          data: metadata || {}
        })
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error_description || data.msg || 'Erro no cadastro');
      }

      return data;
    },

    /** Logout */
    async logout() {
      const token = getToken();
      if (token) {
        await fetch(CONFIG.url + '/auth/v1/logout', {
          method: 'POST',
          headers: {
            ...baseHeaders(),
            'Authorization': 'Bearer ' + token
          }
        });
      }
      clearSession();
    },

    /** Retorna o usuário logado ou null */
    getUser() {
      return getUser();
    },

    /** Retorna o token JWT atual ou null */
    getToken() {
      return getToken();
    },

    /** Verifica se está logado */
    isLoggedIn() {
      return !!getToken();
    }
  };

  // ============================================================
  // QUERY BUILDER — Padrão fluente para operações CRUD
  // ============================================================
  function from(tableName) {
    let _select = '*';
    let _filters = [];
    let _order = null;
    let _limit = null;
    let _single = false;

    const builder = {

      /** Define quais colunas retornar */
      select(columns) {
        _select = columns || '*';
        return builder;
      },

      /** Filtro: coluna igual a valor */
      eq(col, val) {
        _filters.push(col + '=eq.' + val);
        return builder;
      },

      /** Filtro: coluna diferente de valor */
      neq(col, val) {
        _filters.push(col + '=neq.' + val);
        return builder;
      },

      /** Filtro: busca parcial (ILIKE) */
      ilike(col, val) {
        _filters.push(col + '=ilike.' + val);
        return builder;
      },

      /** Filtro: maior que */
      gt(col, val) {
        _filters.push(col + '=gt.' + val);
        return builder;
      },

      /** Filtro: menor que */
      lt(col, val) {
        _filters.push(col + '=lt.' + val);
        return builder;
      },

      /** Filtro: valor está na lista */
      in(col, values) {
        _filters.push(col + '=in.(' + values.join(',') + ')');
        return builder;
      },

      /** Ordenação */
      order(col, ascending) {
        _order = col + (ascending === false ? '.desc' : '.asc');
        return builder;
      },

      /** Limitar quantidade */
      limit(n) {
        _limit = n;
        return builder;
      },

      /** Retornar apenas 1 registro */
      single() {
        _single = true;
        return builder;
      },

      /** Monta a URL final */
      _buildUrl() {
        let url = CONFIG.url + '/rest/v1/' + tableName;
        const params = [];
        params.push('select=' + encodeURIComponent(_select));
        _filters.forEach(function (f) { params.push(f); });
        if (_order) params.push('order=' + _order);
        if (_limit) params.push('limit=' + _limit);
        return url + '?' + params.join('&');
      },

      // ---- OPERAÇÕES ----

      /** GET — Buscar registros */
      async get() {
        const headers = authHeaders();
        if (_single) headers['Accept'] = 'application/vnd.pgrst.object+json';

        const res = await fetch(builder._buildUrl(), { headers });
        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.message || 'Erro ao buscar dados');
        }
        return res.json();
      },

      /** POST — Inserir registro */
      async insert(data) {
        const headers = authHeaders();
        headers['Prefer'] = 'return=representation';

        const res = await fetch(CONFIG.url + '/rest/v1/' + tableName, {
          method: 'POST',
          headers,
          body: JSON.stringify(data)
        });

        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.message || 'Erro ao inserir');
        }
        return res.json();
      },

      /** PATCH — Atualizar registro (REQUER filtro!) */
      async update(data) {
        if (_filters.length === 0) {
          throw new Error('SEGURANÇA: PATCH sem filtro é proibido. Use .eq("id", valor) antes de .update()');
        }

        const headers = authHeaders();
        headers['Prefer'] = 'return=representation';

        const url = CONFIG.url + '/rest/v1/' + tableName + '?' + _filters.join('&');
        const res = await fetch(url, {
          method: 'PATCH',
          headers,
          body: JSON.stringify(data)
        });

        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.message || 'Erro ao atualizar');
        }
        return res.json();
      },

      /** DELETE — Remover registro (REQUER filtro!) */
      async delete() {
        if (_filters.length === 0) {
          throw new Error('SEGURANÇA: DELETE sem filtro é proibido. Use .eq("id", valor) antes de .delete()');
        }

        const url = CONFIG.url + '/rest/v1/' + tableName + '?' + _filters.join('&');
        const res = await fetch(url, {
          method: 'DELETE',
          headers: authHeaders()
        });

        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.message || 'Erro ao deletar');
        }
        return res.text();
      }
    };

    return builder;
  }

  // ============================================================
  // API PÚBLICA
  // ============================================================
  return { auth, from, CONFIG };

})();
