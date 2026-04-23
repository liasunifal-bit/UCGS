// js/supabase-config.js
// ⚠️ IMPORTANTE: Você precisa colar suas chaves do Supabase aqui!
// Vá no Supabase -> Settings -> API Keys e substitua os valores abaixo:

const SUPABASE_URL = 'https://llqphjlpypnyvknpfdyn.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow';

// O client global 'supabase' está sendo carregado via CDN no HTML
export const supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
