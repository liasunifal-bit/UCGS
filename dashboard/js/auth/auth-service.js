// js/auth/auth-service.js
import { supabaseClient } from '../supabase-config.js';

export const AuthService = {
    /**
     * Realiza o login via Email e Senha (Retorna JWT para o cache do navegador)
     */
    
    /**
     * Registra um novo usurio via Email e Senha
     */
    async register(email, password) {
        const { data, error } = await supabaseClient.auth.signUp({ 
            email, 
            password 
        });
        if (error) throw error;
        return data;
    },
    async login(email, password) {
        const { data, error } = await supabaseClient.auth.signInWithPassword({ 
            email, 
            password 
        });
        if (error) throw error;
        return data;
    },
    
    /**
     * Encerra a sessão atual e apaga o JWT local
     */
    async logout() {
        const { error } = await supabaseClient.auth.signOut();
        if (error) console.error("Erro ao deslogar:", error);
    },
    
    /**
     * Retorna a sessão ativa (Token JWT), se houver alguma.
     */
    async getSession() {
        const { data: { session }, error } = await supabaseClient.auth.getSession();
        if (error) {
            console.warn("Nenhuma sessão encontrada ou expirada", error);
            return null;
        }
        return session;
    },

    /**
     * Busca as informações da nossa tabela public.profiles (Apenas funciona se o JWT for válido!)
     */
    async getUserProfile(userId) {
        const { data, error } = await supabaseClient
            .from('profiles')
            .select('*')
            .eq('id', userId)
            .single();
            
        if (error) throw error;
        return data;
    },

    /**
     * Realiza login via provedor OAuth (ex: Google)
     */
    async signInWithOAuth(provider) {
        const { data, error } = await supabaseClient.auth.signInWithOAuth({
            provider: provider,
            options: {
                redirectTo: window.location.origin + window.location.pathname
            }
        });
        if (error) throw error;
        return data;
    }
};
