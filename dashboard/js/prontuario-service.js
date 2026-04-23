import { supabaseClient } from './supabase-config.js';

/**
 * Mapeia os dados vindos do banco (snake_case e formato moderno) 
 * para o formato esperado pela UI.
 */
function mapToUI(row) {
    if (!row) return row;
    return {
        id: row.id,
        paciente_id: row.paciente_id,
        tipo: row.tipo_entrada, // Mapeia tipo_entrada -> tipo (UI)
        titulo: row.titulo,
        descricao: row.conteudo, // Mapeia conteudo -> descricao (UI)
        // Se houver conduta nos dados extras, nós expomos para a UI
        conduta: row.dados_extras?.conduta || '',
        especialidade: row.especialidade,
        autor_id: row.profissional_id,
        autor: row.profissional ? row.profissional.nome_completo : 'Profissional não identificado',
        data: row.data_entrada, // A UI pode estar esperando 'data'
        data_criacao: row.created_at,
        status: row.status
    };
}

export const ProntuarioService = {
    /**
     * Busca as entradas do prontuário (antigas evoluções) de um paciente específico.
     * Utiliza a tabela moderna 'entradas_prontuario'.
     */
    async getEvolucoes(pacienteId) {
        const { data, error } = await supabaseClient
            .from('entradas_prontuario')
            .select(`
                *,
                profissional:profissional_id (nome_completo)
            `)
            .eq('paciente_id', pacienteId)
            .order('data_entrada', { ascending: false });

        if (error) throw error;
        
        return data.map(mapToUI);
    },

    /**
     * Insere uma nova entrada no prontuário do paciente (nova evolução).
     */
    async insertEvolucao(evolucaoData) {
        // 1. Pega o usuário autenticado para ser o profissional_id
        const { data: { session } } = await supabaseClient.auth.getSession();
        if (!session) throw new Error("Usuário não autenticado");

        // 2. Busca o profile do usuário para preencher a especialidade padrão, se não for enviada
        let especialidadeEnviada = evolucaoData.especialidade || 'medico'; // default
        
        // Formatar para o schema da tabela 'entradas_prontuario'
        const dataToInsert = {
            paciente_id: evolucaoData.paciente_id,
            profissional_id: session.user.id,
            tipo_entrada: evolucaoData.tipo || 'evolucao',
            especialidade: especialidadeEnviada,
            titulo: evolucaoData.titulo || 'Nova Evolução',
            conteudo: evolucaoData.descricao || '',
            dados_extras: { conduta: evolucaoData.conduta || '' },
            status: 'finalizado', // ou 'rascunho', 'assinado'
            // data_entrada usa o default 'now()' do Postgres
        };

        const { data, error } = await supabaseClient
            .from('entradas_prontuario')
            .insert([dataToInsert])
            .select(`
                *,
                profissional:profissional_id (nome_completo)
            `)
            .single();

        if (error) throw error;
        return mapToUI(data);
    }
};
