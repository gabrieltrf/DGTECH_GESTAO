# 🏢 DGTECH GESTÃO - Sistema de Administração de Vendas

Sistema completo de gestão de vendas online com interface moderna e responsiva, desenvolvido em Python com CustomTkinter para uso offline.

## ✨ Funcionalidades Principais

### 📦 Gestão de Produtos
- ✅ Cadastrar, editar e remover produtos
- 🖼️ Inserir imagens, descrição, preço de custo e preço de venda
- 📁 Categorias e subcategorias de produtos
- 📊 Controle automático de estoque em tempo real
- ⚠️ Alerta visual quando o estoque estiver baixo
- 💡 Calculadora de margem de lucro
- 🔄 Atualização em massa de preços

### 🛒 Gestão de Vendas
- 📝 Registro completo de cada venda (data, produto, quantidade, valor total, cliente)
- 🔄 Atualização automática do estoque após cada venda
- 🔍 Filtros por período, produto e cliente
- 📊 Visualização de histórico completo
- 📄 Exportação de relatórios em PDF e Excel

### 💰 Gestão Financeira
- 📈 Gráficos de lucro, despesas e receitas mensais e anuais
- 💵 Cálculo automático do lucro líquido (baseado no preço de custo e de venda)
- 📝 Área para registrar despesas operacionais (frete, taxas, marketing etc.)
- 📊 Visualização em gráficos de pizza e barras
- 📄 Relatórios exportáveis em PDF e Excel

### 📊 Dashboard (Painel Principal)
- 📅 Visão geral das vendas do dia, semana e mês
- 📈 Gráficos dinâmicos (lucro, despesas, produtos mais vendidos)
- 🎯 Indicadores (KPI): lucro total, estoque total, ticket médio, margem média
- ⚠️ Alertas de estoque baixo
- 🔝 Top 5 produtos mais vendidos

### ⚙️ Configurações
- 🌙 Interface com tema claro e escuro
- 🎨 Customização de preferências
- 📦 Configuração de alertas de estoque
- 💰 Margem de lucro padrão

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.8 ou superior instalado
- pip (gerenciador de pacotes Python)

### Passo 1: Clonar ou baixar o projeto
```bash
cd DGTECH_GESTAO
```

### Passo 2: Criar ambiente virtual (recomendado)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Passo 3: Instalar dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Executar o sistema

**Opção 1 - Mais Rápida (Recomendada):**
```bash
# Duplo clique no arquivo
DGTECH_GESTAO.bat
```

**Opção 2 - Com terminal:**
```bash
# Duplo clique no arquivo
iniciar.bat
```

**Opção 3 - Manual:**
```bash
python main.py
```

## 📁 Estrutura do Projeto

```
DGTECH_GESTAO/
│
├── main.py                 # Aplicação principal
├── database.py            # Gerenciamento do banco de dados SQLite
├── utils.py               # Funções auxiliares e formatação
├── dashboard.py           # Tela do Dashboard
├── produtos.py            # Tela de Produtos
├── vendas.py              # Tela de Vendas
├── financeiro.py          # Tela de Financeiro
├── configuracoes.py       # Tela de Configurações
├── requirements.txt       # Dependências do projeto
├── README.md              # Este arquivo
└── gestao_vendas.db       # Banco de dados (criado automaticamente)
```

## 🎨 Tecnologias Utilizadas

- **Python 3.x** - Linguagem de programação
- **CustomTkinter** - Interface gráfica moderna
- **SQLite** - Banco de dados embutido
- **Matplotlib** - Geração de gráficos
- **Pandas** - Manipulação de dados
- **ReportLab** - Geração de PDFs
- **OpenPyXL** - Geração de arquivos Excel

## 💡 Como Usar

### Primeiro Acesso
1. Execute o sistema com `python main.py`
2. Você será levado ao Dashboard
3. Navegue pelo menu lateral para acessar as diferentes funcionalidades

### Cadastrar Produtos
1. Vá em "📦 Produtos"
2. Clique em "➕ Novo Produto"
3. Preencha os dados (nome, categoria, preços, estoque)
4. Use a calculadora de margem para definir preços
5. Clique em "💾 Salvar"

### Registrar Vendas
1. Vá em "🛒 Vendas"
2. Selecione o produto
3. Informe a quantidade
4. Adicione informações do cliente (opcional)
5. Clique em "💰 Registrar Venda"

### Gerenciar Despesas
1. Vá em "💰 Financeiro"
2. Preencha o formulário de despesas
3. Clique em "➕ Adicionar"
4. Visualize gráficos e relatórios financeiros

### Exportar Relatórios
- Em Vendas ou Financeiro, clique em "📄 Exportar PDF" ou "📊 Exportar Excel"
- Escolha o local para salvar o arquivo
- O relatório será gerado automaticamente

### Personalizar o Sistema
1. Vá em "⚙️ Configurações"
2. Escolha entre tema claro ou escuro
3. Configure alertas de estoque
4. Defina margem de lucro padrão
5. Clique em "💾 Salvar Configurações"

## 📊 Recursos de Análise

### KPIs Disponíveis
- 💰 Receita Total
- 📈 Lucro Líquido
- 🛒 Total de Vendas
- 🎫 Ticket Médio
- 📦 Valor em Estoque
- 💸 Despesas
- 📊 Margem Média
- ⚠️ Alertas de Estoque

### Filtros de Período
- Hoje
- Ontem
- Esta Semana
- Este Mês
- Este Ano
- Mês Anterior
- Personalizado

## 🔒 Segurança e Backup

- O banco de dados SQLite é armazenado localmente
- Faça backup regular do arquivo `gestao_vendas.db`
- Não há conexão com a internet (funcionamento 100% offline)

## ⚠️ Solução de Problemas

### Erro ao iniciar
```bash
# Reinstale as dependências
pip install --upgrade -r requirements.txt
```

### Gráficos não aparecem
```bash
# Instale matplotlib novamente
pip install --upgrade matplotlib
```

### Erro de banco de dados
- Delete o arquivo `gestao_vendas.db` (cuidado: apaga todos os dados)
- Execute novamente o sistema

## 🤝 Suporte

Para suporte ou dúvidas:
- 📧 Email: suporte@dgtech.com
- 🌐 Website: www.dgtech.com

## 📝 Licença

Este sistema foi desenvolvido por DGTECH - © 2025

---

## 🎯 Próximas Atualizações

- [ ] Sistema de backup automático
- [ ] Importação de produtos via CSV
- [ ] Múltiplos usuários com permissões
- [ ] Impressão de nota fiscal
- [ ] Integração com código de barras
- [ ] App mobile complementar

---

**Desenvolvido com ❤️ por DGTECH**
