# 🚀 Guia Rápido de Uso - DGTECH GESTÃO

## ⚡ Início Rápido

### Para Iniciar o Sistema
1. **Duplo clique** em `DGTECH_GESTAO.bat` (mais rápido)
2. Ou duplo clique em `iniciar.bat` (mostra informações)

### Primeiro Uso
Após instalar as dependências (`pip install -r requirements.txt`), você está pronto!

---

## 📋 Fluxo de Trabalho Recomendado

### 1️⃣ Configurar Categorias
1. Vá em **📦 Produtos**
2. Clique no botão **+** ao lado de "Categoria"
3. Crie categorias como: "Eletrônicos", "Roupas", "Alimentos", etc.

### 2️⃣ Cadastrar Produtos
1. **📦 Produtos** → **➕ Novo Produto**
2. Preencha:
   - Nome do produto
   - Categoria
   - Preço de custo
   - Use a **calculadora de margem** para definir o preço de venda
   - Quantidade inicial em estoque
3. **💾 Salvar**

### 3️⃣ Realizar Vendas
1. **🛒 Vendas** → Selecione o produto
2. Informe a quantidade
3. (Opcional) Nome do cliente
4. **💰 Registrar Venda**
5. ✅ Estoque atualizado automaticamente!

### 4️⃣ Registrar Despesas
1. **💰 Financeiro** → Seção "Gestão de Despesas"
2. Preencha descrição, valor e categoria
3. **➕ Adicionar**

### 5️⃣ Visualizar Resultados
1. **📊 Dashboard** → Veja todos os KPIs
2. Gráficos atualizados em tempo real
3. Alertas de estoque baixo
4. Top produtos mais vendidos

---

## 🎯 Dicas Importantes

### ✅ Boas Práticas

**Cadastro de Produtos:**
- Use a calculadora de margem para lucro ideal
- Defina estoque mínimo adequado (padrão: 10)
- Margem recomendada: 30-50%

**Gestão de Estoque:**
- Verifique diariamente os alertas de estoque baixo
- Ajuste o estoque mínimo conforme demanda
- Use o dashboard para acompanhar

**Controle Financeiro:**
- Registre TODAS as despesas
- Categorize despesas corretamente
- Exporte relatórios mensalmente

**Análise de Dados:**
- Use filtros de período no Dashboard
- Compare mês atual vs mês anterior
- Identifique produtos mais lucrativos

### ⚠️ Atenções

❌ **NÃO delete o arquivo** `gestao_vendas.db` (é seu banco de dados!)
✅ Faça backup regular deste arquivo
✅ Use filtros de período para análises específicas
✅ Exporte relatórios antes de fazer mudanças grandes

---

## 📊 Entendendo os KPIs

| KPI | Significado | O que é bom? |
|-----|-------------|--------------|
| 💰 **Receita Total** | Soma de todas as vendas | Crescimento constante |
| 📈 **Lucro Líquido** | Receita - Custo - Despesas | Positivo e crescente |
| 🛒 **Total de Vendas** | Número de transações | Volume alto |
| 🎫 **Ticket Médio** | Receita ÷ Nº de vendas | Crescente |
| 📦 **Valor em Estoque** | Custo × Quantidade | Balanceado |
| 💸 **Despesas** | Custos operacionais | Controladas |
| 📊 **Margem Média** | (Venda - Custo) ÷ Custo | 30-50% |
| ⚠️ **Alertas** | Produtos c/ estoque baixo | Zero é ideal |

---

## 🎨 Personalização

### Tema Escuro/Claro
1. **⚙️ Configurações**
2. Escolha **🌙 Escuro** ou **☀️ Claro**
3. **💾 Salvar Configurações**

### Ajustar Alertas de Estoque
1. **⚙️ Configurações** → "Gestão de Estoque"
2. Defina quantidade mínima (ex: 5, 10, 20)
3. **💾 Salvar**

### Margem Padrão
1. **⚙️ Configurações** → "Gestão de Preços"
2. Defina % padrão (ex: 30%)
3. **💾 Salvar**

---

## 📄 Exportação de Relatórios

### PDF
- Ideal para: Impressão, envio por email
- Contém: Tabelas formatadas, totais
- Botão: **📄 Exportar PDF**

### Excel
- Ideal para: Análises detalhadas, gráficos
- Contém: Dados completos em planilha
- Botão: **📊 Exportar Excel**

### Quando Exportar?
- ✅ Fim de cada mês
- ✅ Antes de reuniões
- ✅ Para declaração de impostos
- ✅ Análise de tendências

---

## 🔧 Atalhos Úteis

| Ação | Como Fazer |
|------|------------|
| Novo Produto | 📦 Produtos → ➕ Novo Produto |
| Nova Venda | 🛒 Vendas → Preencher formulário |
| Ver Dashboard | 📊 Dashboard (primeira tela) |
| Exportar | Botões 📄 ou 📊 nas telas |
| Estoque Baixo | 📦 Produtos → ⚠️ Estoque Baixo |
| Mudar Tema | ⚙️ Configurações → Aparência |

---

## 🆘 Problemas Comuns

### ❓ Sistema não abre?
```bash
# No terminal (PowerShell):
.venv\Scripts\python.exe main.py

# Veja mensagens de erro
```

### ❓ Gráficos não aparecem?
```bash
pip install --upgrade matplotlib
```

### ❓ Erro ao exportar PDF/Excel?
```bash
pip install --upgrade reportlab openpyxl
```

### ❓ Perdi meus dados?
- Procure o arquivo `gestao_vendas.db`
- Restaure de um backup anterior
- **Sempre faça backup!**

---

## 📞 Suporte

**Problemas técnicos?**
1. Verifique o arquivo `README.md` completo
2. Reinstale dependências: `pip install -r requirements.txt`
3. Entre em contato: suporte@dgtech.com

---

## 🎓 Tutoriais Rápidos

### Como definir preço com 40% de margem?
1. Produto custa R$ 100
2. Campo "Preço de Custo": `100`
3. Campo "% margem": `40`
4. Clique **Calcular**
5. Preço sugerido: R$ 140 ✅

### Como ver lucro do mês?
1. **📊 Dashboard**
2. Filtro de período: **"Este Mês"**
3. Veja card **💰 Lucro Líquido**

### Como saber se estou lucrando?
- ✅ Lucro Líquido > 0 (verde)
- ⚠️ Lucro Líquido < 0 (vermelho)
- Use **💰 Financeiro** para detalhes

---

**✨ Pronto para começar! Boa gestão!**
