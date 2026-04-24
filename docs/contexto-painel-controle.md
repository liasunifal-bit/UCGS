# Contexto Técnico: Painel de Controle (Dashboard)

## 1. Visão Geral
O **Painel de Controle** (`dashboard/index.html`) é o ponto de entrada central para profissionais de saúde no ecossistema UCGS. Atualmente, ele funciona como uma Single Page Application (SPA) monolítica que gerencia a autenticação do usuário e fornece a interface para gestão clínica.

## 2. Stack Tecnológica
- **Frontend**: HTML5 Semântico, CSS3 (Vanilla com Design Tokens v25), JavaScript (ES6+).
- **Backend/BaaS**: Supabase (via CDN SDK v2).
- **Iconografia**: Lucide Icons.
- **Tipografia**: Google Fonts (Inter).

## 3. Arquitetura de Autenticação
O sistema utiliza o Supabase para gestão de identidade. A lógica está concentrada em scripts embutidos no final do arquivo:

- **Inicialização (`initSupabase`)**:
  - Configura o cliente Supabase usando credenciais públicas (Anon Key).
  - Escuta mudanças de estado via `onAuthStateChange`.
- **Fluxo de Interface**:
  - `#authOverlay`: Camada global que cobre o dashboard até que uma sessão válida seja detectada.
  - `#login-shell`: Grid responsivo (split-screen) para entrada de credenciais.
- **Cadastro Profissional (`#registerModal`)**:
  - Componente modal para novos profissionais.
  - Campos obrigatórios: Nome, Email, Senha, Registro Profissional (CRM/COREN/etc), Matrícula e Setor.
  - Validação de força de senha em tempo real.
  - Conformidade LGPD com checkbox de consentimento.

## 4. Design System (UCGS v25)
O sistema utiliza um conjunto rigoroso de tokens de design definidos via variáveis CSS (`:root`):

### Cores Principais
- `--primary`: `#60C4FF` (Azul principal)
- `--bg-dark`: `#0B1120` (Fundo profundo)
- `--glass-bg`: `rgba(15, 23, 42, 0.8)` (Efeito de desfoque/vidro)

### Padrões de Nomenclatura (Prefixos)
Para evitar conflitos no monólito, as classes seguem convenções por módulo:
- `am-`: Módulos Administrativos.
- `hist-`: Prontuário e Histórico.
- `det-`: Detalhes e Visualização expandida.
- `maint-`: Manutenção e Infraestrutura.
- `ex-`: Exames e Laudos.

### Estilização
- **Glassmorphism**: Uso intensivo de `backdrop-filter: blur()` e bordas translúcidas.
- **Responsividade**: Layout baseado em CSS Grid com colapso de painéis laterais em dispositivos móveis (`max-width: 1024px`).

## 5. Mapeamento de Componentes Críticos
| Componente | ID / Classe Principal | Descrição |
|------------|-----------------------|-----------|
| Overlay de Auth | `#authOverlay` | Bloqueia acesso ao dashboard sem login. |
| Container de Login | `#login-container` | Formulário de entrada principal. |
| Modal de Registro | `#registerModal` | Cadastro detalhado para profissionais. |
| Sidebar (Esqueleto) | `.dashboard-sidebar` | Navegação modular (visto nos estilos). |
| Grid de Conteúdo | `.main-content` | Área central de renderização do dashboard. |

## 6. Acessibilidade e Conformidade
- **Acessibilidade (WCAG)**:
  - Uso de `skip-links` para navegação via teclado.
  - Suporte a `focus-visible` para indicadores de foco claros.
  - Media queries de `prefers-reduced-motion` para desativar animações pesadas.
- **LGPD**:
  - Coleta explícita de consentimento no cadastro.
  - Tratamento diferenciado para dados sensíveis de prontuário (conforme identificado na lógica de backend).

---
*Última atualização: Abril 2026*
