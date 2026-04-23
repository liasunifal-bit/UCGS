import { supabaseClient } from './supabase-config.js';

function mapToUI(row) {
    if (!row) return row;
    return {
        ...row,
        dataCadastro: row.data_cadastro
    };
}

function mapToDB(data) {
    if (!data) return data;
    const { dataCadastro, ...rest } = data;
    const dbData = { ...rest };
    if (dataCadastro !== undefined) dbData.data_cadastro = dataCadastro;
    return dbData;
}

export const PacientesService = {
    /**
     * Busca todos os pacientes
     */
    async getPacientes() {
        const { data, error } = await supabaseClient
            .from('pacientes')
            .select('*')
            .order('data_cadastro', { ascending: false });

        if (error) {
            console.error('Erro ao buscar pacientes:', error);
            throw error;
        }
        return data.map(mapToUI);
    },

    /**
     * Busca um paciente pelo ID
     */
    async getPacienteById(id) {
        const { data, error } = await supabaseClient
            .from('pacientes')
            .select('*')
            .eq('id', id)
            .single();

        if (error) throw error;
        return mapToUI(data);
    },

    /**
     * Insere um novo paciente
     */
    async insertPaciente(pacienteData) {
        const { data, error } = await supabaseClient
            .from('pacientes')
            .insert([mapToDB(pacienteData)])
            .select()
            .single();

        if (error) throw error;
        return mapToUI(data);
    },

    /**
     * Atualiza os dados de um paciente existente
     */
    async updatePaciente(id, pacienteData) {
        const { data, error } = await supabaseClient
            .from('pacientes')
            .update(mapToDB(pacienteData))
            .eq('id', id)
            .select()
            .single();

        if (error) throw error;
        return mapToUI(data);
    },
    
    /**
     * Alterna o status do paciente (ativo/inativo)
     */
    async toggleStatus(id, currentStatus) {
        const newStatus = currentStatus === 'ativo' ? 'inativo' : 'ativo';
        return await this.updatePaciente(id, { status: newStatus });
    }
};
