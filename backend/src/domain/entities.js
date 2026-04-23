/**
 * Domain — Entidades de negócio puras (sem dependências externas)
 * Definem a estrutura e regras de validade de cada entidade do domínio SST.
 */

class Alerta {
  constructor({ id, tipo, titulo, descricao, prazo, ala, prioridade, resolvido = 0 }) {
    this.id = id;
    this.tipo = tipo;              // URGENTE | ATENCAO | PENDENTE
    this.titulo = titulo;
    this.descricao = descricao;
    this.prazo = prazo;
    this.ala = ala;
    this.prioridade = prioridade; // 1=alta 2=media 3=baixa
    this.resolvido = Boolean(resolvido);
  }

  isValido() {
    return Boolean(this.tipo && this.titulo && this.ala);
  }
}

class MapaRisco {
  constructor({ id, ala, status, data_atualizacao, total_riscos, criticos }) {
    this.id = id;
    this.ala = ala;
    this.status = status;          // Atualizado | Vencido | Pendente
    this.dataAtualizacao = data_atualizacao;
    this.totalRiscos = total_riscos;
    this.criticos = criticos;
  }

  isVencido() {
    return this.status === 'Vencido';
  }
}

class Manutencao {
  constructor({ id, equipamento, status, ultima_manutencao, proxima_manutencao }) {
    this.id = id;
    this.equipamento = equipamento;
    this.status = status;          // Em dia | Atrasado
    this.ultimaManutencao = ultima_manutencao;
    this.proximaManutencao = proxima_manutencao;
  }

  isAtrasada() {
    return this.status === 'Atrasado';
  }
}

class Vacina {
  constructor({ id, nome, aplicadas, pendentes, estoque }) {
    this.id = id;
    this.nome = nome;
    this.aplicadas = aplicadas;
    this.pendentes = pendentes;
    this.estoque = estoque;
  }

  getStatusEstoque() {
    if (this.estoque < 50) return 'Crítico';
    if (this.estoque < 80) return 'Médio';
    return 'OK';
  }
}

class Protocolo {
  constructor({ id, tipo, total, revisados, pendentes }) {
    this.id = id;
    this.tipo = tipo;
    this.total = total;
    this.revisados = revisados;
    this.pendentes = pendentes;
  }

  getConformidade() {
    return this.total > 0 ? Math.round((this.revisados / this.total) * 100) : 0;
  }
}

class Acidente {
  constructor({ id, data, tipo, envolvido, descricao, gravidade, ala }) {
    this.id = id;
    this.data = data;
    this.tipo = tipo;
    this.envolvido = envolvido;
    this.descricao = descricao;
    this.gravidade = gravidade;   // Leve | Moderado | Grave
    this.ala = ala;
  }
}

module.exports = { Alerta, MapaRisco, Manutencao, Vacina, Protocolo, Acidente };
